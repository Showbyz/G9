"""
Middleware personalizado para manejar el schema público y la impersonación de tenants.
"""
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import schema_context, get_public_schema_name
from django_tenants.middleware import TenantMainMiddleware
from django_tenants.models import TenantMixin
from clientManager.models import Empresa


class ForcePublicSchemaMiddleware(MiddlewareMixin):
    """
    Middleware que se ejecuta ANTES del TenantMainMiddleware para forzar
    el schema público en URLs que empiezan con /global/
    
    La estrategia es modificar temporalmente el hostname en la request
    para que no coincida con ningún tenant, forzando así el uso del schema público.
    También establece el schema público en la conexión de base de datos.
    """
    def process_request(self, request):
        import sys
        sys.stdout.write(f'[FORCE PUBLIC] Procesando: {request.path}\n')
        sys.stdout.flush()
        # Si la URL empieza con /global/, forzar el schema público
        if request.path.startswith('/global/'):
            # Primero, establecer el schema público en la conexión de base de datos
            # Esto debe hacerse ANTES de que cualquier middleware intente acceder a la BD
            from django.db import connection
            from django_tenants.utils import get_public_schema_name
            from django_tenants.postgresql_backend.base import DatabaseWrapper
            
            public_schema = get_public_schema_name()
            
            try:
                if isinstance(connection, DatabaseWrapper):
                    # Establecer el schema público directamente
                    connection.set_schema_to_public()
            except (AttributeError, Exception):
                pass
            
            # Guardar el hostname original
            original_host = request.get_host()
            request._original_host = original_host
            
            # Modificar temporalmente el hostname para que no coincida con ningún tenant
            # Esto hará que TenantMainMiddleware no encuentre ningún tenant y use el público
            # Usamos un dominio que definitivamente no existe en ningún tenant
            fake_host = 'public-admin-panel.localhost'
            
            # Modificar todos los campos META relevantes que django-tenants puede usar
            request.META['HTTP_HOST'] = fake_host
            request.META['SERVER_NAME'] = fake_host.split(':')[0]
            if 'HTTP_X_FORWARDED_HOST' in request.META:
                del request.META['HTTP_X_FORWARDED_HOST']
            
            # También necesitamos interceptar get_host() usando un descriptor
            # Guardamos el método original como atributo de instancia
            if not hasattr(request, '_saved_get_host'):
                import types
                request._saved_get_host = request.get_host
                # Crear un método bound que siempre devuelva el hostname falso
                # IMPORTANTE: debe aceptar 'self' como primer parámetro
                def fake_get_host(self):
                    return fake_host
                request.get_host = types.MethodType(fake_get_host, request)
        
        return None
    
    def process_response(self, request, response):
        # Restaurar el hostname original después de procesar la respuesta
        if hasattr(request, '_original_host'):
            request.META['HTTP_HOST'] = request._original_host
            host_parts = request._original_host.split(':')
            request.META['SERVER_NAME'] = host_parts[0]
            if hasattr(request, '_saved_get_host'):
                request.get_host = request._saved_get_host
                delattr(request, '_saved_get_host')
        
        # Si la respuesta es 404 en la raíz y no hay tenant, redirigir al panel global
        if response.status_code == 404 and request.path == '/':
            import sys
            sys.stdout.write('[FORCE PUBLIC] Detectado 404 en raíz, redirigiendo a /global/login/\n')
            sys.stdout.flush()
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect('/global/login/')
        
        return response


class PublicSchemaMiddleware(MiddlewareMixin):
    """
    Middleware que detecta si estamos en el schema público y permite
    el acceso a vistas de administración global.
    
    También fuerza el schema público si la URL empieza con /global/
    y TenantMainMiddleware identificó un tenant incorrecto.
    
    Este middleware se ejecuta DESPUÉS de TenantMainMiddleware pero
    ANTES de AuthenticationMiddleware para asegurar que el schema esté
    correctamente establecido antes de que se intente cargar el usuario.
    """
    def process_request(self, request):
        # Si la URL empieza con /global/, asegurar que estamos en el schema público
        if request.path.startswith('/global/'):
            public_schema = get_public_schema_name()
            from django.db import connection
            from django_tenants.postgresql_backend.base import DatabaseWrapper
            
            # Asegurar que el schema público esté establecido en la conexión
            try:
                if isinstance(connection, DatabaseWrapper):
                    connection.set_schema_to_public()
            except (AttributeError, Exception):
                pass
            
            # Si TenantMainMiddleware identificó un tenant que no es público, forzar el público
            if hasattr(request, 'tenant'):
                if request.tenant.schema_name != public_schema:
                    # Crear un objeto tenant público
                    class PublicTenant:
                        def __init__(self):
                            self.schema_name = public_schema
                            self.auto_create_schema = False
                            self.auto_drop_schema = False
                    
                    # Establecer el tenant público
                    tenant_obj = PublicTenant()
                    request.tenant = tenant_obj
                    
                    # Asegurar que el schema esté establecido
                    try:
                        if isinstance(connection, DatabaseWrapper):
                            connection.set_schema_to_public()
                    except (AttributeError, Exception):
                        pass
        
        # Verificar si estamos en el schema público
        if hasattr(request, 'tenant'):
            request.is_public_schema = (
                request.tenant.schema_name == get_public_schema_name()
            )
        else:
            request.is_public_schema = False
        
        # Verificar si hay una sesión de impersonación activa
        if hasattr(request, 'session'):
            impersonated_tenant_id = request.session.get('impersonated_tenant_id')
            if impersonated_tenant_id:
                try:
                    with schema_context(get_public_schema_name()):
                        tenant = Empresa.objects.get(id_empresa=impersonated_tenant_id)
                        request.impersonated_tenant = tenant
                        request.is_impersonating = True
                except Empresa.DoesNotExist:
                    request.session.pop('impersonated_tenant_id', None)
                    request.is_impersonating = False
            else:
                request.is_impersonating = False
        else:
            request.is_impersonating = False
        
        return None


class PublicSchemaAuthMiddleware(MiddlewareMixin):
    """
    Middleware que se ejecuta ANTES de AuthenticationMiddleware para
    manejar correctamente la autenticación en el schema público.
    
    Cuando estamos en /global/, limpia cualquier sesión de usuario del tenant
    y asegura que solo se carguen usuarios del schema público.
    
    NOTA: Este middleware debe ejecutarse DESPUÉS de SessionMiddleware.
    """
    def process_request(self, request):
        # Si estamos en /global/, asegurar que el schema público esté establecido
        if request.path.startswith('/global/'):
            from django.db import connection
            from django_tenants.utils import get_public_schema_name
            from django_tenants.postgresql_backend.base import DatabaseWrapper
            
            public_schema = get_public_schema_name()
            
            # Asegurar que el schema público esté establecido
            try:
                if isinstance(connection, DatabaseWrapper):
                    connection.set_schema_to_public()
            except (AttributeError, Exception):
                pass
            
            # Limpiar cualquier sesión de usuario del tenant ANTES de que
            # AuthenticationMiddleware intente cargar el usuario
            # Verificar que la sesión esté disponible (SessionMiddleware debe haberse ejecutado)
            if hasattr(request, 'session'):
                user_backend = request.session.get('_auth_user_backend', '')
                if user_backend and user_backend != 'globalAdmin.backends.AdministradorGlobalBackend':
                    # Limpiar completamente la sesión de autenticación del tenant
                    request.session.pop('_auth_user_id', None)
                    request.session.pop('_auth_user_backend', None)
                    request.session.pop('_auth_user_hash', None)
                    # También limpiar el cache del usuario si existe
                    if hasattr(request, '_cached_user'):
                        delattr(request, '_cached_user')
        
        return None


class TenantThemeMiddleware(MiddlewareMixin):
    """
    Middleware que agrega información del tema del tenant al request
    y lo establece en settings para que los loaders puedan accederlo.
    """
    def process_request(self, request):
        # Si estamos impersonando, usar el tema del tenant impersonado
        if hasattr(request, 'is_impersonating') and request.is_impersonating:
            if hasattr(request, 'impersonated_tenant') and request.impersonated_tenant:
                theme = getattr(request.impersonated_tenant, 'tema', 'default')
                request.tenant_theme = theme
                from django.conf import settings
                settings.CURRENT_TENANT_THEME = theme
                return None
        
        # Si no estamos impersonando, usar el tema del tenant actual
        if hasattr(request, 'tenant') and request.tenant:
            theme = getattr(request.tenant, 'tema', 'default')
            request.tenant_theme = theme
            # Establecer el tema en settings para que los loaders puedan accederlo
            from django.conf import settings
            settings.CURRENT_TENANT_THEME = theme
        else:
            request.tenant_theme = 'default'
            from django.conf import settings
            settings.CURRENT_TENANT_THEME = 'default'
        return None


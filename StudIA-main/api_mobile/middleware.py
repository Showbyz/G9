"""
Middleware para manejar la identificación de tenant en la API móvil.
Permite especificar el tenant mediante header HTTP o parámetro en la URL.
"""
from django_tenants.utils import schema_context
from clientManager.models import Empresa
from django.http import JsonResponse
import sys


class ApiMobileTenantMiddleware:
    """
    Middleware que identifica el tenant para peticiones de la API móvil.
    Se ejecuta ANTES de TenantMainMiddleware para establecer el tenant correcto.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def _get_tenant_schema(self, request):
        """Obtiene el schema del tenant de diferentes fuentes"""
        # Opción 1: Header HTTP X-Tenant-Schema
        tenant_schema = request.headers.get('X-Tenant-Schema') or request.headers.get('x-tenant-schema')
        
        # Opción 2: Query parameter (ej: ?tenant=tenant_schema)
        if not tenant_schema:
            tenant_schema = request.GET.get('tenant') or request.GET.get('schema')
        
        # Opción 3: Si no se especifica, intentar detectar del hostname
        if not tenant_schema:
            hostname = request.get_host().split(':')[0]
            try:
                with schema_context('public'):
                    # Buscar tenant por dominio
                    from clientManager.models import Dominio
                    dominio = Dominio.objects.filter(domain=hostname).first()
                    if dominio:
                        tenant_schema = dominio.tenant.schema_name
            except Exception:
                pass
        
        # Opción 4: Si aún no hay tenant, usar el primer tenant activo (solo para desarrollo)
        if not tenant_schema:
            try:
                with schema_context('public'):
                    # Obtener el primer tenant activo
                    first_tenant = Empresa.objects.filter(estado='A').first()
                    if not first_tenant:
                        # Si no hay con estado 'A', intentar con cualquier tenant (excepto public)
                        first_tenant = Empresa.objects.exclude(schema_name='public').first()
                    if first_tenant:
                        tenant_schema = first_tenant.schema_name
                        sys.stdout.write(f"[API Mobile] Usando tenant por defecto: {tenant_schema}\n")
                        sys.stdout.flush()
            except Exception as e:
                sys.stdout.write(f"[API Mobile] Error al obtener tenant por defecto: {e}\n")
                sys.stdout.flush()
                pass
        
        return tenant_schema
    
    def _set_tenant(self, request, tenant_schema):
        """Establece el tenant en el request. El schema se manejará con schema_context en las vistas."""
        if not tenant_schema:
            sys.stdout.write("[API Mobile] WARNING: No se pudo identificar ningún tenant\n")
            sys.stdout.flush()
            return False
        
        try:
            with schema_context('public'):
                tenant = Empresa.objects.get(schema_name=tenant_schema)
            
            # Establecer el tenant en el request
            # Las vistas usarán schema_context para todas las operaciones de BD
            request.tenant = tenant
            
            sys.stdout.write(f"[API Mobile] Tenant establecido en request: {tenant_schema} ({tenant.nombre_empresa})\n")
            sys.stdout.flush()
            
            return True
        except Empresa.DoesNotExist:
            # Si el tenant no existe, devolver error
            sys.stdout.write(f"[API Mobile] ERROR: Tenant '{tenant_schema}' no encontrado\n")
            sys.stdout.flush()
            return False
        except Exception as e:
            sys.stdout.write(f"[API Mobile] ERROR al establecer tenant: {e}\n")
            sys.stdout.flush()
            return False

    def __call__(self, request):
        # Solo procesar si es una petición a la API móvil
        if request.path.startswith('/api/mobile/'):
            # Log para todas las peticiones (incluyendo OPTIONS) - FORZAR salida
            sys.stdout.write(f"[API Mobile] Petición recibida: {request.method} {request.path}\n")
            sys.stdout.flush()
            sys.stdout.write(f"[API Mobile] Header X-Tenant-Schema: {request.headers.get('X-Tenant-Schema', 'NO ENVIADO')}\n")
            sys.stdout.flush()
            
            # Obtener el tenant schema
            tenant_schema = self._get_tenant_schema(request)
            
            # Establecer el tenant (para todas las peticiones excepto OPTIONS)
            if request.method != 'OPTIONS':
                if not self._set_tenant(request, tenant_schema):
                    # Devolver error para peticiones que no sean OPTIONS
                    return JsonResponse({
                        'success': False,
                        'error': f'Tenant con schema "{tenant_schema}" no encontrado'
                    }, status=404)

        response = self.get_response(request)
        return response

"""
Middleware para detectar el tenant desde un parámetro de URL.
Útil cuando no se pueden usar subdominios (como en Render.com).
"""
import sys
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import get_public_schema_name, schema_context
from clientManager.models import Empresa, Dominio


class TenantParamMiddleware(MiddlewareMixin):
    """
    Middleware que detecta el tenant desde un parámetro de query string o path.
    Se ejecuta ANTES de TenantMainMiddleware para modificar el hostname.
    
    Soporta:
    - ?tenant=DUOC%20UC (query parameter)
    - /tenant/duoc/ (path parameter)
    """
    
    def process_request(self, request):
        # Solo procesar si estamos en el dominio principal
        host = request.get_host()
        
        # Si ya estamos en un subdominio que funciona, no hacer nada
        if not (host.startswith('studia-8dmp.onrender.com') or host.startswith('localhost')):
            return None
        
        # NO procesar si estamos accediendo al panel de administración global
        # Estas rutas deben funcionar sin tenant
        if request.path.startswith('/global/'):
            # Limpiar tenant_schema_name de la sesión si existe para evitar conflictos
            if hasattr(request, 'session') and 'tenant_schema_name' in request.session:
                del request.session['tenant_schema_name']
            return None
        
        # 1. Intentar detectar desde query parameter: ?tenant=DUOC%20UC
        tenant_param = request.GET.get('tenant', None)
        
        # 2. Intentar detectar desde path: /tenant/duoc/
        if not tenant_param and request.path.startswith('/tenant/'):
            path_parts = request.path.split('/')
            if len(path_parts) >= 3 and path_parts[1] == 'tenant':
                tenant_slug = path_parts[2]
                # Buscar tenant por slug (nombre normalizado)
                try:
                    with schema_context(get_public_schema_name()):
                        tenant = Empresa.objects.get(schema_name__iexact=tenant_slug.replace('-', ' '))
                        tenant_param = tenant.schema_name
                except (Empresa.DoesNotExist, Empresa.MultipleObjectsReturned):
                    pass
        
        # 3. Intentar leer desde la sesión (si ya se estableció antes y la sesión está disponible)
        if not tenant_param and hasattr(request, 'session'):
            tenant_param = request.session.get('tenant_schema_name', None)
        
        if tenant_param:
            try:
                with schema_context(get_public_schema_name()):
                    # Buscar el tenant por schema_name (case-insensitive)
                    try:
                        tenant = Empresa.objects.get(schema_name__iexact=tenant_param)
                    except Empresa.DoesNotExist:
                        # Si no se encuentra con iexact, intentar exacto
                        tenant = Empresa.objects.get(schema_name=tenant_param)
                    
                    # Lista de tenants que deben usar el método de parámetro de query (sin modificar hostname)
                    # Estos tenants no tienen subdominios funcionales en Render.com
                    # Normalizar a minúsculas para comparación case-insensitive
                    tenants_con_parametro = ['duoc uc', 'inacap']
                    schema_name_lower = tenant.schema_name.lower()
                    nombre_empresa_lower = tenant.nombre_empresa.lower() if tenant.nombre_empresa else ''
                    
                    # Verificar si el tenant debe usar el método de parámetro de query (case-insensitive)
                    usar_parametro = (
                        schema_name_lower in tenants_con_parametro or 
                        nombre_empresa_lower in tenants_con_parametro
                    )
                    
                    if usar_parametro:
                        # Para estos tenants, necesitamos modificar el hostname para que TenantMainMiddleware lo reconozca
                        # Primero intentar usar un dominio existente del tenant
                        dominio = tenant.domains.filter(is_primary=True).first()
                        
                        if not dominio:
                            # Si no hay dominio, crear uno temporal basado en el schema_name
                            dominio_temporal = tenant.schema_name.lower().replace(' ', '-').replace('_', '-')
                            dominio_domain = f"{dominio_temporal}.studia-8dmp.onrender.com"
                            
                            # Verificar si este dominio ya existe en la BD
                            dominio_existente = tenant.domains.filter(domain__iexact=dominio_domain).first()
                            
                            if not dominio_existente:
                                # Crear el dominio temporalmente en la BD para que TenantMainMiddleware lo reconozca
                                # Esto es necesario porque TenantMainMiddleware busca dominios en la BD
                                try:
                                    dominio_existente = Dominio.objects.create(
                                        domain=dominio_domain,
                                        tenant=tenant,
                                        is_primary=True
                                    )
                                    sys.stdout.write(f'[TENANT PARAM] Dominio temporal creado en BD: {dominio_domain}\n')
                                    sys.stdout.flush()
                                except Exception as e:
                                    sys.stdout.write(f'[TENANT PARAM] Error al crear dominio temporal: {str(e)}\n')
                                    sys.stdout.flush()
                                    # Si falla, usar el dominio temporal de todas formas
                            
                            dominio_domain = dominio_existente.domain if dominio_existente else dominio_domain
                        else:
                            dominio_domain = dominio.domain
                        
                        # Guardar el hostname original
                        request._original_host = host
                        
                        # Modificar el hostname para que TenantMainMiddleware lo detecte
                        # Aunque el dominio no sea funcional en DNS, TenantMainMiddleware lo reconocerá desde la BD
                        request.META['HTTP_HOST'] = dominio_domain
                        request.META['SERVER_NAME'] = dominio_domain.split(':')[0]  # Sin puerto
                        
                        # También establecer el tenant directamente para asegurar que esté disponible
                        from django.db import connection
                        request.tenant = tenant
                        connection.set_tenant(tenant)
                        
                        # Guardar el tenant en la sesión para mantenerlo en requests posteriores
                        if hasattr(request, 'session'):
                            request.session['tenant_schema_name'] = tenant.schema_name
                        
                        sys.stdout.write(f'[TENANT PARAM] Tenant detectado: {tenant.schema_name} via parámetro\n')
                        sys.stdout.write(f'[TENANT PARAM] Hostname modificado a: {dominio_domain} (solo para TenantMainMiddleware)\n')
                        sys.stdout.flush()
                    else:
                        # Para otros tenants, usar el método original con modificación de hostname
                        dominio = tenant.domains.filter(is_primary=True).first()
                        
                        if dominio:
                            # Guardar el hostname original
                            request._original_host = host
                            
                            # Guardar el tenant en la sesión para mantenerlo en requests posteriores
                            if hasattr(request, 'session'):
                                request.session['tenant_schema_name'] = tenant.schema_name
                            
                            # Modificar el hostname para que TenantMainMiddleware lo detecte
                            request.META['HTTP_HOST'] = dominio.domain
                            request.META['SERVER_NAME'] = dominio.domain.split(':')[0]  # Sin puerto
                            
                            sys.stdout.write(f'[TENANT PARAM] Tenant detectado: {tenant.schema_name} via parámetro/sesión\n')
                            sys.stdout.write(f'[TENANT PARAM] Hostname modificado a: {dominio.domain}\n')
                            sys.stdout.flush()
                        else:
                            sys.stdout.write(f'[TENANT PARAM] Tenant {tenant.schema_name} no tiene dominio configurado\n')
                            sys.stdout.flush()
                        
            except Empresa.DoesNotExist:
                sys.stdout.write(f'[TENANT PARAM] Tenant no encontrado: {tenant_param}\n')
                sys.stdout.flush()
            except Exception as e:
                sys.stdout.write(f'[TENANT PARAM] Error: {str(e)}\n')
                sys.stdout.flush()
        
        return None


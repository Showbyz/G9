"""
Vistas para la administración global de tenants.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection
from django_tenants.utils import schema_context, get_public_schema_name
from django_tenants.models import TenantMixin
from clientManager.models import Empresa, Dominio, AdministradorGlobal
from functools import wraps


def global_admin_required(view_func):
    """
    Decorador que verifica que el usuario sea un administrador global
    y que estemos en el schema público.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar que estamos en el schema público
        from django_tenants.utils import get_public_schema_name, schema_context
        public_schema = get_public_schema_name()
        
        # Si no estamos en el schema público, intentar forzarlo
        if not hasattr(request, 'tenant') or request.tenant.schema_name != public_schema:
            # Si la URL es /global/, forzar el schema público
            if request.path.startswith('/global/'):
                from django.db import connection
                from django_tenants.postgresql_backend.base import DatabaseWrapper
                try:
                    if isinstance(connection, DatabaseWrapper):
                        connection.set_schema_to_public()
                    # Crear un objeto tenant público
                    class PublicTenant:
                        def __init__(self):
                            self.schema_name = public_schema
                            self.auto_create_schema = False
                            self.auto_drop_schema = False
                    request.tenant = PublicTenant()
                except Exception:
                    pass
            
            # Si aún no estamos en el schema público después de intentar forzarlo, redirigir
            if not hasattr(request, 'tenant') or request.tenant.schema_name != public_schema:
                messages.error(request, 'Esta sección solo está disponible en el panel global.')
                return redirect('global_admin:login')
        
        # Verificar la sesión directamente en lugar de usar request.user
        # para evitar problemas de carga del usuario
        user_id = request.session.get('_auth_user_id')
        user_backend = request.session.get('_auth_user_backend')
        
        # Verificar que hay una sesión activa del backend correcto
        if not user_id or user_backend != 'globalAdmin.backends.AdministradorGlobalBackend':
            messages.error(request, 'Debes iniciar sesión como administrador global.')
            return redirect('global_admin:login')
        
        # Verificar que el usuario existe y está activo en el schema público
        try:
            with schema_context(public_schema):
                from clientManager.models import AdministradorGlobal
                user = AdministradorGlobal.objects.get(pk=user_id)
                if not user.is_active:
                    messages.error(request, 'Tu cuenta de administrador global está inactiva.')
                    logout(request)
                    return redirect('global_admin:login')
        except (AdministradorGlobal.DoesNotExist, Exception):
            messages.error(request, 'Sesión inválida. Por favor, inicia sesión nuevamente.')
            logout(request)
            return redirect('global_admin:login')
        
        # No verificamos request.user directamente para evitar problemas con SimpleLazyObject
        # Ya verificamos la sesión y el usuario en el schema público arriba
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def global_login(request):
    """
    Vista de login para administradores globales.
    """
    # Verificar que estamos en el schema público
    from django_tenants.utils import get_public_schema_name, schema_context
    from clientManager.models import AdministradorGlobal
    
    # Debug: verificar el tenant actual
    public_schema = get_public_schema_name()
    current_schema = getattr(request.tenant, 'schema_name', None) if hasattr(request, 'tenant') else None
    
    # Permitir acceso si estamos en el schema público o si no hay tenant (primera carga)
    if hasattr(request, 'tenant') and current_schema != public_schema:
        messages.error(request, 'El panel global solo está disponible en el dominio público.')
        return redirect('/')
    
    # Verificar si hay un usuario autenticado de forma segura
    # Solo verificamos si hay una sesión activa, sin intentar cargar el usuario del tenant
    user_id = request.session.get('_auth_user_id')
    user_backend = request.session.get('_auth_user_backend')
    
    # Si hay un usuario en sesión y es del backend de AdministradorGlobal, verificar
    # PERO solo redirigir si estamos en el schema público para evitar bucles
    if user_id and user_backend == 'globalAdmin.backends.AdministradorGlobalBackend':
        # Solo redirigir si estamos en el schema público
        if current_schema == public_schema:
            try:
                with schema_context(public_schema):
                    user = AdministradorGlobal.objects.get(pk=user_id)
                    if user.is_active:
                        return redirect('global_admin:dashboard')
            except (AdministradorGlobal.DoesNotExist, Exception):
                # Si no existe o hay error, limpiar la sesión
                request.session.flush()
        else:
            # Si no estamos en el schema público, limpiar la sesión
            request.session.flush()
    
    # Si hay una sesión de usuario del tenant, cerrarla
    if user_id and user_backend != 'globalAdmin.backends.AdministradorGlobalBackend':
        logout(request)
        messages.info(request, 'Sesión de usuario normal cerrada. Por favor, inicia sesión como administrador global.')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Autenticar usando el backend personalizado en el schema público
        from globalAdmin.backends import AdministradorGlobalBackend
        backend = AdministradorGlobalBackend()
        user = backend.authenticate(request, username=email, password=password)
        
        if user and user.is_active:
            login(request, user, backend='globalAdmin.backends.AdministradorGlobalBackend')
            messages.success(request, f'Bienvenido, {user.nombre}')
            return redirect('global_admin:dashboard')
        else:
            messages.error(request, 'Credenciales inválidas o cuenta inactiva.')
    
    return render(request, 'globalAdmin/login.html')


@global_admin_required
def global_logout(request):
    """
    Cerrar sesión del administrador global.
    """
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('global_admin:login')


@global_admin_required
def dashboard(request):
    """
    Dashboard principal del administrador global.
    """
    with schema_context(get_public_schema_name()):
        tenants = Empresa.objects.all().order_by('-created_at')
        total_tenants = tenants.count()
        active_tenants = tenants.filter(estado='A').count() if hasattr(Empresa, 'estado') else total_tenants
    
    context = {
        'tenants': tenants,
        'total_tenants': total_tenants,
        'active_tenants': active_tenants,
    }
    return render(request, 'globalAdmin/dashboard.html', context)


@global_admin_required
def tenant_list(request):
    """
    Lista todos los tenants.
    """
    with schema_context(get_public_schema_name()):
        tenants = Empresa.objects.all().order_by('-created_at')
    
    context = {
        'tenants': tenants,
    }
    return render(request, 'globalAdmin/tenant_list.html', context)


@global_admin_required
def tenant_create(request):
    """
    Crear un nuevo tenant.
    """
    if request.method == 'POST':
        nombre_empresa = request.POST.get('nombre_empresa')
        nombre_sn = request.POST.get('nombre_sn', '')
        dominio = request.POST.get('dominio')
        tema = request.POST.get('tema', 'default')
        estado = request.POST.get('estado', 'A')
        
        if nombre_empresa and dominio:
            try:
                with schema_context(get_public_schema_name()):
                    # Crear el tenant con auto_create_schema para que se cree el schema automáticamente
                    schema_name = nombre_empresa.lower().replace(' ', '_').replace('-', '_')
                    
                    # Verificar que el schema_name no exista ya
                    if Empresa.objects.filter(schema_name=schema_name).exists():
                        messages.error(request, f'Ya existe un tenant con el nombre "{schema_name}".')
                        return render(request, 'globalAdmin/tenant_create.html')
                    
                    # Crear el tenant
                    tenant = Empresa(
                        nombre_empresa=nombre_empresa,
                        nombre_sn=nombre_sn,
                        tema=tema,
                        estado=estado,
                        schema_name=schema_name,
                        auto_create_schema=True,  # Crear el schema automáticamente
                        auto_drop_schema=False
                    )
                    tenant.save()
                    
                    # Crear el dominio (normalizar a minúsculas para evitar problemas de case-sensitivity)
                    dominio_normalizado = dominio.lower()
                    dominio_obj = Dominio(
                        domain=dominio_normalizado,
                        tenant=tenant,
                        is_primary=True
                    )
                    dominio_obj.save()
                
                # Ejecutar las migraciones en el schema del tenant
                from django.core.management import call_command
                from io import StringIO
                import sys
                
                # Ejecutar migrate_schemas para el schema específico con --run-syncdb
                # para asegurar que todas las tablas se creen correctamente
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                try:
                    call_command('migrate_schemas', '--schema', schema_name, '--run-syncdb', verbosity=0)
                except Exception as e:
                    sys.stdout = old_stdout
                    # Si hay error, intentar eliminar el tenant creado
                    with schema_context(get_public_schema_name()):
                        tenant.delete()
                    messages.error(request, f'Error al ejecutar migraciones: {str(e)}')
                    return render(request, 'globalAdmin/tenant_create.html')
                finally:
                    sys.stdout = old_stdout
                
                messages.success(request, f'Tenant "{nombre_empresa}" creado exitosamente con todas las migraciones aplicadas.')
                return redirect('global_admin:tenant_list')
            except Exception as e:
                messages.error(request, f'Error al crear el tenant: {str(e)}')
                return render(request, 'globalAdmin/tenant_create.html')
        else:
            messages.error(request, 'Por favor complete todos los campos requeridos.')
    
    return render(request, 'globalAdmin/tenant_create.html')


@global_admin_required
def tenant_run_migrations(request, tenant_id):
    """
    Ejecutar migraciones para un tenant específico.
    """
    with schema_context(get_public_schema_name()):
        tenant = get_object_or_404(Empresa, id_empresa=tenant_id)
    
    try:
        from django.core.management import call_command
        from io import StringIO
        import sys
        from django.db import connection
        
        # Verificar que el schema existe, y crearlo si no existe
        with connection.cursor() as cursor:
            cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", [tenant.schema_name])
            schema_exists = cursor.fetchone() is not None
        
        if not schema_exists:
            # El schema no existe, crearlo manualmente
            try:
                # Crear el schema
                with connection.cursor() as cursor:
                    cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{tenant.schema_name}"')
                messages.info(request, f'Schema "{tenant.schema_name}" creado. Ejecutando migraciones...')
            except Exception as e:
                messages.error(request, f'Error al crear el schema: {str(e)}')
                return redirect('global_admin:tenant_list')
        
        # Ejecutar migrate_schemas para el schema específico con --run-syncdb
        # y --fake-initial para evitar problemas si las migraciones ya están marcadas como aplicadas
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        try:
            # Primero intentar con --run-syncdb para crear todas las tablas
            call_command('migrate_schemas', '--schema', tenant.schema_name, '--run-syncdb', verbosity=1)
            
            # Luego ejecutar las migraciones normalmente
            call_command('migrate_schemas', '--schema', tenant.schema_name, verbosity=1)
            
            output = sys.stdout.getvalue()
            error_output = sys.stderr.getvalue()
            
            if error_output:
                messages.warning(request, f'Migraciones ejecutadas con advertencias para el tenant "{tenant.nombre_empresa}". Verifica los logs.')
            else:
                messages.success(request, f'Migraciones ejecutadas exitosamente para el tenant "{tenant.nombre_empresa}".')
        except Exception as e:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            error_msg = str(e)
            messages.error(request, f'Error al ejecutar migraciones: {error_msg}')
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
        return redirect('global_admin:tenant_list')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('global_admin:tenant_list')


@global_admin_required
def tenant_edit(request, tenant_id):
    """
    Editar un tenant existente.
    """
    with schema_context(get_public_schema_name()):
        tenant = get_object_or_404(Empresa, id_empresa=tenant_id)
        dominios = tenant.domains.all()
    
    if request.method == 'POST':
        tenant.nombre_empresa = request.POST.get('nombre_empresa', tenant.nombre_empresa)
        tenant.nombre_sn = request.POST.get('nombre_sn', tenant.nombre_sn)
        tenant.tema = request.POST.get('tema', tenant.tema)
        tenant.estado = request.POST.get('estado', tenant.estado)
        
        with schema_context(get_public_schema_name()):
            tenant.save()
            
            # Actualizar dominios si se proporcionan
            # Normalizar dominios a minúsculas
            dominio_principal = request.POST.get('dominio_principal', '').strip().lower()
            if dominio_principal:
                # Buscar o crear el dominio principal
                dominio_obj, created = Dominio.objects.get_or_create(
                    domain=dominio_principal,
                    defaults={'tenant': tenant, 'is_primary': True}
                )
                if not created:
                    dominio_obj.is_primary = True
                    dominio_obj.save()
                
                # Marcar otros dominios como no primarios
                Dominio.objects.filter(tenant=tenant).exclude(domain=dominio_principal).update(is_primary=False)
        
        messages.success(request, f'Tenant "{tenant.nombre_empresa}" actualizado exitosamente.')
        return redirect('global_admin:tenant_list')
    
    context = {
        'tenant': tenant,
        'dominios': dominios,
    }
    return render(request, 'globalAdmin/tenant_edit.html', context)


@global_admin_required
def tenant_suspend(request, tenant_id):
    """
    Suspender un tenant (cambiar estado a inactivo).
    """
    with schema_context(get_public_schema_name()):
        tenant = get_object_or_404(Empresa, id_empresa=tenant_id)
        tenant.estado = 'I'  # Inactivo
        tenant.save()
    
    messages.success(request, f'Tenant "{tenant.nombre_empresa}" suspendido.')
    return redirect('global_admin:tenant_list')


@global_admin_required
def tenant_activate(request, tenant_id):
    """
    Activar un tenant suspendido.
    """
    with schema_context(get_public_schema_name()):
        tenant = get_object_or_404(Empresa, id_empresa=tenant_id)
        tenant.estado = 'A'  # Activo
        tenant.save()
    
    messages.success(request, f'Tenant "{tenant.nombre_empresa}" activado.')
    return redirect('global_admin:tenant_list')


@global_admin_required
def tenant_impersonate(request, tenant_id):
    """
    Impersonar (entrar como) un tenant específico.
    """
    from urllib.parse import quote
    
    with schema_context(get_public_schema_name()):
        tenant = get_object_or_404(Empresa, id_empresa=tenant_id)
    
    # Guardar el tenant en la sesión para impersonación
    request.session['impersonated_tenant_id'] = tenant.id_empresa
    request.session['impersonated_tenant_schema'] = tenant.schema_name
    
    # Lista de tenants que deben usar el método de parámetro de query (útil para Render.com)
    # Estos tenants no tienen subdominios configurados o se acceden vía parámetro
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
        # Usar directamente la URL de Render con parámetro de query
        tenant_param = quote(tenant.schema_name)
        tenant_url = f"https://studia-8dmp.onrender.com/?tenant={tenant_param}"
        messages.success(request, f'Redirigiendo a tenant: {tenant.nombre_empresa}')
        return redirect(tenant_url)
    
    # Para otros tenants, usar el método original con dominios
    # Obtener el puerto del request actual
    port = request.get_port()
    if port not in [80, 443]:
        port_str = f":{port}"
    else:
        port_str = ""
    
    # Redirigir al login del tenant (no a la raíz)
    try:
        primary_domain = tenant.get_primary_domain()
        if primary_domain:
            # Construir la URL del tenant con el puerto y redirigir al login
            protocol = 'https' if request.is_secure() else 'http'
            tenant_url = f"{protocol}://{primary_domain.domain}{port_str}/"
            messages.success(request, f'Impersonando tenant: {tenant.nombre_empresa}')
            return redirect(tenant_url)
        else:
            messages.error(request, 'El tenant no tiene un dominio configurado.')
            return redirect('global_admin:tenant_list')
    except Exception as e:
        # Si no hay dominio principal, intentar con el primer dominio
        dominios = tenant.domains.all()
        if dominios.exists():
            dominio = dominios.first()
            protocol = 'https' if request.is_secure() else 'http'
            tenant_url = f"{protocol}://{dominio.domain}{port_str}/"
            messages.success(request, f'Impersonando tenant: {tenant.nombre_empresa}')
            return redirect(tenant_url)
        else:
            messages.error(request, 'El tenant no tiene un dominio configurado.')
            return redirect('global_admin:tenant_list')


@global_admin_required
def tenant_stop_impersonate(request):
    """
    Dejar de impersonar y volver al panel global.
    """
    request.session.pop('impersonated_tenant_id', None)
    request.session.pop('impersonated_tenant_schema', None)
    messages.success(request, 'Has dejado de impersonar el tenant.')
    return redirect('global_admin:dashboard')


@global_admin_required
def tenant_create_admin_user(request, tenant_id):
    """
    Crear un usuario administrador para un tenant específico.
    """
    from loginApp.models import Usuario
    
    with schema_context(get_public_schema_name()):
        tenant = get_object_or_404(Empresa, id_empresa=tenant_id)
    
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        email = request.POST.get('email')
        password = request.POST.get('password')
        telefono = request.POST.get('telefono', '0')
        cargo = request.POST.get('cargo', 'Administrador')
        is_staff = request.POST.get('is_staff', 'on') == 'on'
        
        if nombre_usuario and email and password:
            try:
                # Crear el usuario en el schema del tenant
                with schema_context(tenant.schema_name):
                    # Verificar si el email ya existe
                    if Usuario.objects.filter(email=email).exists():
                        messages.error(request, f'El email {email} ya está en uso en este tenant.')
                        return render(request, 'globalAdmin/tenant_create_admin_user.html', {'tenant': tenant})
                    
                    # Crear el usuario administrador
                    usuario = Usuario(
                        nombre_usuario=nombre_usuario,
                        email=email,
                        telefono=int(telefono) if telefono.isdigit() else 0,
                        cargo=cargo,
                        horario_atencion=0,
                        is_staff=is_staff,
                        is_active=True
                    )
                    usuario.set_password(password)
                    usuario.save()
                    
                    messages.success(request, f'Usuario administrador "{nombre_usuario}" creado exitosamente para el tenant "{tenant.nombre_empresa}".')
                    return redirect('global_admin:tenant_list')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')
        else:
            messages.error(request, 'Por favor complete todos los campos requeridos.')
    
    context = {
        'tenant': tenant,
    }
    return render(request, 'globalAdmin/tenant_create_admin_user.html', context)

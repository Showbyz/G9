"""
Script de inicialización para producción.
Se ejecuta automáticamente al iniciar la aplicación en Render.com.

Este script:
1. Verifica que las migraciones estén aplicadas
2. Crea el administrador global si no existe
3. Crea tenants de ejemplo si no existen
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portalAutoatencion.settings')
django.setup()

from django_tenants.utils import schema_context, get_public_schema_name
from clientManager.models import Empresa, AdministradorGlobal, Dominio
from django.core.management import call_command
from io import StringIO


def init_production():
    """
    Inicializa la aplicación en producción.
    """
    public_schema = get_public_schema_name()
    
    print("[INIT] Iniciando inicialización de producción...")
    
    # 0. Verificar conexión a la base de datos antes de ejecutar migraciones
    try:
        from django.db import connection
        connection.ensure_connection()
        print("[INIT] ✓ Conexión a la base de datos verificada")
    except Exception as e:
        print(f"[INIT] ⚠ No se puede conectar a la base de datos: {str(e)}")
        print("[INIT] ⚠ Las migraciones se ejecutarán en el siguiente intento")
        return  # Salir temprano si no hay conexión a la BD
    
    # 1. Ejecutar migraciones si es necesario
    try:
        print("[INIT] Ejecutando migraciones del schema público...")
        call_command('migrate_schemas', '--shared', verbosity=0)
        print("[INIT] ✓ Migraciones del schema público completadas")
        
        print("[INIT] Ejecutando migraciones de tenants...")
        call_command('migrate_schemas', verbosity=0)
        print("[INIT] ✓ Migraciones de tenants completadas")
    except Exception as e:
        print(f"[INIT] ⚠ Error ejecutando migraciones: {str(e)}")
        print("[INIT] ⚠ Continuando con la inicialización...")
    
    # 2. Verificar/crear administrador global
    with schema_context(public_schema):
        admin_email = os.getenv('GLOBAL_ADMIN_EMAIL', '')
        admin_password = os.getenv('GLOBAL_ADMIN_PASSWORD', '')
        admin_nombre = os.getenv('GLOBAL_ADMIN_NOMBRE', 'Administrador Global')
        
        if admin_email and admin_password:
            if not AdministradorGlobal.objects.filter(email=admin_email).exists():
                print(f"[INIT] Creando administrador global: {admin_email}")
                admin = AdministradorGlobal.objects.create_user(
                    email=admin_email,
                    nombre=admin_nombre,
                    password=admin_password
                )
                admin.is_staff = True
                admin.is_superuser = True
                admin.save()
                print(f"[INIT] ✓ Administrador global creado")
            else:
                print(f"[INIT] ✓ Administrador global ya existe")
        else:
            print("[INIT] ⚠ Variables GLOBAL_ADMIN_EMAIL y GLOBAL_ADMIN_PASSWORD no configuradas")
            print("[INIT] ⚠ El administrador global debe crearse manualmente")
    
    print("[INIT] Inicialización completada")


if __name__ == '__main__':
    try:
        init_production()
    except Exception as e:
        print(f"[INIT] ERROR: {str(e)}")
        # No fallar el despliegue si hay un error en la inicialización
        sys.exit(0)


"""
Script para ejecutar migraciones de un tenant específico.
Uso: python scripts/migrar_tenant.py "inacap"
"""
import os
import sys
import django
from pathlib import Path

# Agregar el directorio raíz del proyecto al PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portalAutoatencion.settings')
django.setup()

from django.core.management import call_command
from django_tenants.utils import schema_context, get_public_schema_name
from clientManager.models import Empresa
from django.db import connection


def schema_exists_in_db(schema_name):
    """Verifica si el schema físico existe en la base de datos."""
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = '{schema_name.lower()}')")
        return cursor.fetchone()[0]


def create_schema_in_db(schema_name):
    """Crea el schema físico en la base de datos."""
    print(f"[MIGRATE] Creando schema físico '{schema_name.lower()}' en la base de datos...")
    with connection.cursor() as cursor:
        cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name.lower()}"')
    print(f"[MIGRATE] ✓ Schema físico '{schema_name.lower()}' creado.")


def migrar_tenant(schema_name):
    """
    Ejecuta las migraciones para un tenant específico.
    """
    try:
        # Verificar que el tenant existe en la tabla pública
        with schema_context(get_public_schema_name()):
            try:
                tenant = Empresa.objects.get(schema_name__iexact=schema_name)
                schema_name_real = tenant.schema_name  # Obtener el schema_name real (puede tener mayúsculas)
            except Empresa.DoesNotExist:
                print(f"[MIGRATE] ✗ Error: No se encontró el tenant '{schema_name}' en el schema público.")
                print(f"[MIGRATE] Tenants disponibles:")
                for tenant_obj in Empresa.objects.all():
                    print(f"  - {tenant_obj.schema_name}")
                return False
        
        print(f"[MIGRATE] Ejecutando migraciones para el tenant: {schema_name_real}")
        
        # Verificar que el schema físico exista
        if not schema_exists_in_db(schema_name_real):
            create_schema_in_db(schema_name_real)
        
        # Ejecutar migraciones del tenant
        print(f"[MIGRATE] Ejecutando migrate_schemas para '{schema_name_real}'...")
        try:
            call_command('migrate_schemas', '--schema', schema_name_real, '--run-syncdb', verbosity=2)
            print(f"[MIGRATE] ✓ Migraciones del tenant '{schema_name_real}' completadas exitosamente")
            return True
        except Exception as e:
            print(f"[MIGRATE] ✗ Error al ejecutar migraciones: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
                
    except Exception as e:
        print(f"[MIGRATE] ✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python scripts/migrar_tenant.py <schema_name>")
        print("\nEjemplo:")
        print('  python scripts/migrar_tenant.py "inacap"')
        print('  python scripts/migrar_tenant.py "DUOC UC"')
        sys.exit(1)
    
    schema_name = sys.argv[1]
    migrar_tenant(schema_name)


"""
Script para importar datos de un tenant específico.
Uso: python scripts/importar_tenant.py "DUOC UC" datos_duoc.json
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
from django_tenants.utils import schema_context
from django.db import connection
from clientManager.models import Empresa


def importar_tenant(schema_name, fixture_file):
    """
    Importa datos de un fixture JSON en un tenant específico.
    """
    try:
        # Verificar que el tenant existe
        tenant = Empresa.objects.get(schema_name=schema_name)
        print(f"[IMPORT] Importando datos al tenant: {schema_name}")
        
        # Verificar que el archivo existe
        if not os.path.exists(fixture_file):
            print(f"[IMPORT] ✗ Error: El archivo '{fixture_file}' no existe")
            return False
        
        # 0. Verificar si el schema físico existe y crearlo si no existe
        print(f"[IMPORT] Verificando si el schema físico existe...")
        with connection.cursor() as cursor:
            # Verificar si el schema existe en PostgreSQL
            cursor.execute("""
                SELECT schema_name 
                FROM information_schema.schemata 
                WHERE schema_name = %s
            """, [schema_name.lower()])
            schema_exists = cursor.fetchone() is not None
        
        if not schema_exists:
            print(f"[IMPORT] El schema físico no existe. Creándolo...")
            try:
                # Crear el schema usando el método del tenant
                tenant.auto_create_schema = True
                tenant.save()
                print(f"[IMPORT] ✓ Schema físico creado")
            except Exception as e:
                print(f"[IMPORT] ✗ Error al crear el schema: {str(e)}")
                # Intentar crear el schema manualmente
                try:
                    with connection.cursor() as cursor:
                        # Crear el schema en PostgreSQL (normalizar a minúsculas)
                        cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name.lower()}"')
                    print(f"[IMPORT] ✓ Schema físico creado manualmente")
                except Exception as e2:
                    print(f"[IMPORT] ✗ Error al crear el schema manualmente: {str(e2)}")
                    return False
        else:
            print(f"[IMPORT] ✓ El schema físico ya existe")
        
        # 1. Ejecutar migraciones del tenant para asegurar que las tablas existan
        print(f"[IMPORT] Ejecutando migraciones del tenant '{schema_name}'...")
        try:
            # Usar migrate_schemas con --schema para ejecutar migraciones en el schema específico
            call_command('migrate_schemas', '--schema', schema_name, '--run-syncdb', verbosity=1)
            print(f"[IMPORT] ✓ Migraciones del tenant completadas")
        except Exception as e:
            print(f"[IMPORT] ⚠ Advertencia al ejecutar migraciones: {str(e)}")
            print(f"[IMPORT] Continuando con la importación de datos...")
        
        # 2. Importar datos dentro del schema del tenant
        with schema_context(schema_name):
            print(f"[IMPORT] Ejecutando loaddata dentro del schema '{schema_name}'...")
            call_command('loaddata', fixture_file, verbosity=2)
            print(f"[IMPORT] ✓ Datos importados exitosamente al tenant: {schema_name}")
            return True
            
    except Empresa.DoesNotExist:
        print(f"[IMPORT] ✗ Error: No se encontró el tenant '{schema_name}'")
        print(f"[IMPORT] Tenants disponibles:")
        for tenant in Empresa.objects.all():
            print(f"  - {tenant.schema_name}")
        return False
    except Exception as e:
        print(f"[IMPORT] ✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python scripts/importar_tenant.py <schema_name> <fixture_file>")
        print("\nEjemplo:")
        print('  python scripts/importar_tenant.py "DUOC UC" datos_duoc.json')
        sys.exit(1)
    
    schema_name = sys.argv[1]
    fixture_file = sys.argv[2]
    
    importar_tenant(schema_name, fixture_file)


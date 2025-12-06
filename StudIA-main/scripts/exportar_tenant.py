"""
Script para exportar datos de un tenant específico.
Uso: python scripts/exportar_tenant.py "DUOC UC" datos_duoc.json
"""
import os
import sys
import django
import json
from pathlib import Path

# Agregar el directorio raíz del proyecto al PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portalAutoatencion.settings')
django.setup()

from django.core.management import call_command
from django_tenants.utils import schema_context
from clientManager.models import Empresa
from io import StringIO


def exportar_tenant(schema_name, output_file):
    """
    Exporta todos los datos de un tenant específico.
    """
    try:
        # Verificar que el tenant existe
        tenant = Empresa.objects.get(schema_name=schema_name)
        print(f"[EXPORT] Exportando datos del tenant: {schema_name}")
        
        # Exportar datos dentro del schema del tenant
        with schema_context(schema_name):
            # Capturar la salida del comando dumpdata
            output = StringIO()
            call_command(
                'dumpdata',
                'loginApp.Usuario',
                'loginApp.Asignatura',
                'loginApp.Ayudantia',
                'loginApp.Inscripcion',
                'loginApp.Sede',
                stdout=output,
                indent=2
            )
            
            # Guardar en archivo
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output.getvalue())
            
            print(f"[EXPORT] ✓ Datos exportados exitosamente a: {output_file}")
            return True
            
    except Empresa.DoesNotExist:
        print(f"[EXPORT] ✗ Error: No se encontró el tenant '{schema_name}'")
        print(f"[EXPORT] Tenants disponibles:")
        for tenant in Empresa.objects.all():
            print(f"  - {tenant.schema_name}")
        return False
    except Exception as e:
        print(f"[EXPORT] ✗ Error: {str(e)}")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python scripts/exportar_tenant.py <schema_name> <output_file>")
        print("\nEjemplo:")
        print('  python scripts/exportar_tenant.py "DUOC UC" datos_duoc.json')
        print("\nTenants disponibles:")
        for tenant in Empresa.objects.all():
            print(f"  - {tenant.schema_name}")
        sys.exit(1)
    
    schema_name = sys.argv[1]
    output_file = sys.argv[2]
    
    exportar_tenant(schema_name, output_file)


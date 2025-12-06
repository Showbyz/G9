"""
Script para actualizar los dominios de los tenants para Render.
Uso: python scripts/actualizar_dominios_tenant.py
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

from django_tenants.utils import get_public_schema_name, schema_context
from clientManager.models import Empresa, Dominio


def actualizar_dominios_tenant():
    """
    Actualiza los dominios de los tenants para que apunten a Render.
    Como Render no soporta subdominios automáticamente, usamos el dominio principal.
    """
    # Dominio base de Render (sin subdominios)
    DOMINIO_BASE = "studia-8dmp.onrender.com"
    
    print(f"[DOMINIOS] Actualizando dominios de tenants para: {DOMINIO_BASE}")
    print("[DOMINIOS] NOTA: Render no soporta subdominios automáticamente.")
    print("[DOMINIOS] Los tenants se accederán usando: ?tenant=SCHEMA_NAME o /tenant/SCHEMA_NAME/")
    print()
    
    # Obtener todos los tenants
    with schema_context(get_public_schema_name()):
        tenants = Empresa.objects.all()
        
        if not tenants.exists():
            print("[DOMINIOS] ✗ No se encontraron tenants")
            return False
        
        for tenant in tenants:
            print(f"[DOMINIOS] Procesando tenant: {tenant.schema_name}")
            
            # Crear un dominio único para cada tenant
            # Aunque no exista en DNS, el middleware lo detectará desde el parámetro
            # y modificará el hostname para que coincida con este dominio
            subdominio = tenant.schema_name.lower().replace(' ', '').replace('_', '')
            nuevo_dominio = f"{subdominio}.{DOMINIO_BASE}"
            
            # Eliminar dominios antiguos que no coincidan
            dominios_antiguos = tenant.domains.exclude(domain=nuevo_dominio)
            if dominios_antiguos.exists():
                print(f"  [DOMINIOS] Eliminando {dominios_antiguos.count()} dominio(s) antiguo(s):")
                for dom in dominios_antiguos:
                    print(f"    - {dom.domain}")
                    dom.delete()
            
            # Crear o actualizar el dominio principal
            dominio_obj, created = Dominio.objects.get_or_create(
                domain=nuevo_dominio,
                defaults={'tenant': tenant, 'is_primary': True}
            )
            
            if not created:
                # Si ya existe, asegurarse de que sea el principal
                if not dominio_obj.is_primary:
                    dominio_obj.is_primary = True
                    dominio_obj.save()
                print(f"  [DOMINIOS] ✓ Dominio actualizado: {nuevo_dominio}")
            else:
                print(f"  [DOMINIOS] ✓ Dominio creado: {nuevo_dominio}")
            
            print()
    
    print("[DOMINIOS] ✓ Proceso completado")
    return True


if __name__ == '__main__':
    try:
        actualizar_dominios_tenant()
    except Exception as e:
        print(f"[DOMINIOS] ✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


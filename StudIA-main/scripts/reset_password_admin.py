"""
Script para resetear la contraseña de un AdministradorGlobal.
Uso: python scripts/reset_password_admin.py edo@admin.com nueva_contraseña
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
from clientManager.models import AdministradorGlobal


def reset_password_admin(email, nueva_password):
    """
    Resetea la contraseña de un AdministradorGlobal.
    """
    with schema_context(get_public_schema_name()):
        try:
            admin = AdministradorGlobal.objects.get(email=email)
            admin.set_password(nueva_password)
            admin.save()
            print(f"[RESET] ✓ Contraseña actualizada para: {email}")
            print(f"[RESET] Nueva contraseña: {nueva_password}")
            return True
        except AdministradorGlobal.DoesNotExist:
            print(f"[RESET] ✗ Error: No se encontró el administrador con email: {email}")
            print(f"[RESET] Administradores disponibles:")
            for admin in AdministradorGlobal.objects.all():
                print(f"  - {admin.email} ({admin.nombre})")
            return False
        except Exception as e:
            print(f"[RESET] ✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python scripts/reset_password_admin.py <email> <nueva_contraseña>")
        print("\nEjemplo:")
        print('  python scripts/reset_password_admin.py edo@admin.com MiNuevaPassword123')
        sys.exit(1)
    
    email = sys.argv[1]
    nueva_password = sys.argv[2]
    
    reset_password_admin(email, nueva_password)


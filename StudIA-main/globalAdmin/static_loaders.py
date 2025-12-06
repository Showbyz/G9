"""
Sistema de carga de archivos estáticos por tenant.
"""
from django.contrib.staticfiles.finders import BaseFinder
from django.conf import settings
import os


class TenantStaticFinder(BaseFinder):
    """
    Finder que busca archivos estáticos en directorios específicos del tenant.
    Estructura esperada:
    - loginApp/static/tenants/{tenant_theme}/...
    - loginApp/static/default/... (fallback)
    """
    
    def find(self, path, all=False):
        """
        Busca archivos estáticos en los directorios del tema del tenant.
        """
        tenant_theme = getattr(settings, 'CURRENT_TENANT_THEME', 'default')
        matches = []
        
        # Directorio base de static files
        base_static_dir = os.path.join(settings.BASE_DIR, 'loginApp', 'static')
        
        # Buscar en el directorio del tema del tenant
        theme_static_dir = os.path.join(base_static_dir, 'tenants', tenant_theme)
        theme_path = os.path.join(theme_static_dir, path)
        if os.path.exists(theme_path):
            if all:
                matches.append(theme_path)
            else:
                return theme_path
        
        # Buscar en el directorio default como fallback
        default_static_dir = os.path.join(base_static_dir, 'tenants', 'default')
        default_path = os.path.join(default_static_dir, path)
        if os.path.exists(default_path):
            if all:
                matches.append(default_path)
            else:
                return default_path
        
        # Buscar en el directorio base (para compatibilidad)
        base_path = os.path.join(base_static_dir, path)
        if os.path.exists(base_path):
            if all:
                matches.append(base_path)
            else:
                return base_path
        
        return matches if all else None
    
    def list(self, ignore_patterns):
        """
        Lista todos los archivos estáticos disponibles en los directorios del tema.
        """
        tenant_theme = getattr(settings, 'CURRENT_TENANT_THEME', 'default')
        files = []
        
        base_static_dir = os.path.join(settings.BASE_DIR, 'loginApp', 'static')
        
        # Listar archivos del tema del tenant
        theme_static_dir = os.path.join(base_static_dir, 'tenants', tenant_theme)
        if os.path.exists(theme_static_dir):
            for root, dirs, filenames in os.walk(theme_static_dir):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, theme_static_dir)
                    files.append((relative_path, file_path))
        
        # Listar archivos del tema default
        default_static_dir = os.path.join(base_static_dir, 'tenants', 'default')
        if os.path.exists(default_static_dir):
            for root, dirs, filenames in os.walk(default_static_dir):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, default_static_dir)
                    # Solo agregar si no existe en el tema del tenant
                    if not any(f[0] == relative_path for f in files):
                        files.append((relative_path, file_path))
        
        return files


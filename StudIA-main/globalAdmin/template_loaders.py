"""
Template loader personalizado para cargar templates según el tema del tenant.
"""
from django.template.loaders.filesystem import Loader as FilesystemLoader
from django.template import TemplateDoesNotExist
from django.conf import settings
import os


class TenantThemeLoader(FilesystemLoader):
    """
    Template loader que busca templates en directorios específicos del tenant.
    Estructura esperada:
    - loginApp/templates/tenants/{tenant_theme}/...
    - loginApp/templates/tenants/default/... (fallback)
    - loginApp/templates/... (compatibilidad)
    
    Si no encuentra el template, lanza TemplateDoesNotExist para que
    el siguiente loader (app_directories) lo intente.
    """
    
    def get_dirs(self):
        """
        Retorna los directorios donde buscar templates, priorizando el tema del tenant.
        """
        dirs = []
        
        # Obtener el tema del tenant desde settings (establecido por el middleware)
        tenant_theme = getattr(settings, 'CURRENT_TENANT_THEME', 'default')
        
        # Directorio base de templates
        base_template_dir = os.path.join(settings.BASE_DIR, 'loginApp', 'templates')
        
        # Agregar directorio del tema del tenant si existe
        theme_dir = os.path.join(base_template_dir, 'tenants', tenant_theme)
        if os.path.exists(theme_dir):
            dirs.append(theme_dir)
        
        # Agregar directorio default como fallback
        default_dir = os.path.join(base_template_dir, 'tenants', 'default')
        if os.path.exists(default_dir) and tenant_theme != 'default':
            dirs.append(default_dir)
        
        # Agregar directorio base de templates (para compatibilidad)
        if os.path.exists(base_template_dir):
            dirs.append(base_template_dir)
        
        # Si no hay directorios, usar el directorio base por defecto
        if not dirs:
            dirs = [base_template_dir]
        
        return dirs
    
    def load_template_source(self, template_name, template_dirs=None):
        """
        Intenta cargar el template. Si no lo encuentra, lanza TemplateDoesNotExist
        para que el siguiente loader lo intente.
        """
        if template_dirs is None:
            template_dirs = self.get_dirs()
        
        for template_dir in template_dirs:
            template_path = os.path.join(template_dir, template_name)
            if os.path.exists(template_path):
                try:
                    with open(template_path, encoding='utf-8') as f:
                        return (f.read(), template_path)
                except (IOError, OSError):
                    pass
        
        # Si no se encuentra, lanzar excepción para que el siguiente loader lo intente
        raise TemplateDoesNotExist(template_name)


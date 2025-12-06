"""
Backend de autenticación para Administradores Globales.
"""
from django.contrib.auth.backends import ModelBackend
from django_tenants.utils import schema_context, get_public_schema_name
from clientManager.models import AdministradorGlobal


class AdministradorGlobalBackend(ModelBackend):
    """
    Backend de autenticación para administradores globales.
    Solo funciona en el schema público.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email')
        
        # Asegurarse de que estamos en el schema público
        with schema_context(get_public_schema_name()):
            try:
                user = AdministradorGlobal.objects.get(email=username)
            except AdministradorGlobal.DoesNotExist:
                return None
            
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
    
    def get_user(self, user_id):
        # Asegurarse de que estamos en el schema público
        with schema_context(get_public_schema_name()):
            try:
                return AdministradorGlobal.objects.get(pk=user_id)
            except AdministradorGlobal.DoesNotExist:
                return None


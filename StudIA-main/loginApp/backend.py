from django.contrib.auth.backends import ModelBackend
from loginApp.models import Usuario

class UsuarioBackend(ModelBackend): # Gracias Chatgpt
    def authenticate(self, request, email=None, clave=None, **kwargs):
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return None
        else:
            if user.check_password(clave):
                # Verificar que el usuario esté activo
                if not user.is_active:
                    return None
                return user
    
    def get_user(self, id_usuario): # Gracias documentacion de django
        try:
            return Usuario.objects.get(pk=id_usuario)
        except Usuario.DoesNotExist:
            return None

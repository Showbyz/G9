"""
Autenticación personalizada para JWT con el modelo Usuario.
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from loginApp.models import Usuario
from django_tenants.utils import schema_context


class CustomJWTAuthentication(JWTAuthentication):
    """
    Autenticación JWT personalizada que funciona con el modelo Usuario.
    """
    def authenticate(self, request):
        """
        Sobrescribir authenticate para guardar el request y poder usarlo en get_user.
        """
        # Llamar al método padre para validar el token
        header = self.get_header(request)
        if header is None:
            return None
        
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        
        validated_token = self.get_validated_token(raw_token)
        
        # Guardar el request para usarlo en get_user
        self.request = request
        
        # Obtener el usuario usando el token validado
        user = self.get_user(validated_token)
        
        return (user, validated_token)
    
    def get_user(self, validated_token):
        """
        Intenta encontrar y retornar un usuario usando el token validado.
        Debe ejecutarse dentro del schema_context del tenant.
        """
        import sys
        
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise InvalidToken('Token no contiene información de usuario válida.')
        
        # Obtener el tenant del request si está disponible
        # El middleware ya debería haber establecido request.tenant
        request = getattr(self, 'request', None)
        
        if not request:
            sys.stdout.write("[API Mobile Authentication] ERROR: No hay request disponible\n")
            sys.stdout.flush()
            raise AuthenticationFailed('No se pudo identificar el tenant para la autenticación.')
        
        if not hasattr(request, 'tenant'):
            sys.stdout.write("[API Mobile Authentication] ERROR: No hay tenant en el request\n")
            sys.stdout.flush()
            raise AuthenticationFailed('No se pudo identificar el tenant para la autenticación.')
        
        tenant_schema = request.tenant.schema_name
        sys.stdout.write(f"[API Mobile Authentication] Buscando usuario {user_id} en schema: {tenant_schema}\n")
        sys.stdout.flush()
        
        # Usar schema_context para asegurar que la query se ejecute en el schema correcto
        with schema_context(tenant_schema):
            try:
                user = Usuario.objects.get(id_usuario=user_id)
                sys.stdout.write(f"[API Mobile Authentication] Usuario {user.email} encontrado en schema: {tenant_schema}\n")
                sys.stdout.flush()
            except Usuario.DoesNotExist:
                sys.stdout.write(f"[API Mobile Authentication] Usuario {user_id} NO encontrado en schema: {tenant_schema}\n")
                sys.stdout.flush()
                raise AuthenticationFailed('Usuario no encontrado.')
            
            if not user.is_active:
                raise AuthenticationFailed('Usuario inactivo.')
            
            return user


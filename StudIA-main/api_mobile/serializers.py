"""
Serializers para la API móvil de estudiantes.
"""
from rest_framework import serializers
from loginApp.models import Usuario, Asignatura, Ayudantia, Inscripcion, Sede
from datetime import date


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Usuario (solo lectura para estudiantes)"""
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre_usuario', 'email', 'telefono', 'cargo']
        read_only_fields = ['id_usuario', 'nombre_usuario', 'email', 'telefono', 'cargo']


class AsignaturaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Asignatura"""
    total_ayudantias_disponibles = serializers.SerializerMethodField()
    
    class Meta:
        model = Asignatura
        fields = [
            'id_asignatura', 
            'nombre', 
            'codigo', 
            'carrera', 
            'descripcion',
            'total_ayudantias_disponibles'
        ]
    
    def get_total_ayudantias_disponibles(self, obj):
        """Cuenta las ayudantías activas y disponibles"""
        # Usar las ayudantías precargadas si están disponibles
        if hasattr(obj, '_prefetched_objects_cache') and 'ayudantias' in obj._prefetched_objects_cache:
            ayudantias = obj._prefetched_objects_cache['ayudantias']
        else:
            # Si no están precargadas, acceder directamente (debe estar en schema_context)
            ayudantias = obj.ayudantias.all()
        
        return sum(1 for a in ayudantias if (
            a.is_active and 
            not a.is_cursada and 
            a.fecha >= date.today() and 
            a.cupos_disponibles > 0
        ))


class TutorSerializer(serializers.ModelSerializer):
    """Serializer simplificado para el tutor de una ayudantía"""
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre_usuario', 'email']


class AyudantiaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Ayudantía"""
    asignatura_nombre = serializers.CharField(source='asignatura.nombre', read_only=True)
    asignatura_codigo = serializers.CharField(source='asignatura.codigo', read_only=True)
    tutor_nombre = serializers.CharField(source='tutor.nombre_usuario', read_only=True)
    tutor_email = serializers.EmailField(source='tutor.email', read_only=True)
    fecha_str = serializers.SerializerMethodField()
    horario_str = serializers.SerializerMethodField()
    puede_inscribirse = serializers.SerializerMethodField()
    esta_inscrito = serializers.SerializerMethodField()
    
    class Meta:
        model = Ayudantia
        fields = [
            'id_ayudantia',
            'titulo',
            'descripcion',
            'sala',
            'fecha',
            'fecha_str',
            'horario',
            'horario_str',
            'duracion',
            'cupos_totales',
            'cupos_disponibles',
            'asignatura_nombre',
            'asignatura_codigo',
            'tutor_nombre',
            'tutor_email',
            'puede_inscribirse',
            'esta_inscrito',
        ]
    
    def get_fecha_str(self, obj):
        """Formatea la fecha como string"""
        return obj.fecha.strftime('%Y-%m-%d') if obj.fecha else None
    
    def get_horario_str(self, obj):
        """Formatea el horario como string"""
        return obj.horario.strftime('%H:%M') if obj.horario else None
    
    def get_puede_inscribirse(self, obj):
        """Verifica si el estudiante puede inscribirse"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        
        # Verificar que no sea staff ni tutor
        if request.user.is_staff or request.user.is_tutor:
            return False
        
        # Verificar condiciones
        if obj.is_cursada:
            return False
        if obj.fecha < date.today():
            return False
        if obj.cupos_disponibles <= 0:
            return False
        
        # Verificar que no esté ya inscrito
        if Inscripcion.objects.filter(
            estudiante=request.user,
            ayudantia=obj,
            estado='activa'
        ).exists():
            return False
        
        return True
    
    def get_esta_inscrito(self, obj):
        """Verifica si el estudiante está inscrito"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        
        return Inscripcion.objects.filter(
            estudiante=request.user,
            ayudantia=obj,
            estado='activa'
        ).exists()


class InscripcionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Inscripción"""
    ayudantia = AyudantiaSerializer(read_only=True)
    ayudantia_id = serializers.IntegerField(write_only=True, required=False)
    estudiante_nombre = serializers.CharField(source='estudiante.nombre_usuario', read_only=True)
    fecha_inscripcion_str = serializers.SerializerMethodField()
    
    class Meta:
        model = Inscripcion
        fields = [
            'id_inscripcion',
            'ayudantia',
            'ayudantia_id',
            'estudiante_nombre',
            'fecha_inscripcion',
            'fecha_inscripcion_str',
            'estado',
            'asistio',
        ]
        read_only_fields = ['id_inscripcion', 'fecha_inscripcion', 'estado', 'asistio']
    
    def get_fecha_inscripcion_str(self, obj):
        """Formatea la fecha de inscripción como string"""
        return obj.fecha_inscripcion.strftime('%Y-%m-%d %H:%M') if obj.fecha_inscripcion else None


class SedeSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Sede"""
    class Meta:
        model = Sede
        fields = [
            'id_sede',
            'nombre',
            'direccion',
            'latitud',
            'longitud',
        ]


class LoginSerializer(serializers.Serializer):
    """Serializer para el login de estudiantes"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        """Valida las credenciales del usuario"""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            from loginApp.models import Usuario
            from django_tenants.utils import schema_context
            
            # Asegurar que estamos en el schema correcto usando schema_context
            # Si hay un tenant en el request, usarlo
            request = self.context.get('request')
            if request and hasattr(request, 'tenant'):
                # Usar schema_context de django-tenants (método recomendado)
                with schema_context(request.tenant.schema_name):
                    print(f"[API Mobile Serializer] Usando schema_context: {request.tenant.schema_name}")
                    try:
                        user = Usuario.objects.get(email=email)
                        print(f"[API Mobile Serializer] Usuario encontrado: {user.email}")
                    except Usuario.DoesNotExist:
                        raise serializers.ValidationError({
                            'non_field_errors': ['Email o contraseña incorrectos.']
                        })
                    
                    # Verificar la contraseña dentro del schema_context
                    if not user.check_password(password):
                        raise serializers.ValidationError({
                            'non_field_errors': ['Email o contraseña incorrectos.']
                        })
                    
                    # Verificar que la cuenta esté activa
                    if not user.is_active:
                        raise serializers.ValidationError({
                            'non_field_errors': ['Tu cuenta está desactivada.']
                        })
                    
                    # Verificar que sea estudiante (no staff ni tutor)
                    if user.is_staff or user.is_tutor:
                        raise serializers.ValidationError({
                            'non_field_errors': ['Esta aplicación es solo para estudiantes.']
                        })
                    
                    # Guardar el usuario en attrs (fuera del schema_context)
                    attrs['user'] = user
            else:
                print(f"[API Mobile Serializer] WARNING: No hay tenant en el request")
                raise serializers.ValidationError({
                    'non_field_errors': ['No se pudo identificar el tenant.']
                })
            
            return attrs
        else:
            raise serializers.ValidationError({
                'non_field_errors': ['Debe proporcionar email y contraseña.']
            })


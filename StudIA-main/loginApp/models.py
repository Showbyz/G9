from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def _create_user(self, nombre_usuario, email, password, **extra_fields):
        if not email:
            raise ValueError('Falta ingresar el email')
    
        email = self.normalize_email(email)
        user = self.model(nombre_usuario=nombre_usuario, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, nombre_usuario, email=None, password=None, **extra_fields):
        return self._create_user(nombre_usuario, email, password, **extra_fields)
    
    def create_superuser(self, nombre_usuario, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        return self._create_user(nombre_usuario, email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nombre_usuario = models.CharField(max_length=25, verbose_name="Nombre de Usuario")
    email = models.EmailField(max_length=25, unique=True)
    telefono = models.IntegerField()
    cargo = models.CharField(max_length=25)
    horario_atencion = models.IntegerField(verbose_name="Horario de Atención")
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    last_login = models.DateTimeField(null=True, verbose_name="Ultimo Ingreso")
    is_active=models.BooleanField(default=True, verbose_name="Cuenta activada")
    is_staff=models.BooleanField(default=False, verbose_name="Cuenta de administrador")
    is_tutor=models.BooleanField(default=False, verbose_name="Cuenta de tutor")

    # Campos de permisos con related_name personalizados para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuario_set',
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_set',
        related_query_name='usuario',
    )

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['nombre_usuario', 'telefono', 'cargo', 'horario_atencion']
    
    objects = UsuarioManager()
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    # Funciones de caracteristicas de usuario
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    def check_password(self, password):
        return check_password(password, self.password)
    
    def __str__(self):
        return self.nombre_usuario

class Asignatura(models.Model):
    id_asignatura = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Asignatura")
    codigo = models.CharField(max_length=20, verbose_name="Código de la Asignatura")
    carrera = models.CharField(max_length=100, verbose_name="Carrera")
    descripcion = models.TextField(verbose_name="Descripción", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Asignatura Activa")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Ayudantia(models.Model):
    id_ayudantia = models.AutoField(primary_key=True)
    tutor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ayudantias_tutor')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name='ayudantias')
    titulo = models.CharField(max_length=200, verbose_name="Título de la Ayudantía")
    descripcion = models.TextField(verbose_name="Descripción")
    sala = models.CharField(max_length=50, verbose_name="Sala o Aula")
    fecha = models.DateField(verbose_name="Fecha de la Ayudantía")
    horario = models.TimeField(verbose_name="Horario")
    duracion = models.IntegerField(verbose_name="Duración (minutos)", default=60)
    cupos_totales = models.IntegerField(verbose_name="Cupos Totales")
    cupos_disponibles = models.IntegerField(verbose_name="Cupos Disponibles")
    is_active = models.BooleanField(default=True, verbose_name="Ayudantía Activa")
    is_cursada = models.BooleanField(default=False, verbose_name="Ayudantía Cursada")
    fecha_cursada = models.DateTimeField(null=True, blank=True, verbose_name="Fecha en que se Cursó")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ayudantía"
        verbose_name_plural = "Ayudantías"
    
    def __str__(self):
        return f"{self.asignatura.nombre} - {self.titulo}"
    
    def save(self, *args, **kwargs):
        # Al crear una nueva ayudantía, los cupos disponibles son iguales a los totales
        if not self.pk:
            self.cupos_disponibles = self.cupos_totales
        super().save(*args, **kwargs)

class Inscripcion(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='inscripciones')
    ayudantia = models.ForeignKey(Ayudantia, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Inscripción")
    estado = models.CharField(max_length=20, choices=[
        ('activa', 'Activa'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada')
    ], default='activa', verbose_name="Estado")
    asistio = models.BooleanField(default=False, verbose_name="Asistió a la Ayudantía")
    
    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = ['estudiante', 'ayudantia']  # Un estudiante no puede inscribirse dos veces en la misma ayudantía
    
    def __str__(self):
        return f"{self.estudiante.nombre_usuario} - {self.ayudantia.titulo}"

class Sede(models.Model):
    """
    Modelo para almacenar las sedes de la institución con sus coordenadas geográficas.
    """
    id_sede = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Sede")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    latitud = models.FloatField(verbose_name="Latitud")
    longitud = models.FloatField(verbose_name="Longitud")
    is_active = models.BooleanField(default=True, verbose_name="Sede Activa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
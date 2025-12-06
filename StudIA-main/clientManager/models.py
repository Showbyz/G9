from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Empresa(TenantMixin):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=25, verbose_name="Nombre de la Empresa")
    created_at = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1, verbose_name="Estado")
    nombre_sn = models.CharField(max_length=30, verbose_name="Nombre de ServiceNow")
    casos_disponibles = ArrayField(models.TextField(), editable=False, default=list)
    
    # Campo para el tema/diseño del tenant
    tema = models.CharField(max_length=50, default='default', verbose_name="Tema del Tenant")
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

class Dominio(DomainMixin):
    pass

# Modelo para Administradores Globales (solo en schema público)
class AdministradorGlobalManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class AdministradorGlobal(AbstractBaseUser, PermissionsMixin):
    """
    Usuario administrador global que existe solo en el schema público.
    No pertenece a ningún tenant específico.
    """
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_staff = models.BooleanField(default=True, verbose_name="Es Staff")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    
    # Campos de permisos con related_name personalizados para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='global_admin_set',
        related_query_name='global_admin',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='global_admin_set',
        related_query_name='global_admin',
    )
    
    objects = AdministradorGlobalManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']
    
    class Meta:
        verbose_name = "Administrador Global"
        verbose_name_plural = "Administradores Globales"
        db_table = 'administradores_globales'
    
    def __str__(self):
        return f"{self.nombre} ({self.email})"

# Create your models here.

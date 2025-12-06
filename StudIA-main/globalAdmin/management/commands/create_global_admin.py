"""
Comando de gestión para crear administradores globales.
"""
from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context, get_public_schema_name
from clientManager.models import AdministradorGlobal


class Command(BaseCommand):
    help = 'Crea un administrador global en el schema público'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email del administrador')
        parser.add_argument('nombre', type=str, help='Nombre completo del administrador')
        parser.add_argument('password', type=str, help='Contraseña del administrador')
        parser.add_argument(
            '--superuser',
            action='store_true',
            help='Crear como superusuario',
        )

    def handle(self, *args, **options):
        with schema_context(get_public_schema_name()):
            try:
                admin = AdministradorGlobal.objects.create_user(
                    email=options['email'],
                    nombre=options['nombre'],
                    password=options['password']
                )
                
                if options['superuser']:
                    admin.is_staff = True
                    admin.is_superuser = True
                    admin.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Superusuario global creado exitosamente: {admin.email}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Administrador global creado exitosamente: {admin.email}'
                        )
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error al crear administrador: {str(e)}')
                )


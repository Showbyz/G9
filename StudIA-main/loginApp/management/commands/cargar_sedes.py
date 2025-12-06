"""
Comando de Django para cargar las sedes iniciales de Duoc UC.
Uso: python manage.py cargar_sedes [--schema SCHEMA_NAME]
Si no se especifica schema, carga en todos los tenants.
"""
from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context, get_tenant_model, tenant_context
from loginApp.models import Sede


class Command(BaseCommand):
    help = 'Carga las sedes iniciales de Duoc UC con sus coordenadas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--schema',
            type=str,
            help='Nombre del schema del tenant (opcional). Si no se especifica, carga en todos los tenants.',
        )

    def handle(self, *args, **options):
        schema_name = options.get('schema')
        
        if schema_name:
            # Cargar solo en el tenant especificado
            self.cargar_sedes_en_tenant(schema_name)
        else:
            # Cargar en todos los tenants
            TenantModel = get_tenant_model()
            tenants = TenantModel.objects.exclude(schema_name='public')
            
            self.stdout.write(f'Cargando sedes en {tenants.count()} tenant(s)...\n')
            
            for tenant in tenants:
                self.stdout.write(f'\n--- Procesando tenant: {tenant.schema_name} ---')
                self.cargar_sedes_en_tenant(tenant.schema_name)
    
    def cargar_sedes_en_tenant(self, schema_name):
        """
        Carga las sedes en un tenant específico.
        """
        with schema_context(schema_name):
            # Datos de las sedes de Duoc UC
            sedes_data = [
            {
                'nombre': 'Sede Alameda',
                'direccion': 'Av. España 8, Santiago Centro',
                'latitud': -33.44885,
                'longitud': -70.66872
            },
            {
                'nombre': 'Sede Antonio Varas',
                'direccion': 'Antonio Varas 666, Providencia',
                'latitud': -33.44392,
                'longitud': -70.62663
            },
            {
                'nombre': 'Sede Maipú',
                'direccion': 'Av. Esquina Blanca 501, Maipú',
                'latitud': -33.51054,
                'longitud': -70.75238
            },
            {
                'nombre': 'Sede Padre Alonso de Ovalle',
                'direccion': 'Alonso de Ovalle 1586, Santiago Centro',
                'latitud': -33.44781,
                'longitud': -70.65563
            },
            {
                'nombre': 'Sede Plaza Norte',
                'direccion': 'Calle 1, N° 1737 (Mall Plaza Norte), Huechuraba',
                'latitud': -33.36642,
                'longitud': -70.67841
            },
            {
                'nombre': 'Sede Plaza Oeste',
                'direccion': 'Av. Américo Vespucio 1501 (Mall Plaza Oeste), Cerrillos',
                'latitud': -33.51661,
                'longitud': -70.71636
            },
            {
                'nombre': 'Sede Plaza Vespucio',
                'direccion': 'Av. Vicuña Mackenna Ote 7110 (Mall Plaza Vespucio), La Florida',
                'latitud': -33.51715,
                'longitud': -70.59852
            },
            {
                'nombre': 'Sede Puente Alto',
                'direccion': 'Av. Concha y Toro 1340, Puente Alto',
                'latitud': -33.58493,
                'longitud': -70.56634
            },
            {
                'nombre': 'Sede San Bernardo',
                'direccion': 'Freire 857, San Bernardo',
                'latitud': -33.59432,
                'longitud': -70.69921
            },
            {
                'nombre': 'Sede San Carlos de Apoquindo',
                'direccion': 'Camino El Alba 12881, Las Condes',
                'latitud': -33.39524,
                'longitud': -70.50461
            },
            {
                'nombre': 'Sede San Joaquín',
                'direccion': 'Av. Vicuña Mackenna 4917, San Joaquín',
                'latitud': -33.50042,
                'longitud': -70.61196
            },
            {
                'nombre': 'Sede Melipilla',
                'direccion': 'Serrano 1105, Melipilla',
                'latitud': -33.69361,
                'longitud': -71.21483
            }
            ]
            
            creadas = 0
            actualizadas = 0
            
            for sede_data in sedes_data:
                sede, created = Sede.objects.get_or_create(
                    nombre=sede_data['nombre'],
                    defaults={
                        'direccion': sede_data['direccion'],
                        'latitud': sede_data['latitud'],
                        'longitud': sede_data['longitud'],
                        'is_active': True
                    }
                )
                
                if created:
                    creadas += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'[OK] Creada: {sede.nombre}')
                    )
                else:
                    # Actualizar si ya existe pero los datos son diferentes
                    actualizado = False
                    if sede.direccion != sede_data['direccion']:
                        sede.direccion = sede_data['direccion']
                        actualizado = True
                    if sede.latitud != sede_data['latitud']:
                        sede.latitud = sede_data['latitud']
                        actualizado = True
                    if sede.longitud != sede_data['longitud']:
                        sede.longitud = sede_data['longitud']
                        actualizado = True
                    
                    if actualizado:
                        sede.save()
                        actualizadas += 1
                        self.stdout.write(
                            self.style.WARNING(f'[UPDATE] Actualizada: {sede.nombre}')
                        )
                    else:
                        self.stdout.write(
                            self.style.NOTICE(f'[EXISTS] Ya existe: {sede.nombre}')
                        )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n[COMPLETADO] Proceso en {schema_name}: {creadas} sedes creadas, {actualizadas} actualizadas'
                )
            )


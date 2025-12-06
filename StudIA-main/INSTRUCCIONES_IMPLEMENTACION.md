# Instrucciones de Implementación - Arquitectura Multi-Tenant

## Pasos para Activar la Nueva Arquitectura

### 1. Crear y Aplicar Migraciones

```bash
# Activar el entorno virtual
.\env\Scripts\Activate.ps1

# Crear las migraciones para los nuevos modelos
python manage.py makemigrations clientManager
python manage.py makemigrations globalAdmin

# Aplicar las migraciones al schema público
python manage.py migrate_schemas --shared
```

### 2. Crear un Administrador Global

Puedes crear un administrador global de dos formas:

#### Opción A: Desde el shell de Django

```bash
python manage.py shell
```

```python
from clientManager.models import AdministradorGlobal

admin = AdministradorGlobal.objects.create_user(
    email='admin@global.com',
    nombre='Administrador Global',
    password='password123'
)
admin.is_staff = True
admin.is_superuser = True
admin.save()
```

#### Opción B: Crear un comando de gestión

Crea el archivo `globalAdmin/management/commands/create_global_admin.py`:

```python
from django.core.management.base import BaseCommand
from clientManager.models import AdministradorGlobal

class Command(BaseCommand):
    help = 'Crea un administrador global'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)
        parser.add_argument('nombre', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        admin = AdministradorGlobal.objects.create_user(
            email=options['email'],
            nombre=options['nombre'],
            password=options['password']
        )
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        self.stdout.write(self.style.SUCCESS(f'Administrador global creado: {admin.email}'))
```

Luego ejecuta:
```bash
python manage.py create_global_admin admin@global.com "Admin Global" password123
```

### 3. Configurar Dominio Público

Asegúrate de tener un dominio configurado para el schema público. Por defecto, django-tenants usa el dominio sin subdominio.

Si estás en desarrollo local, puedes acceder al panel global desde:
- `http://localhost:8000/global/login/`

### 4. Estructura de Directorios para Theming

Crea la estructura base para los temas:

```bash
mkdir -p loginApp/templates/tenants/default
mkdir -p loginApp/static/tenants/default
```

Opcionalmente, copia los templates actuales como base:

```bash
# Copiar templates base al tema default
cp -r loginApp/templates/* loginApp/templates/tenants/default/ 2>/dev/null || true
```

### 5. Reiniciar el Servidor

```bash
# Detener el servidor actual (Ctrl+C)
# Reiniciar
python manage.py runserver
```

## Uso Rápido

### Acceder al Panel Global

1. Ve a: `http://localhost:8000/global/login/`
2. Inicia sesión con las credenciales del AdministradorGlobal
3. Serás redirigido al dashboard

### Crear un Tenant desde el Panel

1. En el dashboard, haz clic en "Ver Todos los Tenants"
2. Haz clic en "Crear Tenant"
3. Completa el formulario:
   - **Nombre de la Empresa**: Nombre del tenant
   - **Dominio Principal**: ej. `tenant1.localhost`
   - **Tema**: Selecciona el tema (default, tema1, tema2, etc.)
   - **Estado**: Activo/Inactivo
4. Haz clic en "Crear Tenant"

### Impersonar un Tenant

1. Desde la lista de tenants, haz clic en "Entrar"
2. Serás redirigido al dominio del tenant
3. Navega como si fueras un usuario del tenant

### Crear un Tema Personalizado

1. Crea los directorios:
   ```bash
   mkdir -p loginApp/templates/tenants/mi_tema
   mkdir -p loginApp/static/tenants/mi_tema/css
   mkdir -p loginApp/static/tenants/mi_tema/js
   mkdir -p loginApp/static/tenants/mi_tema/img
   ```

2. Copia y personaliza los templates:
   ```bash
   cp loginApp/templates/base.html loginApp/templates/tenants/mi_tema/
   cp loginApp/templates/login.html loginApp/templates/tenants/mi_tema/
   # Edita los archivos según necesites
   ```

3. Crea tus archivos CSS/JS personalizados en `loginApp/static/tenants/mi_tema/`

4. Asigna el tema al tenant desde el panel global

## Verificación

### Verificar que Todo Funciona

1. **Panel Global**: Accede a `/global/login/` y verifica que puedas iniciar sesión
2. **Lista de Tenants**: Verifica que puedas ver los tenants existentes
3. **Crear Tenant**: Crea un tenant de prueba
4. **Impersonación**: Verifica que puedas "entrar" al tenant
5. **Theming**: Verifica que los templates se carguen desde el directorio del tema

### Troubleshooting

#### Error: "No module named 'globalAdmin'"
- Verifica que `globalAdmin` esté en `SHARED_APPS` en `settings.py`
- Reinicia el servidor

#### Error: "AdministradorGlobal matching query does not exist"
- Crea un administrador global usando los pasos del punto 2

#### Los templates no se cargan del tema
- Verifica que el directorio `loginApp/templates/tenants/{tema}/` exista
- Verifica que el campo `tema` del tenant esté configurado correctamente
- Revisa los logs del servidor para errores

#### Los static files no se cargan
- Verifica que el directorio `loginApp/static/tenants/{tema}/` exista
- Ejecuta `python manage.py collectstatic` si es necesario
- Verifica que `STATICFILES_FINDERS` incluya `TenantStaticFinder`

## Próximos Pasos

1. **Personalizar Templates del Panel Global**: Edita los templates en `globalAdmin/templates/globalAdmin/`
2. **Crear Más Temas**: Crea temas personalizados para diferentes tenants
3. **Agregar Funcionalidades**: Extiende las vistas del panel global según tus necesidades
4. **Seguridad**: Revisa y ajusta los permisos según tus requerimientos de seguridad

## Notas Importantes

- Los administradores globales **NO** pertenecen a ningún tenant
- El panel global solo funciona en el schema público
- La impersonación funciona mediante redirección al dominio del tenant
- Los temas se aplican automáticamente según el campo `tema` del tenant
- Si un template/static no existe en el tema, se usa el tema `default` como fallback



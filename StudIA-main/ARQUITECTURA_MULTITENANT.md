# Arquitectura Multi-Tenant con Administración Global

## Resumen

Esta implementación proporciona una arquitectura completa para gestionar múltiples tenants con:

1. **Panel de Administración Global** en el schema público
2. **Sistema de Impersonación** de tenants
3. **Sistema de Theming** independiente por tenant

## Componentes Principales

### 1. Modelo de Administrador Global

**Ubicación**: `clientManager/models.py`

El modelo `AdministradorGlobal` permite crear usuarios que existen solo en el schema público y no pertenecen a ningún tenant específico. Estos usuarios pueden gestionar todos los tenants del sistema.

```python
from clientManager.models import AdministradorGlobal

# Crear un administrador global
admin = AdministradorGlobal.objects.create_user(
    email='admin@global.com',
    nombre='Administrador Global',
    password='password123'
)
```

### 2. App globalAdmin

**Ubicación**: `globalAdmin/`

Contiene:
- **Middleware**: Detecta el schema público y maneja la impersonación
- **Vistas**: Panel de administración, gestión de tenants, impersonación
- **Backend de autenticación**: Para administradores globales
- **Template/Static Loaders**: Sistema de theming

### 3. Sistema de Theming

Cada tenant puede tener su propio diseño visual mediante el campo `tema` en el modelo `Empresa`.

#### Estructura de Directorios

```
loginApp/
├── templates/
│   ├── tenants/
│   │   ├── default/          # Tema por defecto (fallback)
│   │   ├── tema1/            # Tema personalizado 1
│   │   └── tema2/            # Tema personalizado 2
│   └── [templates base]      # Templates compartidos
└── static/
    ├── tenants/
    │   ├── default/          # Archivos estáticos por defecto
    │   ├── tema1/            # CSS/JS/Imágenes del tema 1
    │   └── tema2/            # CSS/JS/Imágenes del tema 2
    └── [static base]         # Archivos estáticos compartidos
```

#### Cómo Funciona

1. El middleware `TenantThemeMiddleware` detecta el tema del tenant actual
2. El `TenantThemeLoader` busca templates en `templates/tenants/{tema}/`
3. El `TenantStaticFinder` busca archivos estáticos en `static/tenants/{tema}/`
4. Si no encuentra en el tema específico, usa el tema `default` como fallback

## Uso

### Acceso al Panel Global

1. Acceder a: `http://localhost:8000/global/login/`
2. Iniciar sesión con credenciales de `AdministradorGlobal`
3. Serás redirigido al dashboard global

### Gestión de Tenants

Desde el panel global puedes:

- **Ver lista de tenants**: `/global/tenants/`
- **Crear nuevo tenant**: `/global/tenants/create/`
- **Editar tenant**: `/global/tenants/{id}/edit/`
- **Suspender/Activar tenant**: Botones en la lista
- **Impersonar tenant**: Botón "Entrar" que te redirige al tenant

### Impersonación de Tenants

1. Desde la lista de tenants, hacer clic en "Entrar"
2. Serás redirigido al dominio del tenant
3. La sesión de impersonación se guarda en `request.session`
4. Para dejar de impersonar, usar: `/global/stop-impersonate/`

### Configurar Tema de un Tenant

1. Editar el tenant desde el panel global
2. Seleccionar el tema deseado en el campo "Tema"
3. Guardar cambios
4. El tenant ahora cargará templates y static files de ese tema

## Creación de Temas Personalizados

### Paso 1: Crear Estructura de Directorios

```bash
mkdir -p loginApp/templates/tenants/mi_tema
mkdir -p loginApp/static/tenants/mi_tema/css
mkdir -p loginApp/static/tenants/mi_tema/js
mkdir -p loginApp/static/tenants/mi_tema/img
```

### Paso 2: Crear Templates

Copia los templates base a tu tema y personalízalos:

```bash
cp loginApp/templates/base.html loginApp/templates/tenants/mi_tema/
cp loginApp/templates/login.html loginApp/templates/tenants/mi_tema/
# ... etc
```

### Paso 3: Crear Archivos Estáticos

Crea tus CSS, JS e imágenes personalizadas:

```bash
# loginApp/static/tenants/mi_tema/css/estilos.css
# loginApp/static/tenants/mi_tema/js/custom.js
# loginApp/static/tenants/mi_tema/img/logo.png
```

### Paso 4: Asignar Tema al Tenant

Desde el panel global, edita el tenant y selecciona "mi_tema" como tema.

## Migraciones

Después de agregar los nuevos modelos, ejecutar:

```bash
python manage.py migrate_schemas --shared
```

Esto creará las tablas de `AdministradorGlobal` y actualizará el modelo `Empresa` con el campo `tema`.

## Seguridad

### Decoradores de Seguridad

- `@global_admin_required`: Verifica que el usuario sea AdministradorGlobal y esté en schema público
- `@login_required`: Verifica autenticación estándar de Django

### Middleware de Seguridad

- `PublicSchemaMiddleware`: Detecta y valida acceso al schema público
- `TenantThemeMiddleware`: Establece el tema del tenant actual

## Consideraciones Importantes

1. **Schema Público**: El panel global solo funciona cuando se accede desde el schema público (dominio por defecto sin tenant)

2. **Impersonación**: La impersonación funciona mediante redirección al dominio del tenant. El administrador global debe tener acceso a ese dominio.

3. **Templates Compartidos**: Los templates en `loginApp/templates/` (fuera de `tenants/`) son compartidos y se usan como último recurso.

4. **Static Files**: Similar a templates, los archivos en `loginApp/static/` (fuera de `tenants/`) son compartidos.

5. **Fallback**: Si un template o archivo estático no existe en el tema del tenant, se busca en `default` y luego en el directorio base.

## Ejemplo de Flujo Completo

1. **Admin Global** inicia sesión en `/global/login/`
2. Ve el dashboard con estadísticas de tenants
3. Crea un nuevo tenant con tema "tema1"
4. Hace clic en "Entrar" para impersonar el tenant
5. Es redirigido a `http://tenant1.localhost:8000`
6. El sistema carga templates de `templates/tenants/tema1/`
7. El sistema carga static files de `static/tenants/tema1/`
8. El admin puede navegar el tenant como si fuera un usuario normal
9. Para volver, accede a `/global/stop-impersonate/`

## Troubleshooting

### El tema no se aplica

- Verificar que el campo `tema` del tenant esté configurado correctamente
- Verificar que existan los directorios `templates/tenants/{tema}/` y `static/tenants/{tema}/`
- Revisar los logs del servidor para errores de carga de templates

### No puedo acceder al panel global

- Verificar que estés accediendo desde el dominio público (sin subdominio de tenant)
- Verificar que el usuario sea de tipo `AdministradorGlobal`
- Revisar que el middleware esté correctamente configurado en `settings.py`

### La impersonación no funciona

- Verificar que el tenant tenga al menos un dominio configurado
- Verificar que el dominio sea accesible desde tu navegador
- Revisar la configuración de `ALLOWED_HOSTS` en settings



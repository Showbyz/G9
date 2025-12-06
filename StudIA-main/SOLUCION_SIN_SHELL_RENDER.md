# Solución: Ejecutar Migraciones y Crear Admin sin Shell de Render

## 🔴 Problema

Render.com requiere pago para usar el Shell, pero necesitamos:
- Ejecutar migraciones
- Crear el administrador global

---

## ✅ Solución Aplicada

### 1. Migraciones Automáticas en Build

Las migraciones se ejecutan automáticamente durante el despliegue en el `buildCommand`:

```yaml
buildCommand: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py migrate_schemas --shared && python manage.py migrate_schemas && python manage.py collectstatic --noinput
```

**Esto ejecuta:**
1. `migrate_schemas --shared` - Migraciones del schema público
2. `migrate_schemas` - Migraciones de todos los tenants
3. `collectstatic` - Recopilar archivos estáticos

### 2. Script de Inicialización Automática

Se creó `scripts/init_production.py` que se puede ejecutar al iniciar la aplicación para crear el administrador global automáticamente.

---

## 🔧 Opciones para Crear el Administrador Global

### Opción 1: Variables de Entorno (RECOMENDADA)

Configura estas variables de entorno en Render.com:

1. Ve a tu servicio en Render.com
2. Click en "Environment"
3. Agrega estas variables:
   - `GLOBAL_ADMIN_EMAIL`: `tu-email@ejemplo.com`
   - `GLOBAL_ADMIN_PASSWORD`: `tu-password-segura`
   - `GLOBAL_ADMIN_NOMBRE`: `Administrador Global`

4. El script `init_production.py` creará automáticamente el administrador al iniciar la app.

### Opción 2: Ejecutar desde Local (GRATIS)

Conéctate a la base de datos de Render desde tu máquina local:

1. **Obtén las credenciales de la base de datos:**
   - En Render.com → Tu base de datos → "Info"
   - Copia: `Internal Database URL` o las credenciales individuales

2. **Crea un archivo `.env.production` temporal:**
```env
DATABASE_URL=postgresql://usuario:password@host:puerto/database
SECRET_KEY=tu-secret-key-de-render
DEBUG=False
ALLOWED_HOSTS=tu-app.onrender.com
```

3. **Ejecuta desde local:**
```bash
# Activar tu entorno virtual
.\env\Scripts\activate

# Configurar variables de entorno
set DATABASE_URL=postgresql://usuario:password@host:puerto/database
set SECRET_KEY=tu-secret-key-de-render
set DEBUG=False

# Ejecutar migraciones
python manage.py migrate_schemas --shared
python manage.py migrate_schemas

# Crear administrador global
python manage.py create_global_admin tu-email@ejemplo.com "Tu Nombre" tu-password --superuser
```

### Opción 3: Usar el Panel de Administración (Después de Crear el Primer Admin)

Una vez que tengas el primer administrador global, puedes crear más desde el panel web.

---

## 📝 Pasos Recomendados

### Paso 1: Configurar Variables de Entorno en Render

1. Ve a tu servicio en Render.com
2. Click en "Environment"
3. Agrega:
   ```
   GLOBAL_ADMIN_EMAIL=admin@tu-dominio.com
   GLOBAL_ADMIN_PASSWORD=PasswordSegura123!
   GLOBAL_ADMIN_NOMBRE=Administrador Principal
   ```

### Paso 2: Modificar `wsgi.py` para Ejecutar Inicialización

Opcional: Puedes modificar `wsgi.py` para ejecutar el script de inicialización automáticamente:

```python
# portalAutoatencion/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portalAutoatencion.settings')

# Ejecutar inicialización solo en producción
if os.getenv('RENDER') or os.getenv('DATABASE_URL'):
    try:
        from scripts.init_production import init_production
        init_production()
    except Exception as e:
        print(f"Error en inicialización: {e}")

application = get_wsgi_application()
```

### Paso 3: Hacer Deploy

Las migraciones se ejecutarán automáticamente durante el build.

---

## 🎯 Resumen de Cambios

### `render.yaml`
```diff
- buildCommand: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
+ buildCommand: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py migrate_schemas --shared && python manage.py migrate_schemas && python manage.py collectstatic --noinput
```

### Nuevo archivo: `scripts/init_production.py`
- Script que crea el administrador global automáticamente si las variables de entorno están configuradas

---

## ⚠️ Consideraciones Importantes

### Migraciones Automáticas

- ✅ **Ventaja**: Se ejecutan automáticamente en cada despliegue
- ⚠️ **Cuidado**: Si hay errores en las migraciones, el build fallará
- ⚠️ **Nota**: Solo ejecuta migraciones si la base de datos ya existe

### Administrador Global

- ✅ **Opción 1 (Variables de entorno)**: Automático, pero requiere configurar variables
- ✅ **Opción 2 (Desde local)**: Gratis, pero requiere acceso a la base de datos
- ⚠️ **Seguridad**: Nunca expongas las credenciales del administrador global en el código

---

## 📚 Referencias

- [Render.com Environment Variables](https://render.com/docs/environment-variables)
- [Django-tenants Migrations](https://django-tenants.readthedocs.io/en/latest/use.html#migrations)

---

**¿Necesitas ayuda con alguna de estas opciones?** ¡Pregunta!


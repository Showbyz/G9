# Guía de Despliegue - Portal de Autoatención

Esta guía te ayudará a desplegar tu aplicación Django con multi-tenancy en internet de forma gratuita o económica.

## 📋 Requisitos del Proyecto

- **Django 5.0.2** con django-tenants
- **PostgreSQL** (requerido por django-tenants)
- **Gunicorn** (ya incluido en requirements.txt)
- **API REST** para aplicación móvil
- **Archivos estáticos** (CSS, JS, imágenes)

---

## 🆓 Opción 1: Render.com (RECOMENDADA - GRATIS)

**Ventajas:**
- ✅ **100% Gratis** para proyectos personales/educativos
- ✅ PostgreSQL gratuito incluido
- ✅ SSL/HTTPS automático
- ✅ Despliegue automático desde GitHub
- ✅ Fácil de configurar
- ✅ Soporta Django con multi-tenancy

**Límites del plan gratuito:**
- El servicio se "duerme" después de 15 minutos de inactividad (se despierta en ~30 segundos)
- PostgreSQL: 90 días de datos, luego se elimina si no hay actividad
- 750 horas/mes de tiempo de ejecución

### Pasos para desplegar en Render:

#### 1. Preparar el proyecto

**✅ Ya está listo!** He creado los archivos necesarios:
- `Procfile` - Configuración para Gunicorn
- `render.yaml` - Configuración de Render.com
- `requirements.txt` - Actualizado con dependencias necesarias
- `settings.py` - Configurado para producción

1. **El archivo `runtime.txt`** ya está creado en la raíz del proyecto para forzar Python 3.11.9:
   ```
   python-3.11.9
   ```

2. **El archivo `render.yaml`** ya está creado en la raíz del proyecto:

```yaml
services:
  - type: web
    name: portal-autoatencion
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput
    startCommand: gunicorn portalAutoatencion.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.9
      - key: DATABASE_URL
        fromDatabase:
          name: portal-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: portal-autoatencion.onrender.com
      - key: CSRF_TRUSTED_ORIGINS
        value: https://portal-autoatencion.onrender.com

databases:
  - name: portal-db
    databaseName: portal
    user: portal_user
    plan: free
```

2. **El archivo `Procfile`** ya está creado.

3. **El archivo `settings.py`** ya está actualizado para producción con:

- ✅ Soporte para `DATABASE_URL` y variables individuales
- ✅ Configuración de WhiteNoise para archivos estáticos
- ✅ Variables de entorno para `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- ✅ Configuración de seguridad SSL/HTTPS para producción
- ✅ CORS configurado para producción y desarrollo

#### 2. Verificar que no se suban archivos sensibles

Asegúrate de tener un `.gitignore` que incluya:
```
.env
*.pyc
__pycache__/
staticfiles/
media/
db.sqlite3
```

#### 3. Subir a GitHub

```bash
git init
git add .
git commit -m "Preparado para despliegue"
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
```

#### 4. Desplegar en Render

1. Ve a [render.com](https://render.com) y crea una cuenta (gratis)
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Name**: `portal-autoatencion`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn portalAutoatencion.wsgi:application`
5. Click en "Add Database" → PostgreSQL (Free)
6. Agregar variables de entorno:
   - `SECRET_KEY`: Genera una nueva clave secreta
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `tu-app.onrender.com,*.onrender.com` (el `*` permite subdominios para tenants)
   - `CSRF_TRUSTED_ORIGINS`: `https://tu-app.onrender.com,https://*.onrender.com` (permite subdominios)
   - `CORS_ALLOWED_ORIGINS`: `https://tu-app.onrender.com,https://*.onrender.com` (si usas API móvil)
7. Click "Create Web Service"

#### 5. Ejecutar migraciones

**✅ Las migraciones se ejecutan automáticamente** durante el despliegue en el `buildCommand`.

Si necesitas ejecutarlas manualmente o desde local:

**Opción A: Desde tu máquina local (GRATIS)**

1. Obtén las credenciales de la base de datos de Render:
   - En Render.com → Tu base de datos → "Info"
   - Copia el `Internal Database URL` o las credenciales individuales

2. Configura las variables de entorno localmente:
```bash
# En PowerShell
$env:DATABASE_URL="postgresql://usuario:password@host:puerto/database"
$env:SECRET_KEY="tu-secret-key-de-render"
$env:DEBUG="False"
```

3. Ejecuta las migraciones:
```bash
python manage.py migrate_schemas --shared
python manage.py migrate_schemas
```

**Opción B: Las migraciones ya se ejecutaron automáticamente**

El `buildCommand` en `render.yaml` ya incluye las migraciones, así que deberían estar aplicadas.

**Importante:** Si ya tienes tenants creados localmente, necesitarás:
1. Exportar los datos de tu base de datos local
2. Importarlos en la base de datos de Render

O crear los tenants nuevamente usando el panel de administración global (después de crear el admin).

#### 6. Configurar Dominios de Tenants en Producción

Después de las migraciones, necesitas actualizar los dominios de tus tenants para que funcionen con los subdominios de Render:

1. En el Shell de Render, ejecuta:
```python
python manage.py shell
```

2. Actualiza los dominios (ejemplo para DUOC):
```python
from clientManager.models import Empresa, Dominio

# Obtener el tenant
duoc = Empresa.objects.get(schema_name='DUOC UC')

# Eliminar dominio localhost si existe
Dominio.objects.filter(tenant=duoc, domain__contains='localhost').delete()

# Crear dominio de producción
Dominio.objects.create(
    domain='duoc.tu-app.onrender.com',  # Reemplaza 'tu-app' con tu nombre real
    tenant=duoc,
    is_primary=True
)
```

3. Repite para cada tenant (INACAP, DSA, etc.)

**Nota**: Render.com redirige automáticamente todos los subdominios (`*.onrender.com`) a tu aplicación, así que no necesitas configuración adicional en Render.

**Ver documentación completa**: Ver `TENANTS_EN_PRODUCCION.md` para más detalles.

#### 7. Crear Administrador Global

**Opción A: Usando Variables de Entorno (RECOMENDADA - Automático)**

1. Ve a tu servicio en Render.com → "Environment"
2. Agrega estas variables:
   - `GLOBAL_ADMIN_EMAIL`: `tu-email@ejemplo.com`
   - `GLOBAL_ADMIN_PASSWORD`: `tu-password-segura`
   - `GLOBAL_ADMIN_NOMBRE`: `Administrador Global`
3. Reinicia el servicio (o haz un nuevo deploy)
4. El script `scripts/init_production.py` creará automáticamente el administrador

**Opción B: Desde tu máquina local (GRATIS)**

1. Obtén las credenciales de la base de datos de Render (ver paso 5)
2. Configura las variables de entorno localmente:
```bash
$env:DATABASE_URL="postgresql://usuario:password@host:puerto/database"
$env:SECRET_KEY="tu-secret-key-de-render"
$env:DEBUG="False"
```
3. Ejecuta:
```bash
python manage.py create_global_admin tu-email@ejemplo.com "Tu Nombre" tu-password --superuser
```

4. Accede al panel en:
```
https://tu-app.onrender.com/global/login/
```

**Ver documentación completa**: 
- `PANEL_ADMINISTRACION_PRODUCCION.md` - Panel de administración
- `SOLUCION_SIN_SHELL_RENDER.md` - Solución sin shell de Render
- `GUIA_TRANSFERIR_DATOS_RENDER.md` - **Guía completa para transferir datos desde local a Render**

---

## 🚂 Opción 2: Railway.app (GRATIS con límites)

**Ventajas:**
- ✅ $5 de crédito gratis mensual (suficiente para proyectos pequeños)
- ✅ PostgreSQL incluido
- ✅ SSL automático
- ✅ Despliegue desde GitHub

**Pasos:**

1. Ve a [railway.app](https://railway.app) y crea cuenta
2. "New Project" → "Deploy from GitHub"
3. Agrega PostgreSQL desde "New" → "Database"
4. Configura variables de entorno similares a Render
5. Railway detecta automáticamente Django y lo despliega

---

## 🪂 Opción 3: Fly.io (GRATIS)

**Ventajas:**
- ✅ 3 VMs pequeñas gratis permanentemente
- ✅ PostgreSQL disponible
- ✅ SSL automático
- ✅ Muy rápido

**Pasos:**

1. Instala Fly CLI: `iwr https://fly.io/install.ps1 -useb | iex`
2. Login: `fly auth login`
3. Crea app: `fly launch`
4. Agrega PostgreSQL: `fly postgres create`
5. Conecta: `fly postgres connect -a tu-app-db`

---

## 💰 Opción 4: VPS Gratuito (Oracle Cloud - SIEMPRE GRATIS)

**Ventajas:**
- ✅ **Siempre gratis** (no expira)
- ✅ Control total
- ✅ 2 VMs con 1GB RAM cada una
- ✅ 200GB de almacenamiento

**Desventajas:**
- Requiere más configuración manual
- Necesitas configurar SSL manualmente (Let's Encrypt)

### Pasos básicos:

1. Crea cuenta en [Oracle Cloud](https://www.oracle.com/cloud/free/)
2. Crea una instancia "Always Free"
3. Instala Docker y Docker Compose
4. Clona tu proyecto
5. Configura dominio y SSL con Certbot

---

## 📱 Para la App Móvil

Una vez desplegado el backend, actualiza la URL en la app móvil:

**Archivo: `app-mobile/src/utils/constants.js`**

```javascript
// Cambiar de:
export const API_BASE_URL = 'http://192.168.100.25:8000/api/mobile';

// A:
export const API_BASE_URL = 'https://tu-app.onrender.com/api/mobile';
```

---

## 🔒 Configuración de Seguridad para Producción

### 1. Generar nueva SECRET_KEY

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 2. Variables de entorno importantes

```bash
SECRET_KEY=tu-nueva-secret-key-super-segura
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### 3. Configurar CORS para producción

En `settings.py`:

```python
# Solo en desarrollo
CORS_ALLOW_ALL_ORIGINS = DEBUG

# En producción, especificar dominios
CORS_ALLOWED_ORIGINS = [
    "https://tu-dominio.com",
    "https://www.tu-dominio.com",
]
```

---

## 📝 Checklist Pre-Despliegue

- [x] ✅ Archivos de configuración creados (`Procfile`, `render.yaml`)
- [x] ✅ `settings.py` actualizado para producción
- [x] ✅ Dependencias agregadas (`dj-database-url`, `whitenoise`)
- [ ] Generar nueva `SECRET_KEY` (Render lo hace automáticamente)
- [ ] Subir proyecto a GitHub
- [ ] Crear cuenta en Render.com
- [ ] Conectar repositorio y desplegar
- [ ] Ejecutar migraciones en Render
- [ ] Crear tenants en producción
- [ ] Actualizar URL de API en app móvil
- [ ] Probar la aplicación desplegada
- [ ] Crear backup de base de datos local (opcional)

---

## 🎯 Recomendación Final

**Para presentación estudiantil: Render.com**

- ✅ Completamente gratis
- ✅ Fácil de configurar
- ✅ SSL automático
- ✅ URL profesional: `tu-proyecto.onrender.com`
- ✅ Despliegue automático desde GitHub

**Si necesitas más recursos o sin límites de "sueño":**

- **Railway.app** ($5/mes después del crédito gratis)
- **DigitalOcean App Platform** ($5/mes)
- **Fly.io** (gratis con límites, luego ~$3-5/mes)

---

## 🆘 Soporte

Si tienes problemas durante el despliegue, revisa:

1. **Logs del servicio** en Render (Dashboard → Tu servicio → Logs)
2. **Variables de entorno** configuradas correctamente
3. **Migraciones ejecutadas** (`migrate_schemas`)
4. **Archivos estáticos** recopilados (se hace automáticamente en el build)
5. **Base de datos** conectada y accesible

### Problemas Comunes

**Error: "no existe la relación loginApp_usuario"**
- Asegúrate de ejecutar `migrate_schemas --shared` y luego `migrate_schemas`

**Error: "Static files not found"**
- Verifica que `collectstatic` se ejecute en el build (ya está en `render.yaml`)

**Error: "CSRF verification failed"**
- Verifica que `CSRF_TRUSTED_ORIGINS` incluya tu dominio de Render

**La app móvil no se conecta**
- Actualiza `API_BASE_URL` en `app-mobile/src/utils/constants.js`
- Verifica que CORS esté configurado correctamente

---

## 🎉 ¡Listo para Desplegar!

Tu proyecto está completamente preparado para desplegarse en Render.com de forma gratuita. Solo necesitas:

1. Subir el código a GitHub
2. Crear cuenta en Render.com
3. Conectar el repositorio
4. ¡Desplegar!

**Tiempo estimado:** 15-20 minutos

**Costo:** $0 (completamente gratis)


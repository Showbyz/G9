# Guía: Transferir Datos Locales a Render.com

Esta guía te ayudará a:
1. Conectarte a la base de datos de Render desde tu máquina local
2. Ejecutar migraciones
3. Crear el administrador global
4. Exportar e importar tus datos (tenants, usuarios, etc.)

---

## 📋 Paso 1: Obtener Credenciales de Render

⚠️ **IMPORTANTE**: Necesitas la **External Connection String**, NO la Internal Database URL.

1. Ve a [Render.com](https://render.com) y accede a tu cuenta
2. Selecciona tu base de datos (`portal-db`)
3. Click en "Info" (en la barra lateral)
4. **Busca la sección "Connections"** o "External Connection String"
5. Copia el **External Connection String** (no el Internal Database URL)

**Ejemplo de External Connection String:**
```
postgresql://portal_user:tu_password@dpg-xxxxx-a.oregon-postgres.render.com:5432/portal_xxxxx
```

**Si no encuentras el External Connection String:**
- Busca las credenciales individuales en la sección "Info":
  - `Host` (debe terminar en `.oregon-postgres.render.com` o similar)
  - `Port` (generalmente `5432`)
  - `Database Name`
  - `User`
  - `Password`
- Construye la URL manualmente:
  ```
  postgresql://USER:PASSWORD@HOST:PORT/DATABASE
  ```

**Diferencia importante:**
- ❌ **Internal Database URL**: Solo funciona desde servicios dentro de Render
- ✅ **External Connection String**: Funciona desde tu máquina local

---

## 📋 Paso 2: Configurar Variables de Entorno Localmente

### Opción A: PowerShell (Temporal - Solo para esta sesión)

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
# Cambiar al directorio del proyecto
cd C:\dev\PruebasPortal

# Activar el entorno virtual
.\env\Scripts\Activate.ps1

# Configurar variables de entorno (reemplaza con tus valores reales)
$env:DATABASE_URL="postgresql://portal_user:tu_password@dpg-xxxxx-a.oregon-postgres.render.com:5432/portal_xxxxx"
$env:SECRET_KEY="tu-secret-key-de-render"  # Obtén esto de Render → Environment
$env:DEBUG="False"
$env:ALLOWED_HOSTS="portal-autoatencion.onrender.com"
```

### Opción B: Archivo `.env.production` (Recomendado)

Crea un archivo `.env.production` en la raíz del proyecto:

```env
# Base de datos de Render
DATABASE_URL=postgresql://portal_user:tu_password@dpg-xxxxx-a.oregon-postgres.render.com:5432/portal_xxxxx

# O si prefieres configurar individualmente:
DB_NAME=portal_xxxxx
DB_USER=portal_user
DB_PASSWORD=tu_password
DB_HOST=dpg-xxxxx-a.oregon-postgres.render.com
DB_PORT=5432

# Configuración de Django
SECRET_KEY=tu-secret-key-de-render
DEBUG=False
ALLOWED_HOSTS=portal-autoatencion.onrender.com
CSRF_TRUSTED_ORIGINS=https://portal-autoatencion.onrender.com
```

**⚠️ IMPORTANTE:** Agrega `.env.production` a `.gitignore` para no subir credenciales a Git.

---

## 📋 Paso 3: Ejecutar Migraciones en Render

### Con variables de entorno temporales (PowerShell):

```powershell
# Asegúrate de estar en el entorno virtual
.\env\Scripts\Activate.ps1

# Ejecutar migraciones
python manage.py migrate_schemas --shared
python manage.py migrate_schemas
```

### Con archivo `.env.production`:

Necesitarás modificar `settings.py` para leer este archivo, o usar un script:

```powershell
# Activar entorno virtual
.\env\Scripts\Activate.ps1

# Cargar variables desde .env.production
$env:DATABASE_URL=(Get-Content .env.production | Select-String "DATABASE_URL").ToString().Split("=")[1]
$env:SECRET_KEY=(Get-Content .env.production | Select-String "SECRET_KEY").ToString().Split("=")[1]
$env:DEBUG=(Get-Content .env.production | Select-String "DEBUG").ToString().Split("=")[1]

# Ejecutar migraciones
python manage.py migrate_schemas --shared
python manage.py migrate_schemas
```

---

## 📋 Paso 4: Crear Administrador Global

```powershell
# Asegúrate de tener las variables de entorno configuradas
python manage.py create_global_admin tu-email@ejemplo.com "Tu Nombre" tu-password --superuser
```

**Ejemplo:**
```powershell
python manage.py create_global_admin admin@duoc.cl "Administrador Principal" MiPassword123! --superuser
```

---

## 📋 Paso 5: Exportar Datos de tu Base de Datos Local

### 5.1 Exportar Schema Público (Tenants, Administradores Globales)

```powershell
# Activar entorno virtual local (conectado a tu BD local)
.\env\Scripts\Activate.ps1

# Exportar datos del schema público
python manage.py dumpdata clientManager.Empresa clientManager.Dominio clientManager.AdministradorGlobal --indent 2 -o datos_publicos.json
```

### 5.2 Exportar Datos de Cada Tenant

⚠️ **IMPORTANTE**: Asegúrate de estar conectado a tu base de datos **LOCAL** (no a Render) cuando exportes datos.

**Opción A: Usando el script personalizado (RECOMENDADO):**

```powershell
# Exportar datos del tenant DUOC UC
python scripts/exportar_tenant.py "DUOC UC" datos_duoc.json

# Exportar datos del tenant INACAP (si existe)
python scripts/exportar_tenant.py "INACAP" datos_inacap.json
```

**Opción B: Usando tenant_command (puede fallar):**

```powershell
# Exportar datos del tenant DUOC UC
python manage.py tenant_command dumpdata --schema="DUOC UC" --indent 2 -o datos_duoc.json
```

**Opción C: Método alternativo con Python directamente:**

```powershell
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portalAutoatencion.settings')
django.setup()

from django.core.management import call_command
from django_tenants.utils import schema_context
from clientManager.models import Empresa

# Verificar que el tenant existe
try:
    tenant = Empresa.objects.get(schema_name='DUOC UC')
    print(f'Exportando datos del tenant: {tenant.schema_name}')
    with schema_context('DUOC UC'):
        call_command('dumpdata', 'loginApp.Usuario', 'loginApp.Asignatura', 'loginApp.Ayudantia', 'loginApp.Inscripcion', 'loginApp.Sede', indent=2, output='datos_duoc.json')
    print('Exportación completada')
except Empresa.DoesNotExist:
    print('Error: No se encontró el tenant DUOC UC')
    print('Tenants disponibles:')
    for t in Empresa.objects.all():
        print(f'  - {t.schema_name}')
"
```

**⚠️ Si obtienes el error "There are no tenants in the system":**

1. **Verifica que estés conectado a tu BD local:**
   ```powershell
   # Asegúrate de NO tener DATABASE_URL configurado (o que apunte a localhost)
   echo $env:DATABASE_URL
   # Si muestra una URL de Render, elimínala:
   Remove-Item Env:\DATABASE_URL
   ```

2. **Lista los tenants disponibles:**
   ```powershell
   python manage.py shell
   ```
   Luego en el shell:
   ```python
   from clientManager.models import Empresa
   for t in Empresa.objects.all():
       print(f"Schema: '{t.schema_name}'")
   ```

3. **Verifica el nombre exacto del schema** (puede tener espacios o mayúsculas diferentes)

---

## 📋 Paso 6: Importar Datos a Render

### 6.1 Importar Schema Público

```powershell
# Configurar variables de entorno para Render (ver Paso 2)
$env:DATABASE_URL="postgresql://portal_user:tu_password@dpg-xxxxx-a.oregon-postgres.render.com:5432/portal_xxxxx"
$env:SECRET_KEY="tu-secret-key-de-render"
$env:DEBUG="False"

# Importar datos del schema público
python manage.py loaddata datos_publicos.json
```

### 6.2 Importar Datos de Cada Tenant

```powershell
# Importar datos del tenant DUOC UC
python manage.py tenant_command loaddata --schema="DUOC UC" datos_duoc.json

# Importar datos del tenant INACAP (si existe)
python manage.py tenant_command loaddata --schema="INACAP" datos_inacap.json
```

**Nota:** Si el comando `tenant_command` no funciona, usa este método alternativo:

```powershell
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portalAutoatencion.settings')
django.setup()

from django.core.management import call_command
from django_tenants.utils import schema_context

with schema_context('DUOC UC'):
    call_command('loaddata', 'datos_duoc.json')
"
```

---

## 📋 Paso 7: Actualizar Dominios de Tenants en Render

Después de importar los datos, necesitas actualizar los dominios para que funcionen con Render:

```powershell
# Asegúrate de tener las variables de entorno de Render configuradas
python manage.py shell
```

En el shell de Django:

```python
from clientManager.models import Empresa, Dominio

# Obtener el tenant DUOC UC
duoc = Empresa.objects.get(schema_name='DUOC UC')

# Eliminar dominios localhost si existen
Dominio.objects.filter(tenant=duoc, domain__contains='localhost').delete()

# Crear dominio de producción
Dominio.objects.create(
    domain='duoc.portal-autoatencion.onrender.com',  # Reemplaza con tu dominio real
    tenant=duoc,
    is_primary=True
)

# Repetir para otros tenants
# inacap = Empresa.objects.get(schema_name='INACAP')
# Dominio.objects.filter(tenant=inacap, domain__contains='localhost').delete()
# Dominio.objects.create(
#     domain='inacap.portal-autoatencion.onrender.com',
#     tenant=inacap,
#     is_primary=True
# )
```

---

## 📋 Paso 8: Verificar que Todo Funcione

1. **Verificar administrador global:**
   - Accede a: `https://portal-autoatencion.onrender.com/global/login/`
   - Intenta iniciar sesión con las credenciales que creaste

2. **Verificar tenants:**
   - Accede a: `https://duoc.portal-autoatencion.onrender.com/`
   - Verifica que puedas iniciar sesión con usuarios del tenant

3. **Verificar API móvil:**
   - Verifica que la API responda: `https://portal-autoatencion.onrender.com/api/mobile/asignaturas/`
   - Asegúrate de enviar el header `X-Tenant-Schema: DUOC UC`

---

## 🔧 Script Automatizado (Opcional)

Puedes crear un script `scripts/transferir_a_render.ps1` para automatizar el proceso:

```powershell
# scripts/transferir_a_render.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$DatabaseUrl,
    
    [Parameter(Mandatory=$true)]
    [string]$SecretKey
)

# Activar entorno virtual
.\env\Scripts\Activate.ps1

# Configurar variables de entorno
$env:DATABASE_URL = $DatabaseUrl
$env:SECRET_KEY = $SecretKey
$env:DEBUG = "False"
$env:ALLOWED_HOSTS = "portal-autoatencion.onrender.com"

# Ejecutar migraciones
Write-Host "Ejecutando migraciones..." -ForegroundColor Yellow
python manage.py migrate_schemas --shared
python manage.py migrate_schemas

# Importar datos (si existen)
if (Test-Path "datos_publicos.json") {
    Write-Host "Importando datos públicos..." -ForegroundColor Yellow
    python manage.py loaddata datos_publicos.json
}

if (Test-Path "datos_duoc.json") {
    Write-Host "Importando datos DUOC UC..." -ForegroundColor Yellow
    python manage.py tenant_command loaddata --schema="DUOC UC" datos_duoc.json
}

Write-Host "¡Transferencia completada!" -ForegroundColor Green
```

**Uso:**
```powershell
.\scripts\transferir_a_render.ps1 -DatabaseUrl "postgresql://..." -SecretKey "tu-secret-key"
```

---

## ⚠️ Consideraciones Importantes

### Seguridad

1. **Nunca subas credenciales a Git:**
   - Agrega `.env.production` a `.gitignore`
   - No incluyas credenciales en scripts que subas a Git

2. **Protege tus archivos de exportación:**
   - Los archivos `.json` pueden contener datos sensibles
   - Elimínalos después de importarlos
   - Agrégalos a `.gitignore`

### Problemas Comunes

1. **Error de conexión:**
   - Verifica que la base de datos de Render esté activa
   - Verifica que las credenciales sean correctas
   - Verifica que tu IP esté permitida (Render permite conexiones externas por defecto)

2. **Error de migraciones:**
   - Asegúrate de ejecutar primero `migrate_schemas --shared`
   - Luego ejecuta `migrate_schemas`

3. **Error al importar datos:**
   - Verifica que los tenants existan antes de importar sus datos
   - Verifica que los modelos sean compatibles entre versiones

---

## 📚 Resumen de Comandos

```powershell
# 1. Activar entorno virtual
.\env\Scripts\Activate.ps1

# 2. Configurar variables de entorno
$env:DATABASE_URL="postgresql://..."
$env:SECRET_KEY="..."
$env:DEBUG="False"

# 3. Ejecutar migraciones
python manage.py migrate_schemas --shared
python manage.py migrate_schemas

# 4. Crear administrador global
python manage.py create_global_admin email@ejemplo.com "Nombre" password --superuser

# 5. Exportar datos locales (desde BD local)
python manage.py dumpdata clientManager.Empresa clientManager.Dominio -o datos_publicos.json

# 6. Importar datos a Render (con variables de Render configuradas)
python manage.py loaddata datos_publicos.json
```

---

**¿Necesitas ayuda con algún paso específico?** ¡Pregunta!


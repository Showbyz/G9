# Solución: Error "could not translate host name" al Conectar a Render

## 🔴 Problema

```
psycopg2.OperationalError: could not translate host name "dpg-d4gfh8ruibrs73cupb80-a" to address: Host desconocido.
```

Este error ocurre cuando intentas conectarte a la base de datos de Render usando la **Internal Database URL** desde tu máquina local.

---

## ✅ Solución

### Paso 1: Obtener la URL Externa Correcta

1. Ve a [Render.com](https://render.com)
2. Selecciona tu base de datos (`portal-db`)
3. Click en **"Info"** (barra lateral)
4. Busca la sección **"Connections"** o **"External Connection String"**
5. Copia la URL que dice **"External"** o **"External Connection String"**

**Ejemplo de URL Externa:**
```
postgresql://portal_user:password@dpg-xxxxx-a.oregon-postgres.render.com:5432/portal_xxxxx
```

**Nota:** La URL externa debe tener el dominio completo (termina en `.oregon-postgres.render.com` o similar), NO solo el hostname corto.

---

### Paso 2: Verificar la Configuración de settings.py

Verifica cómo `settings.py` está leyendo `DATABASE_URL`:

```python
# portalAutoatencion/settings.py
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(BASE_DIR, '.env'))

# Si DATABASE_URL está configurado, úsalo
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Configuración local por defecto
    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            'NAME': os.getenv('DB_NAME', 'postgres'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
```

---

### Paso 3: Configurar la Variable de Entorno Correctamente

**En PowerShell:**

```powershell
# Activar entorno virtual
.\env\Scripts\Activate.ps1

# Configurar DATABASE_URL con la URL EXTERNA (reemplaza con tus valores reales)
$env:DATABASE_URL="postgresql://portal_user:tu_password@dpg-xxxxx-a.oregon-postgres.render.com:5432/portal_xxxxx"

# Verificar que se configuró correctamente
echo $env:DATABASE_URL
```

**Verifica que la URL tenga:**
- ✅ El dominio completo (termina en `.oregon-postgres.render.com` o similar)
- ✅ El puerto (`:5432`)
- ✅ El nombre de la base de datos al final

---

### Paso 4: Probar la Conexión

```powershell
# Verificar que puedes conectarte
python manage.py migrate_schemas --shared
```

Si aún tienes problemas, prueba conectarte directamente con psql:

```powershell
# Instalar psql si no lo tienes (o usar Docker)
# O probar con Python directamente:
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://usuario:password@host:5432/database')
print('Conexión exitosa!')
conn.close()
"
```

---

## 🔍 Verificación de la URL

### URL Correcta (Externa):
```
postgresql://user:pass@dpg-xxxxx-a.oregon-postgres.render.com:5432/dbname
```
✅ Tiene el dominio completo
✅ Termina en `.render.com` o similar
✅ Tiene el puerto `:5432`

### URL Incorrecta (Interna):
```
postgresql://user:pass@dpg-xxxxx-a:5432/dbname
```
❌ Solo tiene el hostname corto
❌ No tiene el dominio completo

---

## 🛠️ Alternativa: Usar Credenciales Individuales

Si no puedes obtener la External Connection String, puedes configurar las variables individualmente:

```powershell
# En PowerShell
$env:DB_HOST="dpg-xxxxx-a.oregon-postgres.render.com"  # Con dominio completo
$env:DB_PORT="5432"
$env:DB_NAME="portal_xxxxx"
$env:DB_USER="portal_user"
$env:DB_PASSWORD="tu_password"
$env:SECRET_KEY="tu-secret-key"
$env:DEBUG="False"
```

Luego, asegúrate de que `settings.py` use estas variables cuando `DATABASE_URL` no esté configurado.

---

## 📝 Resumen

1. ✅ Obtén la **External Connection String** de Render
2. ✅ Verifica que tenga el dominio completo (termina en `.render.com`)
3. ✅ Configura `DATABASE_URL` con esa URL
4. ✅ Prueba la conexión con `python manage.py migrate_schemas --shared`

---

**¿Sigue sin funcionar?** Verifica:
- Que la base de datos de Render esté **activa** (no en pausa)
- Que tu IP no esté bloqueada (Render permite conexiones externas por defecto)
- Que las credenciales sean correctas
- Que el dominio completo esté en la URL


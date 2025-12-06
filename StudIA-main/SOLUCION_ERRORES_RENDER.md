# Solución: Errores de Acceso en Render.com

## 🔴 Problemas Reportados

1. **`https://portal-autoatencion.onrender.com/global/login/`** → "Not Found"
2. **`https://duoc.portal-autoatencion.onrender.com/`** → Error SSL (ERR_SSL_VERSION_OR_CIPHER_MISMATCH)

---

## ✅ Soluciones

### Problema 1: "Not Found" en `/global/login/`

**Causas posibles:**
1. El servicio web no está desplegado o está en pausa
2. Las rutas no están configuradas correctamente
3. El servicio está fallando al iniciar

**Soluciones:**

#### A. Verificar que el Servicio Esté Activo

1. Ve a [Render.com](https://render.com) → Tu servicio `portal-autoatencion`
2. Verifica que el estado sea **"Live"** (no "Paused" o "Failed")
3. Si está en pausa, haz click en "Manual Deploy" → "Deploy latest commit"

#### B. Verificar los Logs

1. En Render.com → Tu servicio → "Logs"
2. Busca errores al iniciar el servicio
3. Verifica que Gunicorn se haya iniciado correctamente

#### C. Verificar que las Rutas Estén Configuradas

Las rutas están correctamente configuradas en `portalAutoatencion/urls.py`:
```python
urlpatterns = [
    path('global/', include('globalAdmin.urls')),  # ✅ Correcto
    path('api/mobile/', include('api_mobile.urls')),
    path('', include('loginApp.urls')),
]
```

**Si el problema persiste:**
- Verifica que el código esté actualizado en Render (haz un nuevo deploy)
- Verifica que no haya errores en los logs de Render

---

### Problema 2: Error SSL en Subdominios

**Causa:**
Render.com puede tener problemas con SSL en subdominios si:
1. El servicio está en pausa
2. Los dominios no están correctamente configurados
3. Hay un problema con la configuración de ALLOWED_HOSTS

**Soluciones:**

#### A. Verificar ALLOWED_HOSTS

He actualizado `render.yaml` para incluir subdominios:

```yaml
- key: ALLOWED_HOSTS
  value: portal-autoatencion.onrender.com,*.onrender.com
- key: CSRF_TRUSTED_ORIGINS
  value: https://portal-autoatencion.onrender.com,https://*.onrender.com
```

**Importante:** Después de actualizar `render.yaml`, necesitas:
1. Hacer commit y push de los cambios
2. Render detectará los cambios y hará un nuevo deploy automáticamente

#### B. Verificar que el Servicio Esté Activo

El error SSL puede aparecer si el servicio está en pausa. Verifica que esté "Live".

#### C. Esperar a que Render Configure SSL

Render.com configura SSL automáticamente, pero puede tardar unos minutos después del primer deploy. Si acabas de desplegar, espera 5-10 minutos.

---

## 🔧 Pasos para Resolver

### Paso 1: Verificar Estado del Servicio

1. Ve a Render.com → Tu servicio `portal-autoatencion`
2. Verifica que el estado sea **"Live"**
3. Si está en pausa, haz click en "Manual Deploy"

### Paso 2: Actualizar render.yaml

He actualizado `render.yaml` para incluir subdominios. Ahora necesitas:

```powershell
# Hacer commit de los cambios
git add render.yaml
git commit -m "Fix: Actualizar ALLOWED_HOSTS para subdominios"
git push origin main
```

Render detectará el cambio y hará un nuevo deploy automáticamente.

### Paso 3: Verificar Logs

1. En Render.com → Tu servicio → "Logs"
2. Busca mensajes como:
   - `Starting gunicorn`
   - `Listening at: http://0.0.0.0:XXXX`
   - Errores de importación o configuración

### Paso 4: Probar Acceso

Después de que el deploy termine:

1. **Panel Global:**
   ```
   https://portal-autoatencion.onrender.com/global/login/
   ```

2. **Tenant DUOC UC:**
   ```
   https://duoc.portal-autoatencion.onrender.com/
   ```

**Nota:** Si aún ves errores SSL, espera 5-10 minutos para que Render configure SSL completamente.

---

## 🔍 Verificación de Configuración

### Verificar Variables de Entorno en Render

1. Ve a Render.com → Tu servicio → "Environment"
2. Verifica que tengas:
   - `ALLOWED_HOSTS=portal-autoatencion.onrender.com,*.onrender.com`
   - `CSRF_TRUSTED_ORIGINS=https://portal-autoatencion.onrender.com,https://*.onrender.com`
   - `DEBUG=False`

### Verificar que el Código Esté Actualizado

1. Ve a Render.com → Tu servicio → "Settings"
2. Verifica la rama y el commit desplegado
3. Si es necesario, haz "Manual Deploy" → "Deploy latest commit"

---

## ⚠️ Problemas Comunes

### El Servicio Está en Pausa

**Solución:** Render pausa servicios gratuitos después de 15 minutos de inactividad. Haz click en "Manual Deploy" para reactivarlo.

### SSL No Está Configurado

**Solución:** Espera 5-10 minutos después del primer deploy. Render configura SSL automáticamente.

### Error 404 en Todas las Rutas

**Causa:** El servicio no está iniciando correctamente.

**Solución:**
1. Verifica los logs en Render
2. Verifica que `requirements.txt` tenga todas las dependencias
3. Verifica que `render.yaml` esté correctamente configurado

---

## 📝 Checklist de Verificación

- [ ] El servicio está en estado "Live" (no pausado)
- [ ] Los logs muestran que Gunicorn se inició correctamente
- [ ] `ALLOWED_HOSTS` incluye `*.onrender.com`
- [ ] `CSRF_TRUSTED_ORIGINS` incluye `https://*.onrender.com`
- [ ] El código está actualizado en Render (último commit)
- [ ] Esperaste 5-10 minutos después del deploy para SSL

---

**¿Sigue sin funcionar?** Comparte los logs de Render para diagnosticar el problema específico.


# ✅ Solución Completa: Problema de Tenant en API Móvil

## 🔍 Problema Identificado

El error `no existe la relación «loginApp_usuario»` ocurría porque:
- La API móvil accedía por IP (`192.168.100.25:8000`)
- Django-tenants no podía identificar qué tenant usar
- Intentaba acceder a tablas que no existen en el schema público

## ✅ Solución Implementada

### 1. Middleware Personalizado (`api_mobile/middleware.py`)
- Identifica el tenant de 4 formas diferentes
- Se ejecuta ANTES de TenantMainMiddleware
- Establece el schema correcto en la conexión de BD

### 2. Cliente API Actualizado
- Envía automáticamente el header `X-Tenant-Schema`
- Usa el tenant configurado en `tenant.js`

### 3. Utilidad de Tenant (`app-mobile/src/utils/tenant.js`)
- Permite configurar el tenant por defecto
- Guarda/recupera el tenant de AsyncStorage

## 📋 Pasos para Usar

### Paso 1: Identificar el Tenant

1. Ve al admin: `http://192.168.100.25:8000/global/admin/`
2. Ve a "Empresas"
3. Copia el "Schema name" del tenant que quieres usar

### Paso 2: Configurar en la App

Edita `app-mobile/src/utils/tenant.js`:

```javascript
export const DEFAULT_TENANT = 'duoc'; // Cambiar por tu tenant
```

### Paso 3: Reiniciar Todo

1. **Reinicia Django:**
   ```bash
   # Detén (Ctrl+C) y luego:
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Reinicia la app móvil:**
   ```bash
   # Detén (Ctrl+C) y luego:
   npm start
   ```

### Paso 4: Probar

Intenta hacer login desde la app móvil. Debería funcionar ahora.

## 🔍 Cómo Funciona el Middleware

El middleware intenta identificar el tenant en este orden:

1. **Header HTTP:** `X-Tenant-Schema: duoc`
2. **Query Parameter:** `?tenant=duoc` o `?schema=duoc`
3. **Dominio:** Busca el tenant por el hostname
4. **Automático:** Usa el primer tenant activo encontrado

## 🐛 Debug

Si aún no funciona:

1. **Revisa los logs de Django:**
   - Deberías ver: `[API Mobile] Tenant establecido: duoc (Duoc UC)`
   - Si ves: `[API Mobile] WARNING: No se pudo identificar ningún tenant`, no hay tenants

2. **Verifica que hay tenants:**
   ```bash
   python manage.py shell
   ```
   ```python
   from clientManager.models import Empresa
   from django_tenants.utils import schema_context
   with schema_context('public'):
       for t in Empresa.objects.all():
           print(f"{t.nombre_empresa}: {t.schema_name}")
   ```

3. **Verifica el tenant en la app:**
   - Revisa `app-mobile/src/utils/tenant.js`
   - El schema name debe coincidir exactamente

## 📝 Archivos Modificados

- ✅ `api_mobile/middleware.py` - Nuevo middleware
- ✅ `portalAutoatencion/settings.py` - Agregado middleware
- ✅ `app-mobile/src/api/client.js` - Envía header de tenant
- ✅ `app-mobile/src/utils/tenant.js` - Nueva utilidad

## ⚠️ Importante

- **DEBES reiniciar Django** después de agregar el middleware
- El tenant debe existir en la base de datos
- El schema name es case-sensitive

---

**¡Configura el tenant y reinicia todo! El login debería funcionar ahora.** 🚀


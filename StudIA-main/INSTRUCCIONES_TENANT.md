# 📋 Instrucciones: Configurar Tenant para API Móvil

## 🎯 Problema Resuelto

El error `no existe la relación «loginApp_usuario»` se debía a que la API no sabía qué tenant usar.

## ✅ Solución Implementada

Se creó un middleware que identifica el tenant automáticamente. Si no se especifica, usa el primer tenant activo.

## 🔧 Configurar el Tenant en la App

### Paso 1: Identificar el Schema del Tenant

1. Ve al admin global: `http://192.168.100.25:8000/global/admin/`
2. Ve a "Empresas"
3. Busca el tenant que quieres usar (ej: Duoc, DSA, Inacap)
4. Copia el valor de **"Schema name"** (ej: `duoc`, `dsa`, `inacap`)

### Paso 2: Configurar en la App Móvil

Edita el archivo `app-mobile/src/utils/tenant.js`:

```javascript
export const DEFAULT_TENANT = 'duoc'; // Cambiar por tu tenant
```

**Ejemplos:**
- Si tu tenant es "Duoc": `'duoc'`
- Si tu tenant es "DSA": `'dsa'`
- Si tu tenant es "Inacap": `'inacap'`

### Paso 3: Reiniciar la App

1. Detén la app (Ctrl+C en la terminal de npm start)
2. Reinicia: `npm start`
3. Prueba el login de nuevo

## 🔄 Reiniciar Django

**IMPORTANTE:** Después de los cambios, reinicia Django:

1. Detén Django (Ctrl+C)
2. Inicia de nuevo:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## 🧪 Verificar que Funciona

1. **Verifica que hay tenants:**
   ```bash
   python manage.py shell
   ```
   ```python
   from clientManager.models import Empresa
   from django_tenants.utils import schema_context
   with schema_context('public'):
       for t in Empresa.objects.all():
           print(f"{t.nombre_empresa}: {t.schema_name} (estado: {t.estado})")
   ```

2. **Prueba el login** desde la app móvil

3. **Revisa los logs de Django:**
   - Deberías ver `POST /api/mobile/auth/login/ HTTP/1.1 200` si funciona
   - No deberías ver el error de "no existe la relación"

## 📝 Notas

- El middleware usa el **primer tenant activo** si no especificas uno
- Puedes cambiar el tenant en `tenant.js` según necesites
- El tenant se envía automáticamente en todas las peticiones

## ⚠️ Si Aún No Funciona

1. **Verifica el schema name:**
   - Debe coincidir exactamente con el que está en la BD
   - Es case-sensitive (mayúsculas/minúsculas importan)

2. **Verifica que el tenant esté activo:**
   - El campo `estado` debe ser `'A'` (o el middleware usará cualquier tenant)

3. **Revisa los logs:**
   - Busca errores en la terminal de Django
   - Verifica que el middleware se ejecuta

---

**Configura el tenant en `tenant.js` y reinicia tanto Django como la app móvil.**


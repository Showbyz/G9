# 🔧 Solución: Problema de Tenant en API Móvil

## ❌ Problema Identificado

El error `no existe la relación «loginApp_usuario»` ocurre porque:
- La API móvil intenta acceder a la base de datos
- Pero no está identificando qué **tenant** usar
- Django-tenants necesita saber el tenant para acceder a las tablas correctas

## ✅ Solución Implementada

Se creó un **middleware personalizado** que identifica el tenant de 3 formas:

### 1. Header HTTP (Recomendado)
Enviar el header `X-Tenant-Schema` con el nombre del schema del tenant.

### 2. Query Parameter
Agregar `?tenant=nombre_schema` o `?schema=nombre_schema` a la URL.

### 3. Automático (Desarrollo)
Si no se especifica, usa el **primer tenant activo** encontrado.

## 🔄 Cambios Realizados

1. ✅ Creado `api_mobile/middleware.py` - Middleware para identificar tenant
2. ✅ Agregado al `MIDDLEWARE` en `settings.py`
3. ✅ Actualizado cliente API para enviar header de tenant

## 📋 Cómo Usar

### Opción 1: Configurar Tenant en la App (Recomendado)

1. **Obtener el schema del tenant:**
   - Ve al admin de Django: `/global/admin/`
   - Ve a "Empresas"
   - Busca el tenant que quieres usar
   - Copia el valor de "Schema name" (ej: `duoc`, `dsa`, `inacap`)

2. **Configurar en la app móvil:**
   - Edita `app-mobile/src/utils/constants.js`
   - Agrega una constante con el tenant:
   ```javascript
   export const TENANT_SCHEMA = 'duoc'; // Cambiar por tu tenant
   ```

3. **Actualizar el cliente API:**
   - El cliente ya está configurado para enviar el tenant automáticamente
   - Solo necesitas guardar el tenant en AsyncStorage al iniciar la app

### Opción 2: Usar Query Parameter

Agregar el tenant a la URL base:
```javascript
export const API_BASE_URL = 'http://192.168.100.25:8000/api/mobile?tenant=duoc';
```

### Opción 3: Usar Header Manualmente

En cada petición, agregar el header:
```javascript
headers: {
  'X-Tenant-Schema': 'duoc'
}
```

## 🧪 Probar

1. **Reiniciar el servidor Django** (muy importante)
2. **Verificar que hay al menos un tenant activo:**
   ```bash
   python manage.py shell
   ```
   ```python
   from clientManager.models import Empresa
   from django_tenants.utils import schema_context
   with schema_context('public'):
       tenants = Empresa.objects.filter(estado='A')
       for t in tenants:
           print(f"{t.nombre_empresa}: {t.schema_name}")
   ```

3. **Probar el login** desde la app móvil

## ⚠️ Importante

- **Debes reiniciar Django** después de agregar el middleware
- El tenant debe existir y estar activo (`estado='A'`)
- Si no especificas tenant, usará el primero que encuentre (solo desarrollo)

## 🔍 Debug

Si sigue sin funcionar:

1. **Verificar que el middleware se ejecuta:**
   - Agrega un `print()` en el middleware
   - Deberías ver logs cuando haces peticiones a `/api/mobile/`

2. **Verificar el tenant:**
   - Revisa en el admin que el tenant existe
   - Verifica que `estado='A'`

3. **Verificar logs de Django:**
   - Busca errores relacionados con el schema
   - Verifica que el middleware se ejecuta antes de las vistas

---

**Reinicia Django y prueba de nuevo. El middleware debería identificar el tenant automáticamente.**


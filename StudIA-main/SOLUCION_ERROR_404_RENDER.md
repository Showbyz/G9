# Solución: Error 404 en Render.com

## 🔴 Problema

Los logs muestran que todas las peticiones a la URL raíz (`/`) devuelven **404**:
```
127.0.0.1 - - [21/Nov/2025:21:24:18 -0300] "GET / HTTP/1.1" 404 0
```

**Causa:** El middleware `TenantMainMiddleware` de django-tenants no puede identificar un tenant cuando se accede a la URL raíz sin subdominio (como `https://studia-8dmp.onrender.com/`). Como las rutas de `loginApp` están configuradas como `TENANT_APPS`, solo funcionan cuando hay un tenant identificado.

---

## ✅ Solución Implementada

He configurado `PUBLIC_SCHEMA_URLCONF` para que django-tenants use URLs públicas cuando no se identifica un tenant:

1. **Creado `globalAdmin/views_public.py`**: Vistas públicas para cuando no hay tenant
2. **Creado `globalAdmin/urls_public.py`**: URLs públicas que redirigen al panel global
3. **Actualizado `portalAutoatencion/settings.py`**: Configurado `PUBLIC_SCHEMA_URLCONF = 'globalAdmin.urls_public'`

### Cambios Realizados

#### 1. `portalAutoatencion/settings.py`
```python
# Antes:
PUBLIC_SCHEMA_URLCONF = None  # Usaremos middleware personalizado

# Después:
PUBLIC_SCHEMA_URLCONF = 'globalAdmin.urls_public'
```

#### 2. `globalAdmin/views_public.py` (NUEVO)
- `public_index()`: Redirige a `/global/login/` cuando se accede a la raíz
- `public_welcome()`: Vista de bienvenida pública (opcional)

#### 3. `globalAdmin/urls_public.py` (NUEVO)
- Define las URLs públicas que se usan cuando no hay tenant
- Incluye las rutas de `globalAdmin` y `api_mobile`

---

## 🔧 Próximos Pasos

### Paso 1: Hacer Commit y Push

```powershell
git add .
git commit -m "Fix: Configurar PUBLIC_SCHEMA_URLCONF para manejar URLs sin tenant"
git push origin main
```

Render detectará el cambio y hará un nuevo deploy automáticamente.

### Paso 2: Verificar el Deploy

1. Espera a que Render termine el deploy (2-5 minutos)
2. Accede a: `https://studia-8dmp.onrender.com/`
3. Deberías ser redirigido automáticamente a: `https://studia-8dmp.onrender.com/global/login/`

### Paso 3: Verificar Subdominios

Para acceder a un tenant específico, necesitas usar el subdominio configurado:
- `https://duoc.studia-8dmp.onrender.com/` (si está configurado)
- `https://inacap.studia-8dmp.onrender.com/` (si está configurado)

**Nota:** Los subdominios deben estar configurados en Render y en la base de datos (tabla `clientManager_dominio`).

---

## 🔍 Verificación

### Verificar que Funciona

1. **URL Raíz:**
   ```
   https://studia-8dmp.onrender.com/
   ```
   Debería redirigir a `/global/login/`

2. **Panel Global:**
   ```
   https://studia-8dmp.onrender.com/global/login/
   ```
   Debería mostrar el formulario de login del panel global

3. **API Móvil:**
   ```
   https://studia-8dmp.onrender.com/api/mobile/asignaturas/
   ```
   Debería funcionar (requiere header `X-Tenant-Schema`)

---

## ⚠️ Nota sobre Subdominios

**Importante:** Para que los subdominios funcionen (como `duoc.studia-8dmp.onrender.com`), necesitas:

1. **Configurar dominios en Render:**
   - Render.com → Tu servicio → "Settings" → "Custom Domains"
   - Agregar el subdominio (si Render lo permite)

2. **Configurar dominios en la base de datos:**
   - Los dominios deben estar en la tabla `clientManager_dominio`
   - El dominio debe coincidir con el hostname de la petición

3. **Alternativa:** Si Render no permite subdominios personalizados, puedes usar:
   - Query parameters: `?tenant=DUOC%20UC`
   - Headers: `X-Tenant-Schema: DUOC UC`
   - Path-based routing: `/duoc/` (requiere configuración adicional)

---

## 📝 Resumen

- ✅ Configurado `PUBLIC_SCHEMA_URLCONF` para manejar URLs sin tenant
- ✅ Creadas vistas públicas que redirigen al panel global
- ✅ Las URLs `/global/` y `/api/mobile/` funcionan desde el schema público
- ⏳ Pendiente: Hacer commit y push para aplicar los cambios

**Después del deploy, la URL raíz debería redirigir automáticamente al panel de administración global.**


# Tenants en Producción con Render.com

## 🎯 Tu Pregunta

**En local**: `inacap.localhost:8000` o `duoc.localhost:8000`  
**En producción**: ¿Cómo funcionará con Render.com?

---

## ✅ Respuesta: SÍ Funcionará, pero con Algunas Consideraciones

### Opción 1: Subdominios de Render.com (RECOMENDADO - GRATIS)

Render.com **SÍ soporta subdominios** en su plan gratuito. Puedes usar:

```
duoc.tu-app.onrender.com
inacap.tu-app.onrender.com
dsa.tu-app.onrender.com
```

**Cómo funciona:**
1. Render redirige automáticamente todos los subdominios a tu aplicación
2. Django-tenants detecta el subdominio y carga el tenant correspondiente
3. **NO necesitas configuración adicional en Render** (solo en tu base de datos)

---

## 🔧 Configuración Necesaria

### Paso 1: Actualizar Dominios en la Base de Datos

Cuando despliegues, necesitarás actualizar los dominios de tus tenants en la base de datos de producción.

**Opción A: Desde el Shell de Render (RECOMENDADO)**

1. Ve a tu servicio en Render.com
2. Click en "Shell" (en la barra lateral)
3. Ejecuta:

```python
python manage.py shell
```

4. En el shell de Python:

```python
from clientManager.models import Empresa, Dominio

# Obtener el tenant de DUOC
duoc = Empresa.objects.get(schema_name='DUOC UC')

# Eliminar el dominio antiguo (localhost)
Dominio.objects.filter(tenant=duoc, domain='duoc.localhost').delete()

# Crear el nuevo dominio para producción
Dominio.objects.create(
    domain='duoc.tu-app.onrender.com',
    tenant=duoc,
    is_primary=True
)

# Repetir para otros tenants
inacap = Empresa.objects.get(schema_name='INACAP')
Dominio.objects.filter(tenant=inacap, domain='inacap.localhost').delete()
Dominio.objects.create(
    domain='inacap.tu-app.onrender.com',
    tenant=inacap,
    is_primary=True
)
```

**Opción B: Script de Migración Automática**

Puedo crear un script que haga esto automáticamente. ¿Quieres que lo cree?

---

### Paso 2: Configurar ALLOWED_HOSTS y CSRF_TRUSTED_ORIGINS

En Render.com, configura estas variables de entorno:

```env
ALLOWED_HOSTS=tu-app.onrender.com,*.onrender.com
CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com,https://*.onrender.com
```

**Nota**: El `*` en `*.onrender.com` permite todos los subdominios automáticamente.

---

## 📋 Comparación: Local vs Producción

| Aspecto | Local (Desarrollo) | Producción (Render.com) |
|---------|-------------------|------------------------|
| **URL Base** | `localhost:8000` | `tu-app.onrender.com` |
| **DUOC** | `duoc.localhost:8000` | `duoc.tu-app.onrender.com` |
| **INACAP** | `inacap.localhost:8000` | `inacap.tu-app.onrender.com` |
| **DSA** | `dsa.localhost:8000` | `dsa.tu-app.onrender.com` |
| **HTTPS** | ❌ No (HTTP) | ✅ Sí (automático) |
| **Configuración DNS** | Archivo `hosts` | Automático (Render) |

---

## 🌐 Opción 2: Dominios Personalizados (Si Tienes)

Si tienes dominios propios (ej: `duoc.cl`, `inacap.cl`), puedes configurarlos:

1. **En Render.com:**
   - Ve a tu servicio
   - Click en "Settings" → "Custom Domains"
   - Agrega: `duoc.tu-dominio.com`, `inacap.tu-dominio.com`
   - Render te dará instrucciones de DNS

2. **En tu Base de Datos:**
   ```python
   Dominio.objects.create(
       domain='duoc.tu-dominio.com',
       tenant=duoc,
       is_primary=True
   )
   ```

**Ventajas:**
- ✅ URLs más profesionales
- ✅ Mejor branding

**Desventajas:**
- ⚠️ Requiere configuración DNS
- ⚠️ Puede tener costo adicional

---

## 🔄 Flujo de Trabajo Recomendado

### Al Desplegar por Primera Vez:

```
1. Desplegar en Render.com
   ↓
2. Ejecutar migraciones
   python manage.py migrate_schemas --shared
   python manage.py migrate_schemas
   ↓
3. Crear/Importar tenants (si no existen)
   ↓
4. Actualizar dominios en la base de datos
   (Cambiar de localhost a onrender.com)
   ↓
5. Probar cada tenant:
   - duoc.tu-app.onrender.com
   - inacap.tu-app.onrender.com
```

### Para Nuevos Tenants:

```
1. Crear tenant localmente
   python manage.py create_tenant
   ↓
2. Probar localmente
   nuevo-tenant.localhost:8000
   ↓
3. Hacer push a GitHub
   git push origin main
   ↓
4. En Render (Shell), actualizar dominio:
   Dominio.objects.create(
       domain='nuevo-tenant.tu-app.onrender.com',
       tenant=nuevo_tenant,
       is_primary=True
   )
```

---

## ⚠️ Consideraciones Importantes

### 1. **Base de Datos Separada**

Los dominios en producción son **diferentes** a los de local:

- **Local**: `duoc.localhost` → Base de datos local
- **Producción**: `duoc.tu-app.onrender.com` → Base de datos de Render

**Solución**: Actualizar dominios en producción después del despliegue.

### 2. **HTTPS Automático**

Render.com proporciona HTTPS automático. Tus URLs serán:
- ✅ `https://duoc.tu-app.onrender.com` (HTTPS)
- ❌ `http://duoc.tu-app.onrender.com` (redirige a HTTPS)

### 3. **Plan Gratuito de Render**

- ✅ Subdominios ilimitados
- ✅ HTTPS automático
- ⚠️ El servicio se "duerme" después de 15 min de inactividad
- ⚠️ Se despierta en ~30 segundos cuando alguien accede

---

## 🛠️ Script de Migración Automática

Puedo crear un script que:
1. Detecte automáticamente el dominio de Render
2. Actualice todos los dominios de `localhost` a `onrender.com`
3. Se ejecute automáticamente al desplegar

¿Quieres que lo cree?

---

## 📝 Resumen

**¿Tendrás problemas con los tenants?**
✅ **NO**, funcionará perfectamente.

**¿Cómo será diferente?**
- Local: `duoc.localhost:8000`
- Producción: `duoc.tu-app.onrender.com` (con HTTPS)

**¿Qué necesitas hacer?**
1. Actualizar dominios en la base de datos de producción
2. Configurar `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` en Render
3. ¡Listo! Los tenants funcionarán igual que en local.

---

## 🚀 Próximos Pasos

1. **Despliega** siguiendo `GUIA_DESPLIEGUE.md`
2. **Actualiza dominios** usando el shell de Render
3. **Prueba** cada tenant en producción
4. **¡Disfruta!** Tu aplicación multi-tenant estará online

---

**¿Tienes más preguntas sobre tenants en producción? ¡Pregunta!**


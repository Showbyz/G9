# Panel de Administración Global en Producción

## ✅ Respuesta Directa

**El panel de administración global se despliega automáticamente** con tu aplicación. Solo necesitas:

1. ✅ Crear el primer administrador global (una vez)
2. ✅ Acceder a través de la URL correcta
3. ✅ Configurar CSRF_TRUSTED_ORIGINS (ya está en la guía)

---

## 🌐 Cómo Acceder al Panel en Producción

### En Local (Desarrollo):
```
http://public-admin-panel.localhost:8000/global/
```

### En Producción (Render.com):
```
https://tu-app.onrender.com/global/
```

**Nota**: El panel funciona en el dominio principal (no necesita subdominio especial).

---

## 🔧 Pasos para Configurar en Producción

### Paso 1: Crear el Primer Administrador Global

Después de desplegar en Render.com, necesitas crear el primer administrador global:

1. **Ve al Shell de Render:**
   - En tu servicio de Render.com
   - Click en "Shell" (barra lateral)

2. **Ejecuta el comando:**
```bash
python manage.py create_global_admin tu-email@ejemplo.com "Tu Nombre Completo" tu-password-segura --superuser
```

**Ejemplo:**
```bash
python manage.py create_global_admin admin@portal.com "Administrador Principal" MiPassword123! --superuser
```

3. **Verifica que se creó:**
```bash
python manage.py shell
```

```python
from django_tenants.utils import schema_context, get_public_schema_name
from clientManager.models import AdministradorGlobal

with schema_context(get_public_schema_name()):
    admins = AdministradorGlobal.objects.all()
    for admin in admins:
        print(f"Email: {admin.email}, Nombre: {admin.nombre}, Staff: {admin.is_staff}")
```

---

### Paso 2: Acceder al Panel

1. **Abre tu navegador:**
   ```
   https://tu-app.onrender.com/global/login/
   ```

2. **Inicia sesión con:**
   - Email: El que usaste en el comando
   - Password: La contraseña que configuraste

3. **¡Listo!** Ya puedes:
   - ✅ Ver todos los tenants
   - ✅ Crear nuevos tenants
   - ✅ Editar tenants existentes
   - ✅ Crear usuarios administradores para cada tenant
   - ✅ Ejecutar migraciones para tenants
   - ✅ Impersonar tenants

---

## ⚙️ Configuración Adicional (Ya Incluida)

### Variables de Entorno en Render

Asegúrate de tener estas variables configuradas:

```env
CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com,https://*.onrender.com
ALLOWED_HOSTS=tu-app.onrender.com,*.onrender.com
```

**Nota**: Ya está incluido en `GUIA_DESPLIEGUE.md` con el formato correcto.

---

## 📋 Funcionalidades del Panel Global

### 1. **Dashboard** (`/global/dashboard/`)
- Vista general de todos los tenants
- Estadísticas (total, activos, inactivos)

### 2. **Gestión de Tenants** (`/global/tenants/`)
- Listar todos los tenants
- Crear nuevos tenants
- Editar tenants existentes
- Suspender/Activar tenants

### 3. **Crear Usuarios Administradores** (`/global/tenants/<id>/create-admin-user/`)
- Crear usuarios administradores para cada tenant
- Útil para dar acceso a administradores de cada institución

### 4. **Ejecutar Migraciones** (`/global/tenants/<id>/run-migrations/`)
- Ejecutar migraciones para un tenant específico
- Útil cuando agregas nuevas funcionalidades

### 5. **Impersonar Tenants** (`/global/tenants/<id>/impersonate/`)
- Entrar como si fueras un usuario del tenant
- Útil para debugging y soporte

---

## 🔐 Seguridad

### El Panel Global es Seguro Porque:

1. ✅ **Requiere autenticación**: Solo administradores globales pueden acceder
2. ✅ **Schema público**: Opera en el schema público, separado de los tenants
3. ✅ **Middleware de protección**: `global_admin_required` verifica permisos
4. ✅ **CSRF protegido**: Todas las acciones están protegidas contra CSRF

### Recomendaciones:

- 🔒 Usa contraseñas seguras para administradores globales
- 🔒 Limita el acceso solo a personas de confianza
- 🔒 Considera usar HTTPS (ya está incluido en Render)
- 🔒 No compartas las credenciales del administrador global

---

## 🚀 Flujo de Trabajo en Producción

### Escenario 1: Primera Vez (Setup Inicial)

```
1. Desplegar aplicación en Render.com
   ↓
2. Ejecutar migraciones
   python manage.py migrate_schemas --shared
   python manage.py migrate_schemas
   ↓
3. Crear primer administrador global
   python manage.py create_global_admin admin@ejemplo.com "Admin" password123 --superuser
   ↓
4. Acceder al panel
   https://tu-app.onrender.com/global/login/
   ↓
5. Crear tenants desde el panel
   (O importar desde local si ya existen)
```

### Escenario 2: Crear Nuevo Tenant

```
1. Acceder al panel global
   https://tu-app.onrender.com/global/login/
   ↓
2. Ir a "Crear Tenant"
   /global/tenants/create/
   ↓
3. Llenar formulario:
   - Nombre de empresa: "Nueva Institución"
   - Dominio: "nueva-institucion.tu-app.onrender.com"
   - Tema: "default"
   ↓
4. El sistema automáticamente:
   - Crea el schema en la base de datos
   - Ejecuta las migraciones
   - Crea el dominio
   ↓
5. Crear usuario administrador para el tenant
   /global/tenants/<id>/create-admin-user/
```

### Escenario 3: Gestionar Usuarios de un Tenant

```
1. Acceder al panel global
   ↓
2. Seleccionar tenant
   /global/tenants/
   ↓
3. Click en "Crear Usuario Admin"
   /global/tenants/<id>/create-admin-user/
   ↓
4. Llenar formulario y crear
   ↓
5. El usuario puede acceder al tenant normalmente
   https://tenant.tu-app.onrender.com/
```

---

## 📝 Comparación: Local vs Producción

| Aspecto | Local | Producción |
|---------|-------|------------|
| **URL** | `http://public-admin-panel.localhost:8000/global/` | `https://tu-app.onrender.com/global/` |
| **HTTPS** | ❌ No | ✅ Sí (automático) |
| **Acceso** | Mismo que local | Mismo que producción |
| **Funcionalidades** | ✅ Todas | ✅ Todas |
| **Crear Admin** | `create_global_admin` | `create_global_admin` (en Shell) |

---

## ⚠️ Consideraciones Importantes

### 1. **Primer Administrador Global**

- **DEBE** crearse manualmente usando el comando `create_global_admin`
- No se crea automáticamente
- Es el único paso manual necesario

### 2. **Dominios de Tenants**

Cuando creas un tenant desde el panel en producción:
- Usa el formato: `nombre-tenant.tu-app.onrender.com`
- El sistema crea automáticamente el dominio en la base de datos
- Render redirige automáticamente el subdominio a tu app

### 3. **Migraciones**

- Las migraciones se ejecutan automáticamente al crear un tenant
- Puedes ejecutarlas manualmente desde el panel si es necesario
- Usa `/global/tenants/<id>/run-migrations/` para ejecutar migraciones específicas

---

## 🎯 Resumen

**¿Se despliega automáticamente?**
✅ **SÍ**, el panel se despliega automáticamente con tu aplicación.

**¿Necesitas hacer algo adicional?**
✅ **SÍ**, solo crear el primer administrador global (una vez).

**¿Cómo acceder?**
```
https://tu-app.onrender.com/global/login/
```

**¿Funciona igual que en local?**
✅ **SÍ**, exactamente igual, solo cambia la URL.

---

## 📚 Documentación Relacionada

- `GUIA_DESPLIEGUE.md` - Guía completa de despliegue
- `TENANTS_EN_PRODUCCION.md` - Configuración de tenants en producción
- `FLUJO_TRABAJO_DESPLIEGUE.md` - Flujo de trabajo local vs producción

---

**¿Tienes más preguntas sobre el panel de administración? ¡Pregunta!**


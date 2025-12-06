# 📋 Procedimiento Completo: Login en App Móvil con DUOC UC

## 🔍 Paso 1: Verificar Tenant y Usuarios

### 1.1 Verificar que el Tenant Existe

```bash
python manage.py shell
```

```python
from clientManager.models import Empresa
from django_tenants.utils import schema_context

with schema_context('public'):
    tenant = Empresa.objects.get(schema_name='DUOC UC')
    print(f"Tenant: {tenant.nombre_empresa}")
    print(f"Schema: {tenant.schema_name}")
    print(f"Estado: {tenant.estado}")
```

### 1.2 Verificar Usuarios en el Schema

```python
from loginApp.models import Usuario
from django_tenants.utils import schema_context

with schema_context('DUOC UC'):
    usuarios = Usuario.objects.all()
    print(f"Total usuarios: {usuarios.count()}")
    
    estudiantes = [u for u in usuarios if not (u.is_staff or u.is_tutor) and u.is_active]
    print(f"Estudiantes activos: {len(estudiantes)}")
    
    for e in estudiantes:
        print(f"  - {e.email}")
```

## 🔧 Paso 2: Configurar la App Móvil

### 2.1 Configurar Tenant

Edita `app-mobile/src/utils/tenant.js`:

```javascript
export const DEFAULT_TENANT = 'DUOC UC';
```

### 2.2 Verificar URL de API

Edita `app-mobile/src/utils/constants.js`:

```javascript
export const API_BASE_URL = 'http://192.168.100.25:8000/api/mobile';
```

## 🚀 Paso 3: Iniciar Servidores

### 3.1 Iniciar Django

```bash
python manage.py runserver 0.0.0.0:8000
```

### 3.2 Iniciar App Móvil

```bash
cd app-mobile
npm start
```

## 🧪 Paso 4: Probar Login

### 4.1 Abrir la App

- Presiona `w` para abrir en navegador
- O escanea el QR con Expo Go en tu teléfono

### 4.2 Intentar Login

1. Ingresa el **email** de un estudiante del tenant DUOC UC
2. Ingresa la **contraseña**
3. Presiona "Iniciar Sesión"

### 4.3 Verificar Logs

En Django deberías ver:
```
[API Mobile] Petición recibida: POST /api/mobile/auth/login/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[API Mobile] Schema actual de BD: DUOC UC
```

## ⚠️ Problemas Comunes

### Problema 1: "No se pudo identificar ningún tenant"

**Solución:** Verifica que el tenant 'DUOC UC' exista y esté activo.

### Problema 2: "no existe la relación «loginApp_usuario»"

**Solución:** El schema no está establecido. Verifica los logs del middleware.

### Problema 3: "Email o contraseña incorrectos"

**Solución:** 
- Verifica que el usuario exista en el schema 'DUOC UC'
- Verifica que sea estudiante (no staff ni tutor)
- Verifica que esté activo

### Problema 4: Solo se ven peticiones OPTIONS

**Solución:** 
- Revisa la consola de la app móvil para ver errores
- Verifica que el botón de login esté funcionando
- Revisa la consola de Expo para errores de JavaScript

## 📝 Checklist

- [ ] Tenant 'DUOC UC' existe y está activo
- [ ] Hay usuarios de tipo estudiante en el schema 'DUOC UC'
- [ ] Las migraciones están aplicadas en el schema 'DUOC UC'
- [ ] La app móvil tiene configurado `DEFAULT_TENANT = 'DUOC UC'`
- [ ] La URL de API es correcta (192.168.100.25:8000)
- [ ] Django está corriendo en 0.0.0.0:8000
- [ ] La app móvil está corriendo
- [ ] Los logs del middleware aparecen en Django

---

**Sigue estos pasos en orden y verifica cada uno antes de continuar.**


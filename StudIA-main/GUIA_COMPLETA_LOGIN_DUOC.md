# 📱 Guía Completa: Login en App Móvil con DUOC UC

## ✅ Verificación Completada

**Tenant DUOC UC:**
- ✅ Existe y está activo
- ✅ Schema: `DUOC UC`
- ✅ Estado: `A`

**Estudiantes Disponibles:**
1. `estudiante@duoc.cl`
2. `Garrosh@duocuc.cl`
3. `fei.silva@duocuc.cl`

## 🔧 Configuración Actual

### 1. App Móvil
- ✅ Tenant configurado: `DUOC UC` en `app-mobile/src/utils/tenant.js`
- ✅ URL de API: `http://192.168.100.25:8000/api/mobile`

### 2. Django
- ✅ Middleware configurado
- ✅ CORS configurado
- ✅ API endpoints listos

## 🚀 Procedimiento Paso a Paso

### Paso 1: Verificar que Django Esté Corriendo

```bash
# Debe estar corriendo en:
python manage.py runserver 0.0.0.0:8000
```

**Verifica que veas:**
```
Starting development server at http://0.0.0.0:8000/
```

### Paso 2: Verificar que la App Móvil Esté Corriendo

```bash
cd app-mobile
npm start
```

**Deberías ver:**
```
› Press ? │ show all commands
```

### Paso 3: Abrir la App

**Opción A: Navegador (Más Rápido)**
- Presiona `w` en la terminal de npm start
- Se abrirá en el navegador

**Opción B: Teléfono**
- Instala Expo Go
- Escanea el código QR

### Paso 4: Hacer Login

**Usa uno de estos estudiantes:**

1. **Email:** `estudiante@duoc.cl`
   - Contraseña: (la que configuraste)

2. **Email:** `Garrosh@duocuc.cl`
   - Contraseña: (la que configuraste)

3. **Email:** `fei.silva@duocuc.cl`
   - Contraseña: (la que configuraste)

### Paso 5: Verificar Logs en Django

Cuando intentes hacer login, deberías ver en Django:

```
[API Mobile] Petición recibida: OPTIONS /api/mobile/auth/login/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Usando tenant por defecto: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[API Mobile] Schema actual de BD: DUOC UC
[API Mobile] Petición recibida: POST /api/mobile/auth/login/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[API Mobile] Schema actual de BD: DUOC UC
[API Mobile Serializer] Schema establecido: DUOC UC
[API Mobile Serializer] Usuario encontrado: [email]
```

## ⚠️ Si No Funciona

### Problema 1: No Veo los Logs `[API Mobile]`

**Solución:** El middleware no se está ejecutando. Verifica:
- Que el middleware esté en `settings.py`
- Que Django se haya reiniciado completamente

### Problema 2: Solo Veo OPTIONS, No POST

**Solución:** 
- Revisa la consola de la app móvil (presiona `m` en npm start)
- Busca errores en rojo
- Verifica que el botón de login esté funcionando

### Problema 3: "Email o contraseña incorrectos"

**Solución:**
- Verifica que estés usando uno de los 3 emails de estudiantes
- Verifica la contraseña (puede que necesites resetearla)

### Problema 4: "no existe la relación «loginApp_usuario»"

**Solución:** El schema no se está estableciendo. Verifica los logs:
- Debe aparecer: `[API Mobile] Schema actual de BD: DUOC UC`
- Si no aparece, el middleware no está funcionando

## 🔑 Recordar Contraseñas

Si no recuerdas las contraseñas, puedes:

1. **Resetear desde Django Admin:**
   - Ve a: `http://192.168.100.25:8000/global/admin/`
   - Busca el usuario en el tenant DUOC UC
   - Cambia la contraseña

2. **O crear un nuevo estudiante:**
   ```python
   python manage.py shell
   ```
   ```python
   from loginApp.models import Usuario
   from django_tenants.utils import schema_context
   
   with schema_context('DUOC UC'):
       user = Usuario.objects.create_user(
           email='nuevo@duoc.cl',
           nombre_usuario='Nuevo Estudiante',
           password='password123'
       )
       print(f"Usuario creado: {user.email}")
   ```

## 📋 Checklist Final

- [ ] Django corriendo en `0.0.0.0:8000`
- [ ] App móvil corriendo (`npm start`)
- [ ] App abierta (navegador o teléfono)
- [ ] Email de estudiante listo (uno de los 3)
- [ ] Contraseña conocida
- [ ] Logs del middleware aparecen en Django

---

**¡Sigue estos pasos y deberías poder hacer login!**


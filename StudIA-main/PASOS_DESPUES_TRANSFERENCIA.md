# Pasos Después de Transferir Datos a Render

Has completado la transferencia de datos. Ahora sigue estos pasos para finalizar el despliegue:

---

## ✅ Paso 8: Verificar que Todo Funcione

### 8.1 Verificar Administrador Global

1. Accede al panel de administración global:
   ```
   https://portal-autoatencion.onrender.com/global/login/
   ```

2. Inicia sesión con las credenciales que creaste en el Paso 4

3. Verifica que puedas:
   - Ver la lista de tenants
   - Crear nuevos tenants (si es necesario)
   - Gestionar usuarios globales

### 8.2 Verificar Tenants

1. Accede a cada tenant usando sus subdominios:
   ```
   https://duoc.portal-autoatencion.onrender.com/
   https://inacap.portal-autoatencion.onrender.com/  (si existe)
   ```

2. Verifica que puedas:
   - Iniciar sesión con usuarios del tenant
   - Ver las asignaturas, ayudantías, etc.
   - Navegar por la aplicación

### 8.3 Verificar API Móvil

1. Prueba un endpoint de la API:
   ```
   https://portal-autoatencion.onrender.com/api/mobile/asignaturas/
   ```

2. Debe responder con datos JSON (puede requerir autenticación)

---

## ✅ Paso 9: Actualizar URL de la App Móvil

La app móvil actualmente apunta a tu IP local (`192.168.100.25:8000`). Necesitas actualizarla para que apunte a Render.

### 9.1 Actualizar Constants

Edita `app-mobile/src/utils/constants.js`:

```javascript
// Cambiar de:
export const API_BASE_URL = 'http://192.168.100.25:8000/api/mobile';

// A:
export const API_BASE_URL = 'https://portal-autoatencion.onrender.com/api/mobile';
```

### 9.2 Verificar Tenant por Defecto

Verifica que `app-mobile/src/utils/tenant.js` tenga el tenant correcto:

```javascript
export const DEFAULT_TENANT = 'DUOC UC';  // O el tenant que uses
```

---

## ✅ Paso 10: Probar la App Móvil con Render

1. **Reinicia la app móvil:**
   ```powershell
   cd app-mobile
   npm start
   ```

2. **Prueba el login:**
   - Usa las credenciales de un estudiante del tenant DUOC UC
   - Verifica que puedas iniciar sesión
   - Verifica que puedas ver asignaturas, ayudantías, etc.

3. **Verifica las funcionalidades:**
   - Ver asignaturas
   - Ver ayudantías
   - Inscribirse en ayudantías
   - Ver mis inscripciones
   - Cancelar inscripciones
   - Cerrar sesión

---

## ✅ Paso 11: Configurar CORS para Producción (Si es Necesario)

Si la app móvil tiene problemas de CORS, verifica que en `portalAutoatencion/settings.py` esté configurado:

```python
# En producción, permite solo los orígenes necesarios
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if os.getenv('CORS_ALLOWED_ORIGINS') else []

# O si necesitas permitir todos (solo para desarrollo)
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        'https://portal-autoatencion.onrender.com',
        # Agrega otros orígenes si es necesario
    ]
```

**Nota:** En Render, puedes configurar `CORS_ALLOWED_ORIGINS` como variable de entorno si es necesario.

---

## ✅ Paso 12: Verificar Variables de Entorno en Render

Asegúrate de que todas las variables de entorno estén configuradas en Render:

1. Ve a Render.com → Tu servicio → "Environment"
2. Verifica que tengas:
   - `DATABASE_URL` (automático desde la BD)
   - `SECRET_KEY` (generado automáticamente)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=portal-autoatencion.onrender.com`
   - `CSRF_TRUSTED_ORIGINS=https://portal-autoatencion.onrender.com`
   - `CORS_ALLOWED_ORIGINS` (si es necesario)

---

## ✅ Paso 13: Limpiar Archivos de Exportación

Una vez que hayas verificado que todo funciona, elimina los archivos de exportación por seguridad:

```powershell
# Eliminar archivos JSON de exportación (contienen datos sensibles)
Remove-Item datos_publicos.json
Remove-Item datos_duoc.json
Remove-Item datos_*.json  # Si hay más
```

**Nota:** Estos archivos ya están en `.gitignore`, pero es buena práctica eliminarlos.

---

## ✅ Paso 14: Documentar URLs de Producción

Crea un documento con las URLs importantes:

- **Panel Global Admin:** `https://portal-autoatencion.onrender.com/global/login/`
- **Tenant DUOC UC:** `https://duoc.portal-autoatencion.onrender.com/`
- **API Móvil Base:** `https://portal-autoatencion.onrender.com/api/mobile/`
- **API Login:** `https://portal-autoatencion.onrender.com/api/mobile/auth/login/`

---

## 🔍 Verificación Final

### Checklist:

- [ ] Panel de administración global accesible
- [ ] Puedo iniciar sesión como administrador global
- [ ] Los tenants son accesibles por subdominio
- [ ] Puedo iniciar sesión en los tenants
- [ ] La API móvil responde correctamente
- [ ] La app móvil puede conectarse a Render
- [ ] Puedo iniciar sesión desde la app móvil
- [ ] Las funcionalidades de la app móvil funcionan
- [ ] Los archivos de exportación fueron eliminados

---

## 🎉 ¡Listo!

Tu aplicación está desplegada y funcionando en Render.com. Los datos han sido transferidos exitosamente.

**Próximos pasos opcionales:**
- Configurar un dominio personalizado (si lo deseas)
- Configurar SSL/HTTPS (ya está configurado por Render)
- Optimizar para producción (caché, CDN, etc.)
- Configurar backups automáticos de la base de datos

---

**¿Necesitas ayuda con algún paso específico?** ¡Pregunta!


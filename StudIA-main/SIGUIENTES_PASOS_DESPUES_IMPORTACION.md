# Siguientes Pasos Después de Importar Datos del Tenant

¡Excelente! Has importado exitosamente los datos del tenant "DUOC UC" a Render. Ahora sigue estos pasos:

---

## ✅ Paso 1: Verificar que los Datos se Importaron Correctamente

### 1.1 Verificar desde el Panel de Administración Global

1. Accede al panel de administración global:
   ```
   https://studia-8dmp.onrender.com/global/login/
   ```

2. Inicia sesión con tus credenciales de administrador global

3. Verifica que:
   - Puedes ver el tenant "DUOC UC" en la lista
   - Puedes acceder a la gestión del tenant

### 1.2 Verificar el Tenant Directamente

1. Accede al tenant usando su dominio:
   ```
   https://duoc.studia-8dmp.onrender.com/
   ```
   **Nota:** Si el dominio no está configurado, necesitarás actualizarlo (ver Paso 2).

2. Intenta iniciar sesión con un usuario del tenant para verificar que los datos están correctos

---

## ✅ Paso 2: Actualizar Dominios del Tenant en Render

Los dominios exportados desde tu BD local probablemente apuntan a `localhost`. Necesitas actualizarlos para Render.

### Opción A: Desde el Panel de Administración Global

1. Accede a: `https://studia-8dmp.onrender.com/global/login/`
2. Ve a la gestión de tenants
3. Edita el tenant "DUOC UC"
4. Actualiza el dominio a: `duoc.studia-8dmp.onrender.com`

### Opción B: Desde la Línea de Comandos (Local con DATABASE_URL de Render)

```powershell
# Asegúrate de tener DATABASE_URL configurado para Render
$env:DATABASE_URL="postgresql://studia_user:TU_PASSWORD@dpg-d4gfh8ruibrs73cupb80-a:5432/studia"

# Abrir shell de Django
python manage.py shell
```

Dentro del shell:

```python
from clientManager.models import Empresa, Dominio
from django_tenants.utils import get_public_schema_name, schema_context

# Obtener el tenant
tenant = Empresa.objects.get(schema_name="DUOC UC")

# Ver dominios actuales
print("Dominios actuales:")
for dominio in tenant.domains.all():
    print(f"  - {dominio.domain}")

# Actualizar o crear dominio
dominio_nuevo = "duoc.studia-8dmp.onrender.com"
dominio_obj, created = Dominio.objects.get_or_create(
    domain=dominio_nuevo,
    defaults={'tenant': tenant, 'is_primary': True}
)

if not created:
    dominio_obj.is_primary = True
    dominio_obj.save()

print(f"✓ Dominio actualizado: {dominio_nuevo}")
```

---

## ✅ Paso 3: Actualizar URL de la App Móvil

La app móvil actualmente apunta a tu IP local. Actualízala para que apunte a Render.

### 3.1 Actualizar Constants

Edita `app-mobile/src/utils/constants.js`:

```javascript
export const API_BASE_URL = __DEV__ 
  ? 'http://192.168.100.25:8000/api/mobile'  // Desarrollo - IP local
  : 'https://studia-8dmp.onrender.com/api/mobile'; // Producción - Render
```

### 3.2 Verificar Tenant por Defecto

Verifica que `app-mobile/src/utils/tenant.js` tenga el tenant correcto:

```javascript
export const DEFAULT_TENANT = 'DUOC UC';
```

---

## ✅ Paso 4: Probar la App Móvil con Render

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
   - ✅ Ver asignaturas
   - ✅ Ver ayudantías
   - ✅ Inscribirse en ayudantías
   - ✅ Ver mis inscripciones
   - ✅ Cancelar inscripciones
   - ✅ Cerrar sesión

---

## ✅ Paso 5: Verificar CORS (Si hay Problemas)

Si la app móvil tiene problemas de CORS, verifica que en `portalAutoatencion/settings.py` esté configurado:

```python
# En producción, permite el origen de Render
CORS_ALLOWED_ORIGINS = [
    'https://studia-8dmp.onrender.com',
    # Agrega otros orígenes si es necesario
]

# O temporalmente para desarrollo (NO recomendado en producción)
# CORS_ALLOW_ALL_ORIGINS = True
```

**Nota:** Ya debería estar configurado en `render.yaml`, pero verifica que funcione.

---

## ✅ Paso 6: Verificar Variables de Entorno en Render

Asegúrate de que todas las variables de entorno estén configuradas en Render:

1. Ve a Render.com → Tu servicio → "Environment"
2. Verifica que tengas:
   - ✅ `DATABASE_URL` (automático desde la BD)
   - ✅ `SECRET_KEY` (generado automáticamente)
   - ✅ `DEBUG=False` (o `True` temporalmente para debugging)
   - ✅ `ALLOWED_HOSTS=studia-8dmp.onrender.com,*.onrender.com`
   - ✅ `CSRF_TRUSTED_ORIGINS=https://studia-8dmp.onrender.com`
   - ✅ `CORS_ALLOWED_ORIGINS` (si es necesario)

---

## ✅ Paso 7: Limpiar Archivos de Exportación

Una vez que hayas verificado que todo funciona, elimina los archivos de exportación por seguridad:

```powershell
# Eliminar archivos JSON de exportación (contienen datos sensibles)
Remove-Item datos_publicos.json -ErrorAction SilentlyContinue
Remove-Item datos_duoc.json -ErrorAction SilentlyContinue
Remove-Item datos_*.json -ErrorAction SilentlyContinue
```

**Nota:** Estos archivos ya están en `.gitignore`, pero es buena práctica eliminarlos.

---

## 📋 Checklist de Verificación Final

- [ ] Panel de administración global accesible en `https://studia-8dmp.onrender.com/global/login/`
- [ ] Puedo iniciar sesión como administrador global
- [ ] El tenant "DUOC UC" aparece en la lista de tenants
- [ ] El dominio del tenant está actualizado a `duoc.studia-8dmp.onrender.com`
- [ ] Puedo acceder al tenant por su dominio
- [ ] Puedo iniciar sesión en el tenant con usuarios importados
- [ ] La API móvil responde correctamente en `https://studia-8dmp.onrender.com/api/mobile/`
- [ ] La app móvil puede conectarse a Render
- [ ] Puedo iniciar sesión desde la app móvil
- [ ] Las funcionalidades de la app móvil funcionan (asignaturas, ayudantías, inscripciones)
- [ ] Los archivos de exportación fueron eliminados

---

## 🎉 ¡Listo!

Tu aplicación está desplegada y funcionando en Render.com. Los datos han sido transferidos exitosamente.

**URLs importantes:**
- **Panel Global Admin:** `https://studia-8dmp.onrender.com/global/login/`
- **Tenant DUOC UC:** `https://duoc.studia-8dmp.onrender.com/` (después de actualizar dominio)
- **API Móvil Base:** `https://studia-8dmp.onrender.com/api/mobile/`
- **API Login:** `https://studia-8dmp.onrender.com/api/mobile/auth/login/`

---

**¿Necesitas ayuda con algún paso específico?** ¡Pregunta!


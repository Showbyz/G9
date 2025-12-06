# ✅ Solución: Error al guardar last_login

## 🔍 Problema Identificado

El error era:
```
no existe la relación «loginApp_usuario»
LINE 1: UPDATE "loginApp_usuario" SET "last_login" = '2025-11-21T13:...
```

**Causa:** El usuario se encontró correctamente dentro del `schema_context` en el serializer, pero cuando intentamos guardar el `last_login` en la vista (`user.save()`), estamos fuera del `schema_context`, por lo que intenta guardar en el schema público.

## ✅ Solución Aplicada

**Envolver el `user.save()` dentro del `schema_context`** en la vista `LoginView`.

### Cambios en `api_mobile/views.py`:

```python
from django_tenants.utils import schema_context

if hasattr(request, 'tenant'):
    with schema_context(request.tenant.schema_name):
        # Actualizar last_login
        from django.utils import timezone
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
```

## 🔄 Próximo Paso

**REINICIA Django** para que los cambios surtan efecto:

1. Detén Django (Ctrl+C)
2. Inicia de nuevo:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## 🧪 Probar Ahora

1. **Intenta hacer login de nuevo** desde la app móvil
2. **Usa uno de estos emails:**
   - `estudiante@duoc.cl`
   - `Garrosh@duocuc.cl`
   - `fei.silva@duocuc.cl`
3. **Deberías ver:**
   - ✅ El login funciona completamente
   - ✅ Se actualiza el `last_login` correctamente
   - ✅ Se generan los tokens JWT
   - ✅ Se retorna la respuesta exitosa

## 📋 Logs Esperados

En Django deberías ver:
```
[API Mobile] Petición recibida: POST /api/mobile/auth/login/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[API Mobile Serializer] Usando schema_context: DUOC UC
[API Mobile Serializer] Usuario encontrado: estudiante@duoc.cl
[21/Nov/2025 10:XX:XX] "POST /api/mobile/auth/login/ HTTP/1.1" 200 XX
```

---

**¡Reinicia Django y prueba el login! Debería funcionar completamente ahora.** 🚀


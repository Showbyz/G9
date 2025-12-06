# ✅ Solución: Uso de schema_context

## 🔍 Problema Identificado

El error era:
```
'psycopg2.extensions.connection' object has no attribute 'schema_name'
```

**Causa:** Intentábamos acceder directamente a `connection.connection`, que es la conexión de psycopg2, no el DatabaseWrapper de django-tenants. No podemos asignar `schema_name` directamente a una conexión de psycopg2.

## ✅ Solución Aplicada

**Usar `schema_context` de django-tenants** - Este es el método recomendado y correcto para cambiar el schema en django-tenants.

### Cambios en `api_mobile/serializers.py`:

1. **Eliminado:** Intentos de manipular directamente la conexión
2. **Agregado:** Uso de `schema_context(request.tenant.schema_name)` para envolver todas las consultas
3. **Todas las validaciones** ahora se ejecutan dentro del `schema_context`

### Código corregido:

```python
from django_tenants.utils import schema_context

with schema_context(request.tenant.schema_name):
    user = Usuario.objects.get(email=email)
    # Todas las validaciones dentro del contexto
    if not user.check_password(password):
        raise ValidationError(...)
    if not user.is_active:
        raise ValidationError(...)
    # etc.
    attrs['user'] = user
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
   - ✅ El schema se establece correctamente usando `schema_context`
   - ✅ Los logs muestran el schema correcto
   - ✅ El login funciona

## 📋 Logs Esperados

En Django deberías ver:
```
[API Mobile] Petición recibida: POST /api/mobile/auth/login/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[API Mobile Serializer] Usando schema_context: DUOC UC
[API Mobile Serializer] Usuario encontrado: estudiante@duoc.cl
```

---

**¡Reinicia Django y prueba el login! Debería funcionar ahora.** 🚀


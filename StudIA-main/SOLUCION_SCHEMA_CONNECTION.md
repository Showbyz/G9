# ✅ Solución: Error de Schema en Conexión

## 🔍 Problema Identificado

El error era:
```
no existe la relación «loginApp_usuario»
[API Mobile] WARNING: No se pudo establecer schema (connection type: <class 'django.utils.connection.ConnectionProxy'>)
```

**Causa:** `connection` es un `ConnectionProxy`, no un `DatabaseWrapper` directamente. Necesitamos acceder a la conexión real usando `connection.connection`.

## ✅ Solución Aplicada

1. **Middleware (`api_mobile/middleware.py`):**
   - Acceder a la conexión real usando `connection.connection`
   - Intentar múltiples métodos para establecer el schema:
     - `set_tenant_to()` si es `DatabaseWrapper`
     - `set_schema_to()` si está disponible
     - Asignar `schema_name` directamente como último recurso

2. **Serializer (`api_mobile/serializers.py`):**
   - Misma lógica: acceder a la conexión real
   - Establecer el schema antes de consultar `Usuario`

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
   - ✅ El schema se establece correctamente
   - ✅ Los logs muestran el schema correcto
   - ✅ El login funciona

## 📋 Logs Esperados

En Django deberías ver:
```
[API Mobile] Petición recibida: POST /api/mobile/auth/login/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[API Mobile] Schema actual de BD: DUOC UC
[API Mobile Serializer] Schema establecido: DUOC UC
[API Mobile Serializer] Usuario encontrado: estudiante@duoc.cl
```

---

**¡Reinicia Django y prueba el login! Debería funcionar ahora.** 🚀


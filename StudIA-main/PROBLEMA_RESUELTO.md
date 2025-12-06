# ✅ Problema Resuelto: Error de CORS

## 🔍 Problema Identificado

El error era:
```
Access to XMLHttpRequest at 'http://192.168.100.25:8000/api/mobile/auth/login/' from origin 'http://localhost:19006' has been blocked by CORS policy: Request header field x-tenant-schema is not allowed by Access-Control-Allow-Headers in preflight response.
```

**Causa:** El header `X-Tenant-Schema` no estaba en la lista de headers permitidos por CORS.

## ✅ Solución Aplicada

Se agregó `x-tenant-schema` y `X-Tenant-Schema` a `CORS_ALLOW_HEADERS` en `settings.py`.

## 🔄 Acción Requerida: REINICIAR DJANGO

**IMPORTANTE:** Debes reiniciar Django para que los cambios surtan efecto:

1. **Detén Django** (Ctrl+C en la terminal de Django)
2. **Inicia de nuevo:**
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
   - ✅ La petición POST se envía correctamente
   - ✅ Los logs `[API Mobile]` aparecen en Django
   - ✅ El login funciona

## 📋 Logs Esperados

### En Django:
```
[API Mobile] Petición recibida: OPTIONS /api/mobile/auth/login/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[API Mobile] Petición recibida: POST /api/mobile/auth/login/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[API Mobile Serializer] Schema establecido: DUOC UC
[API Mobile Serializer] Usuario encontrado: estudiante@duoc.cl
```

### En la App:
```
[LoginScreen] handleLogin llamado
[APP] Intentando login con: estudiante@duoc.cl
[APP] Enviando petición POST a /auth/login/
[APP] Agregando header X-Tenant-Schema: DUOC UC
```

---

**¡Reinicia Django y prueba el login! Debería funcionar ahora.** 🚀


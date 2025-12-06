# 🔍 Debug Completo - Login No Funciona

## Problema

Solo se ven peticiones **OPTIONS** pero **NO se ven peticiones POST**. Además, **NO se ven los logs del middleware** `[API Mobile]`.

## Logs Agregados

He agregado logs detallados en:

1. **LoginScreen** - Verás cuando se presiona el botón
2. **AuthContext** - Verás el flujo de autenticación
3. **auth.js** - Verás la petición HTTP
4. **client.js** - Verás la configuración de la petición
5. **Middleware Django** - Verás cada petición que llega

## 🔍 Qué Verificar

### 1. En la Consola de la App Móvil (presiona `m` en npm start)

Deberías ver:
```
[LoginScreen] handleLogin llamado
[LoginScreen] Email: [email]
[LoginScreen] Password length: [número]
[LoginScreen] Iniciando proceso de login...
[LoginScreen] Llamando a login() del contexto...
[AuthContext] login llamado con email: [email]
[AuthContext] Llamando a apiLogin...
[APP] Intentando login con: [email]
[APP] URL de API: http://192.168.100.25:8000/api/mobile
[APP] Enviando petición POST a /auth/login/
[APP] Agregando header X-Tenant-Schema: DUOC UC
[APP] Petición configurada: POST /auth/login/
```

### 2. En los Logs de Django

Deberías ver:
```
[API Mobile] Petición recibida: OPTIONS /api/mobile/auth/login/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[API Mobile] Petición recibida: POST /api/mobile/auth/login/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
```

## ⚠️ Si NO Ves los Logs

### Si NO ves logs `[LoginScreen]`:
- El botón no se está presionando
- Hay un error antes de ejecutar handleLogin

### Si ves logs `[LoginScreen]` pero NO `[APP]`:
- Hay un error en AuthContext o apiLogin
- Revisa la consola para errores

### Si ves logs `[APP]` pero NO petición POST:
- La petición no se está enviando
- Puede ser un problema de CORS o red

### Si NO ves logs `[API Mobile]`:
- El middleware no se está ejecutando
- Reinicia Django completamente

## 🧪 Prueba Ahora

1. **Abre la consola de la app** (presiona `m` en npm start)
2. **Intenta hacer login**
3. **Revisa TODOS los logs** que aparecen
4. **Comparte los logs** que ves (tanto de la app como de Django)

---

**Con estos logs podremos identificar exactamente dónde está el problema.**


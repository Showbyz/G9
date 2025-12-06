# 🧪 Test del Middleware

## Verificar que el Middleware Funciona

Cuando hagas una petición POST a `/api/mobile/auth/login/`, deberías ver en los logs de Django:

```
[API Mobile] Usando tenant por defecto: inacap
[API Mobile] Tenant establecido: inacap (inacap)
[API Mobile] Schema actual de BD: inacap
```

Si NO ves estos logs, el middleware no se está ejecutando.

## Si No Ves los Logs

1. Verifica que el middleware está en `settings.py`
2. Verifica que está ANTES de `TenantMainMiddleware`
3. Reinicia Django completamente (no solo recarga)

## Si Ves los Logs pero Sigue el Error

El problema puede ser que el schema se está reseteando después del middleware. En ese caso, necesitamos usar `schema_context` en el serializer también.


# 🔍 Instrucciones para Debug

## Cambios Realizados

1. ✅ **Tenant configurado a 'DUOC UC'** en la app móvil
2. ✅ **Logs agregados** en middleware y serializer
3. ✅ **Migraciones verificadas** (ya están aplicadas)

## 🔍 Qué Verificar

### 1. Verificar que el Middleware se Ejecuta

Cuando hagas una petición POST (no solo OPTIONS), deberías ver en los logs de Django:

```
[API Mobile] Petición recibida: POST /api/mobile/auth/login/
[API Mobile] Usando tenant por defecto: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[API Mobile] Schema actual de BD: DUOC UC
```

**Si NO ves estos logs:**
- El middleware no se está ejecutando
- O solo estás viendo peticiones OPTIONS (preflight de CORS)

### 2. Verificar Petición POST

En los logs deberías ver:
- `OPTIONS /api/mobile/auth/login/` (preflight de CORS) ✅ Ya lo veo
- `POST /api/mobile/auth/login/` (petición real) ❌ No lo veo

**Si solo ves OPTIONS:**
- La petición POST no se está enviando desde la app
- O está fallando antes de llegar al servidor
- Revisa la consola de la app móvil para ver errores

### 3. Verificar Schema con Espacios

El schema "DUOC UC" tiene espacios, lo cual puede causar problemas. Si ves errores relacionados, puede ser necesario usar comillas.

## 🧪 Próximos Pasos

1. **Intenta hacer login de nuevo**
2. **Revisa la consola de la app móvil** (presiona `m` en npm start)
3. **Revisa los logs de Django** - Busca mensajes `[API Mobile]`
4. **Comparte los logs** que aparecen cuando intentas hacer login

## ⚠️ Si No Ves Peticiones POST

Si solo ves OPTIONS pero no POST, el problema está en:
- La app móvil no está enviando la petición POST
- Hay un error en el cliente antes de enviar
- Revisa la consola de Expo/React Native

---

**Intenta el login y comparte TODOS los logs que aparecen (tanto en Django como en la app móvil).**


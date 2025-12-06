# 🔄 Instrucciones para Reiniciar y Probar

## ✅ Cambios Realizados

1. ✅ **CORS configurado** - Permite peticiones desde la app móvil
2. ✅ **Manejo de errores mejorado** - Los campos NO se limpian si hay error
3. ✅ **Logging mejorado** - Verás más información en la consola
4. ✅ **Assets configurados** - Error de favicon solucionado

## 🔄 PASO CRÍTICO: Reiniciar Servidor Django

**DEBES reiniciar el servidor Django** para que los cambios de CORS surtan efecto:

1. **Detén el servidor actual:**
   - Ve a la terminal donde corre Django
   - Presiona `Ctrl+C`

2. **Inicia de nuevo:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## 🧪 Probar el Login

1. **Abre la app móvil** (presiona `w` en la terminal de npm start o usa tu teléfono)

2. **Intenta hacer login** con credenciales de estudiante

3. **Revisa la consola de Expo:**
   - Presiona `m` en la terminal de npm start para ver logs
   - Busca mensajes que empiecen con "Intentando login" y "Respuesta del servidor"

4. **Revisa la terminal de Django:**
   - Deberías ver: `"POST /api/mobile/auth/login/ HTTP/1.1" 200 XX` si es exitoso
   - O `400`/`401` si hay error

## 🔍 Debug

Si el login sigue sin funcionar:

### En la Consola de Expo (presiona `m`):
- Busca los logs que dicen "Intentando login con:"
- Busca "Respuesta del servidor:"
- Busca cualquier error en rojo

### En la Terminal de Django:
- Verifica que veas la petición POST (no solo OPTIONS)
- Verifica el código de estado (200 = éxito, 400/401 = error)

### Verificar Credenciales:
- Asegúrate de que el usuario sea estudiante (no staff ni tutor)
- Verifica que el email y contraseña sean correctos
- Verifica que la cuenta esté activa

## 📋 Checklist

- [ ] Servidor Django reiniciado
- [ ] App móvil abierta
- [ ] Credenciales de estudiante listas
- [ ] Consola de Expo abierta para ver logs
- [ ] Terminal de Django visible para ver peticiones

## ⚠️ Si Aún No Funciona

1. **Verifica la URL de la API:**
   - Debe ser: `http://192.168.100.25:8000/api/mobile`
   - Verifica en `app-mobile/src/utils/constants.js`

2. **Verifica que Django esté corriendo:**
   - Debe estar en `0.0.0.0:8000`
   - No solo `127.0.0.1:8000`

3. **Verifica la red:**
   - Tu teléfono y computadora deben estar en la misma WiFi

---

**¡Reinicia Django y prueba de nuevo!** 🚀


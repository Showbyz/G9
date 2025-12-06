# 🔧 Solución de Errores de Login

## ✅ Problemas Corregidos

### 1. CORS Configurado
- ✅ Instalado `django-cors-headers`
- ✅ Agregado al middleware
- ✅ Configurado para permitir peticiones desde la app móvil

### 2. Assets Faltantes
- ✅ Creada carpeta `assets`
- ✅ Configurado `app.json` para usar icon.png como favicon también

### 3. Manejo de Errores Mejorado
- ✅ Mejor logging en el cliente
- ✅ Mejor manejo de errores en AuthContext
- ✅ Los campos NO se limpian si hay error

## 🔄 Reiniciar el Servidor Django

**IMPORTANTE:** Después de los cambios, debes reiniciar el servidor Django:

1. **Detén el servidor actual** (Ctrl+C en la terminal donde corre)
2. **Inicia de nuevo:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## 🧪 Probar el Login

1. **Abre la app móvil** (en navegador con `w` o en tu teléfono)
2. **Intenta hacer login** con credenciales de estudiante
3. **Revisa la consola** de Expo para ver los logs de debug

## 📋 Verificar que Funciona

### En la Terminal de Django deberías ver:
```
[20/Nov/2025 XX:XX:XX] "POST /api/mobile/auth/login/ HTTP/1.1" 200 XX
```

Si ves `200`, el login fue exitoso.

### Si ves `400` o `401`:
- Verifica las credenciales
- Verifica que el usuario sea estudiante (no staff ni tutor)
- Revisa los logs en la consola de Expo

## 🐛 Debug

Si el login sigue sin funcionar:

1. **Abre la consola de Expo** (presiona `m` en la terminal de npm start)
2. **Revisa los logs** que aparecen cuando intentas hacer login
3. **Verifica en Django** qué respuesta está enviando

## ⚠️ Nota sobre Assets

Los archivos `icon.png`, `splash.png` y `favicon.png` son opcionales para desarrollo.
Si quieres crearlos:
- **icon.png**: 1024x1024 px
- **splash.png**: 1242x2436 px (iOS) o 2048x2732 px
- **favicon.png**: 48x48 px

Por ahora, la app funcionará sin ellos (solo verás advertencias).

---

**Reinicia el servidor Django y prueba de nuevo el login.**


# 📱 Cómo Ver la App Móvil

## 🚀 Después de Ejecutar `npm start`

Cuando ejecutas `npm start`, se abrirá **Expo** y verás varias opciones. Aquí te explico cómo ver la app:

## 📋 Opciones Disponibles

### Opción 1: Ver en el Navegador Web (Más Rápido para Probar)

1. **Presiona la tecla `w`** en la terminal donde está corriendo `npm start`
2. Se abrirá automáticamente en tu navegador
3. Verás la app funcionando (aunque es una versión web, útil para probar)

### Opción 2: Ver en Emulador Android (Si tienes Android Studio)

1. **Presiona la tecla `a`** en la terminal
2. Se abrirá el emulador de Android (si está instalado)
3. La app se cargará automáticamente

### Opción 3: Ver en Emulador iOS (Solo Mac)

1. **Presiona la tecla `i`** en la terminal
2. Se abrirá el simulador de iOS (solo disponible en Mac)

### Opción 4: Ver en Tu Teléfono Físico (Recomendado) 📱

Esta es la mejor opción para probar la app real:

#### Paso 1: Instalar Expo Go en tu Teléfono

**Android:**
- Abre Google Play Store
- Busca "Expo Go"
- Instala la app

**iOS:**
- Abre App Store
- Busca "Expo Go"
- Instala la app

#### Paso 2: Conectar tu Teléfono

1. **Asegúrate de que tu teléfono y computadora estén en la misma red WiFi**

2. **En la terminal donde corre `npm start`, verás un código QR**

3. **Escanear el código QR:**
   - **Android:** Abre Expo Go → Toca "Scan QR code" → Escanea el código
   - **iOS:** Abre la app Cámara → Apunta al código QR → Toca la notificación

4. **La app se cargará automáticamente en tu teléfono**

## 🎯 Resumen de Teclas

Cuando veas la pantalla de Expo, puedes presionar:

- **`w`** → Abrir en navegador web
- **`a`** → Abrir en emulador Android
- **`i`** → Abrir en simulador iOS (solo Mac)
- **`r`** → Recargar la app
- **`m`** → Abrir menú de desarrollador
- **`Ctrl+C`** → Detener el servidor

## 📱 Qué Verás en la App

Una vez que la app se cargue, verás:

1. **Pantalla de Login** - Ingresa con tus credenciales de estudiante
2. **Pantalla de Asignaturas** - Después del login
3. **Navegación inferior** - Tabs para Asignaturas, Inscripciones y Perfil

## ⚠️ Solución de Problemas

### El código QR no aparece:
- Verifica que `npm start` esté corriendo
- Espera unos segundos a que cargue completamente

### No puedo escanear el QR:
- Asegúrate de tener Expo Go instalado
- Verifica que estés en la misma red WiFi
- Intenta escribir la URL manualmente en Expo Go

### La app no carga:
- Verifica que el servidor Django esté corriendo en `0.0.0.0:8000`
- Verifica que la URL en `constants.js` sea correcta (192.168.100.25:8000)
- Revisa la consola de Expo para errores

### Error de conexión:
- Verifica que tu teléfono y computadora estén en la misma red WiFi
- Verifica que el firewall no esté bloqueando el puerto 19000 (Expo)
- Intenta reiniciar `npm start`

## 🎉 ¡Listo!

Una vez que veas la app, podrás:
- ✅ Hacer login
- ✅ Ver asignaturas
- ✅ Ver ayudantías
- ✅ Inscribirte
- ✅ Ver tus inscripciones
- ✅ Ver tu perfil

---

**¡Disfruta probando tu app móvil!** 🚀


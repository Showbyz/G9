# 🚀 Inicio Rápido - App Móvil

## ✅ URL Configurada

La URL de la API ya está configurada con tu IP: **192.168.100.25**

## 📋 Pasos para Ejecutar la App

### 1. Verificar que el Servidor Django esté Corriendo

Asegúrate de que el servidor Django esté corriendo y accesible desde la red:

```bash
# En el directorio del proyecto Django
python manage.py runserver 0.0.0.0:8000
```

El `0.0.0.0` permite que el servidor sea accesible desde otros dispositivos en la red.

### 2. Instalar Node.js (si no lo tienes)

Si no tienes Node.js instalado:

1. Descarga Node.js desde: https://nodejs.org/
2. Instala la versión LTS
3. Reinicia la terminal

### 3. Instalar Dependencias de la App

```bash
cd app-mobile
npm install
```

### 4. Iniciar la Aplicación

```bash
npm start
```

Esto abrirá Expo. Luego puedes:

- Presionar `a` para Android
- Presionar `i` para iOS
- Presionar `w` para web (prueba rápida)
- Escanear el código QR con la app Expo Go en tu teléfono

### 5. Probar en Dispositivo Físico

1. **Instala Expo Go** en tu teléfono:
   - Android: [Google Play](https://play.google.com/store/apps/details?id=host.exp.exponent)
   - iOS: [App Store](https://apps.apple.com/app/expo-go/id982107779)

2. **Asegúrate de que tu teléfono esté en la misma red WiFi** que tu computadora

3. **Escanear el código QR** que aparece en la terminal

## 🔧 Verificación de Conexión

Para verificar que la API es accesible desde tu IP, puedes probar en el navegador:

```
http://192.168.100.25:8000/api/mobile/asignaturas/
```

(Debería pedir autenticación, pero si ves un error de autenticación significa que la conexión funciona)

## ⚠️ Solución de Problemas

### Error: "npm no se reconoce"
- Instala Node.js desde nodejs.org
- Reinicia la terminal después de instalar

### Error de conexión en la app
- Verifica que el servidor Django esté corriendo con `0.0.0.0:8000`
- Verifica que tu teléfono esté en la misma red WiFi
- Verifica que el firewall no esté bloqueando el puerto 8000

### La app no carga
- Verifica que Expo Go esté instalado
- Asegúrate de estar en la misma red WiFi
- Intenta reiniciar el servidor de Expo

## 📱 Estructura de la App

La app ya está completamente configurada con:
- ✅ URL de API: `http://192.168.100.25:8000/api/mobile`
- ✅ Todas las pantallas implementadas
- ✅ Autenticación JWT
- ✅ Navegación completa

## 🎯 Próximos Pasos

1. Instalar Node.js (si no lo tienes)
2. Ejecutar `npm install` en la carpeta `app-mobile`
3. Ejecutar `npm start`
4. Probar en dispositivo o emulador

---

**¡La app está lista para ejecutarse!** Solo necesitas Node.js y npm instalados.


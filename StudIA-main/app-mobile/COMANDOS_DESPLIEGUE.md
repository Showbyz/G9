# 🚀 Comandos para Desplegar la App Móvil

## ✅ URL Configurada

La URL de la API ya está configurada con tu IP: **192.168.100.25:8000**

## 📋 Pasos para Ejecutar

### 1. Verificar Node.js

Abre una nueva terminal y verifica que Node.js esté instalado:

```bash
node --version
npm --version
```

Si no está instalado, descárgalo desde: https://nodejs.org/

### 2. Instalar Dependencias

```bash
cd app-mobile
npm install
```

### 3. Iniciar la App

```bash
npm start
```

Esto iniciará Expo. Luego puedes:

- Presionar **`a`** para Android
- Presionar **`i`** para iOS
- Presionar **`w`** para web
- **Escanear el QR** con Expo Go en tu teléfono

## 🔧 Servidor Django

El servidor Django debe estar corriendo en:

```bash
python manage.py runserver 0.0.0.0:8000
```

El `0.0.0.0` permite acceso desde otros dispositivos en la red.

## 📱 Probar en Dispositivo Físico

1. **Instala Expo Go** en tu teléfono:
   - Android: https://play.google.com/store/apps/details?id=host.exp.exponent
   - iOS: https://apps.apple.com/app/expo-go/id982107779

2. **Asegúrate de estar en la misma red WiFi**

3. **Escanear el código QR** que aparece al ejecutar `npm start`

## ✅ Configuración Completada

- ✅ URL de API: `http://192.168.100.25:8000/api/mobile`
- ✅ Todas las pantallas implementadas
- ✅ Autenticación configurada
- ✅ Navegación completa

## 🎯 Resumen de Comandos

```bash
# 1. Ir a la carpeta de la app
cd app-mobile

# 2. Instalar dependencias (solo la primera vez)
npm install

# 3. Iniciar la app
npm start
```

---

**¡Listo! La app está configurada y lista para ejecutarse.**


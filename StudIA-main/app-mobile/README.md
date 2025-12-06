# 📱 Portal de Ayudantías - App Móvil

Aplicación móvil React Native para estudiantes del Portal de Ayudantías.

## 🚀 Características

- ✅ Login de estudiantes
- ✅ Ver asignaturas disponibles
- ✅ Ver ayudantías por asignatura
- ✅ Inscribirse en ayudantías
- ✅ Ver mis inscripciones
- ✅ Cancelar inscripciones
- ✅ Ver perfil de usuario
- ✅ Autenticación JWT con refresh automático

## 📋 Requisitos Previos

- Node.js (v14 o superior)
- npm o yarn
- Expo CLI
- Android Studio (para Android) o Xcode (para iOS)

## 🔧 Instalación

1. **Instalar dependencias:**
```bash
cd app-mobile
npm install
```

2. **Configurar URL de la API:**
Edita `src/utils/constants.js` y cambia `API_BASE_URL` según tu entorno:
```javascript
export const API_BASE_URL = __DEV__ 
  ? 'http://TU_IP_LOCAL:8000/api/mobile'  // Para desarrollo físico
  : 'https://tu-dominio.com/api/mobile';   // Para producción
```

**Nota importante:** Si pruebas en dispositivo físico, usa tu IP local en lugar de `localhost`.

3. **Iniciar la aplicación:**
```bash
npm start
```

Luego presiona:
- `a` para Android
- `i` para iOS
- `w` para web

## 📱 Estructura del Proyecto

```
app-mobile/
├── src/
│   ├── api/              # Servicios API
│   │   ├── client.js
│   │   ├── auth.js
│   │   ├── asignaturas.js
│   │   ├── ayudantias.js
│   │   ├── inscripciones.js
│   │   └── sedes.js
│   ├── screens/          # Pantallas
│   │   ├── LoginScreen.js
│   │   ├── HomeScreen.js
│   │   ├── AyudantiasScreen.js
│   │   ├── AyudantiaDetailScreen.js
│   │   ├── MisInscripcionesScreen.js
│   │   └── PerfilScreen.js
│   ├── navigation/        # Navegación
│   │   └── AppNavigator.js
│   ├── context/           # Contextos
│   │   └── AuthContext.js
│   └── utils/             # Utilidades
│       └── constants.js
├── App.js
├── package.json
└── app.json
```

## 🔐 Autenticación

La app usa JWT tokens que se guardan automáticamente en AsyncStorage. El refresh token se renueva automáticamente cuando el access token expira.

## 🎨 Pantallas

### 1. Login
- Email y contraseña
- Validación de campos
- Manejo de errores

### 2. Home (Asignaturas)
- Lista de asignaturas disponibles
- Contador de ayudantías por asignatura
- Pull to refresh
- Navegación a ayudantías

### 3. Ayudantías
- Lista de ayudantías de una asignatura
- Información de fecha, horario, sala
- Estado de cupos
- Navegación a detalle

### 4. Detalle de Ayudantía
- Información completa
- Botón de inscripción
- Validaciones

### 5. Mis Inscripciones
- Lista de inscripciones activas
- Información de cada ayudantía
- Botón para cancelar
- Badges de estado

### 6. Perfil
- Información del usuario
- Botón de actualizar
- Cerrar sesión

## 🛠️ Desarrollo

### Ejecutar en desarrollo:
```bash
npm start
```

### Ejecutar en Android:
```bash
npm run android
```

### Ejecutar en iOS:
```bash
npm run ios
```

## 📦 Generar APK

### Android (Expo Build):

1. **Instalar EAS CLI:**
```bash
npm install -g eas-cli
```

2. **Configurar proyecto:**
```bash
eas build:configure
```

3. **Generar APK:**
```bash
eas build --platform android --profile preview
```

### Android (React Native CLI):

1. **Generar keystore:**
```bash
keytool -genkeypair -v -storetype PKCS12 -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
```

2. **Configurar gradle.properties:**
```properties
MYAPP_RELEASE_STORE_FILE=my-release-key.keystore
MYAPP_RELEASE_KEY_ALIAS=my-key-alias
MYAPP_RELEASE_STORE_PASSWORD=*****
MYAPP_RELEASE_KEY_PASSWORD=*****
```

3. **Generar APK:**
```bash
cd android
./gradlew assembleRelease
```

El APK estará en: `android/app/build/outputs/apk/release/app-release.apk`

## ⚙️ Configuración

### Cambiar URL de API:
Edita `src/utils/constants.js`

### Cambiar colores:
Edita `src/utils/constants.js` - sección `COLORS`

## 🐛 Solución de Problemas

### Error de conexión:
- Verifica que la URL de la API sea correcta
- Si usas dispositivo físico, usa tu IP local (no localhost)
- Verifica que el servidor Django esté corriendo
- Verifica que CORS esté configurado si es necesario

### Error de autenticación:
- Verifica que los tokens se estén guardando correctamente
- Revisa la consola para ver errores de API

## 📝 Notas

- La app está diseñada exclusivamente para estudiantes
- Requiere conexión a internet para funcionar
- Los tokens se guardan localmente en el dispositivo

## 🔗 Enlaces Útiles

- [React Native Docs](https://reactnative.dev/)
- [Expo Docs](https://docs.expo.dev/)
- [React Navigation](https://reactnavigation.org/)


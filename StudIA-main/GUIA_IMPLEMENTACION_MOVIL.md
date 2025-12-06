# 📱 Guía de Implementación de la App Móvil

## 🎯 Objetivo

Crear una aplicación móvil para estudiantes que se comunique con la API REST del portal de ayudantías.

## 🛠️ Tecnologías Recomendadas

### Opción 1: React Native (Recomendada)
- **Ventajas**: 
  - Un solo código para iOS y Android
  - Gran comunidad y librerías
  - Fácil de aprender si conoces React
- **Desventajas**: 
  - Requiere conocimiento de JavaScript/TypeScript
  - Puede tener problemas de rendimiento en apps muy complejas

### Opción 2: Flutter
- **Ventajas**: 
  - Excelente rendimiento
  - UI muy pulida
  - Un solo código para iOS y Android
- **Desventajas**: 
  - Requiere aprender Dart
  - Curva de aprendizaje más pronunciada

### Opción 3: Ionic + Capacitor
- **Ventajas**: 
  - Usa tecnologías web (HTML, CSS, JS)
  - Fácil para desarrolladores web
- **Desventajas**: 
  - Menor rendimiento nativo
  - UI menos nativa

## 📋 Estructura Recomendada del Proyecto

```
app-mobile/
├── src/
│   ├── api/
│   │   ├── client.js          # Cliente HTTP configurado
│   │   ├── auth.js            # Endpoints de autenticación
│   │   ├── asignaturas.js     # Endpoints de asignaturas
│   │   ├── ayudantias.js      # Endpoints de ayudantías
│   │   └── inscripciones.js   # Endpoints de inscripciones
│   ├── screens/
│   │   ├── LoginScreen.js
│   │   ├── HomeScreen.js
│   │   ├── AsignaturasScreen.js
│   │   ├── AyudantiasScreen.js
│   │   ├── MisInscripcionesScreen.js
│   │   └── PerfilScreen.js
│   ├── components/
│   │   ├── AyudantiaCard.js
│   │   ├── AsignaturaCard.js
│   │   └── LoadingSpinner.js
│   ├── navigation/
│   │   └── AppNavigator.js
│   ├── storage/
│   │   └── tokenStorage.js    # Guardar/recuperar tokens
│   ├── context/
│   │   └── AuthContext.js    # Contexto de autenticación
│   └── utils/
│       └── constants.js       # URLs, constantes
├── package.json
└── App.js
```

## 🔧 Configuración Inicial (React Native)

### 1. Instalar dependencias

```bash
npx react-native init PortalAyudantias
cd PortalAyudantias
npm install axios react-navigation @react-navigation/native @react-navigation/stack
npm install @react-native-async-storage/async-storage
npm install react-native-vector-icons
```

### 2. Configurar cliente API

**src/api/client.js**
```javascript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'http://localhost:8000/api/mobile'; // Cambiar en producción

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token a todas las peticiones
apiClient.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar refresh token
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = await AsyncStorage.getItem('refresh_token');
        const response = await axios.post(
          `${API_BASE_URL}/auth/token/refresh/`,
          { refresh: refreshToken }
        );
        
        const { access } = response.data;
        await AsyncStorage.setItem('access_token', access);
        
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Refresh falló, redirigir a login
        await AsyncStorage.multiRemove(['access_token', 'refresh_token']);
        // Navegar a login
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
```

### 3. Servicios API

**src/api/auth.js**
```javascript
import apiClient from './client';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const login = async (email, password) => {
  try {
    const response = await apiClient.post('/auth/login/', {
      email,
      password,
    });
    
    const { tokens, user } = response.data;
    
    // Guardar tokens
    await AsyncStorage.setItem('access_token', tokens.access);
    await AsyncStorage.setItem('refresh_token', tokens.refresh);
    await AsyncStorage.setItem('user', JSON.stringify(user));
    
    return { success: true, user, tokens };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.errors || 'Error al iniciar sesión',
    };
  }
};

export const logout = async () => {
  await AsyncStorage.multiRemove(['access_token', 'refresh_token', 'user']);
};

export const getProfile = async () => {
  try {
    const response = await apiClient.get('/auth/perfil/');
    return { success: true, data: response.data.data };
  } catch (error) {
    return { success: false, error: error.response?.data };
  }
};
```

**src/api/asignaturas.js**
```javascript
import apiClient from './client';

export const getAsignaturas = async (page = 1) => {
  try {
    const response = await apiClient.get('/asignaturas/', {
      params: { page },
    });
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.response?.data };
  }
};

export const getAsignatura = async (id) => {
  try {
    const response = await apiClient.get(`/asignaturas/${id}/`);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.response?.data };
  }
};
```

**src/api/ayudantias.js**
```javascript
import apiClient from './client';

export const getAyudantias = async (asignaturaId = null, page = 1) => {
  try {
    const params = { page };
    if (asignaturaId) params.asignatura_id = asignaturaId;
    
    const response = await apiClient.get('/ayudantias/', { params });
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.response?.data };
  }
};

export const getAyudantia = async (id) => {
  try {
    const response = await apiClient.get(`/ayudantias/${id}/`);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.response?.data };
  }
};

export const inscribirse = async (ayudantiaId) => {
  try {
    const response = await apiClient.post(`/ayudantias/${ayudantiaId}/inscribirse/`);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.message || 'Error al inscribirse',
    };
  }
};
```

**src/api/inscripciones.js**
```javascript
import apiClient from './client';

export const getInscripciones = async (page = 1) => {
  try {
    const response = await apiClient.get('/inscripciones/', {
      params: { page },
    });
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.response?.data };
  }
};

export const cancelarInscripcion = async (inscripcionId) => {
  try {
    const response = await apiClient.post(`/inscripciones/${inscripcionId}/cancelar/`);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.message || 'Error al cancelar',
    };
  }
};
```

## 📱 Pantallas Principales

### 1. Login Screen

```javascript
import React, { useState } from 'react';
import { View, TextInput, Button, Text, StyleSheet, Alert } from 'react-native';
import { login } from '../api/auth';

const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    const result = await login(email, password);
    setLoading(false);

    if (result.success) {
      navigation.replace('Home');
    } else {
      Alert.alert('Error', result.error?.non_field_errors?.[0] || 'Error al iniciar sesión');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Portal de Ayudantías</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      <TextInput
        style={styles.input}
        placeholder="Contraseña"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title="Iniciar Sesión" onPress={handleLogin} disabled={loading} />
    </View>
  );
};
```

### 2. Home Screen (Lista de Asignaturas)

```javascript
import React, { useEffect, useState } from 'react';
import { View, FlatList, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { getAsignaturas } from '../api/asignaturas';

const HomeScreen = ({ navigation }) => {
  const [asignaturas, setAsignaturas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAsignaturas();
  }, []);

  const loadAsignaturas = async () => {
    const result = await getAsignaturas();
    if (result.success) {
      setAsignaturas(result.data.results);
    }
    setLoading(false);
  };

  const renderAsignatura = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => navigation.navigate('Ayudantias', { asignaturaId: item.id_asignatura })}
    >
      <Text style={styles.nombre}>{item.nombre}</Text>
      <Text style={styles.codigo}>{item.codigo}</Text>
      <Text style={styles.ayudantias}>
        {item.total_ayudantias_disponibles} ayudantías disponibles
      </Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={asignaturas}
        renderItem={renderAsignatura}
        keyExtractor={(item) => item.id_asignatura.toString()}
        refreshing={loading}
        onRefresh={loadAsignaturas}
      />
    </View>
  );
};
```

## 🚀 Pasos para Generar APK

### Android (React Native)

1. **Configurar build.gradle**
```gradle
// android/app/build.gradle
android {
    ...
    defaultConfig {
        applicationId "com.portalyudantias"
        ...
    }
}
```

2. **Generar keystore**
```bash
keytool -genkeypair -v -storetype PKCS12 -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
```

3. **Configurar gradle.properties**
```properties
MYAPP_RELEASE_STORE_FILE=my-release-key.keystore
MYAPP_RELEASE_KEY_ALIAS=my-key-alias
MYAPP_RELEASE_STORE_PASSWORD=*****
MYAPP_RELEASE_KEY_PASSWORD=*****
```

4. **Generar APK**
```bash
cd android
./gradlew assembleRelease
```

El APK estará en: `android/app/build/outputs/apk/release/app-release.apk`

### iOS (React Native)

1. Abrir proyecto en Xcode
2. Configurar signing & capabilities
3. Product > Archive
4. Distribuir App

## 📝 Checklist de Implementación

- [ ] Configurar proyecto React Native/Flutter
- [ ] Implementar cliente API con interceptors
- [ ] Crear servicios para cada endpoint
- [ ] Implementar pantalla de login
- [ ] Implementar pantalla de asignaturas
- [ ] Implementar pantalla de ayudantías
- [ ] Implementar pantalla de inscripciones
- [ ] Implementar pantalla de perfil
- [ ] Manejar refresh token automático
- [ ] Agregar manejo de errores
- [ ] Agregar estados de carga
- [ ] Probar en dispositivos reales
- [ ] Generar APK/IPA
- [ ] Testing completo

## 🔗 Recursos Útiles

- [React Native Docs](https://reactnative.dev/)
- [Flutter Docs](https://flutter.dev/)
- [Axios Docs](https://axios-http.com/)
- [React Navigation](https://reactnavigation.org/)

## ⚠️ Consideraciones Importantes

1. **URL Base**: Cambiar la URL base según el entorno (desarrollo/producción)
2. **Seguridad**: Nunca hardcodear tokens o credenciales
3. **Manejo de Errores**: Implementar manejo robusto de errores
4. **Offline**: Considerar caché para funcionar offline
5. **Notificaciones**: Implementar notificaciones push para recordatorios
6. **Testing**: Probar en diferentes dispositivos y versiones de OS


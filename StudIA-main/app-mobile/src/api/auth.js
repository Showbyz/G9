import apiClient from './client';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const login = async (email, password) => {
  try {
    console.log('[APP] Intentando login con:', email);
    console.log('[APP] URL de API:', apiClient.defaults.baseURL);
    console.log('[APP] Enviando petición POST a /auth/login/');
    
    const response = await apiClient.post('/auth/login/', {
      email,
      password,
    });
    
    console.log('[APP] Respuesta del servidor:', response.status, response.data);
    
    if (response.data && response.data.success) {
      const { tokens, user } = response.data;
      
      // Guardar tokens y usuario
      await AsyncStorage.setItem('access_token', tokens.access);
      await AsyncStorage.setItem('refresh_token', tokens.refresh);
      await AsyncStorage.setItem('user', JSON.stringify(user));
      
      return { success: true, user, tokens };
    }
    
    return { success: false, error: 'Error en la respuesta del servidor' };
  } catch (error) {
    console.error('[APP] Error completo en login:', error);
    console.error('[APP] Error response:', error.response?.data);
    console.error('[APP] Error status:', error.response?.status);
    console.error('[APP] Error message:', error.message);
    if (error.request) {
      console.error('[APP] Error request:', error.request);
    }
    
    let errorMessage = 'Error al iniciar sesión. Verifica tus credenciales.';
    
    if (error.response) {
      // El servidor respondió con un error
      const data = error.response.data;
      
      // DRF puede devolver errores en diferentes formatos
      if (data.errors) {
        // Formato: { errors: { non_field_errors: [...] } }
        if (data.errors.non_field_errors && Array.isArray(data.errors.non_field_errors)) {
          errorMessage = data.errors.non_field_errors[0];
        } else if (data.errors.email && Array.isArray(data.errors.email)) {
          errorMessage = data.errors.email[0];
        } else if (data.errors.password && Array.isArray(data.errors.password)) {
          errorMessage = data.errors.password[0];
        } else {
          // Si es un objeto con strings
          const firstError = Object.values(data.errors)[0];
          if (Array.isArray(firstError)) {
            errorMessage = firstError[0];
          } else {
            errorMessage = String(firstError);
          }
        }
      } else if (data.message) {
        errorMessage = data.message;
      } else if (data.error) {
        errorMessage = data.error;
      } else if (data.detail) {
        errorMessage = data.detail;
      } else if (typeof data === 'string') {
        errorMessage = data;
      }
    } else if (error.request) {
      // La petición se hizo pero no hubo respuesta
      errorMessage = 'No se pudo conectar con el servidor. Verifica que esté corriendo en http://192.168.100.25:8000';
    } else {
      errorMessage = error.message || 'Error de conexión';
    }
    
    return { success: false, error: errorMessage };
  }
};

export const logout = async () => {
  try {
    await AsyncStorage.multiRemove(['access_token', 'refresh_token', 'user']);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
};

export const getProfile = async () => {
  try {
    const response = await apiClient.get('/auth/perfil/');
    if (response.data.success) {
      return { success: true, data: response.data.data };
    }
    return { success: false, error: 'Error al obtener perfil' };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.message || 'Error al obtener perfil' 
    };
  }
};

export const getStoredUser = async () => {
  try {
    const userJson = await AsyncStorage.getItem('user');
    if (userJson) {
      return JSON.parse(userJson);
    }
    return null;
  } catch (error) {
    return null;
  }
};

export const isAuthenticated = async () => {
  try {
    const token = await AsyncStorage.getItem('access_token');
    return !!token;
  } catch (error) {
    return false;
  }
};


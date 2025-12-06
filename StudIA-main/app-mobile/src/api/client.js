import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_BASE_URL } from '../utils/constants';
import { getTenant } from '../utils/tenant';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 15000,
});

// Interceptor para agregar token y tenant a todas las peticiones
apiClient.interceptors.request.use(
  async (config) => {
    try {
      const token = await AsyncStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      
      // Agregar tenant si está configurado
      const tenant = await getTenant();
      if (tenant) {
        config.headers['X-Tenant-Schema'] = tenant;
        console.log('[APP] Agregando header X-Tenant-Schema:', tenant);
      } else {
        console.log('[APP] WARNING: No se pudo obtener tenant');
      }
      
      console.log('[APP] Petición configurada:', config.method?.toUpperCase(), config.url);
      console.log('[APP] Headers:', JSON.stringify(config.headers, null, 2));
    } catch (error) {
      console.error('[APP] Error al obtener token o tenant:', error);
    }
    return config;
  },
  (error) => {
    console.error('[APP] Error en interceptor de request:', error);
    return Promise.reject(error);
  }
);

// Interceptor para manejar refresh token automáticamente
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Si el error es 401 y no hemos intentado refrescar el token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = await AsyncStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No hay refresh token');
        }
        
        const response = await axios.post(
          `${API_BASE_URL}/auth/token/refresh/`,
          { refresh: refreshToken }
        );
        
        const { access } = response.data;
        await AsyncStorage.setItem('access_token', access);
        
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Si el refresh falla, limpiar tokens y redirigir a login
        await AsyncStorage.multiRemove(['access_token', 'refresh_token', 'user']);
        // Emitir evento para que el contexto de auth maneje el logout
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;


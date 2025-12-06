// Configuración de la API
// Cambiar esta URL según el entorno (desarrollo/producción)
export const API_BASE_URL = __DEV__ 
  ? 'http://192.168.100.25:8000/api/mobile'  // Desarrollo - IP local configurada
  : 'https://studia-8dmp.onrender.com/api/mobile'; // Producción - Render.com

// Colores de la aplicación
export const COLORS = {
  primary: '#007bff',
  secondary: '#6c757d',
  success: '#28a745',
  danger: '#dc3545',
  warning: '#ffc107',
  info: '#17a2b8',
  light: '#f8f9fa',
  dark: '#343a40',
  white: '#ffffff',
  black: '#000000',
};

// Tamaños de fuente
export const FONT_SIZES = {
  small: 12,
  medium: 16,
  large: 20,
  xlarge: 24,
  xxlarge: 32,
};

// Espaciado
export const SPACING = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};


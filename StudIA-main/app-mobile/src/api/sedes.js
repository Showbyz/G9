import apiClient from './client';

export const getSedes = async () => {
  try {
    const response = await apiClient.get('/sedes/');
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.message || 'Error al cargar sedes' 
    };
  }
};


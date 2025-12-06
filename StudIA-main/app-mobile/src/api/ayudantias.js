import apiClient from './client';

export const getAyudantias = async (asignaturaId = null, page = 1) => {
  try {
    const params = { page };
    if (asignaturaId) {
      params.asignatura_id = asignaturaId;
    }
    
    const response = await apiClient.get('/ayudantias/', { params });
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.message || 'Error al cargar ayudantías' 
    };
  }
};

export const getAyudantia = async (id) => {
  try {
    const response = await apiClient.get(`/ayudantias/${id}/`);
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.message || 'Error al cargar ayudantía' 
    };
  }
};

export const inscribirse = async (ayudantiaId) => {
  try {
    console.log('[API Ayudantias] Iniciando inscripción para ayudantía:', ayudantiaId);
    console.log('[API Ayudantias] URL:', `/ayudantias/${ayudantiaId}/inscribirse/`);
    
    const response = await apiClient.post(`/ayudantias/${ayudantiaId}/inscribirse/`);
    console.log('[API Ayudantias] Respuesta del servidor:', response.status, response.data);
    
    if (response.data.success) {
      return { success: true, data: response.data };
    }
    return { success: false, error: response.data.message || 'Error al inscribirse' };
  } catch (error) {
    console.error('[API Ayudantias] Error completo:', error);
    console.error('[API Ayudantias] Error response:', error.response?.data);
    console.error('[API Ayudantias] Error status:', error.response?.status);
    
    let errorMessage = 'Error al inscribirse en la ayudantía';
    if (error.response?.data) {
      if (error.response.data.message) {
        errorMessage = error.response.data.message;
      } else if (error.response.data.error) {
        errorMessage = error.response.data.error;
      } else if (error.response.data.detail) {
        errorMessage = error.response.data.detail;
      }
    }
    
    return {
      success: false,
      error: errorMessage,
    };
  }
};


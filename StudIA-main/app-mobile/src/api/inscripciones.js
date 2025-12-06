import apiClient from './client';

export const getInscripciones = async (page = 1) => {
  try {
    const response = await apiClient.get('/inscripciones/', {
      params: { page },
    });
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.message || 'Error al cargar inscripciones' 
    };
  }
};

export const cancelarInscripcion = async (inscripcionId) => {
  try {
    console.log('[API Inscripciones] Iniciando cancelación para inscripción:', inscripcionId);
    console.log('[API Inscripciones] URL:', `/inscripciones/${inscripcionId}/cancelar/`);
    
    const response = await apiClient.post(`/inscripciones/${inscripcionId}/cancelar/`);
    console.log('[API Inscripciones] Respuesta del servidor:', response.status, response.data);
    
    if (response.data.success) {
      return { success: true, data: response.data };
    }
    return { success: false, error: response.data.message || 'Error al cancelar' };
  } catch (error) {
    console.error('[API Inscripciones] Error completo:', error);
    console.error('[API Inscripciones] Error response:', error.response?.data);
    console.error('[API Inscripciones] Error status:', error.response?.status);
    
    let errorMessage = 'Error al cancelar la inscripción';
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


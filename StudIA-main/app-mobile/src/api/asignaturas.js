import apiClient from './client';

export const getAsignaturas = async (page = 1) => {
  try {
    const response = await apiClient.get('/asignaturas/', {
      params: { page },
    });
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.message || 'Error al cargar asignaturas' 
    };
  }
};

export const getAsignatura = async (id) => {
  try {
    const response = await apiClient.get(`/asignaturas/${id}/`);
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.message || 'Error al cargar asignatura' 
    };
  }
};


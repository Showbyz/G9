import AsyncStorage from '@react-native-async-storage/async-storage';

// Constante del tenant (cambiar según el tenant que quieras usar)
// Opciones disponibles según verificación:
// - 'DUOC UC' (schema: DUOC UC, nombre: DUOC UC) - ⚠️ Tiene espacios
// - 'inacap' (schema: inacap, nombre: inacap) - ✅ Recomendado
// - 'asd' (schema: asd, nombre: dsa)
export const DEFAULT_TENANT = 'DUOC UC'; // Cambiar por el schema name de tu tenant

/**
 * Obtiene el tenant configurado
 */
export const getTenant = async () => {
  try {
    const tenant = await AsyncStorage.getItem('tenant_schema');
    return tenant || DEFAULT_TENANT;
  } catch (error) {
    console.error('Error al obtener tenant:', error);
    return DEFAULT_TENANT;
  }
};

/**
 * Guarda el tenant configurado
 */
export const setTenant = async (tenant) => {
  try {
    await AsyncStorage.setItem('tenant_schema', tenant);
    return true;
  } catch (error) {
    console.error('Error al guardar tenant:', error);
    return false;
  }
};


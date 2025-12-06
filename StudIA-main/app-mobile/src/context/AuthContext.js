import React, { createContext, useState, useEffect, useContext } from 'react';
import { login as apiLogin, logout as apiLogout, getStoredUser, isAuthenticated } from '../api/auth';

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const isAuth = await isAuthenticated();
      if (isAuth) {
        const storedUser = await getStoredUser();
        if (storedUser) {
          setUser(storedUser);
          setAuthenticated(true);
        }
      }
    } catch (error) {
      console.error('Error al verificar autenticación:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    console.log('[AuthContext] login llamado con email:', email);
    setLoading(true);
    try {
      console.log('[AuthContext] Llamando a apiLogin...');
      const result = await apiLogin(email, password);
      console.log('[AuthContext] Resultado de apiLogin:', result);
      
      if (result.success) {
        console.log('[AuthContext] Login exitoso, estableciendo usuario y autenticación');
        setUser(result.user);
        setAuthenticated(true);
        return { success: true };
      } else {
        console.log('[AuthContext] Login falló:', result.error);
        return { success: false, error: result.error || 'Credenciales incorrectas' };
      }
    } catch (error) {
      console.error('[AuthContext] Error capturado:', error);
      return { success: false, error: error.message || 'Error al iniciar sesión' };
    } finally {
      setLoading(false);
      console.log('[AuthContext] login finalizado');
    }
  };

  const logout = async () => {
    console.log('[AuthContext] logout llamado');
    setLoading(true);
    try {
      console.log('[AuthContext] Llamando a apiLogout...');
      await apiLogout();
      console.log('[AuthContext] apiLogout completado, limpiando estado');
      setUser(null);
      setAuthenticated(false);
      console.log('[AuthContext] Logout exitoso, authenticated = false');
      return { success: true };
    } catch (error) {
      console.error('[AuthContext] Error en logout:', error);
      console.error('[AuthContext] Stack trace:', error.stack);
      // Aún así, limpiar el estado local
      setUser(null);
      setAuthenticated(false);
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
      console.log('[AuthContext] logout finalizado');
    }
  };

  const value = {
    user,
    loading,
    authenticated,
    login,
    logout,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};


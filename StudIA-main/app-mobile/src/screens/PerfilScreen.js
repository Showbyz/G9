import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  Modal,
} from 'react-native';
import { useAuth } from '../context/AuthContext';
import { getProfile } from '../api/auth';
import { COLORS, SPACING, FONT_SIZES } from '../utils/constants';
import Icon from 'react-native-vector-icons/MaterialIcons';

const PerfilScreen = () => {
  const { user: contextUser, logout } = useAuth();
  const [user, setUser] = useState(contextUser);
  const [loading, setLoading] = useState(false);
  const [showLogoutModal, setShowLogoutModal] = useState(false);
  const [logoutLoading, setLogoutLoading] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    setLoading(true);
    const result = await getProfile();
    if (result.success) {
      setUser(result.data);
    }
    setLoading(false);
  };

  const handleLogout = () => {
    console.log('[PerfilScreen] handleLogout llamado');
    setShowLogoutModal(true);
  };

  const handleConfirmarLogout = async () => {
    console.log('[PerfilScreen] Confirmación de logout presionada');
    setShowLogoutModal(false);
    setLogoutLoading(true);
    try {
      const result = await logout();
      console.log('[PerfilScreen] Resultado de logout:', result);
      setLogoutLoading(false);
      if (!result.success) {
        Alert.alert('Error', result.error || 'Error al cerrar sesión');
      }
    } catch (error) {
      console.error('[PerfilScreen] Error en logout:', error);
      console.error('[PerfilScreen] Stack trace:', error.stack);
      setLogoutLoading(false);
      Alert.alert('Error', error.message || 'Error al cerrar sesión');
    }
  };

  const handleCancelarLogout = () => {
    console.log('[PerfilScreen] Logout cancelado');
    setShowLogoutModal(false);
  };

  if (loading && !user) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.header}>
          <View style={styles.avatarContainer}>
            <Icon name="person" size={60} color={COLORS.white} />
          </View>
          <Text style={styles.name}>{user?.nombre_usuario || 'Usuario'}</Text>
          <Text style={styles.email}>{user?.email || ''}</Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Información Personal</Text>
          
          <View style={styles.infoCard}>
            <View style={styles.infoRow}>
              <Icon name="person" size={20} color={COLORS.primary} />
              <View style={styles.infoContent}>
                <Text style={styles.infoLabel}>Nombre</Text>
                <Text style={styles.infoValue}>{user?.nombre_usuario || 'N/A'}</Text>
              </View>
            </View>
            
            <View style={styles.infoRow}>
              <Icon name="email" size={20} color={COLORS.primary} />
              <View style={styles.infoContent}>
                <Text style={styles.infoLabel}>Email</Text>
                <Text style={styles.infoValue}>{user?.email || 'N/A'}</Text>
              </View>
            </View>
            
            {user?.telefono && (
              <View style={styles.infoRow}>
                <Icon name="phone" size={20} color={COLORS.primary} />
                <View style={styles.infoContent}>
                  <Text style={styles.infoLabel}>Teléfono</Text>
                  <Text style={styles.infoValue}>{user.telefono}</Text>
                </View>
              </View>
            )}
            
            {user?.cargo && (
              <View style={styles.infoRow}>
                <Icon name="work" size={20} color={COLORS.primary} />
                <View style={styles.infoContent}>
                  <Text style={styles.infoLabel}>Cargo</Text>
                  <Text style={styles.infoValue}>{user.cargo}</Text>
                </View>
              </View>
            )}
          </View>
        </View>

        <View style={styles.section}>
          <TouchableOpacity style={styles.actionButton} onPress={loadProfile}>
            <Icon name="refresh" size={20} color={COLORS.primary} />
            <Text style={styles.actionButtonText}>Actualizar información</Text>
            <Icon name="chevron-right" size={20} color={COLORS.secondary} />
          </TouchableOpacity>
        </View>

        <View style={styles.section}>
          <TouchableOpacity
            style={[styles.actionButton, styles.logoutButton]}
            onPress={() => {
              console.log('[PerfilScreen] Botón de logout presionado directamente');
              handleLogout();
            }}
            activeOpacity={0.7}
          >
            <Icon name="logout" size={20} color={COLORS.danger} />
            <Text style={[styles.actionButtonText, styles.logoutButtonText]}>
              Cerrar sesión
            </Text>
            <Icon name="chevron-right" size={20} color={COLORS.secondary} />
          </TouchableOpacity>
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerText}>Portal de Ayudantías</Text>
          <Text style={styles.footerVersion}>Versión 1.0.0</Text>
        </View>
      </View>

      {/* Modal de confirmación de logout */}
      <Modal
        visible={showLogoutModal}
        transparent={true}
        animationType="fade"
        onRequestClose={handleCancelarLogout}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Cerrar sesión</Text>
            <Text style={styles.modalMessage}>
              ¿Estás seguro de que deseas cerrar sesión?
            </Text>
            <View style={styles.modalButtons}>
              <TouchableOpacity
                style={[styles.modalButton, styles.modalButtonCancel]}
                onPress={handleCancelarLogout}
                disabled={logoutLoading}
              >
                <Text style={styles.modalButtonTextCancel}>Cancelar</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.modalButton, styles.modalButtonConfirm]}
                onPress={handleConfirmarLogout}
                disabled={logoutLoading}
              >
                {logoutLoading ? (
                  <ActivityIndicator color={COLORS.white} />
                ) : (
                  <Text style={styles.modalButtonTextConfirm}>Cerrar sesión</Text>
                )}
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.light,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    padding: SPACING.md,
  },
  header: {
    alignItems: 'center',
    marginBottom: SPACING.xl,
    paddingTop: SPACING.lg,
  },
  avatarContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  name: {
    fontSize: FONT_SIZES.xlarge,
    fontWeight: 'bold',
    color: COLORS.dark,
    marginBottom: SPACING.xs,
  },
  email: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.secondary,
  },
  section: {
    marginBottom: SPACING.lg,
  },
  sectionTitle: {
    fontSize: FONT_SIZES.large,
    fontWeight: 'bold',
    color: COLORS.dark,
    marginBottom: SPACING.md,
  },
  infoCard: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  infoContent: {
    marginLeft: SPACING.md,
    flex: 1,
  },
  infoLabel: {
    fontSize: FONT_SIZES.small,
    color: COLORS.secondary,
  },
  infoValue: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.dark,
    fontWeight: '600',
    marginTop: 2,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    borderRadius: 12,
    marginBottom: SPACING.sm,
  },
  actionButtonText: {
    flex: 1,
    fontSize: FONT_SIZES.medium,
    color: COLORS.dark,
    marginLeft: SPACING.sm,
  },
  logoutButton: {
    borderWidth: 1,
    borderColor: COLORS.danger + '30',
  },
  logoutButtonText: {
    color: COLORS.danger,
    fontWeight: '600',
  },
  footer: {
    alignItems: 'center',
    marginTop: SPACING.xl,
    marginBottom: SPACING.xl,
  },
  footerText: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.secondary,
    fontWeight: '600',
  },
  footerVersion: {
    fontSize: FONT_SIZES.small,
    color: COLORS.secondary,
    marginTop: SPACING.xs,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.lg,
    width: '80%',
    maxWidth: 400,
  },
  modalTitle: {
    fontSize: FONT_SIZES.large,
    fontWeight: 'bold',
    color: COLORS.dark,
    marginBottom: SPACING.md,
    textAlign: 'center',
  },
  modalMessage: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.secondary,
    marginBottom: SPACING.lg,
    textAlign: 'center',
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: SPACING.md,
  },
  modalButton: {
    flex: 1,
    padding: SPACING.md,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 44,
  },
  modalButtonCancel: {
    backgroundColor: COLORS.light,
    borderWidth: 1,
    borderColor: COLORS.secondary,
  },
  modalButtonConfirm: {
    backgroundColor: COLORS.danger,
  },
  modalButtonTextCancel: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.dark,
    fontWeight: '600',
  },
  modalButtonTextConfirm: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.white,
    fontWeight: '600',
  },
});

export default PerfilScreen;


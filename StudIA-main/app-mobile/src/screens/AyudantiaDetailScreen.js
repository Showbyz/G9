import React, { useState } from 'react';
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
import { useRoute, useNavigation } from '@react-navigation/native';
import { inscribirse } from '../api/ayudantias';
import { COLORS, SPACING, FONT_SIZES } from '../utils/constants';
import Icon from 'react-native-vector-icons/MaterialIcons';

const AyudantiaDetailScreen = () => {
  const route = useRoute();
  const navigation = useNavigation();
  const { ayudantia: initialAyudantia, onInscripcionSuccess } = route.params || {};
  
  const [ayudantia, setAyudantia] = useState(initialAyudantia);
  const [loading, setLoading] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const handleInscribirse = async () => {
    console.log('[AyudantiaDetailScreen] handleInscribirse llamado');
    console.log('[AyudantiaDetailScreen] ayudantia:', ayudantia);
    console.log('[AyudantiaDetailScreen] esta_inscrito:', ayudantia.esta_inscrito);
    console.log('[AyudantiaDetailScreen] puede_inscribirse:', ayudantia.puede_inscribirse);
    
    if (ayudantia.esta_inscrito) {
      console.log('[AyudantiaDetailScreen] Ya está inscrito, mostrando alerta');
      Alert.alert('Ya estás inscrito', 'Ya te encuentras inscrito en esta ayudantía');
      return;
    }

    if (!ayudantia.puede_inscribirse) {
      console.log('[AyudantiaDetailScreen] No puede inscribirse, mostrando alerta');
      Alert.alert('No disponible', 'No puedes inscribirte en esta ayudantía');
      return;
    }

    console.log('[AyudantiaDetailScreen] Mostrando modal de confirmación');
    setShowConfirmModal(true);
  };

  const handleConfirmarInscripcion = async () => {
    console.log('[AyudantiaDetailScreen] Confirmación presionada, iniciando inscripción');
    setShowConfirmModal(false);
    setLoading(true);
    try {
      console.log('[AyudantiaDetailScreen] Llamando a inscribirse con id:', ayudantia.id_ayudantia);
      const result = await inscribirse(ayudantia.id_ayudantia);
      console.log('[AyudantiaDetailScreen] Resultado de inscribirse:', result);
      setLoading(false);

      if (result.success) {
        console.log('[AyudantiaDetailScreen] Inscripción exitosa');
        // Actualizar el estado inmediatamente para reflejar los cambios en la UI
        setAyudantia(prev => ({
          ...prev,
          esta_inscrito: true,
          puede_inscribirse: false,
          cupos_disponibles: Math.max(0, prev.cupos_disponibles - 1), // Decrementar cupos
        }));
        
        // Notificar a la pantalla anterior para que refresque
        if (onInscripcionSuccess) {
          onInscripcionSuccess();
        }
        
        Alert.alert('Éxito', result.data?.message || result.data?.data?.message || 'Te has inscrito exitosamente', [
          {
            text: 'OK',
            onPress: () => {
              console.log('[AyudantiaDetailScreen] Navegando hacia atrás');
              navigation.goBack();
            },
          },
        ]);
      } else {
        console.log('[AyudantiaDetailScreen] Error en inscripción:', result.error);
        Alert.alert('Error', result.error || 'Error al inscribirse');
      }
    } catch (error) {
      console.error('[AyudantiaDetailScreen] Excepción en inscripción:', error);
      console.error('[AyudantiaDetailScreen] Stack trace:', error.stack);
      setLoading(false);
      Alert.alert('Error', error.message || 'Error al inscribirse');
    }
  };

  const handleCancelarInscripcion = () => {
    console.log('[AyudantiaDetailScreen] Inscripción cancelada');
    setShowConfirmModal(false);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.header}>
          <View style={styles.iconContainer}>
            <Icon name="event" size={40} color={COLORS.primary} />
          </View>
          <Text style={styles.title}>{ayudantia.titulo}</Text>
          <Text style={styles.subtitle}>{ayudantia.asignatura_nombre}</Text>
        </View>

        {ayudantia.descripcion && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Descripción</Text>
            <Text style={styles.description}>{ayudantia.descripcion}</Text>
          </View>
        )}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Información</Text>
          <View style={styles.infoItem}>
            <Icon name="calendar-today" size={20} color={COLORS.primary} />
            <View style={styles.infoContent}>
              <Text style={styles.infoLabel}>Fecha</Text>
              <Text style={styles.infoValue}>{formatDate(ayudantia.fecha_str)}</Text>
            </View>
          </View>
          <View style={styles.infoItem}>
            <Icon name="access-time" size={20} color={COLORS.primary} />
            <View style={styles.infoContent}>
              <Text style={styles.infoLabel}>Horario</Text>
              <Text style={styles.infoValue}>{ayudantia.horario_str}</Text>
            </View>
          </View>
          <View style={styles.infoItem}>
            <Icon name="room" size={20} color={COLORS.primary} />
            <View style={styles.infoContent}>
              <Text style={styles.infoLabel}>Sala</Text>
              <Text style={styles.infoValue}>{ayudantia.sala}</Text>
            </View>
          </View>
          <View style={styles.infoItem}>
            <Icon name="timer" size={20} color={COLORS.primary} />
            <View style={styles.infoContent}>
              <Text style={styles.infoLabel}>Duración</Text>
              <Text style={styles.infoValue}>{ayudantia.duracion} minutos</Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Tutor</Text>
          <View style={styles.tutorCard}>
            <Icon name="person" size={24} color={COLORS.primary} />
            <View style={styles.tutorInfo}>
              <Text style={styles.tutorName}>{ayudantia.tutor_nombre}</Text>
              <Text style={styles.tutorEmail}>{ayudantia.tutor_email}</Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Cupos</Text>
          <View style={styles.cuposCard}>
            <View style={styles.cuposInfo}>
              <Text style={styles.cuposLabel}>Disponibles</Text>
              <Text style={[
                styles.cuposValue,
                ayudantia.cupos_disponibles === 0 && styles.cuposValueFull
              ]}>
                {ayudantia.cupos_disponibles} / {ayudantia.cupos_totales}
              </Text>
            </View>
            {ayudantia.cupos_disponibles === 0 && (
              <View style={styles.fullBadge}>
                <Text style={styles.fullBadgeText}>Sin cupos</Text>
              </View>
            )}
          </View>
        </View>

        {ayudantia.esta_inscrito ? (
          <View style={styles.inscritoCard}>
            <Icon name="check-circle" size={24} color={COLORS.success} />
            <Text style={styles.inscritoText}>Ya estás inscrito en esta ayudantía</Text>
          </View>
        ) : ayudantia.puede_inscribirse ? (
          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={() => {
              console.log('[AyudantiaDetailScreen] Botón presionado directamente');
              handleInscribirse();
            }}
            disabled={loading}
            activeOpacity={0.7}
          >
            {loading ? (
              <ActivityIndicator color={COLORS.white} />
            ) : (
              <>
                <Icon name="add-circle" size={20} color={COLORS.white} />
                <Text style={styles.buttonText}>Inscribirme</Text>
              </>
            )}
          </TouchableOpacity>
        ) : (
          <View style={styles.noDisponibleCard}>
            <Icon name="info" size={24} color={COLORS.warning} />
            <Text style={styles.noDisponibleText}>
              No puedes inscribirte en esta ayudantía
            </Text>
          </View>
        )}
      </View>

      {/* Modal de confirmación */}
      <Modal
        visible={showConfirmModal}
        transparent={true}
        animationType="fade"
        onRequestClose={handleCancelarInscripcion}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Confirmar inscripción</Text>
            <Text style={styles.modalMessage}>
              ¿Deseas inscribirte en "{ayudantia.titulo}"?
            </Text>
            <View style={styles.modalButtons}>
              <TouchableOpacity
                style={[styles.modalButton, styles.modalButtonCancel]}
                onPress={handleCancelarInscripcion}
              >
                <Text style={styles.modalButtonTextCancel}>Cancelar</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.modalButton, styles.modalButtonConfirm]}
                onPress={handleConfirmarInscripcion}
                disabled={loading}
              >
                {loading ? (
                  <ActivityIndicator color={COLORS.white} />
                ) : (
                  <Text style={styles.modalButtonTextConfirm}>Confirmar</Text>
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
  content: {
    padding: SPACING.md,
  },
  header: {
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  iconContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: COLORS.primary + '20',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: FONT_SIZES.xlarge,
    fontWeight: 'bold',
    color: COLORS.dark,
    textAlign: 'center',
    marginBottom: SPACING.xs,
  },
  subtitle: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.secondary,
    textAlign: 'center',
  },
  section: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.md,
  },
  sectionTitle: {
    fontSize: FONT_SIZES.large,
    fontWeight: 'bold',
    color: COLORS.dark,
    marginBottom: SPACING.md,
  },
  description: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.secondary,
    lineHeight: 22,
  },
  infoItem: {
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
  tutorCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.light,
    padding: SPACING.md,
    borderRadius: 8,
  },
  tutorInfo: {
    marginLeft: SPACING.md,
    flex: 1,
  },
  tutorName: {
    fontSize: FONT_SIZES.medium,
    fontWeight: 'bold',
    color: COLORS.dark,
  },
  tutorEmail: {
    fontSize: FONT_SIZES.small,
    color: COLORS.secondary,
    marginTop: 2,
  },
  cuposCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: COLORS.light,
    padding: SPACING.md,
    borderRadius: 8,
  },
  cuposInfo: {
    flex: 1,
  },
  cuposLabel: {
    fontSize: FONT_SIZES.small,
    color: COLORS.secondary,
  },
  cuposValue: {
    fontSize: FONT_SIZES.large,
    fontWeight: 'bold',
    color: COLORS.success,
    marginTop: 4,
  },
  cuposValueFull: {
    color: COLORS.danger,
  },
  fullBadge: {
    backgroundColor: COLORS.danger,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
    borderRadius: 12,
  },
  fullBadgeText: {
    color: COLORS.white,
    fontWeight: 'bold',
    fontSize: FONT_SIZES.small,
  },
  button: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    height: 50,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: SPACING.md,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: COLORS.white,
    fontSize: FONT_SIZES.medium,
    fontWeight: 'bold',
    marginLeft: SPACING.xs,
  },
  inscritoCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.success + '20',
    padding: SPACING.md,
    borderRadius: 12,
    marginTop: SPACING.md,
  },
  inscritoText: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.success,
    marginLeft: SPACING.sm,
    fontWeight: '600',
  },
  noDisponibleCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.warning + '20',
    padding: SPACING.md,
    borderRadius: 12,
    marginTop: SPACING.md,
  },
  noDisponibleText: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.warning,
    marginLeft: SPACING.sm,
    fontWeight: '600',
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
    backgroundColor: COLORS.primary,
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

export default AyudantiaDetailScreen;


import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  RefreshControl,
  ActivityIndicator,
  Alert,
  Modal,
} from 'react-native';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import { getInscripciones, cancelarInscripcion } from '../api/inscripciones';
import { COLORS, SPACING, FONT_SIZES } from '../utils/constants';
import Icon from 'react-native-vector-icons/MaterialIcons';

const MisInscripcionesScreen = () => {
  const navigation = useNavigation();
  const [inscripciones, setInscripciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [inscripcionACancelar, setInscripcionACancelar] = useState(null);
  const [cancelando, setCancelando] = useState(false);
  const [initialLoad, setInitialLoad] = useState(true);

  useEffect(() => {
    loadInscripciones();
    setInitialLoad(false);
  }, []);

  // Refrescar cuando la pantalla recibe foco (cuando se vuelve desde otra pestaña)
  useFocusEffect(
    React.useCallback(() => {
      // Solo refrescar si no es la carga inicial
      if (!initialLoad && !loading) {
        console.log('[MisInscripcionesScreen] Pantalla enfocada, refrescando inscripciones');
        loadInscripciones();
      }
    }, [initialLoad, loading])
  );

  const loadInscripciones = async () => {
    try {
      const result = await getInscripciones();
      if (result.success) {
        setInscripciones(result.data.results || []);
      } else {
        Alert.alert('Error', result.error || 'Error al cargar inscripciones');
      }
    } catch (error) {
      Alert.alert('Error', 'Error al conectar con el servidor');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadInscripciones();
  };

  const handleCancelar = (inscripcion) => {
    console.log('[MisInscripcionesScreen] handleCancelar llamado para:', inscripcion.id_inscripcion);
    setInscripcionACancelar(inscripcion);
    setShowCancelModal(true);
  };

  const handleConfirmarCancelar = async () => {
    if (!inscripcionACancelar) return;
    
    console.log('[MisInscripcionesScreen] Confirmación de cancelar presionada');
    setShowCancelModal(false);
    setCancelando(true);
    
    try {
      const result = await cancelarInscripcion(inscripcionACancelar.id_inscripcion);
      console.log('[MisInscripcionesScreen] Resultado de cancelar:', result);
      
      if (result.success) {
        // Actualizar el estado inmediatamente removiendo la inscripción cancelada
        setInscripciones(prev => prev.filter(ins => ins.id_inscripcion !== inscripcionACancelar.id_inscripcion));
        Alert.alert('Éxito', 'Inscripción cancelada exitosamente');
        // Recargar para asegurar que los datos estén actualizados
        loadInscripciones();
      } else {
        Alert.alert('Error', result.error || 'Error al cancelar inscripción');
      }
    } catch (error) {
      console.error('[MisInscripcionesScreen] Error en cancelar:', error);
      Alert.alert('Error', error.message || 'Error al cancelar inscripción');
    } finally {
      setCancelando(false);
      setInscripcionACancelar(null);
    }
  };

  const handleCancelarCancelar = () => {
    console.log('[MisInscripcionesScreen] Cancelación cancelada');
    setShowCancelModal(false);
    setInscripcionACancelar(null);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const renderInscripcion = ({ item }) => {
    const ayudantia = item.ayudantia;
    const fechaAyudantia = new Date(ayudantia.fecha_str);
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    const esProxima = fechaAyudantia >= hoy;

    return (
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <View style={styles.iconContainer}>
            <Icon name="event" size={24} color={COLORS.primary} />
          </View>
          <View style={styles.cardTitleContainer}>
            <Text style={styles.cardTitle}>{ayudantia.titulo}</Text>
            <Text style={styles.cardSubtitle}>{ayudantia.asignatura_nombre}</Text>
          </View>
        </View>

        <View style={styles.cardInfo}>
          <View style={styles.infoRow}>
            <Icon name="calendar-today" size={16} color={COLORS.secondary} />
            <Text style={styles.infoText}>
              {formatDate(ayudantia.fecha_str)} a las {ayudantia.horario_str}
            </Text>
          </View>
          <View style={styles.infoRow}>
            <Icon name="room" size={16} color={COLORS.secondary} />
            <Text style={styles.infoText}>{ayudantia.sala}</Text>
          </View>
          <View style={styles.infoRow}>
            <Icon name="person" size={16} color={COLORS.secondary} />
            <Text style={styles.infoText}>Tutor: {ayudantia.tutor_nombre}</Text>
          </View>
          <View style={styles.infoRow}>
            <Icon name="schedule" size={16} color={COLORS.secondary} />
            <Text style={styles.infoText}>
              Inscrito el {formatDate(item.fecha_inscripcion_str)} a las {formatTime(item.fecha_inscripcion_str)}
            </Text>
          </View>
        </View>

        <View style={styles.cardFooter}>
          {esProxima && (
            <View style={styles.badgeProxima}>
              <Icon name="notifications-active" size={14} color={COLORS.white} />
              <Text style={styles.badgeText}>Próxima</Text>
            </View>
          )}
          {item.asistio !== null && (
            <View style={[
              styles.badgeAsistencia,
              item.asistio ? styles.badgeAsistio : styles.badgeNoAsistio
            ]}>
              <Icon 
                name={item.asistio ? "check-circle" : "cancel"} 
                size={14} 
                color={COLORS.white} 
              />
              <Text style={styles.badgeText}>
                {item.asistio ? 'Asistió' : 'No asistió'}
              </Text>
            </View>
          )}
        </View>

        {esProxima && (
          <TouchableOpacity
            style={styles.cancelButton}
            onPress={() => {
              console.log('[MisInscripcionesScreen] Botón cancelar presionado directamente');
              handleCancelar(item);
            }}
            activeOpacity={0.7}
            disabled={cancelando}
          >
            <Icon name="cancel" size={18} color={COLORS.danger} />
            <Text style={styles.cancelButtonText}>Cancelar inscripción</Text>
          </TouchableOpacity>
        )}
      </View>
    );
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
        <Text style={styles.loadingText}>Cargando inscripciones...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={inscripciones}
        renderItem={renderInscripcion}
        keyExtractor={(item) => item.id_inscripcion.toString()}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Icon name="event-busy" size={64} color={COLORS.secondary} />
            <Text style={styles.emptyText}>No tienes inscripciones activas</Text>
            <Text style={styles.emptySubtext}>
              Inscríbete en ayudantías desde la sección de Asignaturas
            </Text>
          </View>
        }
      />

      {/* Modal de confirmación de cancelación */}
      <Modal
        visible={showCancelModal}
        transparent={true}
        animationType="fade"
        onRequestClose={handleCancelarCancelar}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Cancelar inscripción</Text>
            <Text style={styles.modalMessage}>
              ¿Estás seguro de cancelar tu inscripción en "{inscripcionACancelar?.ayudantia?.titulo}"?
            </Text>
            <View style={styles.modalButtons}>
              <TouchableOpacity
                style={[styles.modalButton, styles.modalButtonCancel]}
                onPress={handleCancelarCancelar}
                disabled={cancelando}
              >
                <Text style={styles.modalButtonTextCancel}>No</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.modalButton, styles.modalButtonConfirm]}
                onPress={handleConfirmarCancelar}
                disabled={cancelando}
              >
                {cancelando ? (
                  <ActivityIndicator color={COLORS.white} />
                ) : (
                  <Text style={styles.modalButtonTextConfirm}>Sí, cancelar</Text>
                )}
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
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
  loadingText: {
    marginTop: SPACING.md,
    color: COLORS.secondary,
    fontSize: FONT_SIZES.medium,
  },
  listContent: {
    padding: SPACING.md,
  },
  card: {
    backgroundColor: COLORS.white,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    shadowColor: COLORS.black,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: SPACING.sm,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: COLORS.primary + '20',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.sm,
  },
  cardTitleContainer: {
    flex: 1,
  },
  cardTitle: {
    fontSize: FONT_SIZES.large,
    fontWeight: 'bold',
    color: COLORS.dark,
  },
  cardSubtitle: {
    fontSize: FONT_SIZES.small,
    color: COLORS.secondary,
    marginTop: 2,
  },
  cardInfo: {
    marginBottom: SPACING.sm,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  infoText: {
    fontSize: FONT_SIZES.small,
    color: COLORS.dark,
    marginLeft: SPACING.xs,
  },
  cardFooter: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.xs,
    marginTop: SPACING.sm,
    paddingTop: SPACING.sm,
    borderTopWidth: 1,
    borderTopColor: COLORS.light,
  },
  badgeProxima: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.info,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: 12,
  },
  badgeAsistencia: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: 12,
  },
  badgeAsistio: {
    backgroundColor: COLORS.success,
  },
  badgeNoAsistio: {
    backgroundColor: COLORS.danger,
  },
  badgeText: {
    fontSize: FONT_SIZES.small,
    color: COLORS.white,
    marginLeft: SPACING.xs,
    fontWeight: '600',
  },
  cancelButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: SPACING.sm,
    padding: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.danger,
    borderRadius: 8,
  },
  cancelButtonText: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.danger,
    marginLeft: SPACING.xs,
    fontWeight: '600',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: SPACING.xl * 2,
  },
  emptyText: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.secondary,
    marginTop: SPACING.md,
    fontWeight: '600',
  },
  emptySubtext: {
    fontSize: FONT_SIZES.small,
    color: COLORS.secondary,
    marginTop: SPACING.xs,
    textAlign: 'center',
    paddingHorizontal: SPACING.lg,
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

export default MisInscripcionesScreen;


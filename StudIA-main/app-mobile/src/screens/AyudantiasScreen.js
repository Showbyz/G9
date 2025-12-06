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
} from 'react-native';
import { useRoute, useNavigation, useFocusEffect } from '@react-navigation/native';
import { getAyudantias } from '../api/ayudantias';
import { COLORS, SPACING, FONT_SIZES } from '../utils/constants';
import Icon from 'react-native-vector-icons/MaterialIcons';

const AyudantiasScreen = () => {
  const route = useRoute();
  const navigation = useNavigation();
  const { asignaturaId } = route.params || {};
  
  const [ayudantias, setAyudantias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [initialLoad, setInitialLoad] = useState(true);

  useEffect(() => {
    loadAyudantias();
    setInitialLoad(false);
  }, [asignaturaId]);

  // Refrescar cuando la pantalla recibe foco (cuando se vuelve desde el detalle)
  useFocusEffect(
    React.useCallback(() => {
      // Solo refrescar si no es la carga inicial
      if (!initialLoad && !loading) {
        loadAyudantias();
      }
    }, [initialLoad, loading])
  );

  const loadAyudantias = async () => {
    try {
      const result = await getAyudantias(asignaturaId);
      if (result.success) {
        setAyudantias(result.data.results || []);
      } else {
        Alert.alert('Error', result.error || 'Error al cargar ayudantías');
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
    loadAyudantias();
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const renderAyudantia = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => navigation.navigate('AyudantiaDetail', { 
        ayudantia: item,
        onInscripcionSuccess: () => {
          // Refrescar la lista cuando se completa una inscripción
          loadAyudantias();
        }
      })}
      activeOpacity={0.7}
    >
      <View style={styles.cardHeader}>
        <View style={styles.iconContainer}>
          <Icon name="event" size={24} color={COLORS.primary} />
        </View>
        <View style={styles.cardTitleContainer}>
          <Text style={styles.cardTitle}>{item.titulo}</Text>
          <Text style={styles.cardSubtitle}>{item.asignatura_nombre}</Text>
        </View>
      </View>

      {item.descripcion ? (
        <Text style={styles.cardDescription} numberOfLines={2}>
          {item.descripcion}
        </Text>
      ) : null}

      <View style={styles.cardInfo}>
        <View style={styles.infoRow}>
          <Icon name="calendar-today" size={16} color={COLORS.secondary} />
          <Text style={styles.infoText}>{formatDate(item.fecha_str)}</Text>
        </View>
        <View style={styles.infoRow}>
          <Icon name="access-time" size={16} color={COLORS.secondary} />
          <Text style={styles.infoText}>{item.horario_str}</Text>
        </View>
        <View style={styles.infoRow}>
          <Icon name="room" size={16} color={COLORS.secondary} />
          <Text style={styles.infoText}>{item.sala}</Text>
        </View>
      </View>

      <View style={styles.cardFooter}>
        <View style={styles.cuposContainer}>
          <Icon 
            name={item.cupos_disponibles > 0 ? "people" : "people-outline"} 
            size={16} 
            color={item.cupos_disponibles > 0 ? COLORS.success : COLORS.danger} 
          />
          <Text style={[
            styles.cuposText,
            item.cupos_disponibles === 0 && styles.cuposTextFull
          ]}>
            {item.cupos_disponibles} cupos disponibles
          </Text>
        </View>
        {item.esta_inscrito && (
          <View style={styles.badgeInscrito}>
            <Text style={styles.badgeText}>Inscrito</Text>
          </View>
        )}
        {item.puede_inscribirse && !item.esta_inscrito && (
          <View style={styles.badgeDisponible}>
            <Text style={styles.badgeText}>Disponible</Text>
          </View>
        )}
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
        <Text style={styles.loadingText}>Cargando ayudantías...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={ayudantias}
        renderItem={renderAyudantia}
        keyExtractor={(item) => item.id_ayudantia.toString()}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Icon name="event-busy" size={64} color={COLORS.secondary} />
            <Text style={styles.emptyText}>No hay ayudantías disponibles</Text>
          </View>
        }
      />
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
  cardDescription: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.secondary,
    marginBottom: SPACING.sm,
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
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: SPACING.sm,
    paddingTop: SPACING.sm,
    borderTopWidth: 1,
    borderTopColor: COLORS.light,
  },
  cuposContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  cuposText: {
    fontSize: FONT_SIZES.small,
    color: COLORS.success,
    marginLeft: SPACING.xs,
    fontWeight: '600',
  },
  cuposTextFull: {
    color: COLORS.danger,
  },
  badgeInscrito: {
    backgroundColor: COLORS.info,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: 12,
  },
  badgeDisponible: {
    backgroundColor: COLORS.success + '20',
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: 12,
  },
  badgeText: {
    fontSize: FONT_SIZES.small,
    color: COLORS.white,
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
  },
});

export default AyudantiasScreen;


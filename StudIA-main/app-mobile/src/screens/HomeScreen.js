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
import { useNavigation } from '@react-navigation/native';
import { getAsignaturas } from '../api/asignaturas';
import { COLORS, SPACING, FONT_SIZES } from '../utils/constants';
import Icon from 'react-native-vector-icons/MaterialIcons';

const HomeScreen = () => {
  const navigation = useNavigation();
  const [asignaturas, setAsignaturas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [nextPage, setNextPage] = useState(null);

  useEffect(() => {
    loadAsignaturas();
  }, []);

  const loadAsignaturas = async (page = 1, append = false) => {
    try {
      const result = await getAsignaturas(page);
      if (result.success) {
        const newAsignaturas = result.data.results || [];
        setAsignaturas(append ? [...asignaturas, ...newAsignaturas] : newAsignaturas);
        setNextPage(result.data.next ? page + 1 : null);
      } else {
        Alert.alert('Error', result.error || 'Error al cargar asignaturas');
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
    loadAsignaturas(1, false);
  };

  const loadMore = () => {
    if (nextPage && !loading) {
      loadAsignaturas(nextPage, true);
    }
  };

  const renderAsignatura = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => navigation.navigate('Ayudantias', { asignaturaId: item.id_asignatura })}
      activeOpacity={0.7}
    >
      <View style={styles.cardHeader}>
        <Icon name="book" size={24} color={COLORS.primary} />
        <View style={styles.cardTitleContainer}>
          <Text style={styles.cardTitle}>{item.nombre}</Text>
          <Text style={styles.cardCode}>{item.codigo}</Text>
        </View>
      </View>
      
      {item.descripcion ? (
        <Text style={styles.cardDescription} numberOfLines={2}>
          {item.descripcion}
        </Text>
      ) : null}
      
      <View style={styles.cardFooter}>
        <View style={styles.badge}>
          <Icon name="event-available" size={16} color={COLORS.success} />
          <Text style={styles.badgeText}>
            {item.total_ayudantias_disponibles} ayudantías
          </Text>
        </View>
        <Icon name="chevron-right" size={24} color={COLORS.secondary} />
      </View>
    </TouchableOpacity>
  );

  if (loading && asignaturas.length === 0) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
        <Text style={styles.loadingText}>Cargando asignaturas...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={asignaturas}
        renderItem={renderAsignatura}
        keyExtractor={(item) => item.id_asignatura.toString()}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        onEndReached={loadMore}
        onEndReachedThreshold={0.5}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Icon name="menu-book" size={64} color={COLORS.secondary} />
            <Text style={styles.emptyText}>No hay asignaturas disponibles</Text>
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
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  cardTitleContainer: {
    flex: 1,
    marginLeft: SPACING.sm,
  },
  cardTitle: {
    fontSize: FONT_SIZES.large,
    fontWeight: 'bold',
    color: COLORS.dark,
  },
  cardCode: {
    fontSize: FONT_SIZES.small,
    color: COLORS.secondary,
    marginTop: 2,
  },
  cardDescription: {
    fontSize: FONT_SIZES.medium,
    color: COLORS.secondary,
    marginBottom: SPACING.sm,
  },
  cardFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: SPACING.sm,
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.success + '20',
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: 12,
  },
  badgeText: {
    fontSize: FONT_SIZES.small,
    color: COLORS.success,
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
  },
});

export default HomeScreen;


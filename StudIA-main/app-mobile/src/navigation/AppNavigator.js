import React, { useEffect } from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { ActivityIndicator, View } from 'react-native';
import { useAuth } from '../context/AuthContext';
import { COLORS } from '../utils/constants';
import Icon from 'react-native-vector-icons/MaterialIcons';

// Screens
import LoginScreen from '../screens/LoginScreen';
import HomeScreen from '../screens/HomeScreen';
import AyudantiasScreen from '../screens/AyudantiasScreen';
import MisInscripcionesScreen from '../screens/MisInscripcionesScreen';
import PerfilScreen from '../screens/PerfilScreen';
import AyudantiaDetailScreen from '../screens/AyudantiaDetailScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

const MainTabs = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Home') {
            iconName = 'menu-book';
          } else if (route.name === 'Inscripciones') {
            iconName = 'event';
          } else if (route.name === 'Perfil') {
            iconName = 'person';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.secondary,
        headerStyle: {
          backgroundColor: COLORS.primary,
        },
        headerTintColor: COLORS.white,
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      })}
    >
      <Tab.Screen 
        name="Home" 
        component={HomeScreen} 
        options={{ title: 'Asignaturas' }}
      />
      <Tab.Screen 
        name="Inscripciones" 
        component={MisInscripcionesScreen}
        options={{ title: 'Mis Inscripciones' }}
      />
      <Tab.Screen 
        name="Perfil" 
        component={PerfilScreen}
        options={{ title: 'Mi Perfil' }}
      />
    </Tab.Navigator>
  );
};

const AppNavigator = () => {
  const { authenticated, loading } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  // Usar key para forzar re-render cuando cambie authenticated
  return (
    <Stack.Navigator 
      key={authenticated ? 'authenticated' : 'unauthenticated'}
      screenOptions={{ headerShown: false }}
    >
      {authenticated ? (
        <>
          <Stack.Screen name="MainTabs" component={MainTabs} />
          <Stack.Screen 
            name="Ayudantias" 
            component={AyudantiasScreen}
            options={{
              headerShown: true,
              title: 'Ayudantías',
              headerStyle: { backgroundColor: COLORS.primary },
              headerTintColor: COLORS.white,
            }}
          />
          <Stack.Screen 
            name="AyudantiaDetail" 
            component={AyudantiaDetailScreen}
            options={{
              headerShown: true,
              title: 'Detalle Ayudantía',
              headerStyle: { backgroundColor: COLORS.primary },
              headerTintColor: COLORS.white,
            }}
          />
        </>
      ) : (
        <Stack.Screen name="Login" component={LoginScreen} />
      )}
    </Stack.Navigator>
  );
};

export default AppNavigator;


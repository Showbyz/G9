# ✅ Solución: Ayudantías no visibles y Logout no funciona

## 🔍 Problemas Identificados

### Problema 1: Ayudantías no se ven en la app móvil
**Causa:** Los ViewSets (`AsignaturaViewSet`, `AyudantiaViewSet`, `InscripcionViewSet`, `SedeViewSet`, `PerfilView`) no estaban usando `schema_context`, por lo que consultaban en el schema público en lugar del schema del tenant.

### Problema 2: Botón de cerrar sesión no funciona
**Causa:** React Navigation no se re-renderiza automáticamente cuando cambia el estado `authenticated` del contexto. El `AppNavigator` usa `authenticated` para decidir qué pantallas mostrar, pero cuando cambia, React Navigation no actualiza automáticamente.

## ✅ Soluciones Aplicadas

### 1. Ayudantías - Uso de `schema_context` en ViewSets

**Archivo:** `api_mobile/views.py`

Se envolvieron todos los querysets y operaciones de base de datos en `schema_context`:

- ✅ `AsignaturaViewSet.get_queryset()`: Envuelto en `schema_context`
- ✅ `AyudantiaViewSet.get_queryset()`: Envuelto en `schema_context`
- ✅ `InscripcionViewSet.get_queryset()`: Envuelto en `schema_context`
- ✅ `InscripcionViewSet.create()`: Envuelto en `schema_context`
- ✅ `InscripcionViewSet.cancelar()`: Envuelto en `schema_context`
- ✅ `AyudantiaViewSet.inscribirse()`: Envuelto en `schema_context`
- ✅ `SedeViewSet.get_queryset()`: Envuelto en `schema_context`
- ✅ `PerfilView.get()`: Envuelto en `schema_context`

**Ejemplo de cambio:**
```python
def get_queryset(self):
    from django_tenants.utils import schema_context
    
    if hasattr(self.request, 'tenant'):
        with schema_context(self.request.tenant.schema_name):
            return Asignatura.objects.filter(...)
    else:
        return Asignatura.objects.none()
```

### 2. Logout - Forzar re-render de React Navigation

**Archivo:** `app-mobile/src/navigation/AppNavigator.js`

Se agregó una `key` prop al `Stack.Navigator` que cambia cuando cambia el estado de autenticación, forzando un re-render completo:

```javascript
<Stack.Navigator 
  key={authenticated ? 'authenticated' : 'unauthenticated'}
  screenOptions={{ headerShown: false }}
>
```

**Archivo:** `app-mobile/src/context/AuthContext.js`

Se agregaron logs de depuración para el logout:

```javascript
const logout = async () => {
  setLoading(true);
  try {
    await apiLogout();
    setUser(null);
    setAuthenticated(false);
    console.log('[AuthContext] Logout exitoso, authenticated = false');
    return { success: true };
  } catch (error) {
    console.error('[AuthContext] Error en logout:', error);
    // Aún así, limpiar el estado local
    setUser(null);
    setAuthenticated(false);
    return { success: false, error: error.message };
  } finally {
    setLoading(false);
  }
};
```

## 🔄 Próximos Pasos

1. **Reinicia Django** (si no se reinició automáticamente):
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Recarga la app móvil** (si no se recargó automáticamente):
   - Presiona `r` en la terminal de Expo para recargar
   - O agita el dispositivo y selecciona "Reload"

## 🧪 Probar Ahora

### Test 1: Ver Ayudantías
1. **Crea una ayudantía en el portal web** (como admin/tutor)
2. **Abre la app móvil** y ve a la pestaña "Asignaturas"
3. **Deberías ver:**
   - ✅ La asignatura con la ayudantía creada
   - ✅ Al tocar la asignatura, ver las ayudantías disponibles

### Test 2: Logout
1. **En la app móvil**, ve a la pestaña "Perfil"
2. **Toca "Cerrar sesión"**
3. **Confirma** en el diálogo
4. **Deberías ver:**
   - ✅ La pantalla de login aparece inmediatamente
   - ✅ Los tokens se eliminan del almacenamiento
   - ✅ El estado `authenticated` se actualiza a `false`

## 📋 Logs Esperados

### Django (al listar ayudantías):
```
[API Mobile] Petición recibida: GET /api/mobile/asignaturas/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[21/Nov/2025 XX:XX:XX] "GET /api/mobile/asignaturas/ HTTP/1.1" 200 XX
```

### App Móvil (al hacer logout):
```
[AuthContext] Logout exitoso, authenticated = false
```

---

**¡Reinicia Django y recarga la app móvil para probar los cambios!** 🚀


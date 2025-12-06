# ✅ Solución: Error 500 al obtener asignaturas

## 🔍 Problema Identificado

**Error:** `GET http://192.168.100.25:8000/api/mobile/asignaturas/?page=1 500 (Internal Server Error)`

**Causa:** Cuando DRF intenta paginar el queryset, el `schema_context` ya se cerró porque el `with` statement terminó en `get_queryset()`. La paginación necesita acceder a la base de datos, pero el schema ya no está establecido.

## ✅ Solución Aplicada

**Archivo:** `api_mobile/views.py`

Se sobrescribió el método `list()` en todos los ViewSets para asegurar que el `schema_context` esté activo durante toda la operación de listado, incluyendo la paginación:

- ✅ `AsignaturaViewSet.list()`: Envuelto en `schema_context`
- ✅ `AyudantiaViewSet.list()`: Envuelto en `schema_context`
- ✅ `InscripcionViewSet.list()`: Envuelto en `schema_context`
- ✅ `SedeViewSet.list()`: Envuelto en `schema_context`

**Ejemplo de cambio:**
```python
def list(self, request, *args, **kwargs):
    """Sobrescribir list para asegurar que el schema_context esté activo"""
    from django_tenants.utils import schema_context
    
    if hasattr(request, 'tenant'):
        with schema_context(request.tenant.schema_name):
            return super().list(request, *args, **kwargs)
    else:
        return Response({
            'success': False,
            'error': 'No se pudo identificar el tenant'
        }, status=status.HTTP_400_BAD_REQUEST)
```

### Bonus: Corrección de icono

**Archivo:** `app-mobile/src/navigation/AppNavigator.js`

Se cambió el icono `'book'` por `'menu-book'` para evitar el warning:
```
"book-outline" is not a valid icon name for family "material"
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

1. **Abre la app móvil** y ve a la pestaña "Asignaturas"
2. **Deberías ver:**
   - ✅ Las asignaturas se cargan correctamente
   - ✅ No hay error 500
   - ✅ La paginación funciona si hay más de 20 asignaturas
   - ✅ El icono "book" se muestra correctamente (sin warnings)

## 📋 Logs Esperados

### Django (al listar asignaturas):
```
[API Mobile] Petición recibida: GET /api/mobile/asignaturas/
[API Mobile] Header X-Tenant-Schema: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[21/Nov/2025 XX:XX:XX] "GET /api/mobile/asignaturas/?page=1 HTTP/1.1" 200 XX
```

### App Móvil (en la consola):
```
[APP] Petición configurada: GET /asignaturas/
[APP] Headers: { ... }
```

**Sin errores 500** ✅

---

**¡Reinicia Django y recarga la app móvil para probar los cambios!** 🚀


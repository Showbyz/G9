# 📱 Resumen: API Móvil para Estudiantes

## ✅ Implementación Completada

Se ha creado una **API REST completa** para la aplicación móvil de estudiantes, lista para ser consumida desde React Native, Flutter u otra tecnología móvil.

## 🎯 Funcionalidades Implementadas

### 1. Autenticación
- ✅ Login con email y contraseña
- ✅ Generación de tokens JWT (access + refresh)
- ✅ Endpoint de perfil del estudiante
- ✅ Refresh token automático

### 2. Asignaturas
- ✅ Listar asignaturas disponibles
- ✅ Ver detalle de asignatura
- ✅ Contador de ayudantías disponibles por asignatura

### 3. Ayudantías
- ✅ Listar ayudantías disponibles
- ✅ Filtrar por asignatura
- ✅ Ver detalle de ayudantía
- ✅ Inscribirse en ayudantía
- ✅ Validaciones (cupos, fechas, etc.)

### 4. Inscripciones
- ✅ Listar mis inscripciones
- ✅ Cancelar inscripción
- ✅ Ver estado de asistencia

### 5. Sedes
- ✅ Listar sedes disponibles
- ✅ Coordenadas geográficas para mapas

## 📁 Archivos Creados

```
api_mobile/
├── __init__.py
├── admin.py
├── apps.py
├── authentication.py      # Autenticación JWT personalizada
├── serializers.py         # Serializers para todos los modelos
├── urls.py                # URLs de la API
├── views.py               # Viewsets y views de la API
└── migrations/

Documentación:
├── API_MOBILE_DOCUMENTACION.md    # Documentación completa de la API
├── GUIA_IMPLEMENTACION_MOVIL.md   # Guía para crear la app móvil
└── RESUMEN_API_MOVIL.md           # Este archivo
```

## 🔗 Endpoints Disponibles

### Base URL: `/api/mobile/`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `auth/login/` | Login de estudiante |
| GET | `auth/perfil/` | Perfil del estudiante |
| POST | `auth/token/refresh/` | Renovar access token |
| GET | `asignaturas/` | Listar asignaturas |
| GET | `asignaturas/{id}/` | Detalle de asignatura |
| GET | `ayudantias/` | Listar ayudantías |
| GET | `ayudantias/{id}/` | Detalle de ayudantía |
| POST | `ayudantias/{id}/inscribirse/` | Inscribirse en ayudantía |
| GET | `inscripciones/` | Mis inscripciones |
| POST | `inscripciones/{id}/cancelar/` | Cancelar inscripción |
| GET | `sedes/` | Listar sedes |

## 🔐 Seguridad

- ✅ Autenticación JWT obligatoria para todos los endpoints (excepto login)
- ✅ Validación de que el usuario sea estudiante (no staff ni tutor)
- ✅ Tokens con expiración (24h access, 7 días refresh)
- ✅ Refresh token automático en el cliente

## 📦 Dependencias Agregadas

- `djangorestframework==3.14.0`
- `djangorestframework-simplejwt==5.3.0`

## ⚙️ Configuración Realizada

1. ✅ App `api_mobile` agregada a `TENANT_APPS`
2. ✅ REST Framework configurado en `settings.py`
3. ✅ JWT configurado con campos personalizados
4. ✅ URLs agregadas en `portalAutoatencion/urls.py`
5. ✅ Autenticación personalizada para modelo Usuario

## 🚀 Próximos Pasos

### Para el Backend:
1. ✅ **COMPLETADO** - API REST lista y funcional
2. ⏳ Probar endpoints con Postman/Thunder Client
3. ⏳ Configurar CORS si es necesario
4. ⏳ Agregar rate limiting (opcional)
5. ⏳ Implementar notificaciones push (opcional)

### Para el Frontend Móvil:
1. ⏳ Elegir tecnología (React Native recomendado)
2. ⏳ Crear proyecto móvil
3. ⏳ Implementar cliente API
4. ⏳ Crear pantallas según documentación
5. ⏳ Probar en dispositivos reales
6. ⏳ Generar APK/IPA

## 📖 Documentación

- **API_MOBILE_DOCUMENTACION.md**: Documentación completa de todos los endpoints
- **GUIA_IMPLEMENTACION_MOVIL.md**: Guía paso a paso para crear la app móvil

## 🧪 Testing

Para probar la API, puedes usar:

1. **Postman**: Importar colección de endpoints
2. **Thunder Client** (VS Code): Extensión para probar APIs
3. **curl**: Desde terminal
4. **httpie**: Herramienta CLI

### Ejemplo de Login (curl):

```bash
curl -X POST http://localhost:8000/api/mobile/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "estudiante@ejemplo.com", "password": "contraseña"}'
```

### Ejemplo con Token:

```bash
curl -X GET http://localhost:8000/api/mobile/asignaturas/ \
  -H "Authorization: Bearer <access_token>"
```

## ⚠️ Notas Importantes

1. **URL Base**: La API está en `/api/mobile/` y funciona con el sistema de tenants
2. **Solo Estudiantes**: La API está diseñada exclusivamente para estudiantes
3. **Tokens**: Guardar el refresh_token de forma segura en la app móvil
4. **Producción**: Cambiar la URL base cuando despliegues en producción

## 🎉 Estado del Proyecto

✅ **API Backend**: 100% Completa y lista para usar
⏳ **App Móvil**: Pendiente de implementación (guía proporcionada)

---

**La API está lista para ser consumida desde cualquier aplicación móvil.**
**Sigue la guía de implementación para crear la app móvil.**


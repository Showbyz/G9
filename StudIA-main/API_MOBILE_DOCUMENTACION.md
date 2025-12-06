# Documentación API Móvil - Portal de Ayudantías

## 📱 Descripción General

Esta API REST está diseñada específicamente para la aplicación móvil de estudiantes. Permite a los estudiantes:
- Autenticarse con email y contraseña
- Ver asignaturas disponibles
- Ver ayudantías disponibles
- Inscribirse en ayudantías
- Ver sus inscripciones
- Cancelar inscripciones
- Ver sedes disponibles

## 🔐 Autenticación

La API utiliza **JWT (JSON Web Tokens)** para autenticación.

### Endpoint de Login

**POST** `/api/mobile/auth/login/`

**Body:**
```json
{
    "email": "estudiante@ejemplo.com",
    "password": "contraseña123"
}
```

**Respuesta Exitosa (200):**
```json
{
    "success": true,
    "message": "Login exitoso",
    "user": {
        "id_usuario": 1,
        "nombre_usuario": "Juan Pérez",
        "email": "estudiante@ejemplo.com",
        "telefono": 123456789,
        "cargo": "Estudiante"
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

**Respuesta de Error (400):**
```json
{
    "success": false,
    "errors": {
        "non_field_errors": ["Email o contraseña incorrectos."]
    }
}
```

### Uso de Tokens

Una vez obtenido el token, inclúyelo en todas las peticiones en el header:

```
Authorization: Bearer <access_token>
```

**Nota:** El `access_token` expira en 24 horas. Usa el `refresh_token` para obtener un nuevo `access_token`.

## 📚 Endpoints Disponibles

### 1. Perfil del Estudiante

**GET** `/api/mobile/auth/perfil/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Respuesta (200):**
```json
{
    "success": true,
    "data": {
        "id_usuario": 1,
        "nombre_usuario": "Juan Pérez",
        "email": "estudiante@ejemplo.com",
        "telefono": 123456789,
        "cargo": "Estudiante"
    }
}
```

---

### 2. Listar Asignaturas

**GET** `/api/mobile/asignaturas/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Respuesta (200):**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id_asignatura": 1,
            "nombre": "Matemáticas",
            "codigo": "MAT101",
            "carrera": "Ingeniería",
            "descripcion": "Curso de matemáticas básicas",
            "total_ayudantias_disponibles": 3
        },
        ...
    ]
}
```

**Query Parameters:**
- `page`: Número de página (paginación)
- `page_size`: Tamaño de página (default: 20)

---

### 3. Detalle de Asignatura

**GET** `/api/mobile/asignaturas/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Respuesta (200):**
```json
{
    "id_asignatura": 1,
    "nombre": "Matemáticas",
    "codigo": "MAT101",
    "carrera": "Ingeniería",
    "descripcion": "Curso de matemáticas básicas",
    "total_ayudantias_disponibles": 3
}
```

---

### 4. Listar Ayudantías

**GET** `/api/mobile/ayudantias/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `asignatura_id`: Filtrar por asignatura (opcional)
- `page`: Número de página

**Respuesta (200):**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id_ayudantia": 1,
            "titulo": "Repaso de Álgebra",
            "descripcion": "Repaso de conceptos básicos de álgebra",
            "sala": "A-101",
            "fecha": "2025-01-15",
            "fecha_str": "2025-01-15",
            "horario": "14:00:00",
            "horario_str": "14:00",
            "duracion": 60,
            "cupos_totales": 20,
            "cupos_disponibles": 15,
            "asignatura_nombre": "Matemáticas",
            "asignatura_codigo": "MAT101",
            "tutor_nombre": "Prof. García",
            "tutor_email": "tutor@ejemplo.com",
            "puede_inscribirse": true,
            "esta_inscrito": false
        },
        ...
    ]
}
```

---

### 5. Detalle de Ayudantía

**GET** `/api/mobile/ayudantias/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Respuesta (200):** (Mismo formato que el item en la lista)

---

### 6. Inscribirse en Ayudantía

**POST** `/api/mobile/ayudantias/{id}/inscribirse/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:** (vacío)

**Respuesta Exitosa (201):**
```json
{
    "success": true,
    "message": "Te has inscrito exitosamente en la ayudantía: Repaso de Álgebra",
    "data": {
        "id_inscripcion": 1,
        "ayudantia": {...},
        "estudiante_nombre": "Juan Pérez",
        "fecha_inscripcion": "2025-01-10T10:30:00Z",
        "fecha_inscripcion_str": "2025-01-10 10:30",
        "estado": "activa",
        "asistio": false
    }
}
```

**Errores Posibles:**
- `400`: Ya estás inscrito / No hay cupos / Ayudantía ya pasó / Ya fue cursada

---

### 7. Listar Mis Inscripciones

**GET** `/api/mobile/inscripciones/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Respuesta (200):**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id_inscripcion": 1,
            "ayudantia": {
                "id_ayudantia": 1,
                "titulo": "Repaso de Álgebra",
                "fecha_str": "2025-01-15",
                "horario_str": "14:00",
                "sala": "A-101",
                ...
            },
            "estudiante_nombre": "Juan Pérez",
            "fecha_inscripcion": "2025-01-10T10:30:00Z",
            "fecha_inscripcion_str": "2025-01-10 10:30",
            "estado": "activa",
            "asistio": false
        },
        ...
    ]
}
```

---

### 8. Cancelar Inscripción

**POST** `/api/mobile/inscripciones/{id}/cancelar/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:** (vacío)

**Respuesta Exitosa (200):**
```json
{
    "success": true,
    "message": "Inscripción cancelada exitosamente."
}
```

---

### 9. Listar Sedes

**GET** `/api/mobile/sedes/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Respuesta (200):**
```json
{
    "count": 12,
    "next": null,
    "previous": null,
    "results": [
        {
            "id_sede": 1,
            "nombre": "Sede Alameda",
            "direccion": "Av. España 8, Santiago Centro",
            "latitud": -33.44885,
            "longitud": -70.66872
        },
        ...
    ]
}
```

---

## 🔄 Refresh Token

Para renovar el access token cuando expire:

**POST** `/api/mobile/auth/token/refresh/` (endpoint de DRF Simple JWT)

**Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Respuesta (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## ⚠️ Códigos de Estado HTTP

- `200 OK`: Petición exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Error en los datos enviados
- `401 Unauthorized`: Token inválido o expirado
- `403 Forbidden`: No tienes permisos (ej: no eres estudiante)
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

---

## 📝 Notas Importantes

1. **Solo Estudiantes**: Esta API está diseñada exclusivamente para estudiantes. Los usuarios con rol de staff o tutor no pueden acceder.

2. **Tokens**: Guarda el `refresh_token` de forma segura. Úsalo para renovar el `access_token` cuando expire.

3. **Paginación**: Los endpoints de listado usan paginación. Por defecto, 20 items por página.

4. **Filtros**: Algunos endpoints aceptan query parameters para filtrar resultados.

5. **Base URL**: Asegúrate de usar la URL correcta según el entorno:
   - Desarrollo: `http://localhost:8000/api/mobile/`
   - Producción: `https://tu-dominio.com/api/mobile/`

---

## 🧪 Ejemplo de Uso Completo

```javascript
// 1. Login
const loginResponse = await fetch('http://localhost:8000/api/mobile/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        email: 'estudiante@ejemplo.com',
        password: 'contraseña123'
    })
});

const { tokens, user } = await loginResponse.json();
const accessToken = tokens.access;

// 2. Obtener asignaturas
const asignaturasResponse = await fetch('http://localhost:8000/api/mobile/asignaturas/', {
    headers: {
        'Authorization': `Bearer ${accessToken}`
    }
});

const asignaturas = await asignaturasResponse.json();

// 3. Inscribirse en ayudantía
const inscripcionResponse = await fetch('http://localhost:8000/api/mobile/ayudantias/1/inscribirse/', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${accessToken}`
    }
});

const inscripcion = await inscripcionResponse.json();
```

---

## 🚀 Próximos Pasos

1. Implementar la app móvil usando React Native, Flutter, o tu framework preferido
2. Integrar la autenticación JWT
3. Implementar las pantallas según los endpoints disponibles
4. Manejar errores y estados de carga
5. Implementar refresh token automático
6. Agregar notificaciones push (opcional)


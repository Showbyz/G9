# Flujo de Trabajo: Desarrollo Local vs Producción Online

## 🎯 Respuesta Corta

**Sí, exactamente como lo describes:** Podrás trabajar localmente mientras el proyecto está online, y cuando hagas `git push`, los cambios se actualizarán automáticamente en producción (si configuras auto-deploy).

---

## 🌍 Los Dos "Universos Paralelos"

### 1. **Entorno Local (Desarrollo)**
- **Ubicación**: Tu computadora (`C:\dev\PruebasPortal`)
- **Base de datos**: PostgreSQL local (Docker)
- **URL**: `http://localhost:8000` o `http://192.168.100.25:8000`
- **Propósito**: Desarrollo, pruebas, experimentación
- **Estado**: Siempre activo mientras trabajas

### 2. **Entorno de Producción (Online)**
- **Ubicación**: Render.com (servidores en la nube)
- **Base de datos**: PostgreSQL en Render.com
- **URL**: `https://tu-app.onrender.com`
- **Propósito**: Aplicación en vivo para usuarios reales
- **Estado**: Activo 24/7 (se "duerme" después de 15 min de inactividad en plan gratuito)

---

## 🔄 Flujo de Trabajo Normal

### Escenario 1: Desarrollo y Actualización Continua

```
1. Trabajas localmente
   ↓
2. Haces cambios en tu código
   ↓
3. Pruebas localmente (http://localhost:8000)
   ↓
4. Si todo funciona bien:
   git add .
   git commit -m "Descripción de cambios"
   git push origin main
   ↓
5. Render.com detecta el push automáticamente
   ↓
6. Render.com reconstruye y despliega automáticamente
   ↓
7. Tu app online se actualiza (en ~2-5 minutos)
```

### Escenario 2: Trabajo Paralelo

```
LOCAL (Tu PC)                    PRODUCCIÓN (Render.com)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Servidor corriendo            ✅ Servidor corriendo
✅ Base de datos local           ✅ Base de datos en Render
✅ Usuarios de prueba            ✅ Usuarios reales
✅ Puedes experimentar           ✅ Estable y funcional
✅ Cambios inmediatos            ✅ Cambios solo con push
```

---

## ⚙️ Configuración de Auto-Deploy en Render.com

### Opción A: Auto-Deploy Automático (RECOMENDADO)

Cuando conectas tu repositorio de GitHub a Render.com:

1. **Render detecta automáticamente** cada `git push` a la rama `main`
2. **Reconstruye** la aplicación automáticamente
3. **Despliega** los cambios en ~2-5 minutos
4. **Notifica** por email cuando termine

**Ventajas:**
- ✅ No necesitas hacer nada manual
- ✅ Siempre actualizado
- ✅ Historial completo en GitHub

**Desventajas:**
- ⚠️ Cada push despliega (incluso si hay errores)
- ⚠️ Puede interrumpir el servicio brevemente

### Opción B: Deploy Manual

Puedes desactivar auto-deploy y hacer deploy manual desde el dashboard de Render.

**Ventajas:**
- ✅ Control total sobre cuándo desplegar
- ✅ Puedes probar localmente antes

**Desventajas:**
- ⚠️ Debes recordar hacer deploy manualmente

---

## 📋 Mejores Prácticas

### 1. **Siempre Prueba Localmente Primero**

```bash
# 1. Trabajas localmente
python manage.py runserver

# 2. Pruebas tus cambios
# Navegas a http://localhost:8000

# 3. Si todo funciona, haces commit y push
git add .
git commit -m "Agregar nueva funcionalidad X"
git push origin main
```

### 2. **Usa Ramas para Cambios Grandes**

```bash
# Crear rama para nueva funcionalidad
git checkout -b feature/nueva-funcionalidad

# Trabajar en la rama
# ... hacer cambios ...

# Probar localmente
# Si funciona, mergear a main
git checkout main
git merge feature/nueva-funcionalidad
git push origin main
```

### 3. **Manejo de Base de Datos**

**IMPORTANTE**: Las bases de datos son **separadas**:

- **Local**: PostgreSQL en Docker (tu PC)
- **Producción**: PostgreSQL en Render.com

**Para sincronizar datos:**

```bash
# Opción 1: Migraciones (estructura)
# Las migraciones se aplican automáticamente en producción

# Opción 2: Datos de prueba
# Puedes exportar/importar datos si es necesario
python manage.py dumpdata > datos.json
# Luego importar en producción (desde el dashboard de Render)
```

---

## 🚨 Consideraciones Importantes

### 1. **Variables de Entorno**

**Local** (`.env` en tu PC):
```env
DEBUG=True
SECRET_KEY=tu-clave-local
DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres
```

**Producción** (Render.com Dashboard):
```env
DEBUG=False
SECRET_KEY=clave-generada-por-render
DATABASE_URL=postgres://... (proporcionado por Render)
```

### 2. **Archivos Estáticos**

- **Local**: Se sirven automáticamente por Django
- **Producción**: Se recopilan con `collectstatic` automáticamente en Render

### 3. **Migraciones**

Render.com ejecuta automáticamente:
```bash
python manage.py migrate_schemas --shared
python manage.py migrate_schemas
```

Pero puedes ejecutarlas manualmente desde el dashboard si es necesario.

---

## 📊 Resumen Visual

```
┌─────────────────────────────────────────────────────────┐
│                    TU FLUJO DE TRABAJO                   │
└─────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   LOCAL      │         │   GITHUB     │         │   RENDER     │
│  (Tu PC)     │         │  (Repositorio)│        │  (Producción)│
└──────────────┘         └──────────────┘         └──────────────┘
      │                        │                        │
      │ 1. Trabajas aquí       │                        │
      │    y pruebas           │                        │
      │                        │                        │
      │ 2. git add .           │                        │
      │    git commit          │                        │
      │                        │                        │
      │ 3. git push ──────────>│                        │
      │                        │                        │
      │                        │ 4. Auto-deploy ──────>│
      │                        │    (automático)        │
      │                        │                        │
      │                        │                        │ 5. App actualizada
      │                        │                        │    en ~2-5 min
```

---

## ✅ Respuesta a tu Pregunta

**¿Podrás seguir trabajando localmente mientras está online?**
✅ **SÍ**, completamente independiente.

**¿Habrá dos universos paralelos?**
✅ **SÍ**, local y producción funcionan en paralelo.

**¿Un push desde local actualizará el online?**
✅ **SÍ**, si configuras auto-deploy (recomendado). Render detecta el push y despliega automáticamente.

---

## 🎯 Próximos Pasos

1. **Despliega** siguiendo `GUIA_DESPLIEGUE.md`
2. **Configura auto-deploy** en Render.com (está activado por defecto)
3. **Trabaja localmente** como siempre
4. **Haz push** cuando quieras actualizar producción
5. **Render actualiza automáticamente** en ~2-5 minutos

---

**¿Tienes más preguntas sobre el flujo de trabajo? ¡Pregunta!**


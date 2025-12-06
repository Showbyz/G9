# Cómo Personalizar el Frontend por Tenant

## Estado Actual

**Todos los tenants comparten el mismo frontend** porque:
- Los templates están en `loginApp/templates/` (compartidos)
- Los archivos estáticos (imágenes, CSS) están en `loginApp/static/` (compartidos)

## Sistema de Temas (Ya Configurado)

El sistema de temas **está configurado y funcionando**, pero necesita que crees los archivos personalizados.

### Cómo Funciona

1. **Archivos Estáticos**: El sistema busca archivos en este orden:
   - `loginApp/static/tenants/{tema}/img/` (imágenes del tema específico)
   - `loginApp/static/tenants/default/img/` (imágenes por defecto)
   - `loginApp/static/img/` (imágenes compartidas - donde están ahora)

2. **Templates**: El sistema busca templates en este orden:
   - `loginApp/templates/tenants/{tema}/` (templates del tema específico)
   - `loginApp/templates/tenants/default/` (templates por defecto)
   - `loginApp/templates/` (templates compartidos - donde están ahora)

## Cómo Personalizar un Tenant

### Opción 1: Solo Cambiar Imágenes (Más Simple)

1. **Crear directorio para el tema:**
   ```bash
   mkdir loginApp/static/tenants/{nombre_tema}/img
   ```

2. **Copiar imágenes personalizadas:**
   - Coloca tus imágenes en `loginApp/static/tenants/{nombre_tema}/img/`
   - Usa los mismos nombres que en `loginApp/static/img/`
   - Por ejemplo: `bg7.jpg`, `duoc.png`, `duocWpp.jpg`

3. **El sistema automáticamente usará las imágenes del tema** si existen, o las del directorio base si no existen.

**Ejemplo para Inacap (tema: "tema1"):**
```bash
# Crear directorio
mkdir loginApp/static/tenants/tema1/img

# Copiar imágenes personalizadas (reemplaza con tus imágenes)
cp tu_imagen_fondo.jpg loginApp/static/tenants/tema1/img/bg7.jpg
cp tu_logo.png loginApp/static/tenants/tema1/img/duoc.png
```

### Opción 2: Cambiar Templates e Imágenes (Más Completo)

1. **Crear directorio de templates:**
   ```bash
   mkdir loginApp/templates/tenants/{nombre_tema}
   ```

2. **Copiar templates a personalizar:**
   ```bash
   cp loginApp/templates/login.html loginApp/templates/tenants/{nombre_tema}/login.html
   cp loginApp/templates/base.html loginApp/templates/tenants/{nombre_tema}/base.html
   ```

3. **Editar los templates copiados** para personalizar:
   - Colores
   - Estructura
   - Textos
   - Referencias a imágenes

4. **Crear directorio de imágenes:**
   ```bash
   mkdir loginApp/static/tenants/{nombre_tema}/img
   ```

5. **Agregar imágenes personalizadas** en `loginApp/static/tenants/{nombre_tema}/img/`

## Ejemplo: Personalizar Inacap

Inacap tiene el tema "tema1". Para personalizarlo:

1. **Crear directorios:**
   ```bash
   mkdir loginApp/static/tenants/tema1/img
   ```

2. **Agregar imágenes personalizadas:**
   - Coloca `bg7.jpg` (fondo del login) en `loginApp/static/tenants/tema1/img/bg7.jpg`
   - Coloca `duoc.png` (logo) en `loginApp/static/tenants/tema1/img/duoc.png`
   - Coloca `duocWpp.jpg` (fondo del base) en `loginApp/static/tenants/tema1/img/duocWpp.jpg`

3. **El sistema automáticamente usará estas imágenes** cuando se acceda a Inacap.

## Archivos que se Pueden Personalizar

### Imágenes Actuales:
- `bg7.jpg` - Fondo del login
- `duoc.png` - Logo en el header
- `duocWpp.jpg` - Fondo de la página base (home)

### Templates Actuales:
- `login.html` - Página de login
- `logout.html` - Página de logout
- `base.html` - Template base (usado por home y otras páginas)
- `home.html` - Página principal

## Verificar el Tema de un Tenant

Puedes verificar el tema de un tenant desde el panel global:
1. Ve a `http://localhost:8000/global/tenants/`
2. Haz clic en "Editar" para el tenant
3. Ver el campo "Tema"

## Cambiar el Tema de un Tenant

1. Ve al panel global: `http://localhost:8000/global/tenants/`
2. Haz clic en "Editar" para el tenant
3. Cambia el campo "Tema"
4. Guarda los cambios

## Notas Importantes

1. **Fallback**: Si un archivo no existe en el tema específico, se usa el del directorio base.
2. **Nombres de Archivo**: Los nombres de archivo deben coincidir exactamente (case-sensitive).
3. **Tema por Defecto**: El tema "default" siempre debe existir como fallback.
4. **Actualización**: Después de agregar archivos, reinicia el servidor Django para que los cambios se reflejen.



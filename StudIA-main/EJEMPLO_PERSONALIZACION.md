# Ejemplo Práctico: Personalizar Imágenes por Tenant

## Situación Actual

- **DUOC UC**: Tema "default" - Usa imágenes de `loginApp/static/img/`
- **inacap**: Tema "tema1" - Usa imágenes de `loginApp/static/img/` (porque no hay personalizadas)

## Cómo Personalizar Inacap

### Paso 1: Agregar Imágenes Personalizadas

Copia o agrega tus imágenes personalizadas en:
```
loginApp/static/tenants/tema1/img/
```

**Imágenes que puedes personalizar:**
- `bg7.jpg` - Fondo del login (actualmente en `loginApp/static/img/bg7.jpg`)
- `duoc.png` - Logo en el header (actualmente en `loginApp/static/img/duoc.png`)
- `duocWpp.jpg` - Fondo de la página base (actualmente en `loginApp/static/img/duocWpp.jpg`)

### Paso 2: Ejemplo de Estructura

```
loginApp/
├── static/
│   ├── img/                    # Imágenes compartidas (para todos los tenants)
│   │   ├── bg7.jpg
│   │   ├── duoc.png
│   │   └── duocWpp.jpg
│   └── tenants/
│       ├── default/            # Tema por defecto
│       │   └── img/
│       │       └── (vacío - usa las del directorio base)
│       └── tema1/              # Tema de Inacap
│           └── img/
│               ├── bg7.jpg     # Imagen personalizada para Inacap
│               ├── duoc.png    # Logo personalizado para Inacap
│               └── duocWpp.jpg # Fondo personalizado para Inacap
```

### Paso 3: Cómo Funciona

1. **Cuando accedes a Inacap (tema "tema1"):**
   - El sistema busca `bg7.jpg` en `loginApp/static/tenants/tema1/img/bg7.jpg`
   - Si existe, la usa
   - Si no existe, busca en `loginApp/static/img/bg7.jpg` (fallback)

2. **Cuando accedes a DUOC UC (tema "default"):**
   - El sistema busca `bg7.jpg` en `loginApp/static/tenants/default/img/bg7.jpg`
   - Si no existe, busca en `loginApp/static/img/bg7.jpg` (fallback)

## Comandos para Personalizar

### Para Inacap (tema "tema1"):

```bash
# 1. Crear directorio (ya creado)
mkdir loginApp\static\tenants\tema1\img

# 2. Copiar o agregar imágenes personalizadas
# Ejemplo: copiar imagen personalizada
copy tu_imagen_fondo.jpg loginApp\static\tenants\tema1\img\bg7.jpg
copy tu_logo.png loginApp\static\tenants\tema1\img\duoc.png
copy tu_fondo_base.jpg loginApp\static\tenants\tema1\img\duocWpp.jpg
```

### Para DUOC UC (tema "default"):

```bash
# 1. Crear directorio (ya creado)
mkdir loginApp\static\tenants\default\img

# 2. Copiar o agregar imágenes personalizadas
copy tu_imagen_fondo.jpg loginApp\static\tenants\default\img\bg7.jpg
copy tu_logo.png loginApp\static\tenants\default\img\duoc.png
copy tu_fondo_base.jpg loginApp\static\tenants\default\img\duocWpp.jpg
```

## Verificar que Funciona

1. **Agrega una imagen personalizada** en `loginApp/static/tenants/tema1/img/bg7.jpg`
2. **Accede a Inacap**: `http://inacap.localhost:8000/`
3. **Deberías ver tu imagen personalizada** en lugar de la imagen por defecto

## Notas Importantes

1. **Nombres de Archivo**: Los nombres deben coincidir exactamente con los del directorio base
2. **Ruta en Templates**: Los templates usan `{% static "img/bg7.jpg" %}`, el sistema busca automáticamente en el directorio del tema
3. **Fallback**: Si no existe en el tema, usa la del directorio base
4. **Reiniciar Servidor**: Después de agregar archivos, reinicia el servidor Django para que los cambios se reflejen

## Estructura Completa Recomendada

```
loginApp/
├── static/
│   ├── img/                    # Imágenes compartidas (fallback)
│   │   ├── bg7.jpg
│   │   ├── duoc.png
│   │   └── duocWpp.jpg
│   └── tenants/
│       ├── default/            # Tema por defecto
│       │   └── img/
│       │       └── (opcional: imágenes por defecto)
│       └── tema1/              # Tema de Inacap
│           └── img/
│               ├── bg7.jpg     # Personalizado para Inacap
│               ├── duoc.png    # Personalizado para Inacap
│               └── duocWpp.jpg # Personalizado para Inacap
```



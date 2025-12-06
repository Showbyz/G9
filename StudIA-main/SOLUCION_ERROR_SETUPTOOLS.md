# Solución: Errores de Despliegue en Render.com

## Error 1: `ModuleNotFoundError: No module named 'pkg_resources'`

## 🔴 Problema

Al desplegar en Render.com, aparece el siguiente error:

```
ModuleNotFoundError: No module named 'pkg_resources'
```

Este error ocurre porque `pkg_resources` es parte de `setuptools`, que no está instalado por defecto en Python 3.13.

---

## ✅ Solución Aplicada

### 1. Agregar `setuptools` a `requirements.txt`

Se agregó `setuptools>=65.5.0` al inicio de `requirements.txt` para asegurar que esté disponible antes de instalar otras dependencias.

### 2. Actualizar `buildCommand` en `render.yaml`

Se actualizó el comando de build para instalar `setuptools` y `wheel` primero:

```yaml
buildCommand: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

---

## 🔧 Cambios Realizados

### `requirements.txt`
```diff
+ setuptools>=65.5.0
  asgiref==3.7.2
  Django==5.0.2
  ...
```

### `render.yaml`
```diff
- buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput
+ buildCommand: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

---

## 📝 Pasos para Aplicar

1. **Los cambios ya están aplicados** en los archivos del proyecto.

2. **Hacer commit y push:**
```bash
git add requirements.txt render.yaml
git commit -m "Fix: Agregar setuptools para resolver error pkg_resources"
git push origin main
```

3. **Render.com detectará automáticamente** el cambio y volverá a intentar el despliegue.

---

## 🎯 ¿Por qué ocurre este error?

- **Python 3.13** no incluye `setuptools` por defecto
- `djangorestframework-simplejwt` requiere `pkg_resources` (parte de `setuptools`)
- Render.com puede estar usando Python 3.13 aunque especifiques 3.11.9 en variables de entorno

---

## ✅ Verificación

Después del despliegue, verifica que:

1. ✅ El build se completa sin errores
2. ✅ La aplicación inicia correctamente
3. ✅ No hay errores de importación en los logs

---

## 📚 Referencias

- [setuptools documentation](https://setuptools.pypa.io/)
- [Render.com Python build](https://render.com/docs/python-version)

---

**¿El error persiste?** Verifica que:
- Los cambios se hayan hecho commit y push
- Render.com haya detectado el nuevo commit
- El build log muestre que `setuptools` se instaló correctamente

---

## Error 2: `ImportError: undefined symbol: _PyInterpreterState_Get` (psycopg2-binary)

### 🔴 Problema

Render.com está usando Python 3.13, pero `psycopg2-binary==2.9.9` no es compatible con Python 3.13. El error es:

```
ImportError: /opt/render/project/src/.venv/lib/python3.13/site-packages/psycopg2/_psycopg.cpython-313-x86_64-linux-gnu.so: undefined symbol: _PyInterpreterState_Get
```

Aunque especificamos `PYTHON_VERSION: 3.11.9` en `render.yaml`, Render puede ignorar esta variable y usar Python 3.13 por defecto.

---

### ✅ Solución Aplicada

**Crear archivo `runtime.txt`** en la raíz del proyecto para forzar Python 3.11.9:

```
python-3.11.9
```

Render.com detecta automáticamente este archivo y usa la versión especificada.

---

### 🔧 Cambios Realizados

**Nuevo archivo: `runtime.txt`**
```
python-3.11.9
```

---

### 📝 Pasos para Aplicar

1. **El archivo `runtime.txt` ya está creado** en la raíz del proyecto.

2. **Hacer commit y push:**
```bash
git add runtime.txt
git commit -m "Fix: Forzar Python 3.11.9 para compatibilidad con psycopg2-binary"
git push origin main
```

3. **Render.com detectará automáticamente** el cambio y usará Python 3.11.9.

---

### 🎯 ¿Por qué ocurre este error?

- **Python 3.13** es muy reciente y `psycopg2-binary` aún no tiene binarios compilados para esta versión
- Render.com puede usar Python 3.13 por defecto aunque especifiques otra versión en variables de entorno
- El archivo `runtime.txt` es la forma estándar de especificar la versión de Python en Render.com

---

### ✅ Verificación

Después del despliegue, verifica en el build log que:

1. ✅ Render detecta `runtime.txt`: `Using Python version specified in runtime.txt`
2. ✅ Usa Python 3.11.9: `Python 3.11.9`
3. ✅ `psycopg2-binary` se instala correctamente
4. ✅ No hay errores de importación

---

### 📚 Referencias

- [Render.com Python version](https://render.com/docs/python-version)
- [psycopg2-binary compatibility](https://pypi.org/project/psycopg2-binary/)

---

**¿El error persiste?** Verifica que:
- El archivo `runtime.txt` esté en la raíz del proyecto
- El contenido sea exactamente `python-3.11.9` (sin espacios extra)
- El `render.yaml` tenga `runtime: python-3.11.9` en el servicio
- Render.com haya detectado el nuevo commit
- El build log muestre que está usando Python 3.11.9

---

## Solución Adicional: Especificar Runtime en `render.yaml`

Si `runtime.txt` no funciona, también puedes especificar la versión de Python directamente en `render.yaml`:

```yaml
services:
  - type: web
    name: portal-autoatencion
    env: python
    runtime: python-3.11.9  # ← Agregar esta línea
    buildCommand: ...
```

**Ambos métodos** (`runtime.txt` y `runtime: python-3.11.9` en `render.yaml`) están aplicados para asegurar que Render use Python 3.11.9.


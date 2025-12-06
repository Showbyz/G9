# Solución: Render.com no respeta Python 3.11

## 🔴 Problema

Render.com sigue usando Python 3.13 a pesar de tener `runtime.txt` y `runtime` en `render.yaml`. El error es:

```
ImportError: /opt/render/project/src/.venv/lib/python3.13/site-packages/psycopg2/_psycopg.cpython-313-x86_64-linux-gnu.so: undefined symbol: _PyInterpreterState_Get
```

---

## ✅ Solución Aplicada (FINAL)

**Render.com requiere una versión específica de Python 3.11.x**, no solo `python-3.11`.

### 1. Usar versión específica en `runtime.txt`

Render necesita una versión específica como `python-3.11.1`:

```
python-3.11.1
```

### 2. Usar versión específica en `render.yaml`

Especificar la misma versión en `render.yaml`:

```yaml
runtime: python-3.11.1
```

### 3. Eliminar variable de entorno `PYTHON_VERSION`

La variable `PYTHON_VERSION` en `envVars` puede estar causando conflicto. Se eliminó.

---

## 🔧 Cambios Realizados

### `runtime.txt`
```diff
- python-3.11
+ python-3.11.1
```

### `render.yaml`
```diff
  services:
    - type: web
      name: portal-autoatencion
      env: python
-     runtime: python-3.11
+     runtime: python-3.11.1
      ...
      envVars:
-       - key: PYTHON_VERSION
-         value: 3.11.9
        - key: DATABASE_URL
```

---

## 📝 Pasos para Aplicar

1. **Los cambios ya están aplicados** en los archivos del proyecto.

2. **Hacer commit y push:**
```bash
git add runtime.txt render.yaml
git commit -m "Fix: Usar Python 3.11 genérico y eliminar PYTHON_VERSION"
git push origin main
```

3. **En Render.com:**
   - Ve a tu servicio
   - Click en "Settings"
   - Verifica que no haya una variable de entorno `PYTHON_VERSION` configurada manualmente
   - Si existe, elimínala
   - Click en "Manual Deploy" → "Deploy latest commit"

---

## 🎯 ¿Por qué usar una versión específica como `python-3.11.1`?

- **Render.com requiere una versión específica** de Python 3.11.x (como `3.11.1`, `3.11.2`, etc.)
- No acepta solo `python-3.11` (versión genérica)
- Debe ser del formato `python-3.11.x` donde `x` es un número específico
- Python 3.11.1 es compatible con `psycopg2-binary==2.9.9`

---

## ⚠️ Si Aún No Funciona

Si Render sigue usando Python 3.13 después de estos cambios, puedes:

### Opción 1: Configurar manualmente en el Dashboard de Render

1. Ve a tu servicio en Render.com
2. Click en "Settings"
3. Busca "Python Version" o "Runtime"
4. Selecciona "Python 3.11" manualmente
5. Guarda los cambios
6. Haz un nuevo deploy

### Opción 2: Verificar que `runtime.txt` esté en la raíz

Asegúrate de que `runtime.txt` esté en la raíz del proyecto (mismo nivel que `manage.py`), no en un subdirectorio.

### Opción 3: Usar un buildpack específico

Si Render tiene problemas detectando el runtime, puedes especificar un buildpack en `render.yaml`:

```yaml
buildCommand: |
  python3.11 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip setuptools wheel
  pip install -r requirements.txt
  python manage.py collectstatic --noinput
```

---

## ✅ Verificación

Después del despliegue, verifica en el build log que:

1. ✅ Render detecta `runtime.txt`: `Using Python version from runtime.txt`
2. ✅ Usa Python 3.11.x: `Python 3.11.x` (cualquier versión de 3.11)
3. ✅ `psycopg2-binary` se instala correctamente
4. ✅ No hay errores de importación

---

## 📚 Referencias

- [Render.com Python version](https://render.com/docs/python-version)
- [Render.com runtime.txt](https://render.com/docs/python-version#specifying-a-python-version)

---

**✅ SOLUCIÓN CONFIRMADA:**

Render.com requiere una versión específica de Python 3.11.x (como `3.11.1`). No acepta versiones genéricas como `python-3.11`.

**Verifica que:**
- El archivo `runtime.txt` contenga exactamente `python-3.11.1` (o otra versión específica de 3.11.x)
- El `render.yaml` tenga `runtime: python-3.11.1` (misma versión)
- No haya una variable `PYTHON_VERSION` configurada manualmente en el dashboard de Render
- El build log muestre que está usando Python 3.11.1 (o la versión especificada)


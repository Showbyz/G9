# Cómo Ejecutar el Servidor Django Correctamente

## ✅ Problema Resuelto

El error `ModuleNotFoundError: No module named 'dj_database_url'` ya está resuelto:
- ✅ `dj_database_url` está instalado en el entorno virtual
- ✅ El código ahora maneja el import de forma opcional
- ✅ El servidor funcionará correctamente

## 🚀 Cómo Ejecutar el Servidor

### Opción 1: Activar el Entorno Virtual (RECOMENDADO)

```powershell
# 1. Activar el entorno virtual
.\env\Scripts\Activate.ps1

# 2. Verificar que esté activado (deberías ver "(env)" al inicio de la línea)
# Deberías ver algo como: (env) PS C:\dev\PruebasPortal>

# 3. Ejecutar el servidor
python manage.py runserver
```

### Si tienes problemas con la política de ejecución de PowerShell:

```powershell
# Ejecutar este comando primero para permitir scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego activar el entorno virtual
.\env\Scripts\Activate.ps1
```

### Opción 2: Usar el Python del Entorno Virtual Directamente

Si no quieres activar el entorno virtual, puedes usar el Python directamente:

```powershell
.\env\Scripts\python.exe manage.py runserver
```

## ✅ Verificación

Para verificar que todo está correcto:

```powershell
# Verificar que las dependencias estén instaladas
.\env\Scripts\python.exe -c "import dj_database_url; print('OK')"

# Verificar la configuración de Django
.\env\Scripts\python.exe manage.py check
```

## 📝 Nota Importante

**El servidor DEBE ejecutarse con el entorno virtual activado o usando el Python del entorno virtual directamente.**

Si ejecutas `python manage.py runserver` sin activar el entorno virtual, usará el Python global que no tiene las dependencias instaladas.

---

**✅ Ahora puedes ejecutar el servidor sin problemas usando cualquiera de las opciones arriba.**


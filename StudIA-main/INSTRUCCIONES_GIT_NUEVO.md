# Instrucciones para Conectar el Proyecto a un Nuevo Repositorio Git

## ✅ Pasos Completados

1. ✅ **Remote origin antiguo eliminado** - Ya no hay conexión con el repositorio de la empresa anterior
2. ✅ **Rama main actualizada** - Todos los cambios están en la rama `main`
3. ✅ **.gitignore actualizado** - Incluye archivos de producción y despliegue

## 📝 Próximos Pasos

### 1. Crear un Nuevo Repositorio en GitHub

1. Ve a [GitHub](https://github.com) e inicia sesión
2. Click en el botón **"+"** (arriba a la derecha) → **"New repository"**
3. Configura el repositorio:
   - **Repository name**: `PortalAutoatencion` (o el nombre que prefieras)
   - **Description**: "Portal de Autoatención - Sistema Multi-tenant"
   - **Visibility**: Público o Privado (según prefieras)
   - **NO marques** "Initialize this repository with a README" (ya tienes código)
   - **NO agregues** .gitignore ni licencia (ya los tienes)
4. Click en **"Create repository"**

### 2. Conectar el Proyecto Local al Nuevo Repositorio

Una vez creado el repositorio, GitHub te mostrará instrucciones. Ejecuta estos comandos en tu terminal:

```bash
# Agregar el nuevo remote origin
git remote add origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git

# Verificar que se agregó correctamente
git remote -v

# Subir el código a la rama main
git push -u origin main
```

**Nota:** Reemplaza `TU-USUARIO` y `TU-REPOSITORIO` con tus datos reales.

### 3. (Opcional) Si Quieres Cambiar el Nombre de la Rama

Si prefieres usar `master` en lugar de `main`:

```bash
# Renombrar la rama
git branch -M master

# Subir con el nuevo nombre
git push -u origin master
```

### 4. Verificar la Conexión

```bash
# Ver los remotes configurados
git remote -v

# Deberías ver algo como:
# origin  https://github.com/TU-USUARIO/TU-REPOSITORIO.git (fetch)
# origin  https://github.com/TU-USUARIO/TU-REPOSITORIO.git (push)
```

## 🔄 Comandos Útiles para el Futuro

### Subir cambios al repositorio:
```bash
git add .
git commit -m "Descripción de los cambios"
git push
```

### Ver el estado del repositorio:
```bash
git status
```

### Ver el historial de commits:
```bash
git log --oneline
```

## ⚠️ Importante

- **No subas archivos sensibles**: El `.gitignore` ya está configurado para ignorar:
  - Archivos `.env` (variables de entorno)
  - `staticfiles/` (archivos estáticos compilados)
  - `env/` (entorno virtual)
  - Archivos de base de datos

- **Antes de hacer push**, verifica que no haya archivos sensibles:
```bash
git status
```

Si ves algún archivo que no debería estar (como `.env`), agrégalo al `.gitignore` y haz commit.

## 🎯 Siguiente Paso: Desplegar

Una vez que tengas el código en GitHub, puedes seguir la guía de despliegue en `GUIA_DESPLIEGUE.md` para desplegar en Render.com.

---

**¿Problemas?** Si encuentras algún error, verifica:
1. Que el repositorio esté creado en GitHub
2. Que tengas permisos para escribir en el repositorio
3. Que la URL del remote sea correcta


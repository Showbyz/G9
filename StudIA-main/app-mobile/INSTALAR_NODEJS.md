# 📦 Instalar Node.js - Guía Paso a Paso

## ❌ Error Detectado

El error indica que **Node.js no está instalado** o no está en el PATH del sistema.

## ✅ Solución: Instalar Node.js

### Opción 1: Instalación Manual (Recomendada)

1. **Descargar Node.js:**
   - Ve a: https://nodejs.org/
   - Descarga la versión **LTS (Long Term Support)** - la recomendada
   - Versión actual recomendada: v20.x o v18.x

2. **Instalar Node.js:**
   - Ejecuta el instalador descargado
   - Sigue el asistente de instalación
   - **IMPORTANTE:** Asegúrate de marcar la opción "Add to PATH" durante la instalación
   - Completa la instalación

3. **Verificar la instalación:**
   - Cierra y vuelve a abrir PowerShell/Terminal
   - Ejecuta estos comandos para verificar:
   ```bash
   node --version
   npm --version
   ```
   - Deberías ver números de versión (ej: v20.10.0 y 10.2.3)

4. **Reintentar:**
   ```bash
   cd app-mobile
   npm install
   ```

### Opción 2: Usar Chocolatey (Si lo tienes instalado)

Si tienes Chocolatey instalado:

```powershell
choco install nodejs-lts
```

### Opción 3: Usar winget (Windows 10/11)

```powershell
winget install OpenJS.NodeJS.LTS
```

## 🔄 Después de Instalar

1. **Cierra completamente PowerShell/Terminal**
2. **Abre una nueva terminal**
3. **Navega a la carpeta:**
   ```bash
   cd C:\dev\PruebasPortal\app-mobile
   ```
4. **Instala las dependencias:**
   ```bash
   npm install
   ```
5. **Inicia la app:**
   ```bash
   npm start
   ```

## ✅ Verificación Rápida

Después de instalar, ejecuta esto para verificar:

```powershell
node --version
npm --version
```

Si ves versiones, ¡está instalado correctamente!

## 🎯 Pasos Completos Resumidos

1. ✅ Descargar Node.js desde nodejs.org
2. ✅ Instalar Node.js (marcar "Add to PATH")
3. ✅ Cerrar y reabrir terminal
4. ✅ Verificar: `node --version` y `npm --version`
5. ✅ Ir a `app-mobile`: `cd app-mobile`
6. ✅ Instalar dependencias: `npm install`
7. ✅ Iniciar app: `npm start`

## ⚠️ Nota Importante

**Debes cerrar y reabrir la terminal** después de instalar Node.js para que los cambios en el PATH surtan efecto.

---

**Una vez instalado Node.js, podrás ejecutar `npm install` sin problemas.**


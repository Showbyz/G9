# 🔧 Solución: Instalar Node.js

## ❌ Problema Detectado

**Node.js NO está instalado** en tu sistema. Por eso el comando `npm` no funciona.

## ✅ Solución: Instalar Node.js

### Paso 1: Descargar Node.js

1. **Abre tu navegador** y ve a: **https://nodejs.org/**
2. **Descarga la versión LTS** (Long Term Support) - es la recomendada
   - Busca el botón verde que dice "LTS" o "Recommended"
   - Versión actual: v20.x o v18.x
   - Se descargará un archivo `.msi` (ej: `node-v20.10.0-x64.msi`)

### Paso 2: Instalar Node.js

1. **Ejecuta el instalador** que descargaste
2. **Sigue el asistente de instalación:**
   - Haz clic en "Next" en todas las pantallas
   - **IMPORTANTE:** Asegúrate de que la opción **"Add to PATH"** esté marcada (normalmente viene marcada por defecto)
   - Completa la instalación

### Paso 3: Verificar la Instalación

1. **Cierra completamente PowerShell/Terminal** (muy importante)
2. **Abre una NUEVA terminal/PowerShell**
3. **Ejecuta estos comandos para verificar:**
   ```powershell
   node --version
   npm --version
   ```
   
   Deberías ver algo como:
   ```
   v20.10.0
   10.2.3
   ```

### Paso 4: Instalar Dependencias de la App

Una vez que Node.js esté instalado:

```powershell
# Ir a la carpeta de la app
cd C:\dev\PruebasPortal\app-mobile

# Instalar dependencias
npm install
```

Esto tomará unos minutos la primera vez.

### Paso 5: Iniciar la App

```powershell
npm start
```

## 🎯 Resumen de Pasos

1. ✅ Ir a https://nodejs.org/
2. ✅ Descargar versión LTS
3. ✅ Instalar Node.js (marcar "Add to PATH")
4. ✅ **Cerrar y reabrir terminal** ⚠️ MUY IMPORTANTE
5. ✅ Verificar: `node --version` y `npm --version`
6. ✅ Ir a `app-mobile`: `cd app-mobile`
7. ✅ Instalar: `npm install`
8. ✅ Iniciar: `npm start`

## ⚠️ Nota Crítica

**DEBES cerrar y reabrir la terminal** después de instalar Node.js. Si no lo haces, el comando `npm` seguirá sin funcionar.

## 🔗 Enlaces Útiles

- **Descargar Node.js:** https://nodejs.org/
- **Documentación:** https://nodejs.org/docs/

## ✅ Después de Instalar

Una vez que tengas Node.js instalado y verificado, podrás:

1. Instalar dependencias: `npm install`
2. Iniciar la app: `npm start`
3. Generar APK cuando esté listo

---

**¡Instala Node.js y podrás continuar con la app móvil!** 🚀


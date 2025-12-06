# Script para verificar si Node.js está instalado

Write-Host "=== Verificación de Node.js ===" -ForegroundColor Cyan
Write-Host ""

# Verificar Node.js
Write-Host "Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js está instalado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js NO está instalado" -ForegroundColor Red
    Write-Host "   Descarga Node.js desde: https://nodejs.org/" -ForegroundColor Yellow
    Write-Host ""
}

# Verificar npm
Write-Host "Verificando npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "✅ npm está instalado: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm NO está instalado" -ForegroundColor Red
    Write-Host "   npm viene con Node.js, instala Node.js desde: https://nodejs.org/" -ForegroundColor Yellow
    Write-Host ""
}

# Verificar PATH
Write-Host "Verificando PATH..." -ForegroundColor Yellow
$nodePath = (Get-Command node -ErrorAction SilentlyContinue).Source
if ($nodePath) {
    Write-Host "✅ Node.js encontrado en: $nodePath" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js no está en el PATH" -ForegroundColor Red
    Write-Host "   Si acabas de instalar Node.js, cierra y reabre esta terminal" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Fin de la verificación ===" -ForegroundColor Cyan


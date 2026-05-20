#!/bin/bash

set -e

echo "=== Configuración del ambiente con virtualenv ==="

# Verificar e instalar Python, pip y dependencias si es necesario
if ! command -v python3 &> /dev/null; then
    echo "Python3 no está instalado. Instalando..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-full python3-venv
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip
    elif command -v brew &> /dev/null; then
        brew install python3
    else
        echo "No se pudo instalar Python3. Por favor, instálalo manualmente."
        exit 1
    fi
else
    echo "✓ Python3 ya está instalado: $(python3 --version)"
fi

# Verificar e instalar pipx si es necesario
if ! command -v pipx &> /dev/null; then
    echo "pipx no está instalado. Instalando..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y pipx
    elif command -v yum &> /dev/null; then
        sudo yum install -y pipx
    elif command -v brew &> /dev/null; then
        brew install pipx
    fi
else
    echo "✓ pipx ya está instalado"
fi

# Verificar e instalar virtualenv si es necesario
if ! command -v virtualenv &> /dev/null; then
    echo "virtualenv no está instalado. Instalando con pipx..."
    pipx install virtualenv
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "✓ virtualenv ya está instalado"
fi

# Crear el ambiente virtual
echo "Creando ambiente virtual..."
if [ ! -d ".venv" ]; then
    virtualenv .venv
    echo "✓ Ambiente virtual creado"
else
    echo "✓ El ambiente virtual ya existe"
fi

# Activar el ambiente virtual
echo "Activando ambiente virtual..."
source .venv/bin/activate

if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Error: No se pudo activar el ambiente virtual"
    exit 1
fi
echo "✓ Ambiente virtual activado: $VIRTUAL_ENV"

# Instalar dependencias
echo "Instalando dependencias desde requirements.txt..."
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo ""
echo "=== ✓ Configuración completada ==="
echo "Para activar el ambiente virtual en futuras sesiones, ejecuta:"
echo "  source .venv/bin/activate"
echo ""
echo "Para desactivar el ambiente virtual, ejecuta:"
echo "  deactivate"
echo ""
echo "Asegurate de tener la base de datos MySQL corriendo:"
echo "  docker compose up -d"
echo ""
echo "Iniciando la aplicación..."
echo ""

python app.py

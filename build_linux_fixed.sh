#!/bin/bash

# Script de construcción para FollowTracker (Linux) con imports ocultos
# Uso: ./build_linux_fixed.sh

set -e

echo "=== FollowTracker Linux Builder (Fixed) ==="

# Verificar que Python esté instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no está instalado"
    exit 1
fi

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "Error: No se encontró main.py. Ejecuta este script desde el directorio del proyecto."
    exit 1
fi

# Limpiar directorios anteriores
echo "Limpiando directorios anteriores..."
rm -rf dist build *.spec
echo "✓ Limpieza completada"

# Instalar dependencias
echo "Instalando dependencias..."
python3 -m pip install --upgrade pip --quiet
python3 -m pip install pyinstaller pyyaml --quiet
echo "✓ Dependencias instaladas"

# Obtener ruta del entorno virtual
VENV_PATH=""
if [ -n "$VIRTUAL_ENV" ]; then
    VENV_PATH="$VIRTUAL_ENV"
elif [ -d "venv" ]; then
    VENV_PATH="$(pwd)/venv"
elif [ -d ".venv" ]; then
    VENV_PATH="$(pwd)/.venv"
fi

# Construir ruta de site-packages
SITE_PACKAGES_PATH=""
if [ -n "$VENV_PATH" ]; then
    SITE_PACKAGES_PATH="$VENV_PATH/lib/python$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')/site-packages"
fi

# Construir ejecutable con imports ocultos
echo "Construyendo ejecutable con imports ocultos..."
if [ -n "$SITE_PACKAGES_PATH" ] && [ -d "$SITE_PACKAGES_PATH" ]; then
    echo "Usando ruta de site-packages: $SITE_PACKAGES_PATH"
    python3 -m PyInstaller --onefile --windowed --name FollowTracker --hidden-import=yaml --hidden-import=yaml.loader --paths="$SITE_PACKAGES_PATH" main.py
else
    echo "No se encontró entorno virtual, usando configuración por defecto..."
    python3 -m PyInstaller --onefile --windowed --name FollowTracker --hidden-import=yaml --hidden-import=yaml.loader main.py
fi

# Verificar si se creó el ejecutable
if [ -f "dist/FollowTracker" ]; then
    echo "✓ Ejecutable creado: dist/FollowTracker"
    
    # Crear paquete
    echo "Creando paquete..."
    rm -rf dist/FollowTracker_linux
    mkdir -p dist/FollowTracker_linux
    cp dist/FollowTracker dist/FollowTracker_linux/
    
    # Copiar archivos adicionales
    [ -f "README.md" ] && cp README.md dist/FollowTracker_linux/
    [ -f "config.py" ] && cp config.py dist/FollowTracker_linux/
    [ -f "utils.py" ] && cp utils.py dist/FollowTracker_linux/
    
    # Crear archivo de información
    cat > dist/FollowTracker_linux/INFO.txt << EOF
FollowTracker - Linux

Versión: 1.0
Plataforma: Linux
Fecha: $(date)

Instrucciones:
1. Ejecutar ./FollowTracker
2. Los datos se guardan en follows.yaml

Notas:
- Aplicación standalone
- Compatible con distribuciones Linux modernas
EOF
    
    echo "✓ Paquete creado: dist/FollowTracker_linux/"
    echo ""
    echo "=== Construcción completada ==="
    echo "Ejecutable: dist/FollowTracker"
    echo "Paquete: dist/FollowTracker_linux/"
else
    echo "✗ Error: No se creó el ejecutable"
    echo "Verificando directorio dist..."
    ls -la dist/ 2>/dev/null || echo "Directorio dist no existe"
    exit 1
fi 
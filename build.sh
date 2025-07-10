#!/bin/bash

# Script de construcción para FollowTracker
# Uso: ./build.sh [comando]

set -e  # Salir si hay algún error

echo "=== FollowTracker Builder ==="

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

# Función para limpiar
clean() {
    echo "Limpiando directorios de build..."
    rm -rf dist build *.spec
    echo "✓ Limpieza completada"
}

# Función para instalar dependencias
install_deps() {
    echo "Instalando dependencias..."
    python3 -m pip install --upgrade pip
    python3 -m pip install pyinstaller pyyaml
    echo "✓ Dependencias instaladas"
}

# Función para construir
build() {
    echo "Construyendo ejecutable..."
    python3 build.py build
}

# Función para construir completo
build_all() {
    echo "Iniciando construcción completa..."
    install_deps
    clean
    build
    echo "✓ Construcción completada"
}

# Función para mostrar ayuda
show_help() {
    echo "Uso: ./build.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  build     - Construir ejecutable"
    echo "  clean     - Limpiar directorios de build"
    echo "  deps      - Instalar dependencias"
    echo "  all       - Construcción completa (recomendado)"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  ./build.sh all      # Construcción completa"
    echo "  ./build.sh clean    # Solo limpiar"
    echo "  ./build.sh build    # Solo construir"
}

# Procesar argumentos
case "${1:-all}" in
    "build")
        build
        ;;
    "clean")
        clean
        ;;
    "deps")
        install_deps
        ;;
    "all")
        build_all
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "Comando desconocido: $1"
        show_help
        exit 1
        ;;
esac 
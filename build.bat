@echo off
setlocal enabledelayedexpansion

REM Script de construcción para FollowTracker (Windows)
REM Uso: build.bat [comando]

echo === FollowTracker Builder (Windows) ===

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo Error: No se encontró main.py. Ejecuta este script desde el directorio del proyecto.
    pause
    exit /b 1
)

REM Función para limpiar
:clean
if "%1"=="clean" goto :do_clean
if "%1"=="all" goto :do_clean
goto :build

:do_clean
echo Limpiando directorios de build...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec
echo ✓ Limpieza completada
if "%1"=="clean" goto :end

REM Función para instalar dependencias
:install_deps
echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install pyinstaller pyyaml
echo ✓ Dependencias instaladas

REM Función para construir
:build
if "%1"=="build" goto :do_build
if "%1"=="all" goto :do_build
goto :build_all

:do_build
echo Construyendo ejecutable...
python build.py build
goto :end

REM Función para construir completo
:build_all
if "%1"=="all" goto :do_build_all
goto :help

:do_build_all
echo Iniciando construcción completa...
call :install_deps
call :do_clean
call :do_build
echo ✓ Construcción completada
goto :end

REM Función para mostrar ayuda
:help
if "%1"=="help" goto :show_help
if "%1"=="-h" goto :show_help
if "%1"=="--help" goto :show_help
if "%1"=="" goto :show_help
echo Comando desconocido: %1
goto :show_help

:show_help
echo Uso: build.bat [comando]
echo.
echo Comandos disponibles:
echo   build     - Construir ejecutable
echo   clean     - Limpiar directorios de build
echo   deps      - Instalar dependencias
echo   all       - Construcción completa (recomendado)
echo   help      - Mostrar esta ayuda
echo.
echo Ejemplos:
echo   build.bat all      # Construcción completa
echo   build.bat clean    # Solo limpiar
echo   build.bat build    # Solo construir
goto :end

:end
if "%1"=="" (
    echo.
    echo Presiona cualquier tecla para continuar...
    pause >nul
) 
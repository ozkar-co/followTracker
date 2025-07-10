@echo off
setlocal enabledelayedexpansion

REM Script de construcción para FollowTracker (Windows) con imports ocultos
REM Uso: build_windows_fixed.bat

echo === FollowTracker Windows Builder (Fixed) ===

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

REM Limpiar directorios anteriores
echo Limpiando directorios anteriores...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec
echo ✓ Limpieza completada

REM Instalar dependencias
echo Instalando dependencias...
python -m pip install --upgrade pip --quiet
python -m pip install pyinstaller pyyaml --quiet
echo ✓ Dependencias instaladas

REM Obtener ruta del entorno virtual
set VENV_PATH=
if defined VIRTUAL_ENV (
    set VENV_PATH=%VIRTUAL_ENV%
) else (
    REM Buscar entorno virtual en el directorio actual
    if exist "venv" set VENV_PATH=%CD%\venv
    if exist ".venv" set VENV_PATH=%CD%\.venv
)

REM Construir ruta de site-packages
set SITE_PACKAGES_PATH=
if defined VENV_PATH (
    set SITE_PACKAGES_PATH=%VENV_PATH%\Lib\site-packages
)

REM Construir ejecutable con imports ocultos
echo Construyendo ejecutable con imports ocultos...
if defined SITE_PACKAGES_PATH (
    echo Usando ruta de site-packages: %SITE_PACKAGES_PATH%
    python -m PyInstaller --onefile --windowed --name FollowTracker --hidden-import=yaml --hidden-import=yaml.loader --paths="%SITE_PACKAGES_PATH%" main.py
) else (
    echo No se encontró entorno virtual, usando configuración por defecto...
    python -m PyInstaller --onefile --windowed --name FollowTracker --hidden-import=yaml --hidden-import=yaml.loader main.py
)

REM Verificar si se creó el ejecutable
if exist "dist\FollowTracker.exe" (
    echo ✓ Ejecutable creado: dist\FollowTracker.exe
    
    REM Crear paquete
    echo Creando paquete...
    if exist dist\FollowTracker_windows rmdir /s /q dist\FollowTracker_windows
    mkdir dist\FollowTracker_windows
    copy dist\FollowTracker.exe dist\FollowTracker_windows\
    
    REM Copiar archivos adicionales
    if exist README.md copy README.md dist\FollowTracker_windows\
    if exist config.py copy config.py dist\FollowTracker_windows\
    if exist utils.py copy utils.py dist\FollowTracker_windows\
    
    REM Crear archivo de información
    echo FollowTracker - Windows > dist\FollowTracker_windows\INFO.txt
    echo. >> dist\FollowTracker_windows\INFO.txt
    echo Versión: 1.0 >> dist\FollowTracker_windows\INFO.txt
    echo Plataforma: Windows >> dist\FollowTracker_windows\INFO.txt
    echo Fecha: %date% %time% >> dist\FollowTracker_windows\INFO.txt
    echo. >> dist\FollowTracker_windows\INFO.txt
    echo Instrucciones: >> dist\FollowTracker_windows\INFO.txt
    echo 1. Ejecutar FollowTracker.exe >> dist\FollowTracker_windows\INFO.txt
    echo 2. Los datos se guardan en follows.yaml >> dist\FollowTracker_windows\INFO.txt
    echo. >> dist\FollowTracker_windows\INFO.txt
    echo Notas: >> dist\FollowTracker_windows\INFO.txt
    echo - Aplicación standalone >> dist\FollowTracker_windows\INFO.txt
    echo - Compatible con Windows 7, 8, 10, 11 >> dist\FollowTracker_windows\INFO.txt
    
    echo ✓ Paquete creado: dist\FollowTracker_windows\
    echo.
    echo === Construcción completada ===
    echo Ejecutable: dist\FollowTracker.exe
    echo Paquete: dist\FollowTracker_windows\
) else (
    echo ✗ Error: No se creó el ejecutable
    echo Verificando directorio dist...
    if exist dist (
        dir dist
    ) else (
        echo Directorio dist no existe
    )
    pause
    exit /b 1
)

pause 
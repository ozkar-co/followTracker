# Guía de Construcción - FollowTracker

Esta guía te ayudará a crear ejecutables de FollowTracker para Windows y Linux.

## Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## Instalación de Dependencias

### Linux/macOS
```bash
pip3 install -r requirements.txt
```

### Windows
```cmd
pip install -r requirements.txt
```

## Construcción Automática

### Linux/macOS
```bash
# Construcción completa (recomendado)
./build.sh all

# Solo limpiar
./build.sh clean

# Solo construir
./build.sh build

# Solo instalar dependencias
./build.sh deps
```

### Windows
```cmd
# Construcción completa (recomendado)
build.bat all

# Solo limpiar
build.bat clean

# Solo construir
build.bat build

# Solo instalar dependencias
build.bat deps
```

## Construcción Manual

Si prefieres construir manualmente:

1. **Instalar PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Construir ejecutable:**
   ```bash
   python build.py
   ```

3. **O usar comandos específicos:**
   ```bash
   python build.py clean    # Limpiar
   python build.py spec     # Crear archivo .spec
   python build.py build    # Solo construir
   python build.py package  # Solo crear paquete
   ```

## Estructura de Salida

Después de la construcción exitosa, encontrarás:

```
followTracker/
├── dist/
│   └── FollowTracker          # Ejecutable (Linux)
│   └── FollowTracker.exe      # Ejecutable (Windows)
├── build/                     # Archivos temporales de construcción
├── FollowTracker_linux/       # Paquete para Linux
│   ├── FollowTracker
│   ├── README.md (si existe)
│   └── INFO.txt
└── FollowTracker_windows/     # Paquete para Windows
    ├── FollowTracker.exe
    ├── README.md (si existe)
    └── INFO.txt
```

## Distribución

### Para Linux
1. Copia el directorio `FollowTracker_linux/` a la máquina destino
2. Ejecuta `./FollowTracker` desde el directorio

### Para Windows
1. Copia el directorio `FollowTracker_windows/` a la máquina destino
2. Ejecuta `FollowTracker.exe` desde el directorio

## Notas Importantes

- **Aplicación Standalone:** Los ejecutables no requieren Python instalado en la máquina destino
- **Datos:** La aplicación creará automáticamente `follows.yaml` en el mismo directorio
- **Tamaño:** Los ejecutables pueden ser grandes (50-100MB) debido a que incluyen Python y todas las dependencias
- **Antivirus:** Algunos antivirus pueden detectar falsos positivos en ejecutables generados con PyInstaller

## Solución de Problemas

### Error: "PyInstaller no encontrado"
```bash
pip install pyinstaller
```

### Error: "No se puede importar tkinter"
En Linux, instala tkinter:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter
```

### Error: "Permission denied" en Linux
```bash
chmod +x build.sh
chmod +x dist/FollowTracker
```

### Ejecutable muy lento al iniciar
- Es normal en la primera ejecución
- PyInstaller extrae los archivos temporalmente
- Las siguientes ejecuciones serán más rápidas

## Personalización

### Agregar un ícono
1. Coloca tu archivo `.ico` (Windows) o `.png` (Linux) en el directorio
2. Modifica `build.py` para incluir el ícono en la configuración

### Cambiar el nombre del ejecutable
Modifica la variable `project_name` en `build.py`

### Incluir archivos adicionales
Agrega archivos a la lista `additional_files` en el método `create_package()` de `build.py` 
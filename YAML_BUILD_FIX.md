# Solución para Problema de YAML en PyInstaller

## Problema
PyInstaller no encuentra automáticamente la librería `yaml` al construir el ejecutable, causando errores como:
- `ModuleNotFoundError: No module named 'yaml'`
- `ImportError: cannot import name 'yaml'`

## Solución

### Opción 1: Scripts Actualizados (Recomendado)

#### Para Windows:
```cmd
build_windows_fixed.bat
```

#### Para Linux:
```bash
./build_linux_fixed.sh
```

### Opción 2: Comando Manual

#### Windows:
```cmd
python -m PyInstaller --onefile --windowed --name FollowTracker --hidden-import=yaml --hidden-import=yaml.loader --paths="path/to/your/venv/Lib/site-packages" main.py
```

#### Linux:
```bash
python3 -m PyInstaller --onefile --windowed --name FollowTracker --hidden-import=yaml --hidden-import=yaml.loader --paths="path/to/your/venv/lib/python3.x/site-packages" main.py
```

### Opción 3: Usando el Script Python Actualizado

```bash
python build.py
```

## Cambios Realizados

### 1. Imports Ocultos Agregados
```python
--hidden-import=yaml
--hidden-import=yaml.loader
--hidden-import=yaml.dumper
--hidden-import=yaml.cyaml
--hidden-import=yaml.constructor
--hidden-import=yaml.representer
--hidden-import=yaml.resolver
--hidden-import=yaml.emitter
--hidden-import=yaml.serializer
--hidden-import=yaml.parser
--hidden-import=yaml.scanner
--hidden-import=yaml.tokens
--hidden-import=yaml.events
--hidden-import=yaml.nodes
```

### 2. Rutas de Site-Packages
Los scripts ahora detectan automáticamente:
- Entorno virtual activo (`VIRTUAL_ENV`)
- Entorno virtual en directorio actual (`venv/`, `.venv/`)
- Ruta correcta de `site-packages` según la plataforma

### 3. Archivo .spec Actualizado
El archivo `.spec` generado incluye:
- Todos los imports ocultos de yaml
- Ruta correcta de `site-packages`
- Configuración optimizada para cada plataforma

## Verificación

### 1. Verificar que yaml esté instalado:
```bash
python -c "import yaml; print('YAML OK')"
```

### 2. Verificar la ruta de site-packages:
```bash
python -c "import site; print(site.getsitepackages())"
```

### 3. Verificar el ejecutable:
```bash
# Windows
dist\FollowTracker.exe

# Linux
./dist/FollowTracker
```

## Estructura de Directorios

Después de la construcción exitosa, encontrarás:

```
followTracker/
├── dist/
│   ├── FollowTracker          # Ejecutable (Linux)
│   ├── FollowTracker.exe      # Ejecutable (Windows)
│   ├── FollowTracker_linux/   # Paquete para Linux
│   │   ├── FollowTracker
│   │   ├── README.md (si existe)
│   │   └── INFO.txt
│   └── FollowTracker_windows/ # Paquete para Windows
│       ├── FollowTracker.exe
│       ├── README.md (si existe)
│       └── INFO.txt
└── build/                     # Archivos temporales de construcción
```

**Nota:** Todos los paquetes de distribución ahora se crean dentro del directorio `dist/` para mejor organización.

## Solución de Problemas

### Error: "No module named 'yaml'"
1. Verificar que PyYAML esté instalado:
   ```bash
   pip install pyyaml
   ```

2. Verificar la instalación:
   ```bash
   python -c "import yaml; print(yaml.__version__)"
   ```

### Error: "Cannot import name 'yaml'"
1. Usar los scripts actualizados que incluyen todos los imports ocultos
2. Verificar que estés usando un entorno virtual
3. Limpiar caché de PyInstaller:
   ```bash
   rm -rf build dist *.spec
   ```

### Error: "Module not found in site-packages"
1. Verificar la ruta del entorno virtual
2. Usar el parámetro `--paths` correcto
3. Ejecutar desde el directorio del proyecto

## Comandos de Diagnóstico

### Verificar entorno:
```bash
# Verificar Python
python --version

# Verificar pip
pip --version

# Verificar yaml
python -c "import yaml; print('YAML version:', yaml.__version__)"

# Verificar PyInstaller
python -m PyInstaller --version
```

### Verificar rutas:
```bash
# Verificar entorno virtual
echo $VIRTUAL_ENV

# Verificar site-packages
python -c "import site; print('Site packages:', site.getsitepackages())"

# Verificar instalación de yaml
python -c "import yaml; print('YAML path:', yaml.__file__)"
```

## Scripts Disponibles

1. **`build_windows_fixed.bat`** - Script para Windows con imports ocultos
2. **`build_linux_fixed.sh`** - Script para Linux con imports ocultos
3. **`build.py`** - Script Python actualizado con detección automática

## Recomendaciones

### Para desarrollo:
- Usa siempre un entorno virtual
- Instala las dependencias con `pip install -r requirements.txt`
- Usa los scripts actualizados

### Para distribución:
- Prueba el ejecutable en una máquina limpia
- Verifica que todas las funcionalidades trabajen
- Incluye documentación en el paquete

### Para debugging:
- Usa `--log-level DEBUG` para más información
- Revisa los logs en `build/` para errores específicos
- Verifica que todas las dependencias estén incluidas 
#!/usr/bin/env python3
"""
Script de construcción y distribución para FollowTracker
Genera ejecutables para Windows y Linux usando PyInstaller
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

class FollowTrackerBuilder:
    def __init__(self):
        self.project_name = "FollowTracker"
        self.main_file = "main.py"
        self.dist_dir = "dist"
        self.build_dir = "build"
        self.spec_file = f"{self.project_name}.spec"
        
    def check_dependencies(self):
        """Verificar que PyInstaller esté instalado"""
        try:
            import PyInstaller
            print("✓ PyInstaller encontrado")
        except ImportError:
            print("✗ PyInstaller no encontrado. Instalando...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    def clean_build_dirs(self):
        """Limpiar directorios de build anteriores"""
        dirs_to_clean = [self.dist_dir, self.build_dir]
        for dir_name in dirs_to_clean:
            if os.path.exists(dir_name):
                print(f"Limpiando {dir_name}...")
                shutil.rmtree(dir_name)
        
        if os.path.exists(self.spec_file):
            print(f"Eliminando {self.spec_file}...")
            os.remove(self.spec_file)
    
    def create_spec_file(self):
        """Crear archivo .spec para PyInstaller"""
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{self.main_file}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'yaml',
        'webbrowser',
        'datetime',
        'os',
        'typing'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.project_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
'''
        
        with open(self.spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        print(f"✓ Archivo {self.spec_file} creado")
    
    def build_executable(self):
        """Construir el ejecutable usando PyInstaller"""
        print("Construyendo ejecutable...")
        
        # Ejecutar PyInstaller
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--onefile",
            "--windowed",  # Sin consola para GUI
            "--name", self.project_name,
            self.main_file
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Ejecutable construido exitosamente")
            return True
        else:
            print("✗ Error al construir ejecutable:")
            print(result.stderr)
            return False
    
    def build_with_spec(self):
        """Construir usando archivo .spec"""
        print("Construyendo con archivo .spec...")
        
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            self.spec_file
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Ejecutable construido exitosamente")
            return True
        else:
            print("✗ Error al construir ejecutable:")
            print(result.stderr)
            return False
    
    def create_package(self):
        """Crear paquete de distribución"""
        current_platform = platform.system().lower()
        executable_name = f"{self.project_name}.exe" if current_platform == "windows" else self.project_name
        
        # Buscar el ejecutable
        exe_path = None
        for root, dirs, files in os.walk(self.dist_dir):
            for file in files:
                if file == executable_name:
                    exe_path = os.path.join(root, file)
                    break
            if exe_path:
                break
        
        if not exe_path:
            print(f"✗ No se encontró el ejecutable {executable_name}")
            return False
        
        # Crear directorio de paquete
        package_dir = f"{self.project_name}_{current_platform}"
        if os.path.exists(package_dir):
            shutil.rmtree(package_dir)
        os.makedirs(package_dir)
        
        # Copiar ejecutable
        shutil.copy2(exe_path, package_dir)
        
        # Copiar archivos adicionales si existen
        additional_files = ["README.md", "config.py", "utils.py"]
        for file in additional_files:
            if os.path.exists(file):
                shutil.copy2(file, package_dir)
        
        # Crear archivo de información
        info_content = f"""FollowTracker - {current_platform.title()}

Versión: 1.0
Plataforma: {current_platform.title()}
Fecha de construcción: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}

Instrucciones:
1. Ejecutar {executable_name}
2. La aplicación creará automáticamente el archivo follows.yaml para almacenar datos

Notas:
- Esta es una aplicación standalone que no requiere instalación
- Los datos se guardan en follows.yaml en el mismo directorio
"""
        
        with open(os.path.join(package_dir, "INFO.txt"), 'w', encoding='utf-8') as f:
            f.write(info_content)
        
        print(f"✓ Paquete creado: {package_dir}")
        return True
    
    def build_all(self):
        """Construir para todas las plataformas"""
        print("=== Constructor de FollowTracker ===\n")
        
        # Verificar dependencias
        self.check_dependencies()
        
        # Limpiar builds anteriores
        self.clean_build_dirs()
        
        # Crear archivo .spec
        self.create_spec_file()
        
        # Construir ejecutable
        if self.build_with_spec():
            # Crear paquete
            if self.create_package():
                print("\n=== Construcción completada ===")
                print("El ejecutable está listo para distribución.")
                return True
        
        print("\n=== Error en la construcción ===")
        return False

def main():
    """Función principal"""
    builder = FollowTrackerBuilder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "clean":
            builder.clean_build_dirs()
            print("✓ Directorios de build limpiados")
        elif command == "spec":
            builder.create_spec_file()
        elif command == "build":
            builder.check_dependencies()
            builder.clean_build_dirs()
            builder.create_spec_file()
            builder.build_with_spec()
        elif command == "package":
            builder.create_package()
        else:
            print("Comandos disponibles:")
            print("  python build.py          - Construir completo")
            print("  python build.py clean    - Limpiar directorios de build")
            print("  python build.py spec     - Crear archivo .spec")
            print("  python build.py build    - Solo construir ejecutable")
            print("  python build.py package  - Solo crear paquete")
    else:
        # Construcción completa por defecto
        builder.build_all()

if __name__ == "__main__":
    main() 
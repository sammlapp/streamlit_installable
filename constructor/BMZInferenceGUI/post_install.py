#!/usr/bin/env python
"""
Post-install script for BMZInferenceGUI
Creates desktop shortcuts and menu entries
"""
import os
import sys
import platform
from pathlib import Path


def create_desktop_launcher_files():
    """Create desktop window launcher files for all OS"""
    install_dir = Path(sys.prefix)
    
    # The launch_bmzinferencegui.py file is already included via construct.yaml
    # No need to create it here - it's copied from the source directory
    
    # Windows batch file
    if platform.system() == "Windows":
        batch_content = f"""@echo off
echo Starting BMZ Inference GUI...
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"
set "PYTHON_EXE=%SCRIPT_DIR%\\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=%SCRIPT_DIR%\\Scripts\\python.exe"
)
if not exist "%PYTHON_EXE%" (
    echo Error: Python executable not found in conda environment
    pause
    exit /b 1
)
if not exist "bmz_inference_gui.py" (
    echo Error: bmz_inference_gui.py not found
    pause
    exit /b 1
)
"%PYTHON_EXE%" launch_bmzinferencegui.py
pause
"""
        batch_path = install_dir / "launch_bmzinferencegui.bat"
        with open(batch_path, "w") as f:
            f.write(batch_content)
    
    # macOS command file
    elif platform.system() == "Darwin":
        command_content = f"""#!/bin/bash
echo "Starting BMZ Inference GUI..."
SCRIPT_DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" && pwd )"
cd "$SCRIPT_DIR"
PYTHON_EXE="$SCRIPT_DIR/bin/python"
if [ ! -f "$PYTHON_EXE" ]; then
    PYTHON_EXE="$SCRIPT_DIR/python"
fi
if [ ! -f "$PYTHON_EXE" ]; then
    echo "Error: Python executable not found in conda environment"
    read -p "Press Enter to exit..."
    exit 1
fi
if [ ! -f "bmz_inference_gui.py" ]; then
    echo "Error: bmz_inference_gui.py not found"
    read -p "Press Enter to exit..."
    exit 1
fi
"$PYTHON_EXE" launch_bmzinferencegui.py
"""
        command_path = install_dir / "launch_bmzinferencegui.command"
        with open(command_path, "w") as f:
            f.write(command_content)
        os.chmod(command_path, 0o755)
    
    # Linux shell script
    else:
        shell_content = f"""#!/bin/bash
echo "Starting BMZ Inference GUI..."
SCRIPT_DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" && pwd )"
cd "$SCRIPT_DIR"
PYTHON_EXE="$SCRIPT_DIR/bin/python"
if [ ! -f "$PYTHON_EXE" ]; then
    PYTHON_EXE="$SCRIPT_DIR/python"
fi
if [ ! -f "$PYTHON_EXE" ]; then
    echo "Error: Python executable not found in conda environment"
    read -p "Press Enter to exit..."
    exit 1
fi
if [ ! -f "bmz_inference_gui.py" ]; then
    echo "Error: bmz_inference_gui.py not found"
    read -p "Press Enter to exit..."
    exit 1
fi
"$PYTHON_EXE" launch_bmzinferencegui.py
"""
        shell_path = install_dir / "launch_bmzinferencegui.sh"
        with open(shell_path, "w") as f:
            f.write(shell_content)
        os.chmod(shell_path, 0o755)

def create_desktop_entry():
    """Create desktop entry for Linux"""
    if platform.system() != "Linux":
        return
        
    install_dir = Path(sys.prefix)
    desktop_dir = Path.home() / "Desktop"
    applications_dir = Path.home() / ".local" / "share" / "applications"
    
    desktop_content = f"""[Desktop Entry]
Name=BMZ Inference GUI
Comment=Bioacoustics Model Zoo inference interface
Exec={install_dir}/bmzinferencegui
Icon={install_dir}/icon.png
Terminal=false
Type=Application
Categories=Science;Audio;
"""
    
    # Create applications directory if it doesn't exist
    applications_dir.mkdir(parents=True, exist_ok=True)
    
    # Write desktop entry
    desktop_file = applications_dir / "bmzinferencegui.desktop"
    with open(desktop_file, 'w') as f:
        f.write(desktop_content)
    os.chmod(desktop_file, 0o755)

def install_pip_packages():
    """Install pip packages that aren't available via conda"""
    import subprocess
    
    pip_packages = [
        "streamlit-shortcuts>=0.2.0",
        "streamlit-extras", 
        "filedialpy",
        "bioacoustics-model-zoo",
    ]
    
    print("Installing additional pip packages...")
    
    # Get the conda executable path from the current environment
    conda_prefix = Path(sys.prefix)
    
    # Use the pip from the current conda environment
    pip_executable = conda_prefix / "bin" / "pip"
    if platform.system() == "Windows":
        pip_executable = conda_prefix / "Scripts" / "pip.exe"
    
    for package in pip_packages:
        try:
            # Use the environment-specific pip
            subprocess.check_call([str(pip_executable), "install", package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to install {package}: {e}")
            # Fallback to python -m pip if direct pip fails
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ Installed {package} (fallback method)")
            except subprocess.CalledProcessError as e2:
                print(f"Error: Could not install {package}: {e2}")

def main():
    """Main post-install function"""
    print("Setting up BMZ Inference GUI...")
    
    try:
        install_pip_packages()
        create_desktop_launcher_files()
        create_desktop_entry()
        print("BMZ Inference GUI setup completed successfully!")
        print(f"Installed to: {sys.prefix}")
        
        if platform.system() == "Windows":
            print("Launch: double-click launch_bmzinferencegui.bat")
        elif platform.system() == "Darwin":  # macOS
            print("Launch: double-click launch_bmzinferencegui.command")
        else:  # Linux
            print("Launch: run ./launch_bmzinferencegui.sh")
            
    except Exception as e:
        print(f"Warning: Setup completed with minor issues: {e}")

if __name__ == "__main__":
    main()
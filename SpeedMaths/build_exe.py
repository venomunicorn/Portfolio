import os
import subprocess
import sys

def create_exe():
    """Create standalone executable using PyInstaller"""
    try:
        # Install PyInstaller if not present
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        
        # Create the executable
        command = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name=MathPracticePro',
            '--icon=icon.ico',  # Add icon if you have one
            'main.py'
        ]
        
        subprocess.check_call(command)
        print("✓ Executable created successfully in the 'dist' folder!")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error creating executable: {e}")
    except FileNotFoundError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        create_exe()

if __name__ == "__main__":
    create_exe()

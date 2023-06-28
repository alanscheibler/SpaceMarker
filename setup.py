import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "includes": ["pygame", "tkinter", "math"],
    "excludes": [],
    "packages": [],
    "include_files": ["stars", "background", "sound", "functions.py", "README.md", "shipSDOL.ico"],
    # Add any other required folders or files here
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this for Windows GUI applications

executables = [
    Executable("main.py", base=base, icon=r"C:\Users\alanm\OneDrive\Área de Trabalho\SpaceMarker\shipSDOL.ico")

]

setup(
    name="SpaceMarker",
    version="1.0",
    description="Space Marker Application",
    options={"build_exe": build_exe_options},
    executables=executables
)


# hook-customtkinter.py
from PyInstaller.utils.hooks import copy_metadata, collect_data_files

datas = [
    ('assets', 'assets'),
]

# This line is often necessary to fix the path for Tkinter resources in macOS builds
# It ensures PyInstaller finds the CustomTkinter assets inside the bundled app.
datas += collect_data_files('customtkinter')
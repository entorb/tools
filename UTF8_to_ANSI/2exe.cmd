@echo off
pyinstaller --onefile --console convert_utf8_to_ansi.py
move dist\*.exe .\
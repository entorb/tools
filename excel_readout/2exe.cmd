@echo off
pyinstaller --onefile --console excel_readout.py
move dist\*.exe .\

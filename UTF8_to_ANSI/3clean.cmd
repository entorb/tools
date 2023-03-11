@echo off
rd /S /Q __pycache__
rd /S /Q build
rd /S /Q dist
del /Q *.spec
rem pause 
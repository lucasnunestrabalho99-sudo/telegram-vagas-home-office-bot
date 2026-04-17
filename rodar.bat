if not "%1" == "min" start /min cmd /c %0 min & exit/b
@echo off
cd /d "C:\Users\Lucas\automacao_quero_home"
set PYTHONIOENCODING=utf-8
"C:\Users\Lucas\automacao_quero_home\venv\Scripts\python.exe" main.py > log_homeoffice.txt 2>&1
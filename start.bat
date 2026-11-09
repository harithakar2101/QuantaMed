@echo off
title QuantaMed: Hybrid Quantum Medical Intelligence Platform
cd /d "%~dp0"

echo ========================================================
echo   QuantaMed: National Hybrid Quantum Medical Network
echo ========================================================
echo Starting server at http://127.0.0.1:5000 ...
echo.

py run.py
if %ERRORLEVEL% NEQ 0 (
    echo [!] Retrying with direct Python 3.13 executable...
    "C:\Users\harit\AppData\Local\Programs\Python\Python313\python.exe" run.py
)

pause

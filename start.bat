@echo off
REM ============================================================
REM  Z-Image-Turbo Launcher
REM ============================================================

set "APP_DIR=%~dp0"
set "PYTHON=C:\Users\Jason\AppData\Local\Programs\Python\Python312\python.exe"

if not exist "%PYTHON%" (
    echo [ERROR] Python 3.12 not found at:
    echo         %PYTHON%
    echo Please install Python 3.12 from https://www.python.org/downloads/
    pause
    exit /b 1
)

cd /d "%APP_DIR%"

echo Starting Z-Image-Turbo...
echo.

"%PYTHON%" app/app.py

pause

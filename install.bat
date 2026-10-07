@echo off
REM ============================================================
REM  Z-Image-Turbo Installer
REM ============================================================

set "PYTHON=C:\Users\Jason\AppData\Local\Programs\Python\Python312\python.exe"

if not exist "%PYTHON%" (
    echo [ERROR] Python 3.12 not found at:
    echo         %PYTHON%
    echo Please install Python 3.12 from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Installing dependencies...
"%PYTHON%" -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
"%PYTHON%" -m pip install diffusers transformers accelerate safetensors gradio Pillow

echo.
echo Installation complete!
echo Run start.bat to launch the app.
pause

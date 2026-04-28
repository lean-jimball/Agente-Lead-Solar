@echo off
echo ========================================
echo   CySlean Lead Solar - Inicio Rapido
echo ========================================
echo.

cd /d "%~dp0"

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo activar el entorno virtual
    echo.
    echo Soluciones:
    echo 1. Verifica que .venv exista
    echo 2. Si no existe, ejecuta: python -m venv .venv
    echo 3. Luego: .venv\Scripts\activate.bat
    echo 4. Y: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo Iniciando aplicacion web...
echo La aplicacion se abrira en tu navegador
echo Presiona Ctrl+C para detener
echo.

streamlit run app.py

pause

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
echo.
echo IMPORTANTE: 
echo - La app se abrira en: http://localhost:8501
echo - Si no abre automaticamente, copia esa URL en tu navegador
echo - Para WhatsApp, usa esta version local
echo - Presiona Ctrl+C para detener
echo.

REM Esperar 3 segundos y abrir navegador
timeout /t 3 /nobreak >nul
start http://localhost:8501

streamlit run app.py

pause

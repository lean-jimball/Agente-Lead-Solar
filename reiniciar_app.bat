@echo off
echo ========================================
echo   CySlean Lead Solar - Reinicio
echo ========================================
echo.

REM Matar procesos de Streamlit anteriores
echo Deteniendo procesos anteriores...
taskkill /F /IM streamlit.exe 2>nul
timeout /t 2 /nobreak >nul

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Activar entorno virtual
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo.
echo Iniciando aplicacion...
echo.
echo La aplicacion se abrira en: http://localhost:8501
echo.
echo IMPORTANTE: 
echo - Para WhatsApp, usa esta version local
echo - Para consultas remotas, usa Streamlit Cloud
echo.
echo Presiona Ctrl+C para detener la aplicacion
echo.

REM Iniciar Streamlit
start http://localhost:8501
streamlit run app.py

pause

@echo off
echo ========================================
echo   Deteniendo CySlean Lead Solar
echo ========================================
echo.

echo Buscando procesos de Streamlit...
tasklist | find /I "streamlit.exe" >nul

if errorlevel 1 (
    echo.
    echo No hay procesos de Streamlit ejecutandose
    echo.
) else (
    echo Deteniendo Streamlit...
    taskkill /F /IM streamlit.exe
    echo.
    echo Streamlit detenido correctamente
    echo.
)

echo Buscando procesos de Python relacionados...
tasklist | find /I "python.exe" >nul

if errorlevel 1 (
    echo No hay procesos de Python ejecutandose
) else (
    echo.
    echo NOTA: Hay procesos de Python ejecutandose
    echo Si quieres detenerlos todos, ejecuta:
    echo    taskkill /F /IM python.exe
    echo.
)

echo.
echo Listo! Ahora puedes cerrar esta ventana
echo.
pause

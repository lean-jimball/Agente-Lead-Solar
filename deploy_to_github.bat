@echo off
echo 🚀 Desplegando CySlean Lead Solar a GitHub
echo ============================================

echo.
echo 📝 Configurando Git...
git init
git add .
git commit -m "Initial commit - CySlean Lead Solar App"
git branch -M main

echo.
echo 🔗 Conectando con GitHub...
echo Por favor, crea un repositorio en GitHub llamado 'cyslean-solar-leads'
echo Luego ejecuta estos comandos:
echo.
echo git remote add origin https://github.com/TU_USUARIO/cyslean-solar-leads.git
echo git push -u origin main
echo.

echo 📋 Próximos pasos:
echo 1. Crea el repositorio en GitHub: https://github.com/new
echo 2. Ejecuta los comandos mostrados arriba
echo 3. Ve a https://share.streamlit.io/
echo 4. Conecta tu repositorio y despliega
echo.

pause
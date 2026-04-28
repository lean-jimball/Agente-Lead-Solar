# 🚀 Instrucciones de Despliegue - CySlean Lead Solar

## Opción 1: Streamlit Community Cloud (RECOMENDADO - GRATIS)

### Paso 1: Preparar el repositorio en GitHub

1. **Crear repositorio en GitHub:**
   - Ve a https://github.com/new
   - Nombre: `cyslean-solar-leads`
   - Descripción: `Sistema de gestión de leads para energía solar`
   - Público o Privado (tu elección)
   - ✅ Crear repositorio

2. **Subir código a GitHub:**
   ```bash
   # Inicializar Git (si no está inicializado)
   git init
   
   # Agregar todos los archivos
   git add .
   
   # Hacer commit inicial
   git commit -m "Initial commit - CySlean Lead Solar App"
   
   # Configurar rama principal
   git branch -M main
   
   # Conectar con tu repositorio (CAMBIAR TU_USUARIO)
   git remote add origin https://github.com/TU_USUARIO/cyslean-solar-leads.git
   
   # Subir código
   git push -u origin main
   ```

### Paso 2: Desplegar en Streamlit Cloud

1. **Ir a Streamlit Cloud:**
   - Visita: https://share.streamlit.io/
   - Click en "Sign up" o "Sign in"

2. **Conectar GitHub:**
   - Autoriza el acceso a tu cuenta de GitHub
   - Selecciona tu repositorio `cyslean-solar-leads`

3. **Configurar despliegue:**
   - **Repository**: `tu-usuario/cyslean-solar-leads`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - Click "Deploy!"

4. **Configurar variables de entorno (opcional):**
   - En el dashboard de tu app, ve a "Settings"
   - Sección "Secrets"
   - Agrega tus variables:
     ```toml
     GEMINI_API_KEY = "tu_api_key_aqui"
     ```

### Paso 3: ¡Listo!

Tu aplicación estará disponible en:
`https://cyslean-solar-leads.streamlit.app/`

---

## Opción 2: Railway (FÁCIL)

1. **Ir a Railway:**
   - Visita: https://railway.app/
   - Conecta tu GitHub

2. **Crear proyecto:**
   - "New Project" → "Deploy from GitHub repo"
   - Selecciona tu repositorio
   - Railway detecta automáticamente que es Streamlit

3. **Configurar variables:**
   - En el dashboard, ve a "Variables"
   - Agrega `GEMINI_API_KEY`

4. **Desplegar:**
   - Railway despliega automáticamente
   - Te da una URL como: `https://tu-app.up.railway.app/`

---

## Opción 3: Render (GRATIS con limitaciones)

1. **Ir a Render:**
   - Visita: https://render.com/
   - Conecta GitHub

2. **Crear Web Service:**
   - "New" → "Web Service"
   - Conecta tu repositorio
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

3. **Configurar:**
   - Plan: Free
   - Variables de entorno en "Environment"

---

## 🔧 Configuración Post-Despliegue

### Variables de Entorno Importantes:

```toml
# Para Streamlit Cloud (formato TOML)
GEMINI_API_KEY = "tu_api_key_de_google"
DATABASE_URL = "sqlite:///leads.db"
DEBUG = false

# Para Railway/Render (formato ENV)
GEMINI_API_KEY=tu_api_key_de_google
DATABASE_URL=sqlite:///leads.db
DEBUG=false
```

### Base de Datos en Producción:

Para aplicaciones con mucho tráfico, considera migrar a PostgreSQL:

1. **En Railway:**
   - Agrega "PostgreSQL" a tu proyecto
   - Copia la `DATABASE_URL`
   - Actualiza tu código para usar PostgreSQL

2. **En Render:**
   - Crea una base de datos PostgreSQL
   - Conecta con tu aplicación

---

## 🚨 Consideraciones Importantes

### Seguridad:
- ❌ **NUNCA** subas archivos `.env` a GitHub
- ✅ Usa variables de entorno de la plataforma
- ✅ Mantén privadas las API keys

### Performance:
- SQLite funciona para demos, pero considera PostgreSQL para producción
- Streamlit Cloud tiene límites de recursos (1GB RAM)
- Para apps con mucho tráfico, usa Railway o Render

### Actualizaciones:
- Cada `git push` actualiza automáticamente tu app
- Los cambios tardan 1-2 minutos en reflejarse
- Puedes ver logs en tiempo real en el dashboard

---

## 🎯 URLs de Ejemplo

Después del despliegue, tu app estará disponible en:

- **Streamlit Cloud**: `https://cyslean-solar-leads.streamlit.app/`
- **Railway**: `https://cyslean-solar-leads.up.railway.app/`
- **Render**: `https://cyslean-solar-leads.onrender.com/`

---

## 📞 Soporte

Si tienes problemas:

1. **Revisa los logs** en el dashboard de tu plataforma
2. **Verifica las variables de entorno**
3. **Asegúrate de que requirements.txt esté completo**
4. **Consulta la documentación** de cada plataforma

### Enlaces útiles:
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)

---

¡Tu aplicación CySlean Lead Solar estará disponible 24/7 en internet! 🎉
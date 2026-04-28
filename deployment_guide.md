# 🚀 Guía de Despliegue - CySlean Lead Solar

## 1. Streamlit Community Cloud (RECOMENDADO - GRATIS)

### Pasos para desplegar:

1. **Preparar el repositorio:**
   ```bash
   # Crear repositorio en GitHub
   git init
   git add .
   git commit -m "Initial commit - CySlean Lead Solar App"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/cyslean-solar-leads.git
   git push -u origin main
   ```

2. **Ir a Streamlit Community Cloud:**
   - Visita: https://share.streamlit.io/
   - Conecta tu cuenta de GitHub
   - Selecciona tu repositorio
   - Archivo principal: `app.py`
   - ¡Despliega!

### Ventajas:
- ✅ Completamente GRATIS
- ✅ Integración directa con GitHub
- ✅ SSL automático (HTTPS)
- ✅ Actualizaciones automáticas con git push
- ✅ Dominio personalizado disponible

---

## 2. Railway (FÁCIL - GRATIS con límites)

### Pasos:
1. Ir a https://railway.app/
2. Conectar GitHub
3. Seleccionar repositorio
4. Railway detecta automáticamente Streamlit
5. ¡Despliega!

### Ventajas:
- ✅ Muy fácil de usar
- ✅ Base de datos incluida
- ✅ $5 gratis al mes

---

## 3. Render (GRATIS con limitaciones)

### Pasos:
1. Ir a https://render.com/
2. Conectar GitHub
3. Crear "Web Service"
4. Comando de inicio: `streamlit run app.py --server.port $PORT`

### Ventajas:
- ✅ Plan gratuito disponible
- ✅ SSL automático
- ⚠️ Se duerme después de 15 min de inactividad

---

## 4. Heroku (PAGO - pero muy confiable)

### Ventajas:
- ✅ Muy estable
- ✅ Escalable
- ❌ Ya no tiene plan gratuito

---

## Archivos necesarios para el despliegue:

### `requirements.txt` (ya lo tienes)
```
playwright
google-genai
pywhatkit
streamlit
pandas
python-dotenv
folium
streamlit-folium
pyairtable
selenium
psutil
plotly
```

### `runtime.txt` (opcional - especifica versión de Python)
```
python-3.11.0
```

### `.streamlit/config.toml` (configuración de Streamlit)
```toml
[server]
headless = true
port = $PORT
enableCORS = false

[theme]
base = "dark"
```

---

## 🔒 Consideraciones de Seguridad:

### Variables de entorno (.env):
- ❌ NO subir archivo .env a GitHub
- ✅ Configurar variables en la plataforma de despliegue
- ✅ Usar secrets management de cada plataforma

### Base de datos:
- Para producción, considera migrar a PostgreSQL o MySQL
- SQLite funciona pero tiene limitaciones en la nube

---

## 🎯 RECOMENDACIÓN FINAL:

**Usa Streamlit Community Cloud** porque:
1. Es gratis para siempre
2. Integración perfecta con Streamlit
3. Actualizaciones automáticas
4. SSL incluido
5. Fácil configuración

¡Tu app estará disponible en una URL como: `https://cyslean-solar-leads.streamlit.app/`!
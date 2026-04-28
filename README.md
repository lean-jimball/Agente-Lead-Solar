# 🌞 CySlean Lead Solar - Sistema de Prospección Automatizada

Sistema automatizado para búsqueda, calificación y contacto de leads para instalación de paneles solares en México.

## 🎯 Funcionalidades

### 1. **Búsqueda Automatizada de Leads**
- Scraping de Google Maps con Playwright
- Extracción de: nombre, teléfono, dirección, website, calificación
- Detección automática de ciudad y estado

### 2. **Calificación Inteligente con IA**
- Análisis con Google Gemini AI
- Score de 1-10 basado en potencial de consumo eléctrico
- Filtrado automático de franquicias y corporativos
- Cálculo de consumo estimado, sistema recomendado y ahorro mensual

### 3. **Clasificación Automática de Estados**
- **Nuevo**: Lead recién agregado con teléfono válido
- **Sin teléfono**: No tiene número de contacto
- **No WhatsApp**: Teléfono inválido o no es WhatsApp
- **Contactado**: Mensaje enviado exitosamente
- **Calificado**: Lead con alto potencial (score ≥ 8)

### 4. **Envío Automatizado por WhatsApp**
- Mensajes personalizados con datos reales de ahorro
- Modo preview (revisar antes de enviar)
- Modo automático (envío masivo)
- Actualización automática de estados

### 5. **Dashboard Interactivo**
- Métricas en tiempo real
- Mapa de distribución por estado
- Visualización de pipeline de ventas
- Filtros y búsqueda

## 📋 Requisitos

- Python 3.8+
- Google Chrome o Microsoft Edge (para scraping)
- Cuenta de Google Gemini AI (gratis)
- WhatsApp Web (para envío de mensajes)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd cyslean-lead-solar
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar navegador para Playwright

```bash
# Opción 1: Chromium
python -m playwright install chromium

# Opción 2: Microsoft Edge (recomendado para Windows)
python -m playwright install msedge
```

### 5. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu API key de Gemini
# Obtén tu key gratis en: https://aistudio.google.com/
```

Edita `.env`:
```env
GEMINI_API_KEY=tu_api_key_aqui
```

### 6. Verificar instalación

```bash
python verificar_sistema.py
```

Si todo está correcto, verás:
```
🎉 ¡Sistema listo para usar!
```

## 🚀 Despliegue en la Web

### Streamlit Community Cloud (GRATIS - Recomendado)

1. **Preparar para despliegue**:
```bash
python prepare_deployment.py
```

2. **Subir a GitHub**:
```bash
git init
git add .
git commit -m "Initial commit - CySlean Lead Solar"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/cyslean-solar-leads.git
git push -u origin main
```

3. **Desplegar**:
   - Ve a [share.streamlit.io](https://share.streamlit.io/)
   - Conecta tu cuenta de GitHub
   - Selecciona tu repositorio
   - Archivo principal: `app.py`
   - ¡Despliega!

Tu app estará disponible en: `https://cyslean-solar-leads.streamlit.app/`

### Otras opciones de despliegue:
- **Railway**: https://railway.app/ (Fácil, $5 gratis/mes)
- **Render**: https://render.com/ (Plan gratuito disponible)
- **Heroku**: Opción premium pero muy estable

### Configuración para producción:
- Configura variables de entorno en la plataforma
- Para mayor escala, migra de SQLite a PostgreSQL
- Configura dominio personalizado (opcional)

## 💻 Uso

### Iniciar la aplicación web

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

### Flujo de trabajo típico:

1. **Buscar leads**:
   - En el sidebar, ingresa una búsqueda (ej: "hoteles en Pachuca")
   - Ajusta el número de resultados (1-50)
   - Click en "🚀 Buscar"

2. **Revisar leads**:
   - El sistema automáticamente:
     - Extrae información de Google Maps
     - Analiza con IA y asigna score
     - Calcula ahorro potencial
     - Clasifica por estado (Nuevo/Sin teléfono/No WhatsApp)

3. **Enviar mensajes por WhatsApp**:
   - Abre WhatsApp Web en tu navegador
   - Inicia sesión
   - En la app, click en "📤 WhatsApp (X)"
   - Revisa cada mensaje en modo preview
   - Los leads contactados cambian a estado "Contactado"

### Envío de WhatsApp desde terminal (avanzado)

```bash
python messenger.py
```

Opciones:
- **Modo 1 (Preview)**: Revisas cada mensaje antes de enviar
- **Modo 2 (Auto)**: Envío automático sin confirmación

## 📊 Estados del Pipeline

| Estado | Descripción | Acción |
|--------|-------------|--------|
| **Nuevo** | Lead recién agregado con teléfono válido | Listo para contactar |
| **Sin teléfono** | No tiene número de contacto | Buscar teléfono manualmente |
| **No WhatsApp** | Teléfono inválido o no WhatsApp | Contactar por otro medio |
| **Contactado** | Mensaje enviado exitosamente | Esperar respuesta |
| **Calificado** | Alto potencial (score ≥ 8) | Priorizar seguimiento |

## 🎯 Tipos de Negocio Priorizados

### Score Alto (8-10)
- Lavanderías y tintorerías
- Hoteles y moteles
- Hospitales y clínicas
- Gimnasios

### Score Medio (5-7)
- Restaurantes y bares
- Escuelas privadas
- Car wash
- Salones de eventos

### Score Bajo (3-4)
- Tiendas locales
- Oficinas pequeñas
- Consultorios

### Descartados (Score 0)
- Franquicias (Oxxo, 7-Eleven, etc.)
- Cadenas corporativas (Walmart, Soriana, etc.)
- Bancos

## 🔧 Solución de Problemas

### El scraper no encuentra resultados

```bash
# Reinstalar navegador
python -m playwright install chromium --force
```

### Error de API de Gemini

- Verifica que tu API key sea correcta en `.env`
- Obtén una nueva en: https://aistudio.google.com/
- El sistema funciona en "modo prueba" sin API (scores básicos)

### WhatsApp no envía mensajes

1. Asegúrate de tener WhatsApp Web abierto
2. Verifica que estés logueado
3. Revisa que los números tengan formato correcto (10 dígitos)
4. Espera 12 segundos entre mensajes (límite de WhatsApp)

### Error en la base de datos

```bash
# Reinicializar base de datos
python -c "from database import init_db; init_db()"
```

## 📁 Estructura del Proyecto

```
cyslean-lead-solar/
├── app.py                      # Aplicación Streamlit principal
├── database.py                 # Gestión de base de datos SQLite
├── scraper.py                  # Scraper de Google Maps
├── ai_processor.py             # Análisis con Gemini AI
├── messenger.py                # Envío de WhatsApp
├── verificar_sistema.py        # Script de verificación
├── requirements.txt            # Dependencias
├── .env                        # Configuración (crear desde .env.example)
├── leads.db                    # Base de datos SQLite (se crea automáticamente)
└── src/
    ├── domain/
    │   └── lead.py            # Modelo de dominio
    ├── application/
    │   └── lead_service.py    # Lógica de negocio
    └── infrastructure/
        └── database/
            └── repository.py   # Acceso a datos
```

## 🔐 Seguridad

- **Nunca** compartas tu archivo `.env`
- Las API keys son personales e intransferibles
- La base de datos `leads.db` contiene información sensible
- Agrega `.env` y `leads.db` a `.gitignore`

## 🤝 Soporte

Para problemas o preguntas:
1. Ejecuta `python verificar_sistema.py` para diagnóstico
2. Revisa los logs en la terminal
3. Consulta la documentación de cada componente

## 📝 Notas Importantes

- **Límites de WhatsApp**: No envíes más de 50 mensajes por hora
- **Scraping ético**: Respeta los términos de servicio de Google Maps
- **Datos personales**: Cumple con la ley de protección de datos (LFPDPPP)
- **API de Gemini**: Tiene límites de uso gratuito (15 requests/minuto)

## 🎓 Mejores Prácticas

1. **Búsquedas específicas**: "hoteles en Pachuca" mejor que solo "hoteles"
2. **Lotes pequeños**: Busca 5-10 leads a la vez para mejor calidad
3. **Revisa antes de enviar**: Usa modo preview en WhatsApp
4. **Limpia regularmente**: Borra leads "Nuevo" que no sirvan
5. **Backup**: Respalda `leads.db` periódicamente

## 📈 Roadmap

- [ ] Integración con CRM
- [ ] Seguimiento de respuestas
- [ ] Reportes avanzados
- [ ] API REST
- [ ] App móvil

---

**Desarrollado para CySlean** | Versión 1.0 | 2024

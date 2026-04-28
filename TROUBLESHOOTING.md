# 🔧 Troubleshooting - CySlean Lead Solar

Guía completa para resolver problemas comunes.

---

## 🚨 Problemas de Instalación

### Error: "pip: command not found"

**Causa**: Python no está instalado o no está en PATH

**Solución**:
```bash
# Verificar instalación de Python
python --version

# Si no funciona, descargar de:
# https://www.python.org/downloads/
```

### Error: "No module named 'streamlit'"

**Causa**: Dependencias no instaladas

**Solución**:
```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Si falla, instalar una por una
pip install streamlit
pip install pandas
pip install playwright
pip install google-generativeai
pip install pywhatkit
pip install folium
pip install streamlit-folium
pip install python-dotenv
pip install pyairtable
```

### Error: "playwright install failed"

**Causa**: Navegador no instalado

**Solución**:
```bash
# Opción 1: Chromium (recomendado)
python -m playwright install chromium

# Opción 2: Microsoft Edge (Windows)
python -m playwright install msedge

# Opción 3: Todos los navegadores
python -m playwright install
```

---

## 🔑 Problemas de Configuración

### Error: "GEMINI_API_KEY not found"

**Causa**: Archivo .env no existe o está mal configurado

**Solución**:
```bash
# 1. Verificar que .env existe
ls -la .env  # Linux/Mac
dir .env     # Windows

# 2. Si no existe, crear desde ejemplo
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# 3. Editar .env y agregar tu key
# Obtener key gratis en: https://aistudio.google.com/
```

**Contenido correcto de .env**:
```env
GEMINI_API_KEY=AIzaSyC...tu_key_real_aqui
```

### Error: "Invalid API key"

**Causa**: API key incorrecta o expirada

**Solución**:
1. Ir a https://aistudio.google.com/
2. Crear nueva API key
3. Copiar key completa (empieza con `AIzaSy`)
4. Pegar en `.env`
5. Reiniciar aplicación

### Modo Prueba (sin API key)

Si no tienes API key, el sistema funciona en modo prueba:
- ✅ Scraping funciona normal
- ✅ Scores básicos por industria
- ❌ Sin análisis avanzado de IA

---

## 🌐 Problemas de Scraping

### Error: "Browser not found"

**Causa**: Navegador de Playwright no instalado

**Solución**:
```bash
# Reinstalar navegador
python -m playwright install chromium --force

# Verificar instalación
python -m playwright --version
```

### Error: "Timeout waiting for selector"

**Causa**: Google Maps cambió su estructura o conexión lenta

**Solución**:
```bash
# 1. Verificar conexión a internet
ping google.com

# 2. Aumentar timeout en scraper.py (línea ~50)
# Cambiar: timeout=15000
# Por:     timeout=30000

# 3. Probar con menos resultados
# En lugar de 50, usar 5-10
```

### No encuentra resultados

**Causa**: Búsqueda muy genérica o sin resultados en Google Maps

**Solución**:
- ✅ Usar búsquedas específicas: "hoteles en Pachuca"
- ❌ Evitar genéricas: "hoteles"
- ✅ Incluir ciudad: "lavanderías en Monterrey"
- ✅ Verificar que existan en Google Maps primero

### Resultados duplicados

**Causa**: Sistema de deduplicación no funcionó

**Solución**:
```python
# Ejecutar limpieza manual
python -c "
from database import get_connection
conn = get_connection()
conn.execute('DELETE FROM leads WHERE id NOT IN (SELECT MIN(id) FROM leads GROUP BY telefono)')
conn.commit()
print('Duplicados eliminados')
"
```

---

## 📱 Problemas de WhatsApp

### Error: "WhatsApp Web not open"

**Causa**: WhatsApp Web no está abierto o no hay sesión

**Solución**:
1. Abrir https://web.whatsapp.com en navegador
2. Escanear código QR con tu teléfono
3. Esperar a que cargue completamente
4. Ejecutar messenger.py nuevamente

### Error: "Invalid phone number"

**Causa**: Número no tiene formato correcto

**Solución**:
```python
# Números válidos para México:
✅ 7711234567 (10 dígitos)
✅ 527711234567 (12 dígitos con código país)
✅ +527711234567 (con +)

❌ 771-123-4567 (con guiones)
❌ (771) 123-4567 (con paréntesis)
❌ 1234567 (muy corto)
```

### Mensajes no se envían

**Causa**: Límite de WhatsApp o número bloqueado

**Solución**:
1. **Verificar límites**:
   - Máximo 50 mensajes/hora
   - Esperar 12 segundos entre mensajes
   
2. **Verificar número**:
   - Probar enviando mensaje manual primero
   - Verificar que el número tenga WhatsApp
   
3. **Reiniciar proceso**:
   ```bash
   # Cerrar WhatsApp Web
   # Cerrar navegador
   # Abrir nuevamente
   # Ejecutar messenger.py
   ```

### Error: "Tab close failed"

**Causa**: Navegador bloqueó el cierre automático

**Solución**:
```python
# Editar messenger.py línea ~180
# Cambiar:
tab_close=True

# Por:
tab_close=False
```

---

## 💾 Problemas de Base de Datos

### Error: "Database is locked"

**Causa**: Múltiples procesos accediendo a la BD

**Solución**:
```bash
# 1. Cerrar todas las instancias de la app
# 2. Verificar procesos
ps aux | grep python  # Linux/Mac
tasklist | findstr python  # Windows

# 3. Matar procesos si es necesario
kill -9 <PID>  # Linux/Mac
taskkill /F /PID <PID>  # Windows

# 4. Reiniciar aplicación
```

### Error: "No such table: leads"

**Causa**: Base de datos no inicializada

**Solución**:
```bash
# Inicializar base de datos
python -c "from database import init_db; init_db()"

# Verificar
python -c "from database import get_stats; print(get_stats())"
```

### Corrupción de base de datos

**Causa**: Cierre inesperado o error de disco

**Solución**:
```bash
# 1. Backup de BD actual
cp leads.db leads_backup.db

# 2. Verificar integridad
sqlite3 leads.db "PRAGMA integrity_check;"

# 3. Si está corrupta, recrear
rm leads.db
python -c "from database import init_db; init_db()"

# 4. Restaurar desde backup si es posible
```

---

## 🖥️ Problemas de la Aplicación Web

### Error: "Address already in use"

**Causa**: Puerto 8501 ya está en uso

**Solución**:
```bash
# Opción 1: Matar proceso en puerto 8501
# Linux/Mac
lsof -ti:8501 | xargs kill -9

# Windows
netstat -ano | findstr :8501
taskkill /F /PID <PID>

# Opción 2: Usar otro puerto
streamlit run app.py --server.port 8502
```

### Aplicación muy lenta

**Causa**: Demasiados leads en memoria

**Solución**:
```python
# Editar app.py línea ~161
# Cambiar:
leads = service.get_all_leads(limit=5000)

# Por:
leads = service.get_all_leads(limit=1000)
```

### Mapa no se muestra

**Causa**: Falta folium o streamlit-folium

**Solución**:
```bash
pip install folium streamlit-folium --upgrade

# Verificar instalación
python -c "import folium; import streamlit_folium; print('OK')"
```

### Error: "KeyError: 'direccion'"

**Causa**: Leads sin campo dirección

**Solución**:
```python
# Agregar campo faltante
python -c "
from database import get_connection
conn = get_connection()
conn.execute('UPDATE leads SET direccion = \"Sin dirección\" WHERE direccion IS NULL')
conn.commit()
print('Direcciones actualizadas')
"
```

---

## 🤖 Problemas de IA

### Análisis muy lento

**Causa**: Límite de API de Gemini (15 req/min)

**Solución**:
- Buscar en lotes pequeños (5-10 leads)
- Esperar 1-2 minutos entre búsquedas
- Considerar API key de pago para más límite

### Scores incorrectos

**Causa**: Análisis de IA no preciso

**Solución**:
```python
# Ajustar scores manualmente en database
from database import update_lead
update_lead(lead_id=123, data={'score_ia': 8})
```

### Error: "Rate limit exceeded"

**Causa**: Demasiadas peticiones a Gemini

**Solución**:
```bash
# Esperar 1 minuto
sleep 60

# Reintentar con menos leads
```

---

## 🔍 Diagnóstico General

### Script de verificación completa

```bash
python verificar_sistema.py
```

**Debe mostrar**:
```
✅ OK         Estructura
✅ OK         Dependencias
✅ OK         Configuración
✅ OK         Base de datos
✅ OK         Playwright
```

### Verificación manual paso a paso

```bash
# 1. Python
python --version
# Debe ser 3.8 o superior

# 2. Dependencias
pip list | grep streamlit
pip list | grep playwright
pip list | grep google-generativeai

# 3. Base de datos
ls -la leads.db
sqlite3 leads.db "SELECT COUNT(*) FROM leads;"

# 4. Configuración
cat .env | grep GEMINI_API_KEY

# 5. Playwright
python -m playwright --version
```

---

## 📊 Logs y Debugging

### Ver logs de Streamlit

```bash
# Ejecutar con logs detallados
streamlit run app.py --logger.level=debug
```

### Ver logs de Playwright

```bash
# Ejecutar scraper con logs
PWDEBUG=1 python scraper.py "hoteles en Pachuca" 5
```

### Ver logs de base de datos

```python
# Agregar al inicio de database.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🆘 Soporte Adicional

### Información para reportar problemas

Al reportar un problema, incluye:

1. **Sistema operativo**: Windows/Mac/Linux
2. **Versión de Python**: `python --version`
3. **Mensaje de error completo**
4. **Pasos para reproducir**
5. **Logs relevantes**

### Comandos útiles para diagnóstico

```bash
# Información del sistema
python verificar_sistema.py

# Versiones de paquetes
pip list

# Estado de la base de datos
python -c "from database import get_stats; print(get_stats())"

# Test de API de Gemini
python -c "
from ai_processor import analyze_lead
lead = {'nombre': 'Test Hotel', 'tipo_negocio': 'hotel', 'direccion': 'Pachuca, Hgo.'}
print(analyze_lead(lead))
"
```

---

## ✅ Checklist de Resolución

Cuando tengas un problema, sigue este orden:

- [ ] Verificar que Python 3.8+ esté instalado
- [ ] Verificar que todas las dependencias estén instaladas
- [ ] Verificar que `.env` exista y tenga GEMINI_API_KEY
- [ ] Verificar que `leads.db` exista
- [ ] Ejecutar `python verificar_sistema.py`
- [ ] Revisar logs de error completos
- [ ] Buscar el error específico en esta guía
- [ ] Reiniciar la aplicación después de cambios

---

## 🔄 Reinstalación Completa

Si nada funciona, reinstalar desde cero:

```bash
# 1. Backup de datos
cp leads.db leads_backup.db
cp .env .env.backup

# 2. Limpiar entorno
rm -rf venv/  # o eliminar carpeta venv
rm -rf __pycache__/
rm -rf src/__pycache__/

# 3. Crear nuevo entorno
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# 4. Reinstalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium

# 5. Restaurar configuración
cp .env.backup .env

# 6. Inicializar BD
python -c "from database import init_db; init_db()"

# 7. Restaurar datos (opcional)
cp leads_backup.db leads.db

# 8. Verificar
python verificar_sistema.py

# 9. Iniciar
streamlit run app.py
```

---

**¿Aún tienes problemas?** Ejecuta:

```bash
python verificar_sistema.py > diagnostico.txt
```

Y revisa el archivo `diagnostico.txt` para más detalles.

---

**CySlean Lead Solar** | Troubleshooting Guide | 2024

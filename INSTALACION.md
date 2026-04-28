# 📦 Guía de Instalación - CySlean Lead Solar

Guía detallada paso a paso para instalar y configurar el sistema.

---

## 📋 Requisitos Previos

### Sistema Operativo
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+, Debian, etc.)

### Software Requerido
- **Python 3.8 o superior** (recomendado 3.10+)
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar repositorio)
- **Navegador web** (Chrome, Edge, o Firefox)

### Verificar Python

```bash
# Verificar versión de Python
python --version
# o
python3 --version

# Debe mostrar: Python 3.8.x o superior
```

Si no tienes Python instalado:
- **Windows**: https://www.python.org/downloads/
- **macOS**: `brew install python3`
- **Linux**: `sudo apt install python3 python3-pip`

---

## 🚀 Instalación Paso a Paso

### Paso 1: Obtener el Código

#### Opción A: Clonar con Git (recomendado)

```bash
git clone https://github.com/tu-usuario/cyslean-lead-solar.git
cd cyslean-lead-solar
```

#### Opción B: Descargar ZIP

1. Descargar el archivo ZIP del proyecto
2. Extraer en una carpeta
3. Abrir terminal en esa carpeta

```bash
cd ruta/a/cyslean-lead-solar
```

---

### Paso 2: Crear Entorno Virtual (Recomendado)

Un entorno virtual aísla las dependencias del proyecto.

#### Windows

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Verás (venv) al inicio de la línea de comandos
```

#### macOS / Linux

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Verás (venv) al inicio de la línea de comandos
```

**Nota**: Para desactivar el entorno virtual más tarde, usa `deactivate`

---

### Paso 3: Instalar Dependencias de Python

```bash
# Actualizar pip (recomendado)
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

**Dependencias que se instalarán**:
- streamlit (interfaz web)
- pandas (procesamiento de datos)
- playwright (scraping)
- google-generativeai (IA)
- pywhatkit (WhatsApp)
- folium (mapas)
- streamlit-folium (integración mapas)
- python-dotenv (variables de entorno)
- pyairtable (opcional, para Airtable)

**Tiempo estimado**: 2-5 minutos

---

### Paso 4: Instalar Navegador para Playwright

Playwright necesita un navegador para hacer scraping.

#### Opción 1: Chromium (Recomendado)

```bash
python -m playwright install chromium
```

#### Opción 2: Microsoft Edge (Windows)

```bash
python -m playwright install msedge
```

#### Opción 3: Todos los navegadores

```bash
python -m playwright install
```

**Tiempo estimado**: 1-3 minutos

---

### Paso 5: Configurar Variables de Entorno

#### 5.1 Copiar archivo de ejemplo

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

#### 5.2 Obtener API Key de Google Gemini

1. Ir a: https://aistudio.google.com/
2. Iniciar sesión con cuenta de Google
3. Click en "Get API Key"
4. Crear nueva API key
5. Copiar la key (empieza con `AIzaSy...`)

#### 5.3 Editar archivo .env

Abrir `.env` con un editor de texto y agregar tu API key:

```env
GEMINI_API_KEY=AIzaSyC...tu_key_aqui

# Opcional: Configuración de Airtable
AIRTABLE_API_KEY=
AIRTABLE_BASE_ID=
AIRTABLE_TABLE_NAME=Leads
```

**Importante**: 
- ✅ La API key de Gemini es **GRATIS**
- ✅ Límite: 15 requests/minuto, 1500/día
- ✅ Suficiente para uso normal

---

### Paso 6: Inicializar Base de Datos

```bash
python -c "from database import init_db; init_db()"
```

**Resultado esperado**:
```
Base de datos inicializada
```

Esto crea el archivo `leads.db` con la estructura necesaria.

---

### Paso 7: Verificar Instalación

```bash
python verificar_sistema.py
```

**Resultado esperado**:
```
🔍 Verificando dependencias...
  ✅ streamlit
  ✅ pandas
  ✅ playwright
  ✅ google-generativeai
  ✅ pywhatkit
  ✅ folium
  ✅ streamlit-folium
  ✅ python-dotenv
  ✅ pyairtable
✅ Todas las dependencias instaladas

🔍 Verificando configuración .env...
  ✅ GEMINI_API_KEY - Configurada
✅ Configuración .env correcta

🔍 Verificando base de datos...
  ✅ Base de datos inicializada
  📊 Leads en sistema: 0

🔍 Verificando Playwright (scraper)...
  ✅ Playwright instalado

📋 RESUMEN
  ✅ OK         Estructura
  ✅ OK         Dependencias
  ✅ OK         Configuración
  ✅ OK         Base de datos
  ✅ OK         Playwright

🎉 ¡Sistema listo para usar!

📝 Para iniciar la aplicación:
   streamlit run app.py
```

---

### Paso 8: Ejecutar Pruebas (Opcional)

```bash
python test_sistema.py
```

Esto ejecuta pruebas unitarias de cada componente.

---

## 🎯 Primer Uso

### 1. Iniciar la Aplicación

```bash
streamlit run app.py
```

**Resultado**:
- Se abrirá automáticamente en tu navegador
- URL: http://localhost:8501
- Si no abre, copia la URL de la terminal

### 2. Hacer Primera Búsqueda

1. En el sidebar, ingresa: **"hoteles en Pachuca"**
2. Ajusta resultados a: **5**
3. Click en **🚀 Buscar**
4. Espera 30-60 segundos
5. Verás los leads en el Dashboard

### 3. Revisar Resultados

- **Dashboard**: Métricas y mapa
- **Pipeline**: Tabla de leads
- Verifica que los datos sean correctos

### 4. Configurar WhatsApp (Opcional)

1. Abrir https://web.whatsapp.com
2. Escanear código QR con tu teléfono
3. Mantener la pestaña abierta
4. En la app, click en **📤 WhatsApp**

---

## 🔧 Solución de Problemas Comunes

### Error: "python: command not found"

**Solución**: Usar `python3` en lugar de `python`

```bash
python3 --version
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

### Error: "pip: command not found"

**Solución**: Instalar pip

```bash
# Windows
python -m ensurepip --upgrade

# macOS
python3 -m ensurepip --upgrade

# Linux
sudo apt install python3-pip
```

### Error: "Permission denied"

**Solución**: Usar permisos de administrador

```bash
# Windows (ejecutar terminal como Administrador)
# macOS / Linux
sudo pip install -r requirements.txt
```

### Error: "playwright install failed"

**Solución**: Instalar dependencias del sistema

```bash
# Ubuntu / Debian
sudo apt-get install libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2

# macOS (instalar Homebrew primero)
brew install playwright

# Windows (generalmente no necesita nada extra)
```

### Error: "Module not found"

**Solución**: Verificar que el entorno virtual esté activado

```bash
# Debe aparecer (venv) al inicio de la línea
# Si no aparece, activar:

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Luego reinstalar
pip install -r requirements.txt
```

---

## 📱 Configuración de WhatsApp

### Requisitos
- Teléfono con WhatsApp instalado
- Conexión a internet estable
- WhatsApp Web abierto en navegador

### Pasos

1. **Abrir WhatsApp Web**
   ```
   https://web.whatsapp.com
   ```

2. **Escanear código QR**
   - Abrir WhatsApp en tu teléfono
   - Ir a Configuración > Dispositivos vinculados
   - Escanear código QR de la pantalla

3. **Mantener sesión abierta**
   - No cerrar la pestaña de WhatsApp Web
   - Mantener el teléfono conectado a internet

4. **Probar envío**
   ```bash
   python messenger.py
   ```

---

## 🔐 Seguridad

### Proteger Datos Sensibles

```bash
# Verificar que .gitignore incluya:
.env
leads.db
*.db
```

### Backup de Base de Datos

```bash
# Crear backup
cp leads.db leads_backup_$(date +%Y%m%d).db

# Windows
copy leads.db leads_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db
```

### Rotar API Keys

Si tu API key se compromete:
1. Ir a https://aistudio.google.com/
2. Revocar key antigua
3. Crear nueva key
4. Actualizar en `.env`

---

## 📚 Siguientes Pasos

Después de la instalación:

1. **Leer documentación**
   ```bash
   # Guía rápida
   cat GUIA_RAPIDA.md
   
   # Documentación completa
   cat README.md
   ```

2. **Hacer pruebas**
   - Buscar 5 leads de prueba
   - Revisar Dashboard
   - Probar filtros en Pipeline

3. **Configurar flujo de trabajo**
   - Definir búsquedas objetivo
   - Establecer horarios de envío
   - Configurar backups

---

## 🆘 Obtener Ayuda

### Recursos

- **README.md**: Documentación completa
- **GUIA_RAPIDA.md**: Inicio rápido
- **TROUBLESHOOTING.md**: Solución de problemas
- **RESUMEN_SISTEMA.md**: Arquitectura del sistema

### Comandos de Diagnóstico

```bash
# Verificación completa
python verificar_sistema.py

# Pruebas unitarias
python test_sistema.py

# Información del sistema
python --version
pip list
```

### Reportar Problemas

Al reportar un problema, incluye:

1. Sistema operativo y versión
2. Versión de Python (`python --version`)
3. Mensaje de error completo
4. Pasos para reproducir
5. Salida de `python verificar_sistema.py`

---

## ✅ Checklist de Instalación

Marca cada paso completado:

- [ ] Python 3.8+ instalado
- [ ] Código descargado/clonado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Playwright instalado (`python -m playwright install chromium`)
- [ ] Archivo `.env` creado y configurado
- [ ] API key de Gemini obtenida y agregada
- [ ] Base de datos inicializada
- [ ] Verificación exitosa (`python verificar_sistema.py`)
- [ ] Aplicación iniciada (`streamlit run app.py`)
- [ ] Primera búsqueda realizada
- [ ] WhatsApp Web configurado (opcional)

---

## 🎉 ¡Instalación Completa!

Si todos los pasos están marcados, tu sistema está listo.

**Iniciar aplicación**:
```bash
streamlit run app.py
```

**O usar script de inicio**:
```bash
python iniciar.py
```

---

**CySlean Lead Solar** | Guía de Instalación | v1.0 | 2024

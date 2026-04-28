# 🚀 Guía Rápida - CySlean Lead Solar

## ⚡ Inicio en 3 Pasos

### 1️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 2️⃣ Configurar API Key

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu key
# Obtén tu key gratis en: https://aistudio.google.com/
```

### 3️⃣ Iniciar Aplicación

```bash
# Opción A: Script de inicio
python iniciar.py

# Opción B: Directo
streamlit run app.py
```

---

## 📱 Flujo de Trabajo Completo

### 🔍 Paso 1: Buscar Leads

1. Abre la aplicación web
2. En el sidebar, ingresa búsqueda: **"hoteles en Pachuca"**
3. Ajusta resultados: **5-10** (recomendado)
4. Click **🚀 Buscar**

**Resultado**: Leads guardados automáticamente con:
- ✅ Score de IA (1-10)
- ✅ Ahorro mensual calculado
- ✅ Estado clasificado (Nuevo/Sin teléfono/No WhatsApp)

---

### 📊 Paso 2: Revisar Dashboard

**Métricas principales**:
- 💰 **Ahorro Total**: Potencial de ahorro mensual
- ⚡ **kWp Total**: Capacidad total de sistemas
- 🔥 **Premium**: Leads con score ≥ 8
- ⭐ **Score Promedio**: Calidad general

**Mapa**: Visualiza distribución geográfica de leads

---

### 📋 Paso 3: Filtrar en Pipeline

1. Cambiar a vista **"📋 Pipeline de Leads"**
2. Filtrar por:
   - **Estado**: Nuevo, Contactado, etc.
   - **Score mínimo**: 4+ recomendado
   - **Búsqueda**: Por nombre

3. **Exportar**: Descargar CSV para análisis externo

---

### 📤 Paso 4: Enviar WhatsApp

#### Desde la App Web:

1. Abre **WhatsApp Web** en tu navegador
2. Inicia sesión
3. En la app, click **"📤 WhatsApp (X)"**
4. Revisa cada mensaje
5. Confirma envío

#### Desde Terminal (Avanzado):

```bash
python messenger.py
```

**Opciones**:
- **Modo 1 (Preview)**: Revisas cada mensaje
- **Modo 2 (Auto)**: Envío automático

**Resultado**: Leads cambian a estado **"Contactado"**

---

## 🎯 Clasificación de Estados

| Estado | Significado | Acción |
|--------|-------------|--------|
| 🆕 **Nuevo** | Tiene teléfono válido | ✅ Listo para contactar |
| 📵 **Sin teléfono** | No tiene número | 🔍 Buscar manualmente |
| ❌ **No WhatsApp** | Teléfono inválido | 📧 Usar otro canal |
| ✅ **Contactado** | Mensaje enviado | ⏳ Esperar respuesta |
| ⭐ **Calificado** | Score ≥ 8 | 🔥 Priorizar |

---

## 💡 Tips y Mejores Prácticas

### ✅ Búsquedas Efectivas

**Buenas búsquedas**:
- ✅ "hoteles en Pachuca"
- ✅ "lavanderías en Monterrey"
- ✅ "gimnasios en Guadalajara"

**Malas búsquedas**:
- ❌ "hoteles" (muy genérico)
- ❌ "negocios" (sin contexto)

### ✅ Cantidad de Resultados

- **5-10 leads**: Calidad alta, revisión manual
- **20-30 leads**: Balance calidad/cantidad
- **50 leads**: Cantidad máxima, más ruido

### ✅ Envío de WhatsApp

- ⏰ **Horario**: 9am - 7pm (mejor respuesta)
- 📊 **Límite**: Máximo 50 mensajes/hora
- ⏳ **Espera**: 12 segundos entre mensajes
- 👀 **Preview**: Siempre revisa antes de enviar

### ✅ Mantenimiento

```bash
# Limpiar leads "Nuevo" que no sirven
# Desde la app: Admin > 🗑️ Borrar Nuevos

# Backup de base de datos
cp leads.db leads_backup_$(date +%Y%m%d).db
```

---

## 🔧 Solución Rápida de Problemas

### ❌ Error: "No module named 'playwright'"

```bash
pip install playwright
python -m playwright install chromium
```

### ❌ Error: "GEMINI_API_KEY not found"

1. Verifica que `.env` exista
2. Abre `.env` y agrega tu key
3. Reinicia la aplicación

### ❌ WhatsApp no envía

1. ✅ WhatsApp Web abierto y logueado
2. ✅ Números con 10 dígitos
3. ✅ Espera 12 segundos entre mensajes

### ❌ Scraper no encuentra nada

```bash
# Reinstalar navegador
python -m playwright install chromium --force

# O usar Edge (Windows)
python -m playwright install msedge
```

---

## 📞 Verificación del Sistema

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

🎉 ¡Sistema listo para usar!
```

---

## 🎓 Ejemplos de Uso

### Ejemplo 1: Hoteles en Pachuca

```
1. Búsqueda: "hoteles en Pachuca"
2. Resultados: 10
3. Leads encontrados: 8
4. Con teléfono: 6
5. Score ≥ 4: 5
6. Enviados: 5
7. Contactados: 5
```

### Ejemplo 2: Lavanderías en CDMX

```
1. Búsqueda: "lavanderías en Ciudad de México"
2. Resultados: 20
3. Leads encontrados: 18
4. Con teléfono: 15
5. Score ≥ 4: 14 (lavanderías = score alto)
6. Enviados: 14
7. Contactados: 14
```

---

## 📊 Métricas de Éxito

### Por Tipo de Negocio

| Tipo | Score Típico | Ahorro Mensual | Sistema kWp |
|------|--------------|----------------|-------------|
| Lavandería | 9-10 | $15,000-$30,000 | 40-80 kWp |
| Hotel | 8-9 | $20,000-$50,000 | 50-120 kWp |
| Gimnasio | 7-8 | $10,000-$25,000 | 30-60 kWp |
| Restaurante | 6-7 | $8,000-$15,000 | 20-40 kWp |

---

## 🚨 Límites y Restricciones

### API de Gemini (Gratis)
- ⚠️ 15 requests/minuto
- ⚠️ 1,500 requests/día
- 💡 Solución: Buscar en lotes pequeños

### WhatsApp
- ⚠️ 50 mensajes/hora (recomendado)
- ⚠️ 12 segundos entre mensajes
- 💡 Solución: Enviar en varias sesiones

### Google Maps Scraping
- ⚠️ Uso ético y responsable
- ⚠️ No abusar del scraping
- 💡 Solución: Búsquedas específicas

---

## 📚 Recursos Adicionales

- 📖 **README.md**: Documentación completa
- 🔧 **verificar_sistema.py**: Diagnóstico
- 🚀 **iniciar.py**: Inicio rápido
- 📱 **WHATSAPP_GUIDE.md**: Guía de WhatsApp
- 🛠️ **WHATSAPP_TECHNICAL.md**: Detalles técnicos

---

## ✅ Checklist de Inicio

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Playwright instalado (`python -m playwright install chromium`)
- [ ] Archivo `.env` configurado con GEMINI_API_KEY
- [ ] Base de datos inicializada
- [ ] WhatsApp Web abierto (para envío)
- [ ] Aplicación funcionando (`streamlit run app.py`)

---

**¿Listo para empezar?** 🚀

```bash
python iniciar.py
```

---

**CySlean Lead Solar** | Versión 1.0 | 2024

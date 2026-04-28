# 📖 Cómo Usar CySlean Lead Solar

## 🚀 Inicio Rápido

### Para Enviar WhatsApp (Ejecutar Localmente):

#### **Opción 1: Primera Vez o Inicio Normal**
1. **Doble click** en: `iniciar_app.bat`
2. Espera 3 segundos
3. Se abrirá el navegador automáticamente en: http://localhost:8501
4. Si no abre, copia esa URL y pégala en tu navegador
5. Ingresa contraseña: `Agente.CySlean1`

#### **Opción 2: Si Ya Está Corriendo**
1. **Doble click** en: `reiniciar_app.bat`
2. Esto detendrá la versión anterior y abrirá una nueva
3. Se abrirá el navegador automáticamente

#### **Opción 3: Abrir Manualmente**
Si el script ya está corriendo pero cerraste el navegador:
1. Abre tu navegador
2. Ve a: `http://localhost:8501`
3. ¡Listo!

---

## 🛑 Detener la Aplicación

### **Opción 1: Desde la Ventana Negra (Terminal)**
1. Click en la ventana negra donde está corriendo
2. Presiona `Ctrl + C`
3. Confirma con `S` o `Y`

### **Opción 2: Usar el Script**
1. **Doble click** en: `detener_app.bat`
2. Detendrá todos los procesos de Streamlit

### **Opción 3: Cerrar la Ventana**
1. Simplemente cierra la ventana negra (terminal)
2. El proceso se detendrá automáticamente

---

## 🌐 Dos Formas de Usar la App

### **1. Local (En Tu Computadora)** 💻

**Cuándo usar:**
- ✅ Cuando necesites enviar WhatsApp
- ✅ Cuando estés en casa/oficina
- ✅ Para trabajo con datos sensibles

**Cómo iniciar:**
- Doble click en `iniciar_app.bat`
- O ejecuta: `streamlit run app.py`

**URL:** http://localhost:8501

---

### **2. Streamlit Cloud (En Internet)** 🌍

**Cuándo usar:**
- ✅ Consultar leads desde cualquier lugar
- ✅ Gestionar pipeline remotamente
- ✅ Filtrar y descargar datos
- ❌ **NO para enviar WhatsApp**

**Cómo acceder:**
- Ve a tu URL de Streamlit Cloud
- Ingresa contraseña: `Agente.CySlean1`

---

## 📱 Funcionalidades Disponibles

### **En Ambas Versiones:**
- ✅ Ver dashboard con métricas
- ✅ Mapa interactivo de leads
- ✅ Gráficos de pipeline
- ✅ Buscar nuevos leads (scraping)
- ✅ Filtrar por estado, tipo, score
- ✅ Gestionar estados del pipeline
- ✅ Descargar CSV
- ✅ Eliminar leads sin teléfono
- ✅ Calificar leads automáticamente

### **Solo en Versión Local:**
- ✅ **Enviar mensajes de WhatsApp**

---

## 🔧 Solución de Problemas

### **Problema: "Pide click en alguna letra y no abre navegador"**

**Solución 1:** Abrir manualmente
```
1. Abre tu navegador
2. Ve a: http://localhost:8501
```

**Solución 2:** Reiniciar
```
1. Doble click en: reiniciar_app.bat
2. Esto detendrá el anterior y abrirá uno nuevo
```

**Solución 3:** Detener y volver a iniciar
```
1. Doble click en: detener_app.bat
2. Espera 5 segundos
3. Doble click en: iniciar_app.bat
```

---

### **Problema: "No se puede activar el entorno virtual"**

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### **Problema: "streamlit no se reconoce"**

**Solución:**
```powershell
# Activar entorno virtual primero
.venv\Scripts\Activate.ps1

# Luego ejecutar
streamlit run app.py
```

---

### **Problema: "WhatsApp no funciona"**

**Verificar:**
1. ¿Estás usando la versión LOCAL? (no Streamlit Cloud)
2. ¿Tienes WhatsApp Desktop instalado?
3. ¿WhatsApp Web está activo en tu navegador?

---

## 📋 Archivos Útiles

| Archivo | Función |
|---------|---------|
| `iniciar_app.bat` | Inicia la app normalmente |
| `reiniciar_app.bat` | Detiene y reinicia la app |
| `detener_app.bat` | Detiene todos los procesos |
| `INICIO_RAPIDO.md` | Guía rápida de inicio |
| `SEGURIDAD.md` | Información de seguridad |
| `EJECUTAR_LOCAL.md` | Detalles de ejecución local |

---

## 🔑 Contraseña

**Contraseña única:** `Agente.CySlean1`

(Funciona en ambas versiones: local y cloud)

---

## ✅ Checklist de Uso Diario

### **Para Enviar WhatsApp:**
- [ ] Doble click en `iniciar_app.bat`
- [ ] Esperar a que abra el navegador (o abrir http://localhost:8501)
- [ ] Ingresar contraseña
- [ ] Usar botón de WhatsApp
- [ ] Al terminar, cerrar ventana negra o usar `detener_app.bat`

### **Para Consultas Remotas:**
- [ ] Abrir Streamlit Cloud en navegador
- [ ] Ingresar contraseña
- [ ] Consultar y gestionar leads
- [ ] Cerrar pestaña cuando termines

---

## 💡 Tips

1. **Deja la ventana negra abierta** mientras uses la app
2. **No cierres el navegador** si vas a seguir usando la app
3. **Si cerraste el navegador**, solo abre http://localhost:8501 de nuevo
4. **Para WhatsApp**, siempre usa la versión local
5. **Para consultas rápidas**, usa Streamlit Cloud

---

¡Eso es todo! Ahora sabes cómo usar tu app perfectamente. 🎉

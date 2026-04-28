# 🚀 Cómo Ejecutar la App Localmente para WhatsApp

## ¿Por Qué Ejecutar Localmente?

La funcionalidad de WhatsApp **requiere acceso a tu computadora** porque:
- Usa WhatsApp Desktop instalado en tu PC
- Abre URLs de WhatsApp Web desde tu navegador local
- No puede funcionar desde Streamlit Cloud (servidor remoto)

---

## 📋 Pasos para Ejecutar Localmente

### 1. Abrir Terminal en la Carpeta del Proyecto

**Opción A: Desde el Explorador de Archivos**
1. Abre la carpeta del proyecto en el Explorador
2. Click derecho en un espacio vacío
3. Selecciona "Abrir en Terminal" o "Git Bash Here"

**Opción B: Desde PowerShell**
```powershell
cd C:\Users\proyectos.lean\Desktop\Codigos.py\solar_leads_system
```

### 2. Activar el Entorno Virtual

```powershell
.venv\Scripts\Activate.ps1
```

Si da error de permisos, ejecuta primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Ejecutar la App

```powershell
streamlit run app.py
```

### 4. Acceder a la App

- Se abrirá automáticamente en tu navegador
- O ve a: http://localhost:8501
- Ingresa la contraseña: `Agente.CySlean1`

---

## ✅ Ventajas de Ejecutar Localmente

✅ **WhatsApp funciona perfectamente** - Acceso directo a WhatsApp Desktop  
✅ **Base de datos persistente** - Los datos no se pierden  
✅ **Más rápido** - No depende de internet  
✅ **Sin límites** - No hay restricciones de recursos  
✅ **Gratis** - No necesitas servicios de pago  

---

## 🌐 ¿Cuándo Usar Streamlit Cloud?

Usa la versión en Streamlit Cloud para:
- ✅ Ver el dashboard desde cualquier lugar
- ✅ Consultar leads y estadísticas
- ✅ Filtrar y descargar datos
- ✅ Gestionar el pipeline (cambiar estados)
- ✅ Buscar nuevos leads (scraping)

**NO uses Streamlit Cloud para:**
- ❌ Enviar mensajes de WhatsApp (no funcionará)

---

## 🔄 Flujo de Trabajo Recomendado

### Para Consultar y Gestionar:
1. Usa **Streamlit Cloud** desde cualquier lugar
2. Revisa leads, filtra, gestiona pipeline
3. Descarga datos si necesitas

### Para Enviar WhatsApp:
1. Abre la app **localmente** en tu computadora
2. Usa el botón de WhatsApp
3. Los mensajes se enviarán desde tu WhatsApp Desktop

---

## 🚀 Script Rápido para Iniciar

Puedes usar el archivo `iniciar_app.bat` que ya tienes:

1. Doble click en `iniciar_app.bat`
2. Se abrirá la app automáticamente
3. ¡Listo para usar WhatsApp!

---

## 💡 Tip: Mantener Ambas Versiones

- **Streamlit Cloud**: Para consultas remotas y gestión
- **Local**: Para envío de WhatsApp y trabajo con datos sensibles

Ambas versiones comparten el mismo código, solo cambia dónde se ejecutan.

---

## 🆘 Solución de Problemas

### Error: "streamlit no se reconoce"
```powershell
# Asegúrate de activar el entorno virtual primero
.venv\Scripts\Activate.ps1
```

### Error: "No se puede ejecutar scripts"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### La app no abre automáticamente
- Ve manualmente a: http://localhost:8501

### WhatsApp no funciona
- Asegúrate de tener WhatsApp Desktop instalado
- Verifica que WhatsApp Web esté activo en tu navegador

---

## ✅ Resumen

**Para WhatsApp**: Ejecuta localmente con `streamlit run app.py`  
**Para Consultas**: Usa Streamlit Cloud desde cualquier lugar  
**Contraseña**: `Agente.CySlean1` (funciona en ambas versiones)

¡Así tienes lo mejor de ambos mundos! 🎉

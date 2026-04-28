# 🚀 Inicio Rápido - CySlean Lead Solar

## 📱 Para Enviar Mensajes de WhatsApp

WhatsApp **solo funciona ejecutando la app localmente** en tu computadora.

### Opción 1: Doble Click (MÁS FÁCIL)

1. **Doble click** en el archivo: `iniciar_app.bat`
2. Espera a que se abra el navegador
3. Ingresa contraseña: `Agente.CySlean1`
4. ¡Listo! Ahora puedes enviar WhatsApp

### Opción 2: Desde Terminal

```powershell
# 1. Activar entorno virtual
.venv\Scripts\Activate.ps1

# 2. Ejecutar app
streamlit run app.py
```

---

## 🌐 Para Consultar Datos Remotamente

Usa la versión en Streamlit Cloud:
- Accede desde cualquier lugar
- Consulta leads y estadísticas
- Gestiona el pipeline
- Filtra y descarga datos

**NO uses Streamlit Cloud para WhatsApp** - no funcionará

---

## 🔄 Flujo de Trabajo Recomendado

### Desde Casa/Oficina (Con WhatsApp):
1. Doble click en `iniciar_app.bat`
2. Usa todas las funciones incluyendo WhatsApp

### Desde Cualquier Lugar (Sin WhatsApp):
1. Abre Streamlit Cloud en tu navegador
2. Consulta y gestiona leads
3. Descarga datos si necesitas

---

## ✅ Ventajas de Ejecutar Localmente

✅ **WhatsApp funciona** - Envío directo desde tu PC  
✅ **Gratis** - Sin costos de APIs  
✅ **Rápido** - No depende de internet  
✅ **Datos persistentes** - No se pierden al reiniciar  
✅ **Sin límites** - Envía todos los mensajes que necesites  

---

## 🆘 Problemas Comunes

### "No se puede ejecutar scripts"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "streamlit no se reconoce"
Asegúrate de activar el entorno virtual primero:
```powershell
.venv\Scripts\Activate.ps1
```

### WhatsApp no abre
- Verifica que WhatsApp Desktop esté instalado
- O usa WhatsApp Web en tu navegador

---

## 📞 Contraseña

**Contraseña**: `Agente.CySlean1`

(Funciona tanto en local como en Streamlit Cloud)

---

¡Eso es todo! Ahora puedes usar WhatsApp sin problemas. 🎉

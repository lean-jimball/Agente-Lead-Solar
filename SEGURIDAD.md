# 🔐 Configuración de Seguridad - CySlean Lead Solar

## ✅ Sistema de Autenticación Implementado

Tu aplicación ahora está protegida con un sistema de autenticación por contraseña. Nadie podrá acceder sin la contraseña correcta.

---

## 🔑 Configurar tu Contraseña en Streamlit Cloud

### Paso 1: Ir a Settings de tu App

1. Ve a tu app en Streamlit Cloud: https://share.streamlit.io/
2. Click en tu app **"Agente-Lead-Solar"**
3. Click en el menú **"⚙️ Settings"** (arriba a la derecha)
4. Selecciona **"Secrets"**

### Paso 2: Agregar la Contraseña

En el editor de Secrets, agrega:

```toml
# Contraseña de acceso (CÁMBIALA por una segura)
APP_PASSWORD = "TuContraseñaSegura123!"

# API Key de Google Gemini (si la tienes)
GEMINI_API_KEY = "tu_api_key_aqui"
```

### Paso 3: Guardar

1. Click en **"Save"**
2. La app se reiniciará automáticamente
3. Ahora necesitarás la contraseña para acceder

---

## 🔒 Contraseña por Defecto

Si NO configuras `APP_PASSWORD` en Secrets, la contraseña por defecto es:

```
CySlean2024!
```

⚠️ **IMPORTANTE**: Cambia esta contraseña inmediatamente en Streamlit Cloud Secrets.

---

## 🛡️ Características de Seguridad

### ✅ Lo que está protegido:

- ✅ Acceso completo a la aplicación
- ✅ Visualización de leads
- ✅ Envío de mensajes de WhatsApp
- ✅ Búsqueda y scraping de nuevos leads
- ✅ Gestión del pipeline
- ✅ Descarga de datos

### ✅ Cómo funciona:

1. **Pantalla de Login**: Al entrar a la app, aparece una pantalla de login
2. **Contraseña Hasheada**: La contraseña se encripta con SHA256
3. **Sesión Persistente**: Una vez autenticado, la sesión permanece activa
4. **Sin Acceso = Sin Datos**: Si no ingresas la contraseña correcta, no se carga nada

---

## 🔐 Mejores Prácticas de Seguridad

### 1. **Usa una Contraseña Fuerte**
```
❌ Mala: 123456, password, cyslean
✅ Buena: Cy$L3an!S0l4r#2024_Mx
```

### 2. **No Compartas la Contraseña**
- Solo compártela con personas de confianza
- Usa un gestor de contraseñas (LastPass, 1Password, Bitwarden)

### 3. **Cambia la Contraseña Regularmente**
- Cada 3-6 meses
- Si sospechas que fue comprometida

### 4. **No Subas Secrets a GitHub**
- ✅ El archivo `.env` ya está en `.gitignore`
- ✅ Los secrets solo están en Streamlit Cloud
- ❌ NUNCA hagas commit de contraseñas

---

## 🚨 Si Olvidas tu Contraseña

1. Ve a Streamlit Cloud Settings → Secrets
2. Cambia el valor de `APP_PASSWORD`
3. Guarda y la app se reiniciará
4. Usa la nueva contraseña

---

## 🔄 Cerrar Sesión

Para cerrar sesión y volver a la pantalla de login:

1. Cierra la pestaña del navegador
2. Borra las cookies del sitio
3. O espera a que expire la sesión (al cerrar el navegador)

---

## 📱 Seguridad de WhatsApp

### ⚠️ Consideraciones Importantes:

1. **WhatsApp Desktop**: La app usa tu WhatsApp Desktop instalado
2. **Sesión Local**: Los mensajes se envían desde tu computadora
3. **No se Almacenan Credenciales**: No guardamos tu número ni contraseña de WhatsApp
4. **Control Manual**: Puedes revisar cada mensaje antes de enviarlo

### 🛡️ Recomendaciones:

- ✅ Usa el modo "Preview" para revisar mensajes antes de enviar
- ✅ No dejes la app abierta en computadoras públicas
- ✅ Cierra WhatsApp Desktop cuando no lo uses
- ✅ Revisa los leads antes de enviar mensajes masivos

---

## 🔐 Seguridad de Datos

### Base de Datos:

- **SQLite Local**: Los datos se almacenan en `leads.db`
- **No Persistente en Streamlit Cloud**: La base de datos se reinicia con cada deploy
- **Para Producción**: Considera migrar a PostgreSQL o Supabase

### Datos Sensibles:

- ✅ Teléfonos de clientes
- ✅ Direcciones
- ✅ Información de negocios
- ✅ Scores de IA

**Recomendación**: Para datos críticos de producción, usa una base de datos externa persistente.

---

## 📞 Soporte

Si tienes problemas con la autenticación:

1. Verifica que `APP_PASSWORD` esté configurado en Secrets
2. Asegúrate de no tener espacios extra en la contraseña
3. Prueba con la contraseña por defecto: `CySlean2024!`
4. Revisa los logs en Streamlit Cloud para errores

---

## ✅ Checklist de Seguridad

Antes de usar la app en producción:

- [ ] Cambié la contraseña por defecto en Streamlit Cloud Secrets
- [ ] Configuré `GEMINI_API_KEY` si uso IA
- [ ] Probé el login con la nueva contraseña
- [ ] No compartí la contraseña públicamente
- [ ] Cerré sesión después de usar la app
- [ ] Configuré una base de datos persistente (opcional)
- [ ] Revisé que `.env` no esté en GitHub

---

🎉 **¡Tu aplicación ahora está protegida!** Solo las personas con la contraseña podrán acceder.

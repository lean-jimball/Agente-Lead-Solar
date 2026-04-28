# 🔄 Configuración de Sincronización con Supabase

Esta guía te ayudará a configurar la sincronización automática de la base de datos entre localhost y Streamlit Cloud usando Supabase (PostgreSQL gratuito).

## 📋 **¿Qué es Supabase?**

Supabase es una alternativa open-source a Firebase que ofrece:
- ✅ PostgreSQL gratuito (hasta 500 MB)
- ✅ Sincronización automática
- ✅ Acceso desde localhost y cloud
- ✅ Sin tarjeta de crédito requerida

---

## 🚀 **PASO 1: Crear cuenta en Supabase**

1. Ve a [https://supabase.com](https://supabase.com)
2. Haz clic en "Start your project"
3. Regístrate con GitHub o email
4. Es **GRATIS** - no necesitas tarjeta de crédito

---

## 🗄️ **PASO 2: Crear proyecto**

1. En el dashboard de Supabase, haz clic en "New Project"
2. Completa:
   - **Name:** `cyslean-leads` (o el nombre que prefieras)
   - **Database Password:** Crea una contraseña segura (¡guárdala!)
   - **Region:** Selecciona la más cercana (ej: South America - São Paulo)
   - **Pricing Plan:** Free (gratis)
3. Haz clic en "Create new project"
4. Espera 2-3 minutos mientras se crea el proyecto

---

## 🔑 **PASO 3: Obtener credenciales**

1. En tu proyecto de Supabase, ve a **Settings** (⚙️) en el menú lateral
2. Haz clic en **Database**
3. Busca la sección **Connection string**
4. Selecciona el modo **URI**
5. Copia la URL que se ve así:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
6. **IMPORTANTE:** Reemplaza `[YOUR-PASSWORD]` con la contraseña que creaste en el Paso 2

---

## 💻 **PASO 4: Configurar localhost**

1. En tu carpeta del proyecto, copia el archivo de ejemplo:
   ```bash
   copy .env.supabase.example .env
   ```

2. Abre el archivo `.env` y pega tu URL de conexión:
   ```env
   DATABASE_URL=postgresql://postgres:tu_password@db.xxxxx.supabase.co:5432/postgres
   ```

3. Guarda el archivo

4. Instala el driver de PostgreSQL:
   ```bash
   pip install psycopg2-binary
   ```

5. Ejecuta la aplicación:
   ```bash
   python -m streamlit run app.py
   ```

6. La primera vez, se creará automáticamente la estructura de la base de datos en Supabase

---

## ☁️ **PASO 5: Configurar Streamlit Cloud**

1. Ve a [https://share.streamlit.io](https://share.streamlit.io)
2. Abre tu aplicación (Agente-Lead-Solar)
3. Haz clic en **Settings** (⚙️) → **Secrets**
4. Agrega tu configuración:
   ```toml
   DATABASE_URL = "postgresql://postgres:tu_password@db.xxxxx.supabase.co:5432/postgres"
   ```
5. Haz clic en **Save**
6. La aplicación se reiniciará automáticamente

---

## ✅ **PASO 6: Verificar sincronización**

### Prueba desde localhost:
1. Ejecuta `iniciar_app.bat`
2. Haz una búsqueda de prueba (ej: "hoteles en Pachuca")
3. Verifica que los leads aparezcan en la tabla

### Prueba desde Streamlit Cloud:
1. Abre tu app en el navegador: `https://tu-app.streamlit.app`
2. **¡Los mismos leads deberían aparecer!** 🎉
3. Si haces cambios en cloud, se reflejarán en localhost y viceversa

---

## 🔄 **¿Cómo funciona la sincronización?**

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Localhost  │ ◄─────► │   Supabase   │ ◄─────► │ Cloud (Web) │
│  (tu PC)    │         │  PostgreSQL  │         │  Streamlit  │
└─────────────┘         └──────────────┘         └─────────────┘
```

- **Ambos** (localhost y cloud) se conectan a la **misma base de datos** en Supabase
- **Cambios en tiempo real:** Lo que hagas en uno se ve en el otro
- **Sin duplicados:** La base de datos es única y compartida

---

## 🔐 **Seguridad**

### ⚠️ **IMPORTANTE:**

1. **NUNCA** subas el archivo `.env` a GitHub
   - Ya está en `.gitignore` para protegerte
   
2. **Usa Streamlit Secrets** para la configuración en cloud
   - No pongas credenciales en el código

3. **Contraseña segura** para Supabase
   - Usa letras, números y símbolos

---

## 🆘 **Solución de problemas**

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "connection refused"
- Verifica que la URL de DATABASE_URL sea correcta
- Asegúrate de haber reemplazado `[YOUR-PASSWORD]` con tu contraseña real

### Error: "password authentication failed"
- La contraseña en DATABASE_URL no es correcta
- Ve a Supabase → Settings → Database → Reset password

### Los datos no se sincronizan
- Verifica que ambos (local y cloud) tengan la misma DATABASE_URL
- Revisa que DATABASE_URL esté en Streamlit Secrets (cloud)
- Revisa que DATABASE_URL esté en .env (local)

---

## 📊 **Migrar datos existentes (opcional)**

Si ya tienes leads en SQLite local y quieres migrarlos a Supabase:

1. Asegúrate de tener configurado DATABASE_URL en `.env`
2. Ejecuta el script de migración:
   ```bash
   python migrate_to_supabase.py
   ```
3. Tus leads de SQLite se copiarán a Supabase

---

## 💰 **Límites del plan gratuito**

Supabase Free incluye:
- ✅ 500 MB de base de datos (suficiente para ~50,000 leads)
- ✅ 2 GB de transferencia mensual
- ✅ Sin límite de tiempo
- ✅ Sin tarjeta de crédito

Para este proyecto, el plan gratuito es **más que suficiente**.

---

## 🎯 **Ventajas de usar Supabase**

1. ✅ **Sincronización automática** entre localhost y cloud
2. ✅ **WhatsApp funciona en localhost** con datos sincronizados
3. ✅ **Acceso desde cualquier lugar** a través de Streamlit Cloud
4. ✅ **Backup automático** de tus datos
5. ✅ **Escalable** si crece tu negocio
6. ✅ **Gratis** para siempre (plan básico)

---

## 📞 **¿Necesitas ayuda?**

Si tienes problemas con la configuración, revisa:
1. Que DATABASE_URL esté correctamente configurado
2. Que la contraseña no tenga caracteres especiales sin escapar
3. Que tengas conexión a internet
4. Los logs de error en la terminal

---

## 🔄 **Volver a SQLite local (opcional)**

Si prefieres volver a usar solo SQLite local:

1. Elimina o comenta la línea DATABASE_URL en `.env`
2. Reinicia la aplicación
3. El sistema volverá a usar `leads.db` local automáticamente

---

¡Listo! Con esto tendrás sincronización automática entre localhost y cloud. 🚀

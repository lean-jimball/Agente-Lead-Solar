# 🚀 Guía Rápida: Sincronización Localhost ↔ Cloud

## ✅ **¿Qué se implementó?**

Tu aplicación ahora puede sincronizar automáticamente los datos entre:
- 🏠 **Localhost** (tu computadora)
- ☁️ **Streamlit Cloud** (web)

Ambos compartirán la **misma base de datos** en Supabase (PostgreSQL gratuito).

---

## 📋 **Pasos Rápidos (5 minutos)**

### 1️⃣ **Crear cuenta Supabase** (GRATIS)
- Ve a: https://supabase.com
- Regístrate (sin tarjeta de crédito)
- Crea un proyecto nuevo
- Guarda la contraseña que elijas

### 2️⃣ **Obtener URL de conexión**
- En Supabase: Settings → Database
- Copia la "Connection string" (URI mode)
- Reemplaza `[YOUR-PASSWORD]` con tu contraseña

### 3️⃣ **Configurar Localhost**
```bash
# Crear archivo .env
copy .env.supabase.example .env

# Editar .env y pegar tu URL:
DATABASE_URL=postgresql://postgres:tu_password@db.xxxxx.supabase.co:5432/postgres

# Instalar driver
pip install psycopg2-binary

# Ejecutar app
python -m streamlit run app.py
```

### 4️⃣ **Configurar Streamlit Cloud**
- Ve a: https://share.streamlit.io
- Abre tu app → Settings → Secrets
- Agrega:
```toml
DATABASE_URL = "postgresql://postgres:tu_password@db.xxxxx.supabase.co:5432/postgres"
```
- Save

### 5️⃣ **¡Listo! 🎉**
- Haz una búsqueda en localhost
- Abre la app en cloud
- **¡Los mismos datos aparecerán!**

---

## 🔄 **¿Cómo funciona?**

```
Localhost ←→ Supabase ←→ Cloud
  (tu PC)    (PostgreSQL)   (Web)
```

- **Sincronización automática**
- **Sin configuración adicional**
- **Gratis para siempre** (plan básico)

---

## 📊 **Migrar datos existentes** (opcional)

Si ya tienes leads en SQLite local:

```bash
python migrate_to_supabase.py
```

Esto copiará todos tus leads a Supabase.

---

## 💡 **Ventajas**

✅ WhatsApp funciona en localhost con datos sincronizados  
✅ Acceso desde cualquier lugar vía web  
✅ Backup automático en la nube  
✅ Sin duplicados - base de datos única  
✅ Gratis (hasta 500 MB = ~50,000 leads)

---

## 🆘 **Ayuda**

📖 Guía completa: `SUPABASE_SETUP.md`  
🔧 Problemas: Verifica que DATABASE_URL esté correcto

---

## 🔙 **Volver a SQLite local**

Si prefieres usar solo SQLite:
1. Elimina DATABASE_URL de `.env`
2. Reinicia la app
3. Volverá a usar `leads.db` local

---

¡Disfruta de la sincronización automática! 🚀

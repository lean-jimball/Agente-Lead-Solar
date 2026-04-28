#!/usr/bin/env python3
"""
Script para preparar la aplicación para despliegue
"""
import os
import shutil
import sqlite3

def create_sample_database():
    """Crear una base de datos de ejemplo para el despliegue"""
    print("📊 Creando base de datos de ejemplo...")
    
    # Crear una copia de la base de datos actual pero sin datos sensibles
    if os.path.exists('leads.db'):
        # Crear base de datos de ejemplo con estructura pero sin datos reales
        conn = sqlite3.connect('leads_demo.db')
        
        # Crear las tablas con la misma estructura
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo_negocio TEXT,
                telefono TEXT,
                direccion TEXT,
                poblacion TEXT,
                estado TEXT,
                calificacion REAL DEFAULT 0,
                website TEXT,
                estado_pipeline TEXT DEFAULT 'Nuevo',
                score_ia INTEGER DEFAULT 0,
                razon_score TEXT,
                consumo_estimado INTEGER DEFAULT 0,
                sistema_recomendado REAL DEFAULT 0,
                ahorro_mensual INTEGER DEFAULT 0,
                mensaje_generado TEXT,
                enviado INTEGER DEFAULT 0,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_ultimo_contacto TIMESTAMP,
                fecha_contacto TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_tel ON leads (telefono);
            CREATE INDEX IF NOT EXISTS idx_status ON leads (estado_pipeline);
            CREATE INDEX IF NOT EXISTS idx_score ON leads (score_ia);
        """)
        
        # Insertar algunos datos de ejemplo (ficticios)
        sample_data = [
            ("Lavandería Demo 1", "lavanderias", "+525512345678", "Av. Principal 123, Centro, 42000 Pachuca, Hgo.", "Pachuca", "Hgo.", 4.5, "www.demo1.com", "Nuevo", 8, "Buen potencial", 15000, 24.2, 11025, "", 0),
            ("Hotel Demo Plaza", "hoteles", "+525587654321", "Blvd. Turístico 456, Zona Hotelera, 42100 Pachuca, Hgo.", "Pachuca", "Hgo.", 4.8, "www.hoteldemoplaza.com", "Calificado", 9, "Excelente ubicación", 25000, 35.5, 18500, "", 0),
            ("Restaurante Demo", "restaurantes", "+525555555555", "Calle Gastronómica 789, Centro, 90000 Tlaxcala, Tlax.", "Tlaxcala", "Tlax.", 4.2, "", "Contactado", 7, "Interés moderado", 12000, 18.8, 8575, "", 1),
            ("Tortillería Demo", "tortilleria", "", "Mercado Municipal 101, Popular, 68000 Oaxaca, Oax.", "Oaxaca", "Oax.", 3.8, "", "Sin teléfono", 6, "Requiere validación", 8000, 10.8, 4900, "", 0),
            ("Casino Demo Royal", "casinos", "+525599999999", "Zona Comercial 999, Exclusiva, 29000 Tuxtla, Chis.", "Tuxtla", "Chis.", 4.9, "www.casinodemoroyal.com", "En negociación", 9, "Alto potencial", 30000, 42.0, 22000, "", 0)
        ]
        
        conn.executemany("""
            INSERT INTO leads (
                nombre, tipo_negocio, telefono, direccion, poblacion, estado,
                calificacion, website, estado_pipeline, score_ia, razon_score,
                consumo_estimado, sistema_recomendado, ahorro_mensual, mensaje_generado, enviado
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, sample_data)
        
        conn.commit()
        conn.close()
        print("✅ Base de datos de ejemplo creada: leads_demo.db")
    else:
        print("⚠️ No se encontró leads.db, se creará automáticamente al ejecutar la app")

def create_env_example():
    """Crear archivo .env.example"""
    print("📝 Creando .env.example...")
    
    env_example = """# Configuración de la aplicación CySlean Lead Solar
# Copia este archivo como .env y completa con tus valores reales

# API Keys (opcional - para funcionalidades avanzadas)
GOOGLE_API_KEY=tu_google_api_key_aqui
AIRTABLE_API_KEY=tu_airtable_api_key_aqui
AIRTABLE_BASE_ID=tu_airtable_base_id_aqui

# Configuración de la aplicación
APP_TITLE=CySlean Lead Solar
APP_ICON=☀️
DEBUG=False

# Base de datos (para producción usar PostgreSQL)
DATABASE_URL=sqlite:///leads.db

# Configuración de WhatsApp (opcional)
WHATSAPP_ENABLED=True
"""
    
    with open('.env.example', 'w', encoding='utf-8') as f:
        f.write(env_example)
    
    print("✅ Archivo .env.example creado")

def check_requirements():
    """Verificar que requirements.txt esté actualizado"""
    print("📦 Verificando requirements.txt...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'folium',
        'streamlit-folium',
        'python-dotenv'
    ]
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            
        missing = []
        for package in required_packages:
            if package not in content:
                missing.append(package)
        
        if missing:
            print(f"⚠️ Paquetes faltantes en requirements.txt: {missing}")
        else:
            print("✅ requirements.txt está completo")
            
    except FileNotFoundError:
        print("❌ No se encontró requirements.txt")

def main():
    print("🚀 Preparando CySlean Lead Solar para despliegue")
    print("=" * 60)
    
    create_sample_database()
    create_env_example()
    check_requirements()
    
    print("\n" + "=" * 60)
    print("✅ Preparación completada!")
    print("\n📋 Próximos pasos:")
    print("1. Sube tu código a GitHub")
    print("2. Ve a https://share.streamlit.io/")
    print("3. Conecta tu repositorio de GitHub")
    print("4. ¡Despliega tu aplicación!")
    print("\n💡 Recuerda configurar las variables de entorno en Streamlit Cloud")

if __name__ == "__main__":
    main()
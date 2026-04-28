"""
Script de migración de SQLite a Supabase/PostgreSQL
Copia todos los leads existentes de la base de datos local a Supabase
"""
import os
import sqlite3
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def migrate_sqlite_to_postgres():
    """Migra datos de SQLite local a PostgreSQL/Supabase"""
    
    # Verificar que DATABASE_URL esté configurado
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL no está configurado en .env")
        print("📋 Por favor configura Supabase primero siguiendo SUPABASE_SETUP.md")
        return
    
    print("🔄 Iniciando migración de SQLite a Supabase...")
    print(f"📊 Conectando a Supabase...")
    
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
    except ImportError:
        print("❌ ERROR: psycopg2 no está instalado")
        print("📦 Instala con: pip install psycopg2-binary")
        return
    
    # Conectar a SQLite local
    sqlite_path = os.path.join(os.path.dirname(__file__), 'leads.db')
    if not os.path.exists(sqlite_path):
        print(f"❌ ERROR: No se encontró {sqlite_path}")
        print("💡 No hay datos locales para migrar")
        return
    
    print(f"📁 Leyendo datos de {sqlite_path}...")
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()
    
    # Leer todos los leads de SQLite
    sqlite_cursor.execute("SELECT * FROM leads ORDER BY id")
    leads = [dict(row) for row in sqlite_cursor.fetchall()]
    sqlite_conn.close()
    
    if not leads:
        print("ℹ️  No hay leads en la base de datos local")
        return
    
    print(f"✅ Encontrados {len(leads)} leads en SQLite")
    
    # Conectar a PostgreSQL/Supabase
    print("🐘 Conectando a PostgreSQL...")
    try:
        pg_conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        pg_cursor = pg_conn.cursor()
    except Exception as e:
        print(f"❌ ERROR al conectar a Supabase: {e}")
        print("💡 Verifica que DATABASE_URL sea correcto en .env")
        return
    
    # Crear tabla si no existe
    print("📋 Verificando estructura de tabla...")
    pg_cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id SERIAL PRIMARY KEY,
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
        )
    """)
    pg_conn.commit()
    
    # Verificar cuántos leads ya existen en Supabase
    pg_cursor.execute("SELECT COUNT(*) as count FROM leads")
    existing_count = pg_cursor.fetchone()['count']
    
    if existing_count > 0:
        print(f"⚠️  Ya existen {existing_count} leads en Supabase")
        respuesta = input("¿Deseas continuar? Esto puede crear duplicados (s/n): ")
        if respuesta.lower() != 's':
            print("❌ Migración cancelada")
            pg_conn.close()
            return
    
    # Migrar leads
    print(f"\n🚀 Migrando {len(leads)} leads...")
    migrados = 0
    errores = 0
    
    for lead in leads:
        try:
            pg_cursor.execute("""
                INSERT INTO leads (
                    nombre, tipo_negocio, telefono, direccion, poblacion, estado,
                    calificacion, website, estado_pipeline, score_ia, razon_score,
                    consumo_estimado, sistema_recomendado, ahorro_mensual, 
                    mensaje_generado, enviado, fecha_creacion, fecha_ultimo_contacto,
                    fecha_contacto
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                lead['nombre'],
                lead.get('tipo_negocio'),
                lead.get('telefono'),
                lead.get('direccion'),
                lead.get('poblacion'),
                lead.get('estado'),
                lead.get('calificacion', 0),
                lead.get('website'),
                lead.get('estado_pipeline', 'Nuevo'),
                lead.get('score_ia', 0),
                lead.get('razon_score'),
                lead.get('consumo_estimado', 0),
                lead.get('sistema_recomendado', 0),
                lead.get('ahorro_mensual', 0),
                lead.get('mensaje_generado'),
                lead.get('enviado', 0),
                lead.get('fecha_creacion'),
                lead.get('fecha_ultimo_contacto'),
                lead.get('fecha_contacto')
            ))
            migrados += 1
            if migrados % 10 == 0:
                print(f"   Migrados: {migrados}/{len(leads)}")
        except Exception as e:
            errores += 1
            print(f"   ⚠️  Error con lead '{lead.get('nombre')}': {e}")
    
    pg_conn.commit()
    pg_conn.close()
    
    print(f"\n{'='*50}")
    print(f"✅ MIGRACIÓN COMPLETADA")
    print(f"   Total leads: {len(leads)}")
    print(f"   Migrados: {migrados}")
    print(f"   Errores: {errores}")
    print(f"{'='*50}")
    print(f"\n💡 Ahora puedes usar la aplicación con Supabase")
    print(f"   - Localhost y Cloud compartirán los mismos datos")
    print(f"   - Los cambios se sincronizarán automáticamente")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  MIGRACIÓN SQLITE → SUPABASE")
    print("="*50 + "\n")
    
    migrate_sqlite_to_postgres()

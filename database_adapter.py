"""
Adaptador de base de datos que soporta SQLite (local) y PostgreSQL (Supabase/Cloud)
Permite sincronización automática entre localhost y Streamlit Cloud
"""
import os
import re
import unicodedata
from datetime import datetime

# Detectar si hay configuración de PostgreSQL
USE_POSTGRES = os.getenv('DATABASE_URL') is not None

if USE_POSTGRES:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from urllib.parse import urlparse
    print("🐘 Usando PostgreSQL (Supabase)")
else:
    import sqlite3
    print("📁 Usando SQLite (local)")


class DatabaseAdapter:
    """Adaptador que funciona con SQLite o PostgreSQL según configuración"""
    
    def __init__(self):
        self.use_postgres = USE_POSTGRES
        self.db_url = os.getenv('DATABASE_URL')
        self.sqlite_path = os.path.join(os.path.dirname(__file__), 'leads.db')
    
    def get_connection(self):
        """Retorna conexión a la base de datos configurada"""
        if self.use_postgres:
            # PostgreSQL/Supabase
            conn = psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)
            return conn
        else:
            # SQLite local
            conn = sqlite3.connect(self.sqlite_path)
            conn.row_factory = sqlite3.Row
            return conn
    
    def execute_query(self, query, params=None, fetch=False, fetchone=False, commit=False):
        """Ejecuta query adaptada al motor de BD"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Adaptar query de SQLite a PostgreSQL
        if self.use_postgres:
            query = self._adapt_query_to_postgres(query)
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if commit:
                conn.commit()
            
            if fetchone:
                result = cursor.fetchone()
                conn.close()
                return dict(result) if result else None
            elif fetch:
                results = cursor.fetchall()
                conn.close()
                return [dict(row) for row in results]
            else:
                lastrowid = cursor.lastrowid if hasattr(cursor, 'lastrowid') else None
                conn.close()
                return lastrowid
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def _adapt_query_to_postgres(self, query):
        """Convierte sintaxis SQLite a PostgreSQL"""
        # AUTOINCREMENT -> SERIAL
        query = query.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
        
        # CURRENT_TIMESTAMP está bien en ambos
        
        # CHECK constraints - mantener
        
        # PRAGMA table_info -> información del esquema
        if 'PRAGMA table_info' in query:
            # PostgreSQL usa information_schema
            table_name = re.search(r'PRAGMA table_info\((\w+)\)', query)
            if table_name:
                table = table_name.group(1)
                query = f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = '{table}'
                """
        
        # ALTER TABLE ADD COLUMN - sintaxis similar
        
        # Placeholder ? -> %s para PostgreSQL
        query = query.replace('?', '%s')
        
        return query
    
    def init_db(self):
        """Inicializa la base de datos con la estructura necesaria"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.use_postgres:
            # PostgreSQL
            cursor.execute("""
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
                    fecha_contacto TEXT,
                    CONSTRAINT estado_pipeline_check CHECK (estado_pipeline IN (
                        'Nuevo', 'Sin teléfono', 'No WhatsApp', 'Contactado',
                        'Calificado', 'Propuesta enviada', 'En negociación',
                        'Cerrado ganado', 'Cerrado perdido', 'No responde', 'Descartado'
                    ))
                )
            """)
            
            # Crear índices para mejor performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_estado_pipeline ON leads(estado_pipeline)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_score_ia ON leads(score_ia)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_telefono ON leads(telefono)")
            
        else:
            # SQLite
            cursor.execute("""
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
                    estado_pipeline TEXT DEFAULT 'Nuevo' CHECK (estado_pipeline IN (
                        'Nuevo', 'Sin teléfono', 'No WhatsApp', 'Contactado',
                        'Calificado', 'Propuesta enviada', 'En negociación',
                        'Cerrado ganado', 'Cerrado perdido', 'No responde', 'Descartado'
                    )),
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
        
        conn.commit()
        conn.close()
        print("✅ Base de datos inicializada")


# Instancia global del adaptador
db_adapter = DatabaseAdapter()


# Funciones de compatibilidad con el código existente
def get_connection():
    """Mantiene compatibilidad con código existente"""
    return db_adapter.get_connection()


def init_db():
    """Inicializa la base de datos"""
    db_adapter.init_db()


# Exportar para uso en otros módulos
__all__ = ['db_adapter', 'get_connection', 'init_db', 'USE_POSTGRES']

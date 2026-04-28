# src/infrastructure/database/repository.py
import sqlite3
import os
from typing import List, Optional
from src.domain.lead import Lead
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Detectar si usar PostgreSQL o SQLite
USE_POSTGRES = os.getenv('DATABASE_URL') is not None

if USE_POSTGRES:
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        print("🐘 Repository usando PostgreSQL/Supabase")
    except ImportError:
        print("⚠️  psycopg2 no instalado, repository usando SQLite local")
        USE_POSTGRES = False

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'leads.db')


def get_connection():
    """Retorna conexión a PostgreSQL o SQLite según configuración"""
    if USE_POSTGRES:
        database_url = os.getenv('DATABASE_URL')
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn


class LeadRepository:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if USE_POSTGRES:
            # PostgreSQL/Supabase
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
                    fecha_contacto TEXT
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tel ON leads(telefono)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON leads(estado_pipeline)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_score ON leads(score_ia)")
        else:
            # SQLite
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
        
        conn.commit()
        conn.close()

    def existe_duplicado(self, telefono: Optional[str], nombre_norm: str) -> bool:
        conn = get_connection()
        c = conn.cursor()
        try:
            if telefono:
                tel = ''.join(filter(str.isdigit, telefono))
                if USE_POSTGRES:
                    c.execute("SELECT 1 FROM leads WHERE REPLACE(REPLACE(telefono,' ',''),'-','')=%s LIMIT 1", (tel,))
                else:
                    c.execute("SELECT 1 FROM leads WHERE REPLACE(REPLACE(telefono,' ',''),'-','')=? LIMIT 1", (tel,))
                if c.fetchone():
                    return True
            
            if USE_POSTGRES:
                c.execute("SELECT 1 FROM leads WHERE LOWER(REPLACE(REPLACE(REPLACE(nombre,'\"',''),\"'\",''),' ',''))=%s LIMIT 1", (nombre_norm,))
            else:
                c.execute("SELECT 1 FROM leads WHERE LOWER(REPLACE(REPLACE(REPLACE(nombre,'\"',''),\"'\",''),' ',''))=? LIMIT 1", (nombre_norm,))
            return c.fetchone() is not None
        finally:
            conn.close()

    def save(self, lead: Lead) -> Optional[int]:
        conn = get_connection()
        try:
            placeholder = '%s' if USE_POSTGRES else '?'
            query = f"""
                INSERT INTO leads (
                    nombre, tipo_negocio, telefono, direccion, poblacion, estado,
                    calificacion, website, estado_pipeline, score_ia, razon_score,
                    consumo_estimado, sistema_recomendado, ahorro_mensual, mensaje_generado
                ) VALUES ({','.join([placeholder]*15)})
            """
            
            cur = conn.cursor()
            cur.execute(query, (
                lead.nombre, lead.tipo_negocio, lead.telefono, lead.direccion, lead.poblacion,
                lead.estado, lead.calificacion, lead.website, lead.estado_pipeline, lead.score_ia,
                lead.razon_score, lead.consumo_estimado, lead.sistema_recomendado, lead.ahorro_mensual,
                lead.mensaje_generado
            ))
            conn.commit()
            
            if USE_POSTGRES:
                cur.execute("SELECT lastval()")
                return cur.fetchone()[0]
            else:
                return cur.lastrowid
        except Exception as e:
            print(f"❌ Error BD: {e}")
            return None
        finally:
            conn.close()

    def get_all(self, limit: int = 2000) -> List[dict]:
        """Obtiene leads desde la BD con límite para performance. Los más recientes primero."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            placeholder = '%s' if USE_POSTGRES else '?'
            cursor.execute(
                f"SELECT * FROM leads ORDER BY fecha_creacion DESC, score_ia DESC LIMIT {placeholder}",
                (limit,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_stats(self) -> dict:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            placeholder = '%s' if USE_POSTGRES else '?'
            cursor.execute(f"""
                SELECT COUNT(*) as t, AVG(score_ia) as a, SUM(ahorro_mensual) as ah, SUM(sistema_recomendado) as k
                FROM leads WHERE score_ia >= {placeholder}
            """, (4,))
            row = cursor.fetchone()
            return {
                'leads_calificados': row['t'] if isinstance(row, dict) else row[0] or 0,
                'score_promedio': round((row['a'] if isinstance(row, dict) else row[1]) or 0, 1),
                'ahorro_potencial': int((row['ah'] if isinstance(row, dict) else row[2]) or 0),
                'kwp_potencial': round((row['k'] if isinstance(row, dict) else row[3]) or 0, 1)
            }
        finally:
            conn.close()

    def delete_by_status(self, status: str) -> int:
        """Borra leads por estado y retorna cuántos se borraron."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            placeholder = '%s' if USE_POSTGRES else '?'
            cursor.execute(f"DELETE FROM leads WHERE estado_pipeline = {placeholder}", (status,))
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    def keep_only_statuses(self, allowed_statuses: List[str]) -> int:
        """Borra todos los leads EXCEPTO los que estén en allowed_statuses."""
        conn = get_connection()
        try:
            placeholders = ','.join(('%s' if USE_POSTGRES else '?') for _ in allowed_statuses)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM leads WHERE estado_pipeline NOT IN ({placeholders})", allowed_statuses)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    def update_status(self, lead_id: int, new_status: str) -> bool:
        """Actualiza el estado de un lead."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            placeholder = '%s' if USE_POSTGRES else '?'
            
            # Actualizar con timestamp
            cursor.execute(
                f"UPDATE leads SET estado_pipeline = {placeholder}, fecha_ultimo_contacto = CURRENT_TIMESTAMP WHERE id = {placeholder}",
                (new_status, lead_id)
            )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error actualizando estado: {e}")
            return False
        finally:
            conn.close()
# src/infrastructure/database/repository.py
import sqlite3
import os
from typing import List, Optional
from src.domain.lead import Lead

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'leads.db')


class LeadRepository:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
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
        conn.close()

    def existe_duplicado(self, telefono: Optional[str], nombre_norm: str) -> bool:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            if telefono:
                tel = ''.join(filter(str.isdigit, telefono))
                c.execute("SELECT 1 FROM leads WHERE REPLACE(REPLACE(telefono,' ',''),'-','')=? LIMIT 1", (tel,))
                if c.fetchone():
                    return True
            c.execute("SELECT 1 FROM leads WHERE LOWER(REPLACE(REPLACE(REPLACE(nombre,'\"',''),\"'\",''),' ',''))=? LIMIT 1", (nombre_norm,))
            return c.fetchone() is not None
        finally:
            conn.close()

    def save(self, lead: Lead) -> Optional[int]:
        conn = sqlite3.connect(DB_PATH)
        try:
            cur = conn.execute("""
                INSERT INTO leads (
                    nombre, tipo_negocio, telefono, direccion, poblacion, estado,
                    calificacion, website, estado_pipeline, score_ia, razon_score,
                    consumo_estimado, sistema_recomendado, ahorro_mensual, mensaje_generado
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                lead.nombre, lead.tipo_negocio, lead.telefono, lead.direccion, lead.poblacion,
                lead.estado, lead.calificacion, lead.website, lead.estado_pipeline, lead.score_ia,
                lead.razon_score, lead.consumo_estimado, lead.sistema_recomendado, lead.ahorro_mensual,
                lead.mensaje_generado
            ))
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            print(f"❌ Error BD: {e}")
            return None
        finally:
            conn.close()

    def get_all(self, limit: int = 2000) -> List[dict]:
        """Obtiene leads desde la BD con límite para performance."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.execute(
                "SELECT * FROM leads ORDER BY score_ia DESC, fecha_creacion DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            return [dict(zip(row.keys(), row)) for row in rows]
        finally:
            conn.close()

    def get_stats(self) -> dict:
        conn = sqlite3.connect(DB_PATH)
        try:
            row = conn.execute("""
                SELECT COUNT(*) as t, AVG(score_ia) as a, SUM(ahorro_mensual) as ah, SUM(sistema_recomendado) as k
                FROM leads WHERE score_ia >= 4
            """).fetchone()
            return {
                'leads_calificados': row[0] or 0,
                'score_promedio': round(row[1] or 0, 1),
                'ahorro_potencial': int(row[2] or 0),
                'kwp_potencial': round(row[3] or 0, 1)
            }
        finally:
            conn.close()

    def delete_by_status(self, status: str) -> int:
        """Borra leads por estado y retorna cuántos se borraron."""
        conn = sqlite3.connect(DB_PATH)
        try:
            cursor = conn.execute("DELETE FROM leads WHERE estado_pipeline = ?", (status,))
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    def keep_only_statuses(self, allowed_statuses: List[str]) -> int:
        """Borra todos los leads EXCEPTO los que estén en allowed_statuses."""
        conn = sqlite3.connect(DB_PATH)
        try:
            placeholders = ','.join('?' for _ in allowed_statuses)
            cursor = conn.execute(f"DELETE FROM leads WHERE estado_pipeline NOT IN ({placeholders})", allowed_statuses)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    def update_status(self, lead_id: int, new_status: str) -> bool:
        """Actualiza el estado de un lead."""
        conn = sqlite3.connect(DB_PATH)
        try:
            # Verificar si la columna fecha_ultimo_contacto existe
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(leads)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'fecha_ultimo_contacto' in columns:
                # Si existe la columna, actualizar con timestamp
                conn.execute(
                    "UPDATE leads SET estado_pipeline = ?, fecha_ultimo_contacto = CURRENT_TIMESTAMP WHERE id = ?",
                    (new_status, lead_id)
                )
            else:
                # Si no existe, solo actualizar el estado
                conn.execute(
                    "UPDATE leads SET estado_pipeline = ? WHERE id = ?",
                    (new_status, lead_id)
                )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error actualizando estado: {e}")
            return False
        finally:
            conn.close()
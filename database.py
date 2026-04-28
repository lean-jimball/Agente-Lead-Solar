import sqlite3
import os
import re
import unicodedata
from datetime import datetime

DB_NAME = 'leads.db'
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def agregar_columna_si_no_existe(cursor, tabla, columna, tipo):
    cursor.execute(f"PRAGMA table_info({tabla})")
    columnas = [col[1] for col in cursor.fetchall()]
    if columna not in columnas:
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo}")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

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
                'Nuevo',
                'Sin teléfono',
                'No WhatsApp',
                'Contactado',
                'Calificado',
                'Propuesta enviada',
                'En negociación',
                'Cerrado ganado',
                'Cerrado perdido',
                'No responde',
                'Descartado'
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

    # Agrega columnas si la tabla ya existía
    agregar_columna_si_no_existe(cursor, 'leads', 'poblacion', 'TEXT')
    agregar_columna_si_no_existe(cursor, 'leads', 'estado', 'TEXT')
    agregar_columna_si_no_existe(cursor, 'leads', 'calificacion', 'REAL DEFAULT 0')
    agregar_columna_si_no_existe(cursor, 'leads', 'website', 'TEXT')
    agregar_columna_si_no_existe(cursor, 'leads', 'enviado', 'INTEGER DEFAULT 0')
    agregar_columna_si_no_existe(cursor, 'leads', 'fecha_contacto', 'TEXT')

    conn.commit()
    conn.close()
    print("Base de datos inicializada")
    # Intentar rellenar poblacion para filas antiguas
    try:
        backfill_poblacion_from_direccion()
    except Exception:
        pass

def backfill_poblacion_from_direccion():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, direccion, poblacion FROM leads")
    rows = cursor.fetchall()
    updates = 0
    for r in rows:
        pid = r['id']
        pobl = r['poblacion']
        direccion = r['direccion']
        if (pobl is None or str(pobl).strip() == '') and direccion:
            partes = str(direccion).split(',')
            if len(partes) >= 2:
                new_pob = partes[-2].strip()
            else:
                new_pob = ''
            cursor.execute("UPDATE leads SET poblacion =? WHERE id =?", (new_pob, pid))
            updates += 1
    if updates > 0:
        conn.commit()
        print(f"Backfilled {updates} filas con 'poblacion' desde 'direccion'")
    conn.close()

def normalizar_nombre(nombre):
    """Para comparar duplicados: quita comillas, espacios extra, minúsculas"""
    if not nombre:
        return ""
    s = str(nombre).lower().strip()
    s = re.sub(r'["\']', '', s)
    s = re.sub(r"\s+", ' ', s)
    # quitar acentos
    s = unicodedata.normalize('NFKD', s)
    s = ''.join([c for c in s if not unicodedata.combining(c)])
    return s

def es_numero_whatsapp(telefono):
    """Valida si un teléfono es válido para WhatsApp México"""
    if not telefono:
        return False
    # Limpia el número
    num = re.sub(r'\D', '', str(telefono))
    # México: 10 dígitos, o 52 + 10 dígitos
    if len(num) == 10:
        return True
    if len(num) == 12 and num.startswith('52'):
        return True
    return False

def insert_lead(lead):
    """Inserta lead nuevo. Descarta duplicados y corporativos con score_ia = 0"""

    if lead.get('score_ia', 0) == 0:
        print(f"Descartado: {lead.get('nombre')} - Score 0 o corporativo")
        return None

    conn = get_connection()
    cursor = conn.cursor()

    # Normalizar y derivar campos faltantes
    nombre_norm = normalizar_nombre(lead.get('nombre'))
    telefono = (lead.get('telefono') or '').strip()
    direccion = lead.get('direccion')
    poblacion = lead.get('poblacion')
    if not poblacion or str(poblacion).strip() == '':
        # intentar derivar población desde la dirección
        try:
            if direccion:
                partes = str(direccion).split(',')
                if len(partes) >= 2:
                    poblacion = partes[-2].strip()
                else:
                    poblacion = ''
            else:
                poblacion = ''
        except Exception:
            poblacion = ''

    # Clasificación automática de estado_pipeline
    estado_inicial = lead.get('estado_pipeline', 'Nuevo')
    if not telefono or telefono == '':
        estado_inicial = 'Sin teléfono'
    elif not es_numero_whatsapp(telefono):
        estado_inicial = 'No WhatsApp'

    # Mejor detección de duplicados: revisar en Python filas existentes
    cursor.execute("SELECT id, nombre, telefono, direccion FROM leads")
    rows = cursor.fetchall()
    for r in rows:
        existing_nombre = r['nombre']
        existing_tel = r['telefono'] or ''
        if existing_tel:
            if telefono and re.sub(r"\D", '', existing_tel) == re.sub(r"\D", '', telefono):
                print(f"Duplicado por telefono omitido: {lead.get('nombre')} - Ya existe ID {r['id']}")
                conn.close()
                return None
        # comparar por nombre normalizado
        if normalizar_nombre(existing_nombre) == nombre_norm:
            print(f"Duplicado por nombre omitido: {lead.get('nombre')} - Ya existe ID {r['id']}")
            conn.close()
            return None

    try:
        cursor.execute("""
            INSERT INTO leads (
                nombre, tipo_negocio, telefono, direccion, poblacion, estado,
                calificacion, website, estado_pipeline, score_ia, razon_score,
                consumo_estimado, sistema_recomendado, ahorro_mensual, mensaje_generado
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            lead.get('nombre'),
            lead.get('tipo_negocio'),
            telefono,
            direccion,
            poblacion,
            lead.get('estado'),
            lead.get('calificacion', 0),
            lead.get('website'),
            estado_inicial,
            lead.get('score_ia', 0),
            lead.get('razon_score'),
            lead.get('consumo_estimado', 0),
            lead.get('sistema_recomendado', 0),
            lead.get('ahorro_mensual', 0),
            lead.get('mensaje_generado')
        ))

        lead_id = cursor.lastrowid
        conn.commit()
        print(f"Lead guardado: {lead.get('nombre')} - ID {lead_id} - Score {lead.get('score_ia')} - Estado: {estado_inicial} - Dir: {lead.get('direccion','Sin dir')[:30]}")
        return lead_id

    except Exception as e:
        print(f"Error insertando lead: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_all_leads():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM leads
        ORDER BY score_ia DESC, fecha_creacion DESC
    """)
    leads = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return leads

def get_leads_for_messenger(min_score=4):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, telefono, score_ia, ahorro_mensual,
               sistema_recomendado, mensaje_generado, estado_pipeline, direccion
        FROM leads
        WHERE score_ia >=?
        AND estado_pipeline IN ('Nuevo', 'Contactado')
        AND telefono IS NOT NULL
        AND telefono!= ''
        AND (enviado IS NULL OR enviado = 0)
        ORDER BY score_ia DESC
    """, (min_score,))
    leads = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return leads

def update_lead_status(lead_id, nuevo_estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE leads
        SET estado_pipeline =?,
            fecha_ultimo_contacto = CURRENT_TIMESTAMP
        WHERE id =?
    """, (nuevo_estado, lead_id))
    conn.commit()
    conn.close()
    print(f"✅ Lead {lead_id} actualizado a: {nuevo_estado}")

def update_lead(lead_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    for key, value in data.items():
        fields.append(f"{key} =?")
        values.append(value)
    values.append(lead_id)
    query = f"UPDATE leads SET {', '.join(fields)} WHERE id =?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()

def delete_all_leads():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM leads")
    count = cursor.fetchone()[0]
    cursor.execute("DELETE FROM leads")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='leads'")
    conn.commit()
    conn.close()
    print(f"Borrados {count} leads. IDs reseteados a 1.")
    return count


def delete_new_leads():
    """Borra todos los leads cuyo estado de pipeline sea 'Nuevo' y retorna la cantidad borrada."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM leads WHERE estado_pipeline = 'Nuevo'")
    count = cursor.fetchone()[0]
    if count > 0:
        cursor.execute("DELETE FROM leads WHERE estado_pipeline = 'Nuevo'")
        # No resetear IDs si se quiere mantener integridad, pero aquí seguimos patrón de delete_all
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='leads'")
        conn.commit()
    conn.close()
    print(f"Borrados {count} leads con estado 'Nuevo'.")
    return count


def prune_to_followup(keep_states=None):
    """Borra todos los leads que no estén en `keep_states`.
    Por defecto mantiene ['Contactado', 'No WhatsApp'].
    Devuelve la cantidad de filas borradas."""
    if keep_states is None:
        keep_states = ['Contactado', 'No WhatsApp']
    placeholders = ','.join('?' for _ in keep_states)
    conn = get_connection()
    cursor = conn.cursor()
    # Contar los que se mantendrán
    cursor.execute(f"SELECT COUNT(*) FROM leads WHERE estado_pipeline IN ({placeholders})", tuple(keep_states))
    keep_count = cursor.fetchone()[0]
    # Contar total
    cursor.execute("SELECT COUNT(*) FROM leads")
    total = cursor.fetchone()[0]
    # Calcular a borrar
    to_delete = total - keep_count
    if to_delete > 0:
        # Borrar todos los que no estén en los estados a mantener
        cursor.execute(f"DELETE FROM leads WHERE estado_pipeline NOT IN ({placeholders})", tuple(keep_states))
        # También borrar filas sin teléfono por si quedaron
        cursor.execute("DELETE FROM leads WHERE telefono IS NULL OR trim(telefono) = ''")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='leads'")
        conn.commit()
    conn.close()
    print(f"Prune: total {total}, keep {keep_count}, borrados aproximados {to_delete}.")
    return to_delete

def tag_missing_phone(state_name='Sin teléfono'):
    """Marca en `estado_pipeline` a los leads que no tienen teléfono."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM leads WHERE telefono IS NULL OR trim(telefono) = ''")
    count = cursor.fetchone()[0]
    if count > 0:
        cursor.execute("UPDATE leads SET estado_pipeline =? WHERE telefono IS NULL OR trim(telefono) = ''", (state_name,))
        conn.commit()
    conn.close()
    return count

def tag_no_whatsapp(state_name='No WhatsApp'):
    """Marca en `estado_pipeline` a los leads con intento de envío fallido (enviado = -1)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM leads WHERE enviado = -1")
    count = cursor.fetchone()[0]
    if count > 0:
        cursor.execute("UPDATE leads SET estado_pipeline =? WHERE enviado = -1", (state_name,))
        conn.commit()
    conn.close()
    return count

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    stats = {}
    cursor.execute("SELECT COUNT(*) FROM leads")
    stats['total_leads'] = cursor.fetchone()[0]
    cursor.execute("""
        SELECT estado_pipeline, COUNT(*) as count
        FROM leads
        GROUP BY estado_pipeline
    """)
    stats['por_estado'] = {row[0]: row[1] for row in cursor.fetchall()}
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            AVG(score_ia) as avg_score,
            SUM(ahorro_mensual) as ahorro_total,
            SUM(sistema_recomendado) as kwp_total
        FROM leads
        WHERE score_ia >= 4
    """)
    row = cursor.fetchone()
    stats['leads_calificados'] = row[0] or 0
    stats['score_promedio'] = round(row[1] or 0, 1)
    stats['ahorro_potencial'] = int(row[2] or 0)
    stats['kwp_potencial'] = round(row[3] or 0, 1)
    conn.close()
    return stats

def get_unsynced_leads():
    return []

def mark_as_synced(lead_id):
    pass

if __name__ == "__main__":
    init_db()
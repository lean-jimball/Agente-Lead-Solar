import streamlit as st
import pandas as pd
import os
import sys
import sqlite3
import folium
from streamlit_folium import st_folium

# ─── AUTENTICACIÓN ─────────────────────────────────────────────────────────
from auth import check_password

st.set_page_config(page_title="CySlean Lead Solar", page_icon="☀️", layout="wide")

# Verificar autenticación ANTES de cargar cualquier cosa
if not check_password():
    st.stop()  # Detener ejecución si no está autenticado

# ─── COMPATIBILIDAD: Para messenger.py antiguo ─────────────────────────────
def get_connection():
    """Función de compatibilidad para messenger.py"""
    import sqlite3
    DB_PATH = os.path.join(os.path.dirname(__file__), 'leads.db')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
from src.application.lead_service import LeadService

service = LeadService()
service.repo._init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #060d1a; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem!important; }
[data-testid="stSidebar"] { background: #0a1628!important; border-right: 1px solid #1a2d4a!important; }
[data-testid="stSidebar"] * { color: #94a3b8!important; }
[data-testid="stMetric"] { background: linear-gradient(135deg, #0f1f38 0%, #0a1628 100%); border: 1px solid #1a3356; border-radius: 16px; padding: 20px 24px!important; }
[data-testid="stMetricValue"] { color: #f1f5f9!important; font-family: 'Syne', sans-serif!important; font-size: 1.9rem!important; font-weight: 700!important; }
[data-testid="stMetricLabel"] { color: #64748b!important; font-size: 0.72rem!important; text-transform: uppercase!important; }
.stButton > button { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%)!important; color: #000!important; font-weight: 700!important; border: none!important; border-radius: 10px!important; }
.header-title { font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800; color: #f1f5f9; }
.header-badge { background: #f59e0b22; border: 1px solid #f59e0b44; color: #f59e0b; padding: 5px 14px; border-radius: 20px; font-size: 0.76rem; font-weight: 600; }
.section-title { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; color: #e2e8f0; margin-bottom: 14px; }

/* Estilos para gráficos más profesionales */
.stPlotlyChart, .stAltairChart { 
    background: transparent !important; 
}
.stPlotlyChart > div, .stAltairChart > div { 
    background: transparent !important; 
    border: none !important;
}

/* Mejorar el contenedor de las columnas */
[data-testid="column"] {
    background: rgba(15, 31, 56, 0.3) !important;
    border: 1px solid rgba(26, 53, 86, 0.5) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin: 5px !important;
}

/* Eliminar espacios problemáticos entre columnas del dashboard */
.block-container [data-testid="column"] {
    background: transparent !important;
    border: none !important;
    margin: 0 !important;
    padding: 10px !important;
}

/* Contenedor específico para mapa y gráfico */
.dashboard-columns [data-testid="column"] {
    background: rgba(15, 31, 56, 0.3) !important;
    border: 1px solid rgba(26, 53, 86, 0.5) !important;
    border-radius: 12px !important;
    padding: 15px !important;
    margin: 0 5px !important;
}

/* Eliminar bordes blancos entre columnas */
.element-container {
    margin: 0 !important;
}

/* Ajustar espaciado del contenedor principal */
.main .block-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* Eliminar cualquier fondo blanco residual */
.main, .stApp, .block-container {
    background: #060d1a !important;
}

/* Asegurar que las columnas no tengan espacios blancos */
.element-container, .stMarkdown, .stPlotlyChart {
    background: transparent !important;
}

/* Forzar que el contenedor del mapa no tenga márgenes */
.streamlit-folium, .streamlit-folium iframe {
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    background: #060d1a !important;
}

/* Estilo para el mapa - Eliminar fondo blanco completamente */
.folium-map {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(26, 53, 86, 0.5) !important;
    background: #060d1a !important;
}

/* Forzar fondo oscuro en todos los elementos del mapa */
iframe[title*="folium"], iframe[src*="folium"] {
    background: #060d1a !important;
    border: none !important;
}

/* Eliminar cualquier fondo blanco del contenedor del mapa */
.stPlotlyChart iframe, .element-container iframe {
    background: #060d1a !important;
}

/* Ajustar el contenedor del mapa para que ocupe todo el espacio */
[data-testid="stIFrame"] {
    background: #060d1a !important;
    border: none !important;
    width: 100% !important;
    height: 100% !important;
}

/* Forzar fondo oscuro en el elemento que contiene el mapa */
.streamlit-folium {
    background: #060d1a !important;
    border: none !important;
}

/* Eliminar márgenes y padding que puedan causar líneas blancas */
.streamlit-folium > div {
    background: #060d1a !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Estilos mejorados para la tabla del Pipeline */
.pipeline-table-header {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    color: #f1f5f9 !important;
    font-weight: 600 !important;
    padding: 12px 8px !important;
    border-radius: 8px 8px 0 0 !important;
    border-bottom: 2px solid #334155 !important;
    font-size: 0.9rem !important;
    text-align: center !important;
}

.pipeline-table-row {
    background: rgba(30, 41, 59, 0.4) !important;
    border: 1px solid rgba(51, 65, 85, 0.3) !important;
    border-radius: 6px !important;
    margin-bottom: 8px !important;
    padding: 8px !important;
    transition: all 0.2s ease !important;
}

.pipeline-table-row:hover {
    background: rgba(30, 41, 59, 0.6) !important;
    border-color: rgba(59, 130, 246, 0.5) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}

.pipeline-table-cell {
    color: #e2e8f0 !important;
    font-size: 0.85rem !important;
    padding: 4px 8px !important;
    vertical-align: middle !important;
}

.pipeline-table-cell strong {
    color: #f1f5f9 !important;
    font-weight: 600 !important;
}

/* Mejorar selectbox en la tabla */
.stSelectbox > div > div {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(51, 65, 85, 0.6) !important;
    border-radius: 6px !important;
    color: #e2e8f0 !important;
}

.stSelectbox > div > div > div {
    color: #e2e8f0 !important;
    font-size: 0.85rem !important;
}

/* Botones de acción en la tabla */
.pipeline-action-btn {
    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 6px 12px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

.pipeline-action-btn:hover {
    background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
    transform: translateY(-1px) !important;
}

/* Mejorar texto de la tabla */
div[data-testid="column"] p, div[data-testid="column"] span {
    color: #e2e8f0 !important;
}

/* Separadores de la tabla */
hr {
    border-color: rgba(51, 65, 85, 0.3) !important;
    margin: 8px 0 !important;
}

/* ESTILOS ESPECÍFICOS PARA BOTONES DEL SIDEBAR */
/* Botón Buscar (primary) */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
    color: #ffffff !important;
    border: 2px solid #3b82f6 !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    text-shadow: none !important;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(29, 78, 216, 0.4) !important;
}

/* Botón WhatsApp (secondary/normal) */
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {
    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    color: #ffffff !important;
    border: 2px solid #10b981 !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    text-shadow: none !important;
}

[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover {
    background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(5, 150, 105, 0.4) !important;
}

/* Botón WhatsApp deshabilitado */
[data-testid="stSidebar"] .stButton > button:disabled {
    background: #374151 !important;
    color: #d1d5db !important;
    border: 2px solid #4b5563 !important;
    font-weight: 700 !important;
    cursor: not-allowed !important;
}

/* Forzar color de texto en botones del sidebar */
[data-testid="stSidebar"] .stButton > button span {
    color: inherit !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

ESTADOS_MX = {
    'Hidalgo': [20.10, -98.75], 'Ciudad de México': [19.43, -99.13], 'CDMX': [19.43, -99.13],
    'México': [19.29, -99.65], 'Puebla': [19.04, -98.20], 'Querétaro': [20.58, -100.38],
    'Jalisco': [20.65, -103.34], 'Nuevo León': [25.68, -100.31], 'Veracruz': [19.17, -96.13],
    'Guanajuato': [21.01, -101.25], 'Michoacán': [19.56, -101.70], 'Guerrero': [17.43, -99.54],
    'Oaxaca': [17.07, -96.72], 'Chiapas': [16.75, -93.12], 'Yucatán': [20.70, -89.19],
    'Quintana Roo': [19.18, -88.46], 'Tamaulipas': [23.73, -99.14], 'Chihuahua': [28.63, -106.08],
    'Sonora': [29.29, -110.33], 'Baja California': [30.84, -115.28], 'Sinaloa': [25.17, -107.46],
    'San Luis Potosí': [22.15, -100.97], 'Aguascalientes': [21.88, -102.29], 'Morelos': [18.68, -99.10],
    'Tlaxcala': [19.31, -98.23], 'Durango': [24.02, -104.65], 'Zacatecas': [22.77, -102.58],
    'Nayarit': [21.75, -104.84], 'Colima': [19.24, -103.72], 'Baja California Sur': [26.04, -111.66],
    'Campeche': [19.83, -90.52], 'Coahuila': [27.05, -101.70], 'Tabasco': [17.84, -92.61]
}

ABREVIATURAS = {
    'HGO': 'Hidalgo', 'HGO.': 'Hidalgo', 'HIDALGO': 'Hidalgo',
    'PUE': 'Puebla', 'PUE.': 'Puebla', 'PUEBLA': 'Puebla',
    'DF': 'CDMX', 'CDMX': 'CDMX', 'CIUDAD DE MEXICO': 'CDMX',
    'MEX': 'México', 'MEX.': 'México', 'EDO MEX': 'México', 'ESTADO DE MEXICO': 'México',
    'QRO': 'Querétaro', 'QRO.': 'Querétaro', 'QUERETARO': 'Querétaro',
    'JAL': 'Jalisco', 'JAL.': 'Jalisco', 'JALISCO': 'Jalisco',
    'NL': 'Nuevo León', 'N.L.': 'Nuevo León', 'NUEVO LEON': 'Nuevo León', 'MONTERREY': 'Nuevo León',
    'VER': 'Veracruz', 'VER.': 'Veracruz', 'VERACRUZ': 'Veracruz',
    'GTO': 'Guanajuato', 'GTO.': 'Guanajuato', 'GUANAJUATO': 'Guanajuato',
    'MICH': 'Michoacán', 'MICH.': 'Michoacán', 'MICHOACAN': 'Michoacán',
    'GRO': 'Guerrero', 'GRO.': 'Guerrero', 'GUERRERO': 'Guerrero',
    'OAX': 'Oaxaca', 'OAX.': 'Oaxaca', 'OAXACA': 'Oaxaca',
    'CHIS': 'Chiapas', 'CHIS.': 'Chiapas', 'CHIAPAS': 'Chiapas',
    'YUC': 'Yucatán', 'YUC.': 'Yucatán', 'YUCATAN': 'Yucatán',
    'QR': 'Quintana Roo', 'Q.ROO': 'Quintana Roo', 'QUINTANA ROO': 'Quintana Roo',
    'TAMPS': 'Tamaulipas', 'TAMPS.': 'Tamaulipas', 'TAMAULIPAS': 'Tamaulipas',
    'CHIH': 'Chihuahua', 'CHIH.': 'Chihuahua', 'CHIHUAHUA': 'Chihuahua',
    'SON': 'Sonora', 'SON.': 'Sonora', 'SONORA': 'Sonora',
    'BC': 'Baja California', 'B.C.': 'Baja California', 'BAJA CALIFORNIA': 'Baja California',
    'SIN': 'Sinaloa', 'SIN.': 'Sinaloa', 'SINALOA': 'Sinaloa',
    'SLP': 'San Luis Potosí', 'S.L.P.': 'San Luis Potosí', 'SAN LUIS POTOSI': 'San Luis Potosí',
    'AGS': 'Aguascalientes', 'AGS.': 'Aguascalientes', 'AGUASCALIENTES': 'Aguascalientes',
    'MOR': 'Morelos', 'MOR.': 'Morelos', 'MORELOS': 'Morelos',
    'TLAX': 'Tlaxcala', 'TLAX.': 'Tlaxcala', 'TLAXCALA': 'Tlaxcala', 'TLAXCALINGO': 'Tlaxcala'
}

def extraer_estado(direccion):
    if not direccion or pd.isna(direccion): 
        return 'Desconocido'
    texto = str(direccion).upper().strip()
    
    # Primero buscar abreviaciones específicas (más precisas)
    for abr, estado in ABREVIATURAS.items():
        # Buscar abreviación seguida de punto o al final
        if f"{abr}." in texto or texto.endswith(f" {abr}") or f", {abr}" in texto:
            return estado
    
    # Luego buscar nombres completos de estados, pero evitar falsos positivos
    for estado in ESTADOS_MX.keys():
        estado_upper = estado.upper()
        # Evitar confundir "MORELOS" (avenida) con "Morelos" (estado)
        # Solo considerar si aparece después de una coma o al final
        if f", {estado_upper}" in texto or texto.endswith(f" {estado_upper}"):
            return estado
        # También considerar si aparece al inicio seguido de coma
        if texto.startswith(f"{estado_upper},"):
            return estado
    
    return 'Desconocido'

# Cargar datos (sin cache para asegurar datos frescos)
leads = service.get_all_leads(limit=5000)
df = pd.DataFrame(leads) if leads else pd.DataFrame()

# Calcular estadísticas globales para usar en toda la app
DB_PATH = os.path.join(os.path.dirname(__file__), 'leads.db')
conn = sqlite3.connect(DB_PATH)
calificados = conn.execute("""
SELECT COUNT(*) FROM leads 
WHERE estado_pipeline IN ('Nuevo', 'Calificado', 'Contactado')
AND telefono IS NOT NULL AND telefono != ''
AND (enviado IS NULL OR enviado = 0)
AND score_ia >= 4
""").fetchone()[0]

# Contar leads sin teléfono
sin_telefono = conn.execute("""
SELECT COUNT(*) FROM leads 
WHERE estado_pipeline = 'Sin teléfono'
""").fetchone()[0]
conn.close()

with st.sidebar:
    st.markdown("### ☀️ CySlean Lead Solar")
    st.markdown("---")
    vista = st.radio("Vista", ["📊 Dashboard", "📋 Pipeline de Leads"])
    st.markdown("---")
    search_query = st.text_input("🔍 Búsqueda", placeholder="ej. hoteles en Pachuca")
    max_results = st.slider("Resultados", 1, 50, 5)
    
    if st.button("🚀 Buscar", type="primary") and search_query:
        with st.spinner("Buscando..."):
            try:
                import subprocess, json
                python_exe = sys.executable
                result = subprocess.run(f'"{python_exe}" scraper.py "{search_query}" {max_results}', capture_output=True, text=True, shell=True)
                leads_raw = []
                if result.returncode == 0:
                    try:
                        with open("temp_results.json", "r", encoding="utf-8") as f:
                            leads_raw = json.load(f)
                    except: pass
                leads_guardados = 0
                for lead in leads_raw:
                    try:
                        from ai_processor import analyze_lead
                        analisis = analyze_lead(lead)
                        if service.create_lead({**lead, **analisis, 'estado_pipeline': 'Nuevo'}):
                            leads_guardados += 1
                    except: pass
                st.success(f"✅ {leads_guardados} guardados")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("---")
    
    if st.button(f"📤 WhatsApp ({calificados})", disabled=calificados==0):
        try:
            from messenger import send_whatsapp_messages
            enviados = send_whatsapp_messages()
            st.success(f"✅ {enviados} enviados")
        except Exception as e:
            st.error(f"Error: {e}")
    
    st.markdown("---")
    
    # Calcular leads calificables (siempre visible)
    leads_calificables = len(df[
        (df['estado_pipeline'].isin(['Nuevo', 'Sin teléfono', 'No WhatsApp'])) & 
        (df['score_ia'] >= 4) &
        (df['telefono'].notna()) &
        (df['telefono'] != '')
    ]) if not df.empty else 0
    
    # Botón 1: Eliminar Sin Teléfono
    if st.button(f"🗑️ Eliminar Sin Teléfono ({sin_telefono})", 
                disabled=sin_telefono==0,
                help="Elimina permanentemente todos los leads marcados como 'Sin teléfono'",
                key="sidebar_eliminar"):
        try:
            n = service.repo.delete_by_status('Sin teléfono')
            if n > 0:
                st.success(f"✅ Eliminados {n} leads sin teléfono")
                st.rerun()
            else:
                st.info("ℹ️ No había leads sin teléfono para eliminar")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    # Botón 2: Calificar Nuevos ≥4 (siempre visible)
    if st.button(f"⭐ Calificar Nuevos ≥4 ({leads_calificables})", 
                help="Marca como 'Calificado' leads con score ≥ 4 y teléfono válido",
                disabled=leads_calificables==0,
                key="sidebar_calificar"):
        try:
            leads_calificar = df[
                (df['estado_pipeline'].isin(['Nuevo', 'Sin teléfono', 'No WhatsApp'])) & 
                (df['score_ia'] >= 4) &
                (df['telefono'].notna()) &
                (df['telefono'] != '')
            ]
            
            count = 0
            estados_origen = []
            for _, lead in leads_calificar.iterrows():
                estados_origen.append(lead['estado_pipeline'])
                service.update_lead_status(lead['id'], 'Calificado')
                count += 1
            
            if count > 0:
                estados_unicos = list(set(estados_origen))
                st.success(f"✅ {count} leads promovidos a 'Calificado' desde: {', '.join(estados_unicos)}")
                st.rerun()
            else:
                st.info("ℹ️ No hay leads elegibles para calificar")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    # Botón 3: Refrescar Datos
    if st.button("🔄 Refrescar Datos", 
                help="Actualiza la vista con los datos más recientes de la base de datos",
                key="sidebar_refresh"):
        st.rerun()

if df.empty:
    st.info("📊 Sin datos aún.")
else:
    if vista == "📊 Dashboard":
        st.markdown(f"""
        <div class="header-bar" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; border-bottom:1px solid #1a2d4a; padding-bottom:15px;">
            <div><div class="header-title">☀️ CySlean Lead Solar</div>
            <div style="font-size:0.8rem; color:#475569;">Prospecting México · {len(df)} oportunidades</div></div>
            <div class="header-badge">🟢 ACTIVO</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        # Ensure ahorro_mensual is numeric for calculations
        try:
            ahorro_total = df['ahorro_mensual'].apply(lambda x: float(x) if pd.notna(x) and str(x).replace('.','').replace('-','').isdigit() else 0).sum()
        except Exception as e:
            st.error(f"Error calculating ahorro_total: {e}")
            ahorro_total = 0
        
        # Calcular precio por kWp
        try:
            # Filtrar datos válidos para el cálculo
            df_valid = df[(df['ahorro_mensual'] > 0) & (df['sistema_recomendado'] > 0)].copy()
            if not df_valid.empty:
                # Factor de recuperación típico en México (6 años = 72 meses)
                factor_recuperacion = 72
                df_valid['ahorro_clean'] = df_valid['ahorro_mensual'].apply(lambda x: float(x) if pd.notna(x) else 0)
                
                # Calcular precio por kWp global
                total_ahorro_valid = df_valid['ahorro_clean'].sum()
                total_kwp_valid = df_valid['sistema_recomendado'].sum()
                precio_kwp = (total_ahorro_valid * factor_recuperacion) / total_kwp_valid if total_kwp_valid > 0 else 0
            else:
                precio_kwp = 0
        except Exception as e:
            precio_kwp = 0
        
        c1.metric("💰 Ahorro Total", f"${ahorro_total:,.0f}", "MXN/mes")
        c2.metric("⚡ kWp Total", f"{df['sistema_recomendado'].sum():,.1f}")
        c3.metric("🔥 Premium", len(df[df['score_ia']>=8]))
        c4.metric("⭐ Score", f"{df['score_ia'].mean():.1f}/10")
        c5.metric("💎 Precio/kWp", f"${precio_kwp:,.0f}", "MXN estimado")

        st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
        
        # Contenedor para las columnas del dashboard
        st.markdown('<div class="dashboard-columns">', unsafe_allow_html=True)
        
        # Dividir en dos columnas: Mapa (izquierda) y Gráficos (derecha)
        col_map, col_graficos = st.columns([1, 1], gap="small")
        
        # COLUMNA 1: MAPA (ocupa toda la altura)
        with col_map:
            st.markdown('<div class="section-title">🗺️ Distribución por Estado</div>', unsafe_allow_html=True)
            
            df['estado_limpio'] = df['direccion'].apply(extraer_estado)
            # Ensure ahorro_mensual is numeric for aggregation
            try:
                df['ahorro_mensual_clean'] = df['ahorro_mensual'].apply(lambda x: float(x) if pd.notna(x) and str(x).replace('.','').replace('-','').isdigit() else 0)
            except Exception as e:
                st.error(f"Error processing ahorro_mensual for map: {e}")
                df['ahorro_mensual_clean'] = 0
            
            # Función para obtener precio por sector (misma que en el gráfico)
            def get_precio_por_sector_map(tipo_negocio):
                if pd.isna(tipo_negocio):
                    return 32000
                tipo_lower = str(tipo_negocio).lower()
                if 'lavander' in tipo_lower:
                    return 28000
                elif 'restaurante' in tipo_lower or 'restaurant' in tipo_lower:
                    return 32000
                elif 'hotel' in tipo_lower:
                    return 35000
                elif 'casino' in tipo_lower:
                    return 38000
                elif 'tortiller' in tipo_lower:
                    return 26000
                elif 'farmacia' in tipo_lower:
                    return 30000
                elif 'supermercado' in tipo_lower or 'super' in tipo_lower:
                    return 34000
                elif 'taller' in tipo_lower:
                    return 29000
                elif 'oficina' in tipo_lower:
                    return 31000
                else:
                    return 32000
            
            # Calcular proyecciones y datos adicionales por estado
            df_map_detailed = []
            for estado in df[df['estado_limpio'] != 'Desconocido']['estado_limpio'].unique():
                leads_estado = df[df['estado_limpio'] == estado]
                
                # Estadísticas básicas
                total_leads = len(leads_estado)
                score_prom = leads_estado['score_ia'].mean()
                ahorro_total = leads_estado['ahorro_mensual_clean'].sum()
                kwp_total = leads_estado['sistema_recomendado'].sum()
                
                # Calcular proyección de ventas
                proyeccion_ventas = 0
                precios_kwp = []
                sectores_count = {}
                
                for _, lead in leads_estado.iterrows():
                    if pd.notna(lead['sistema_recomendado']) and lead['sistema_recomendado'] > 0:
                        precio_kwp = get_precio_por_sector_map(lead['tipo_negocio'])
                        proyeccion_ventas += lead['sistema_recomendado'] * precio_kwp
                        precios_kwp.append(precio_kwp)
                        
                        # Contar sectores
                        sector = lead['tipo_negocio'] if pd.notna(lead['tipo_negocio']) else 'Otros'
                        sectores_count[sector] = sectores_count.get(sector, 0) + 1
                
                # Precio promedio por kWp en este estado
                precio_kwp_promedio = sum(precios_kwp) / len(precios_kwp) if precios_kwp else 32000
                
                # Top 3 sectores en este estado
                top_sectores = sorted(sectores_count.items(), key=lambda x: x[1], reverse=True)[:3]
                sectores_texto = ", ".join([f"{sector} ({count})" for sector, count in top_sectores])
                
                df_map_detailed.append({
                    'estado': estado,
                    'leads': total_leads,
                    'score_prom': score_prom,
                    'ahorro_total': ahorro_total,
                    'kwp_total': kwp_total,
                    'proyeccion_ventas': proyeccion_ventas,
                    'precio_kwp_promedio': precio_kwp_promedio,
                    'sectores_principales': sectores_texto,
                    'valor_promedio_lead': proyeccion_ventas / total_leads if total_leads > 0 else 0
                })
            
            df_map = pd.DataFrame(df_map_detailed)
            
            # Agregar coordenadas explícitas
            df_map['lat'] = df_map['estado'].apply(lambda x: ESTADOS_MX.get(x, [23.0, -102.0])[0])
            df_map['lon'] = df_map['estado'].apply(lambda x: ESTADOS_MX.get(x, [23.0, -102.0])[1])

            if not df_map.empty:
                st.write(f"📍 {len(df_map)} estados")
                
                # Crear mapa centrado en México con estilo profesional y sin fondo blanco
                m = folium.Map(
                    location=[23.5, -102.0], 
                    zoom_start=5.2,  # Zoom ligeramente mayor para mejor ajuste
                    tiles=None,
                    prefer_canvas=True  # Mejor rendimiento
                )
                
                # Agregar tile layer personalizado (más profesional y sin fondo blanco)
                folium.TileLayer(
                    tiles='https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png',
                    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                    name='CartoDB Dark No Labels',
                    overlay=False,
                    control=True
                ).add_to(m)
                
                # Calcular tamaños proporcionales de burbujas (más pequeñas)
                max_leads = df_map['leads'].max()
                min_leads = df_map['leads'].min()
                
                # Función para calcular color tipo semáforo basado en cantidad de leads
                def get_semaforo_color(leads_count, max_count, min_count):
                    if max_count == min_count:
                        return '#10b981'  # Verde medio si todos son iguales
                    
                    # Calcular proporción (0 = mínimo, 1 = máximo)
                    proportion = (leads_count - min_count) / (max_count - min_count)
                    
                    if proportion >= 0.8:
                        return '#059669'  # Verde oscuro (más leads)
                    elif proportion >= 0.6:
                        return '#10b981'  # Verde medio
                    elif proportion >= 0.4:
                        return '#34d399'  # Verde claro
                    elif proportion >= 0.2:
                        return '#fbbf24'  # Amarillo
                    else:
                        return '#ef4444'  # Rojo (menos leads)
                
                # Agregar círculos por estado con tamaño proporcional más pequeño
                for _, row in df_map.iterrows():
                    # Calcular radio proporcional: mínimo 4, máximo 18 (más pequeño)
                    if max_leads == min_leads:
                        radius = 10  # Si todos tienen el mismo número, usar tamaño medio
                    else:
                        # Escala proporcional: estado con más leads = burbuja más grande
                        proportion = (row['leads'] - min_leads) / (max_leads - min_leads)
                        radius = 4 + (proportion * 14)  # Rango de 4 a 18 píxeles (reducido)
                    
                    # Color tipo semáforo basado en cantidad de leads
                    color = get_semaforo_color(row['leads'], max_leads, min_leads)
                    
                    # Determinar descripción del color
                    proportion = (row['leads'] - min_leads) / (max_leads - min_leads) if max_leads != min_leads else 0.5
                    if proportion >= 0.8:
                        color_desc = "🟢 Muy Alto"
                    elif proportion >= 0.6:
                        color_desc = "🟢 Alto"
                    elif proportion >= 0.4:
                        color_desc = "🟡 Medio"
                    elif proportion >= 0.2:
                        color_desc = "🟠 Bajo"
                    else:
                        color_desc = "🔴 Muy Bajo"
                    
                    folium.CircleMarker(
                        location=[float(row['lat']), float(row['lon'])],
                        radius=radius,
                        color=color,
                        weight=2,
                        fill=True,
                        fillColor=color,
                        fillOpacity=0.8,
                        opacity=0.9,
                        popup=folium.Popup(
                            f"""
                            <div style='font-family: Arial; min-width: 280px; background: #1e293b; color: #f1f5f9; padding: 15px; border-radius: 8px;'>
                                <h4 style='margin: 0; color: #f1f5f9; text-align: center; border-bottom: 2px solid #334155; padding-bottom: 10px; margin-bottom: 12px;'>
                                    🗺️ {row['estado']}
                                </h4>
                                
                                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px;'>
                                    <div style='background: rgba(59, 130, 246, 0.1); padding: 8px; border-radius: 6px; border-left: 3px solid #3b82f6;'>
                                        <div style='font-size: 0.8rem; color: #94a3b8;'>📊 Leads</div>
                                        <div style='font-weight: 600; font-size: 1.1rem;'>{row['leads']}</div>
                                        <div style='font-size: 0.75rem; color: #94a3b8;'>{row['leads']/len(df)*100:.1f}% del total</div>
                                    </div>
                                    <div style='background: rgba(16, 185, 129, 0.1); padding: 8px; border-radius: 6px; border-left: 3px solid #10b981;'>
                                        <div style='font-size: 0.8rem; color: #94a3b8;'>⭐ Score Prom</div>
                                        <div style='font-weight: 600; font-size: 1.1rem;'>{row['score_prom']:.1f}/10</div>
                                        <div style='font-size: 0.75rem; color: #94a3b8;'>{color_desc}</div>
                                    </div>
                                </div>
                                
                                <div style='background: rgba(245, 158, 11, 0.1); padding: 10px; border-radius: 6px; border-left: 3px solid #f59e0b; margin-bottom: 12px;'>
                                    <div style='font-size: 0.85rem; color: #f59e0b; font-weight: 600; margin-bottom: 6px;'>💰 Proyección Financiera</div>
                                    <div style='font-size: 0.8rem; margin-bottom: 3px;'>
                                        <span style='color: #94a3b8;'>Total:</span> 
                                        <span style='font-weight: 600; color: #10b981;'>${row['proyeccion_ventas']:,.0f} MXN</span>
                                    </div>
                                    <div style='font-size: 0.8rem; margin-bottom: 3px;'>
                                        <span style='color: #94a3b8;'>Promedio/Lead:</span> 
                                        <span style='font-weight: 600;'>${row['valor_promedio_lead']:,.0f} MXN</span>
                                    </div>
                                    <div style='font-size: 0.8rem;'>
                                        <span style='color: #94a3b8;'>Precio/kWp:</span> 
                                        <span style='font-weight: 600;'>${row['precio_kwp_promedio']:,.0f} MXN</span>
                                    </div>
                                </div>
                                
                                <div style='background: rgba(139, 92, 246, 0.1); padding: 10px; border-radius: 6px; border-left: 3px solid #8b5cf6; margin-bottom: 12px;'>
                                    <div style='font-size: 0.85rem; color: #8b5cf6; font-weight: 600; margin-bottom: 6px;'>🏢 Sectores Principales</div>
                                    <div style='font-size: 0.8rem; line-height: 1.3;'>{row['sectores_principales'] if row['sectores_principales'] else 'Sin datos'}</div>
                                </div>
                                
                                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 8px;'>
                                    <div style='text-align: center; background: rgba(34, 197, 94, 0.1); padding: 6px; border-radius: 4px;'>
                                        <div style='font-size: 0.75rem; color: #94a3b8;'>💰 Ahorro/mes</div>
                                        <div style='font-size: 0.85rem; font-weight: 600;'>${row['ahorro_total']:,.0f}</div>
                                    </div>
                                    <div style='text-align: center; background: rgba(234, 179, 8, 0.1); padding: 6px; border-radius: 4px;'>
                                        <div style='font-size: 0.75rem; color: #94a3b8;'>⚡ Total kWp</div>
                                        <div style='font-size: 0.85rem; font-weight: 600;'>{row['kwp_total']:,.1f}</div>
                                    </div>
                                </div>
                                
                                <div style='margin-top: 10px; padding-top: 8px; border-top: 1px solid #334155; font-size: 0.75rem; color: #94a3b8; text-align: center;'>
                                    💡 Proyección basada en precios diferenciados por sector
                                </div>
                            </div>
                            """,
                            max_width=320
                        ),
                        tooltip=f"{row['estado']}: {row['leads']} leads • ${row['proyeccion_ventas']:,.0f} MXN • {color_desc}"
                    ).add_to(m)
                
                # Mostrar mapa con configuración mejorada y sin fondo blanco
                map_data = st_folium(
                    m, 
                    width="100%",  # Usar porcentaje en lugar de píxeles fijos
                    height=900,  # Altura mayor para ocupar el espacio de los dos gráficos
                    returned_objects=["last_object_clicked"]
                )
                
                # Agregar leyenda del sistema de colores con información financiera
                proyeccion_total_mapa = df_map['proyeccion_ventas'].sum()
                valor_promedio_general = df_map['valor_promedio_lead'].mean()
                
                st.markdown(f"""
                <div style='font-size: 0.8rem; color: #94a3b8; text-align: center; margin-top: 8px; background: rgba(15, 31, 56, 0.3); padding: 12px; border-radius: 6px; border: 1px solid rgba(26, 53, 86, 0.5);'>
                    <div style='margin-bottom: 8px;'>
                        <strong>🚦 Sistema de Colores:</strong><br>
                        <span style='color: #059669;'>🟢 Verde Oscuro</span> = Más leads | 
                        <span style='color: #10b981;'>🟢 Verde</span> = Muchos | 
                        <span style='color: #fbbf24;'>🟡 Amarillo</span> = Medio | 
                        <span style='color: #ef4444;'>🔴 Rojo</span> = Pocos leads
                    </div>
                    <div style='border-top: 1px solid rgba(51, 65, 85, 0.5); padding-top: 8px;'>
                        <strong>💰 Proyección Total del Mapa:</strong> ${proyeccion_total_mapa:,.0f} MXN<br>
                        <strong>💎 Valor Promedio por Lead:</strong> ${valor_promedio_general:,.0f} MXN<br>
                        <small>Rango de leads: {df_map['leads'].min()} - {df_map['leads'].max()} por estado</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ No se reconocieron estados")
        
        # COLUMNA 2: GRÁFICOS APILADOS (Pipeline + Tipos de Negocio)
        with col_graficos:
            # GRÁFICO 1: ESTADO DEL PIPELINE
            st.markdown('<div class="section-title">📊 Estado del Pipeline</div>', unsafe_allow_html=True)
            
            # Contar leads por estado de pipeline
            pipeline_counts = df['estado_pipeline'].value_counts().reset_index()
            pipeline_counts.columns = ['Estado', 'Cantidad']
            
            # Calcular porcentajes
            pipeline_counts['Porcentaje'] = (pipeline_counts['Cantidad'] / len(df) * 100).round(1)
            
            # Calcular proyección de ventas por estado
            def get_precio_por_sector(tipo_negocio):
                """Obtiene el precio por kWp según el tipo de negocio"""
                if pd.isna(tipo_negocio):
                    return 32000  # Precio default
                
                tipo_lower = str(tipo_negocio).lower()
                
                if 'lavander' in tipo_lower:
                    return 28000
                elif 'restaurante' in tipo_lower or 'restaurant' in tipo_lower:
                    return 32000
                elif 'hotel' in tipo_lower:
                    return 35000
                elif 'casino' in tipo_lower:
                    return 38000
                elif 'tortiller' in tipo_lower:
                    return 26000
                elif 'farmacia' in tipo_lower:
                    return 30000
                elif 'supermercado' in tipo_lower or 'super' in tipo_lower:
                    return 34000
                elif 'taller' in tipo_lower:
                    return 29000
                elif 'oficina' in tipo_lower:
                    return 31000
                else:
                    return 32000  # Precio default
            
            # Calcular proyección de ventas por estado
            proyecciones = []
            for estado in pipeline_counts['Estado']:
                leads_estado = df[df['estado_pipeline'] == estado]
                proyeccion_total = 0
                
                for _, lead in leads_estado.iterrows():
                    if pd.notna(lead['sistema_recomendado']) and lead['sistema_recomendado'] > 0:
                        precio_kwp = get_precio_por_sector(lead['tipo_negocio'])
                        proyeccion_lead = lead['sistema_recomendado'] * precio_kwp
                        proyeccion_total += proyeccion_lead
                
                proyecciones.append(proyeccion_total)
            
            pipeline_counts['Proyeccion_Ventas'] = proyecciones
            
            # Crear etiquetas con cantidad y porcentaje
            pipeline_counts['Etiqueta'] = pipeline_counts.apply(
                lambda row: f"{row['Cantidad']} ({row['Porcentaje']}%)", axis=1
            )
            
            # Ordenar por cantidad descendente
            pipeline_counts = pipeline_counts.sort_values('Cantidad', ascending=True)
            
            if not pipeline_counts.empty:
                st.write(f"📈 {len(df)} leads totales")
                
                # Crear gráfico de barras horizontales con Plotly (más estable)
                import plotly.graph_objects as go
                import plotly.express as px
                
                # Definir colores por estado
                color_map = {
                    'Nuevo': '#3b82f6',           # Azul
                    'Sin teléfono': '#6b7280',    # Gris
                    'No WhatsApp': '#ef4444',     # Rojo
                    'Contactado': '#10b981',      # Verde
                    'Calificado': '#f59e0b',      # Naranja
                    'Propuesta enviada': '#8b5cf6', # Púrpura
                    'En negociación': '#ec4899',  # Rosa
                    'Cerrado ganado': '#059669',  # Verde oscuro
                    'Cerrado perdido': '#dc2626', # Rojo oscuro
                    'No responde': '#9ca3af',     # Gris claro
                    'Descartado': '#374151'       # Gris oscuro
                }
                
                # Asignar colores a cada estado
                colors = [color_map.get(estado, '#64748b') for estado in pipeline_counts['Estado']]
                
                # Crear texto personalizado para el hover
                hover_text = []
                for _, row in pipeline_counts.iterrows():
                    if row['Proyeccion_Ventas'] > 0:
                        hover_text.append(
                            f"<b>{row['Estado']}</b><br>" +
                            f"Leads: {row['Cantidad']}<br>" +
                            f"Porcentaje: {row['Porcentaje']}%<br>" +
                            f"💰 Proyección: ${row['Proyeccion_Ventas']:,.0f} MXN<br>" +
                            f"💎 Promedio/Lead: ${row['Proyeccion_Ventas']/row['Cantidad']:,.0f} MXN"
                        )
                    else:
                        hover_text.append(
                            f"<b>{row['Estado']}</b><br>" +
                            f"Leads: {row['Cantidad']}<br>" +
                            f"Porcentaje: {row['Porcentaje']}%<br>" +
                            f"💰 Proyección: Sin datos de sistema"
                        )
                
                # Crear gráfico de barras horizontales
                fig = go.Figure(data=[
                    go.Bar(
                        y=pipeline_counts['Estado'],
                        x=pipeline_counts['Cantidad'],
                        orientation='h',
                        marker=dict(
                            color=colors,
                            line=dict(color='rgba(0,0,0,0)', width=0)
                        ),
                        text=pipeline_counts['Etiqueta'],
                        textposition='outside',
                        textfont=dict(color='#e2e8f0', size=11),
                        hovertemplate='%{customdata}<extra></extra>',
                        customdata=hover_text
                    )
                ])
                
                # Configurar layout
                fig.update_layout(
                    height=400,
                    margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e2e8f0'),
                    xaxis=dict(
                        showgrid=False,
                        showticklabels=False,
                        showline=False,
                        zeroline=False
                    ),
                    yaxis=dict(
                        showgrid=False,
                        showline=False,
                        tickfont=dict(color='#e2e8f0', size=12),
                        categoryorder='total ascending'
                    ),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                
            else:
                st.info("No hay datos de pipeline")
            
            # Separador entre gráficos
            st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
            
            # GRÁFICO 2: TIPOS DE NEGOCIO
            st.markdown('<div class="section-title">🏢 Proyección por Tipo de Negocio</div>', unsafe_allow_html=True)
            
            # Agrupar por tipo de negocio
            if 'tipo_negocio' in df.columns and df['tipo_negocio'].notna().any():
                # Contar leads por tipo de negocio
                negocio_counts = df['tipo_negocio'].value_counts().reset_index()
                negocio_counts.columns = ['Tipo', 'Cantidad']
                
                # Calcular proyecciones financieras por tipo de negocio
                proyecciones_negocio = []
                kwp_totales = []
                ahorro_totales = []
                
                for tipo in negocio_counts['Tipo']:
                    leads_tipo = df[df['tipo_negocio'] == tipo]
                    proyeccion_total = 0
                    kwp_total = 0
                    ahorro_total = 0
                    
                    for _, lead in leads_tipo.iterrows():
                        if pd.notna(lead['sistema_recomendado']) and lead['sistema_recomendado'] > 0:
                            precio_kwp = get_precio_por_sector(lead['tipo_negocio'])
                            proyeccion_lead = lead['sistema_recomendado'] * precio_kwp
                            proyeccion_total += proyeccion_lead
                            kwp_total += lead['sistema_recomendado']
                        
                        # Sumar ahorro mensual
                        if 'ahorro_mensual_clean' in lead.index and pd.notna(lead['ahorro_mensual_clean']):
                            ahorro_total += lead['ahorro_mensual_clean']
                    
                    proyecciones_negocio.append(proyeccion_total)
                    kwp_totales.append(kwp_total)
                    ahorro_totales.append(ahorro_total)
                
                negocio_counts['Proyeccion_Ventas'] = proyecciones_negocio
                negocio_counts['kWp_Total'] = kwp_totales
                negocio_counts['Ahorro_Total'] = ahorro_totales
                negocio_counts['Porcentaje'] = (negocio_counts['Cantidad'] / len(df) * 100).round(1)
                
                # Ordenar por proyección de ventas descendente y tomar top 8
                negocio_counts = negocio_counts.sort_values('Proyeccion_Ventas', ascending=True).tail(8)
                
                if not negocio_counts.empty:
                    st.write(f"📊 Top {len(negocio_counts)} tipos de negocio")
                    
                    # Crear colores degradados basados en proyección
                    max_proyeccion = negocio_counts['Proyeccion_Ventas'].max()
                    colors_negocio = []
                    for proyeccion in negocio_counts['Proyeccion_Ventas']:
                        if max_proyeccion > 0:
                            intensity = proyeccion / max_proyeccion
                            if intensity >= 0.8:
                                colors_negocio.append('#059669')  # Verde oscuro
                            elif intensity >= 0.6:
                                colors_negocio.append('#10b981')  # Verde
                            elif intensity >= 0.4:
                                colors_negocio.append('#f59e0b')  # Naranja
                            elif intensity >= 0.2:
                                colors_negocio.append('#f97316')  # Naranja oscuro
                            else:
                                colors_negocio.append('#ef4444')  # Rojo
                        else:
                            colors_negocio.append('#64748b')  # Gris
                    
                    # Crear texto personalizado para el hover con datos financieros
                    hover_text_negocio = []
                    for _, row in negocio_counts.iterrows():
                        precio_kwp_tipo = get_precio_por_sector(row['Tipo'])
                        hover_text_negocio.append(
                            f"<b>{row['Tipo']}</b><br>" +
                            f"<br>" +
                            f"📊 <b>Leads:</b> {row['Cantidad']} ({row['Porcentaje']}%)<br>" +
                            f"<br>" +
                            f"💰 <b>Proyección Total:</b> ${row['Proyeccion_Ventas']:,.0f} MXN<br>" +
                            f"💎 <b>Promedio/Lead:</b> ${row['Proyeccion_Ventas']/row['Cantidad']:,.0f} MXN<br>" +
                            f"<br>" +
                            f"⚡ <b>kWp Total:</b> {row['kWp_Total']:,.1f} kWp<br>" +
                            f"⚡ <b>kWp Promedio:</b> {row['kWp_Total']/row['Cantidad']:,.1f} kWp/lead<br>" +
                            f"<br>" +
                            f"💵 <b>Ahorro Mensual:</b> ${row['Ahorro_Total']:,.0f} MXN<br>" +
                            f"💵 <b>Ahorro/Lead:</b> ${row['Ahorro_Total']/row['Cantidad']:,.0f} MXN/mes<br>" +
                            f"<br>" +
                            f"🏷️ <b>Precio/kWp:</b> ${precio_kwp_tipo:,.0f} MXN"
                        )
                    
                    # Crear etiquetas con proyección
                    negocio_counts['Etiqueta'] = negocio_counts.apply(
                        lambda row: f"${row['Proyeccion_Ventas']/1000000:.1f}M" if row['Proyeccion_Ventas'] >= 1000000 
                        else f"${row['Proyeccion_Ventas']/1000:.0f}k", 
                        axis=1
                    )
                    
                    # Crear gráfico de barras horizontales
                    fig_negocio = go.Figure(data=[
                        go.Bar(
                            y=negocio_counts['Tipo'],
                            x=negocio_counts['Proyeccion_Ventas'],
                            orientation='h',
                            marker=dict(
                                color=colors_negocio,
                                line=dict(color='rgba(0,0,0,0)', width=0)
                            ),
                            text=negocio_counts['Etiqueta'],
                            textposition='outside',
                            textfont=dict(color='#e2e8f0', size=10),
                            hovertemplate='%{customdata}<extra></extra>',
                            customdata=hover_text_negocio
                        )
                    ])
                    
                    # Configurar layout
                    fig_negocio.update_layout(
                        height=400,
                        margin=dict(l=10, r=10, t=10, b=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e2e8f0'),
                        xaxis=dict(
                            showgrid=False,
                            showticklabels=False,
                            showline=False,
                            zeroline=False
                        ),
                        yaxis=dict(
                            showgrid=False,
                            showline=False,
                            tickfont=dict(color='#e2e8f0', size=11),
                            categoryorder='total ascending'
                        ),
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_negocio, use_container_width=True, config={'displayModeBar': False})
                    
                    # Resumen financiero
                    total_proyeccion_negocios = negocio_counts['Proyeccion_Ventas'].sum()
                    st.markdown(f"""
                    <div style='font-size: 0.8rem; color: #94a3b8; text-align: center; margin-top: 8px; background: rgba(15, 31, 56, 0.3); padding: 10px; border-radius: 6px; border: 1px solid rgba(26, 53, 86, 0.5);'>
                        <strong>💰 Proyección:</strong> ${total_proyeccion_negocios:,.0f} MXN • 
                        <strong>⚡ kWp:</strong> {negocio_counts['kWp_Total'].sum():,.1f} • 
                        <strong>📊 Leads:</strong> {negocio_counts['Cantidad'].sum()}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No hay datos de tipos de negocio")
            else:
                st.info("No hay información de tipos de negocio disponible")
        
        # Cerrar contenedor de columnas del dashboard
        st.markdown('</div>', unsafe_allow_html=True)
           

    else:  # Vista Pipeline de Leads
        st.markdown('<div class="section-title">📋 Pipeline de Leads</div>', unsafe_allow_html=True)
        
        # Filtros expandidos
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            filtro_estado_pipeline = st.selectbox(
                "Estado Pipeline",
                ["Todos", "Nuevo", "Sin teléfono", "No WhatsApp", "Contactado", "Calificado", 
                 "Propuesta enviada", "En negociación", "Cerrado ganado", "Cerrado perdido", 
                 "No responde", "Descartado"]
            )
        with col2:
            # Filtro de Estado Geográfico - usar los mismos estados que el mapa
            df['estado_limpio'] = df['direccion'].apply(extraer_estado)
            estados_geograficos = ["Todos"] + sorted(df[df['estado_limpio'] != 'Desconocido']['estado_limpio'].dropna().unique().tolist())
            filtro_estado_geo = st.selectbox(
                "Estado Geográfico",
                estados_geograficos
            )
        with col3:
            # Filtro de Tipo de Negocio
            tipos_negocio = ["Todos"] + sorted(df['tipo_negocio'].dropna().unique().tolist())
            filtro_tipo = st.selectbox(
                "Tipo de Negocio",
                tipos_negocio
            )
        with col4:
            filtro_score = st.slider("Score mínimo", 0, 10, 0)
        with col5:
            filtro_busqueda = st.text_input("Buscar por nombre", "")
        
        # Aplicar filtros expandidos
        df_filtrado = df.copy()
        
        # Asegurar que estado_limpio esté disponible para el filtro
        if 'estado_limpio' not in df_filtrado.columns:
            df_filtrado['estado_limpio'] = df_filtrado['direccion'].apply(extraer_estado)
        
        if filtro_estado_pipeline != "Todos":
            df_filtrado = df_filtrado[df_filtrado['estado_pipeline'] == filtro_estado_pipeline]
        
        if filtro_estado_geo != "Todos":
            df_filtrado = df_filtrado[df_filtrado['estado_limpio'] == filtro_estado_geo]
        
        if filtro_tipo != "Todos":
            df_filtrado = df_filtrado[df_filtrado['tipo_negocio'] == filtro_tipo]
        
        if filtro_score > 0:
            df_filtrado = df_filtrado[df_filtrado['score_ia'] >= filtro_score]
        
        if filtro_busqueda:
            df_filtrado = df_filtrado[
                df_filtrado['nombre'].str.contains(filtro_busqueda, case=False, na=False)
            ]
        
        # Mostrar estadísticas del filtro
        st.markdown(f"**{len(df_filtrado)}** leads encontrados")
        
        # Tabla de leads con editor de estados en columna Pipeline
        if not df_filtrado.empty:
            # Estados disponibles para el pipeline
            estados_pipeline = [
                "Nuevo", "Sin teléfono", "No WhatsApp", "Contactado", "Calificado",
                "Propuesta enviada", "En negociación", "Cerrado ganado", 
                "Cerrado perdido", "No responde", "Descartado"
            ]
            
            # Preparar datos para la tabla
            df_display = df_filtrado[[
                'id', 'nombre', 'tipo_negocio', 'telefono', 'poblacion', 
                'estado', 'score_ia', 'ahorro_mensual', 'estado_pipeline', 'fecha_creacion'
            ]].copy()
            
            # ORDENAR: Más recientes primero (por ID descendente como proxy de fecha)
            df_display = df_display.sort_values('id', ascending=False)
            
            # Formatear columnas - mantener ahorro_mensual como numérico para cálculos
            try:
                df_display['ahorro_mensual_num'] = df_display['ahorro_mensual'].apply(
                    lambda x: float(x) if pd.notna(x) and str(x).replace('.','').replace('-','').isdigit() else 0
                )
            except Exception as e:
                st.error(f"Error processing ahorro_mensual for table: {e}")
                df_display['ahorro_mensual_num'] = 0
            
            # Crear tabla con editor de estados
            st.markdown("### 📝 Gestión de Estados")
            st.markdown("*Tabla compacta - Los cambios en Pipeline se guardan automáticamente*")
            
            # Headers compactos
            col_headers = st.columns([0.4, 2.8, 0.9, 1.1, 0.6, 1.1, 1.4])
            headers = ['ID', 'Lead Info', 'Tipo', 'Tel/Ciudad', 'Score', 'Ahorro', 'Pipeline']
            
            # Headers con estilo mejorado
            for i, header in enumerate(headers):
                col_headers[i].markdown(f'<div class="pipeline-table-header">{header}</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Mostrar cada fila compacta
            for idx, row in df_display.iterrows():
                with st.container():
                    st.markdown('<div class="pipeline-table-row">', unsafe_allow_html=True)
                    
                    cols = st.columns([0.4, 2.8, 0.9, 1.1, 0.6, 1.1, 1.4])
                    
                    # ID compacto
                    cols[0].markdown(f'<div class="pipeline-table-cell"><strong>{row["id"]}</strong></div>', unsafe_allow_html=True)
                    
                    # Lead Info (Nombre + Estado geográfico)
                    lead_info = f'<strong>{row["nombre"]}</strong><br><small style="color: #94a3b8;">{row["poblacion"]}, {row["estado"]}</small>'
                    cols[1].markdown(f'<div class="pipeline-table-cell">{lead_info}</div>', unsafe_allow_html=True)
                    
                    # Tipo compacto
                    tipo_short = (row["tipo_negocio"][:8] + "...") if pd.notna(row["tipo_negocio"]) and len(str(row["tipo_negocio"])) > 8 else (row["tipo_negocio"] if pd.notna(row["tipo_negocio"]) else "-")
                    cols[2].markdown(f'<div class="pipeline-table-cell" title="{row["tipo_negocio"] if pd.notna(row["tipo_negocio"]) else ""}">{tipo_short}</div>', unsafe_allow_html=True)
                    
                    # Teléfono compacto con estado
                    telefono_text = row['telefono'] if pd.notna(row['telefono']) else 'Sin tel'
                    if len(str(telefono_text)) > 10 and telefono_text != 'Sin tel':
                        telefono_display = telefono_text[:10] + "..."
                    else:
                        telefono_display = telefono_text
                    
                    telefono_color = '#ef4444' if telefono_text == 'Sin tel' else '#e2e8f0'
                    cols[3].markdown(f'<div class="pipeline-table-cell" style="color: {telefono_color}; font-size: 0.8rem;" title="{telefono_text}">{telefono_display}</div>', unsafe_allow_html=True)
                    
                    # Score con color
                    score_color = '#10b981' if row['score_ia'] >= 7 else '#f59e0b' if row['score_ia'] >= 4 else '#ef4444'
                    cols[4].markdown(f'<div class="pipeline-table-cell" style="color: {score_color}; font-weight: 600; text-align: center;">{row["score_ia"]}</div>', unsafe_allow_html=True)
                    
                    # Ahorro compacto
                    try:
                        ahorro_num = row['ahorro_mensual_num'] if pd.notna(row['ahorro_mensual_num']) else 0
                        if ahorro_num >= 1000:
                            # Better formatting for thousands
                            if ahorro_num >= 1000000:
                                ahorro_short = f"${ahorro_num/1000000:.1f}M"
                            else:
                                ahorro_short = f"${ahorro_num/1000:.0f}k"
                        else:
                            ahorro_short = f"${ahorro_num:,.0f}"
                    except Exception as e:
                        ahorro_short = "$0"
                    cols[5].markdown(f'<div class="pipeline-table-cell" style="color: #10b981; font-weight: 600; font-size: 0.8rem;" title="${ahorro_num:,.0f}/mes">{ahorro_short}</div>', unsafe_allow_html=True)
                    
                    # Lista desplegable para Pipeline con auto-guardado mejorado
                    estado_actual = row['estado_pipeline']
                    nuevo_estado = cols[6].selectbox(
                        "",
                        estados_pipeline,
                        index=estados_pipeline.index(estado_actual) if estado_actual in estados_pipeline else 0,
                        key=f"pipeline_{row['id']}",
                        label_visibility="collapsed"
                    )
                    
                    # Auto-guardar cuando cambia el estado (lógica simplificada)
                    if nuevo_estado != estado_actual:
                        try:
                            # Guardar inmediatamente
                            service.update_lead_status(row['id'], nuevo_estado)
                            st.success(f"✅ {row['nombre']}: {nuevo_estado}")
                            # Forzar actualización de la página
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error actualizando {row['nombre']}: {e}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('<div style="height: 2px;"></div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Solo mantener el botón de descarga CSV
            csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label=f"📥 Descargar CSV ({len(df_filtrado)} leads)",
                data=csv,
                file_name=f"leads_{filtro_estado_pipeline.lower().replace(' ', '_')}.csv",
                mime="text/csv",
                help=f"Descarga {len(df_filtrado)} leads filtrados en formato CSV"
            )
        else:
            st.info("No hay leads que coincidan con los filtros seleccionados")

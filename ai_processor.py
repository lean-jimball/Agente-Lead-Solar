import os
import json
import time
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1'})
else:
    client = None
    print("⚠️ ADVERTENCIA: No se encontró GEMINI_API_KEY. Usando modo prueba.")

# Lista negra: negocios con decisión corporativa centralizada
CORPORATE_BLACKLIST = [
    'oxxo', '7-eleven', 'seven eleven', 'extra', 'circulo k', 'kiosko',
    'walmart', 'bodega aurrera', 'soriana', 'chedraui', 'coppel', 'elektra',
    'farmacia guadalajara', 'farmacia del ahorro', 'benavides', 'samborns',
    'sanborns', 'vips', 'toks', 'starbucks', 'mcdonalds', 'burger king',
    'kfc', 'dominos', 'little caesars', 'subway', 'ihop', 'carls jr',
    'bbva', 'santander', 'banorte', 'hsbc', 'citibanamex', 'scotiabank'
]

# Ranking solo negocios con decisión local
INDUSTRY_SCORES = {
    'lavanderia': 9, 'tintoreria': 9, 'lavamatica': 9,
    'hotel': 8, 'motel': 8, 'posada': 7, 'hostal': 7,
    'hospital': 9, 'clinica': 8, 'sanatorio': 8, 'consultorio': 5,
    'restaurante': 7, 'bar': 7, 'cantina': 6, 'taqueria': 6, 'fondita': 5,
    'gimnasio': 7, 'crossfit': 7, 'box': 7, 'alberca': 7,
    'escuela': 6, 'colegio': 6, 'universidad': 7, 'guarderia': 5,
    'carwash': 6, 'autolavado': 6, 'autobaño': 6,
    'salon de eventos': 5, 'jardin de eventos': 5, 'salon de fiestas': 5,
    'taller': 5, 'mecanico': 5, 'hojalateria': 5, 'vulcanizadora': 4,
    'oficina': 4, 'coworking': 4, 'despacho': 4,
    'tienda': 3, 'abarrotes': 3, 'papeleria': 3, 'boutique': 3,
    'iglesia': 2, 'templo': 2, 'casa': 3
}

def is_corporate(nombre):
    """Detecta si es franquicia/corporativo"""
    nombre_lower = nombre.lower()
    return any(banned in nombre_lower for banned in CORPORATE_BLACKLIST)

def get_base_score(tipo_negocio, nombre):
    """Asigna score base. Si es corporativo regresa 0"""
    if is_corporate(nombre):
        return 0
    
    if not tipo_negocio:
        return 5
    
    # Normalizar: quitar acentos para comparación
    import unicodedata
    tipo_lower = tipo_negocio.lower()
    tipo_normalized = ''.join(c for c in unicodedata.normalize('NFD', tipo_lower) if unicodedata.category(c) != 'Mn')
    
    for keyword, score in INDUSTRY_SCORES.items():
        keyword_normalized = ''.join(c for c in unicodedata.normalize('NFD', keyword) if unicodedata.category(c) != 'Mn')
        if keyword_normalized in tipo_normalized:
            return score
    return 4  # Default para negocios locales no listados

def analyze_lead(lead_data):
    nombre = lead_data.get('nombre', 'Sin nombre')
    tipo = lead_data.get('tipo_negocio', 'negocio')
    direccion = lead_data.get('direccion', 'México')
    
    # Filtro 1: Si es corporativo, descartar antes de llamar API
    if is_corporate(nombre):
        print(f"🚫 Descartado: {nombre} - Decisión corporativa")
        return {
            "score_ia": 0,
            "razon_score": "Franquicia/corporativo - No decide localmente",
            "consumo_estimado": 0,
            "sistema_recomendado": 0,
            "ahorro_mensual": 0,
            "mensaje_generado": ""
        }
    
    base_score = get_base_score(tipo, nombre)

    # Modo prueba sin API
    if not API_KEY or not client:
        print(f"🔧 Modo prueba: {nombre} - Score {base_score}")
        return {
            "score_ia": base_score,
            "razon_score": "Modo prueba - Score por industria local",
            "consumo_estimado": base_score * 350,
            "sistema_recomendado": round(base_score * 350 / 130, 1),
            "ahorro_mensual": int(base_score * 350 / 130 * 130 * 3.5),
            "mensaje_generado": f"Hola {nombre}, vi que puedes ahorrar en luz con paneles solares."
        }

    try:
        prompt = f"""Eres un analista experto en ventas de paneles solares B2B en México.

IMPORTANTE: Solo analiza negocios con decisión de compra LOCAL. IGNORA franquicias y cadenas.

Datos:
- Nombre: {nombre}
- Tipo: {tipo}
- Ubicación: {direccion}
- Score base por industria: {base_score}

REGLAS DE SCORING:
1. score_ia: 1-10. Usa {base_score} como base.
   - Lavandería/tintorería/hospital: 9-10
   - Hotel/motel/clínica/gimnasio: 8-9
   - Restaurante/bar/escuela privada: 7-8
   - Carwash/salón eventos/taller: 5-6
   - Oficina/consultorio: 4-5
   - Tienda local/abastos: 3-4
   - Si detectas que es franquicia aunque no esté en lista: score 0
   
2. consumo_estimado: kWh mensuales realistas para negocio LOCAL.
   - Hotel 20 cuartos: 8000-12000 kWh
   - Lavandería: 3000-6000 kWh
   - Restaurante mediano: 2500-4500 kWh
   - Gimnasio: 4000-8000 kWh

3. sistema_recomendado: kWp = consumo_estimado / 130. 1 decimal.

4. ahorro_mensual: MXN = sistema_recomendado * 130 * 3.5. Redondea a cientos.

5. mensaje_generado: 1 frase WhatsApp con nombre + ahorro.

Regresa SOLO JSON:
{{
    "score_ia": {base_score},
    "razon_score": "Hotel local con consumo 24/7 en A/C",
    "consumo_estimado": 9000,
    "sistema_recomendado": 69.2,
    "ahorro_mensual": 31500,
    "mensaje_generado": "Hola {nombre}, tu hotel puede ahorrar ~$31,500/mes en CFE."
}}"""

        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )

        text = response.text.strip().replace('```json', '').replace('```', '').strip()
        match = re.search(r'\{[\s\S]*\}', text)
        if not match:
            raise ValueError(f"No JSON: {text[:100]}")

        result = json.loads(match.group(0))

        # Validación
        result['score_ia'] = max(0, min(10, int(float(result.get('score_ia', base_score)))))
        
        # Filtro 2: Si Gemini detectó corporativo, forzar 0
        if 'franquicia' in result.get('razon_score', '').lower() or 'cadena' in result.get('razon_score', '').lower():
            print(f"🚫 Gemini detectó corporativo: {nombre}")
            result['score_ia'] = 0
            result['ahorro_mensual'] = 0
            result['sistema_recomendado'] = 0

        result['consumo_estimado'] = int(float(result.get('consumo_estimado', 2000)))
        result['sistema_recomendado'] = round(float(result.get('sistema_recomendado', 10)), 1)
        result['ahorro_mensual'] = int(float(result.get('ahorro_mensual', 3000)))
        
        # Mínimo 7 para industrias calientes locales
        if base_score >= 7 and result['score_ia'] < 7 and result['score_ia'] > 0:
            result['score_ia'] = 7
            result['razon_score'] += " | Score ajustado por industria local"

        print(f"✅ {nombre} - Score {result['score_ia']} - ${result['ahorro_mensual']}/mes")
        time.sleep(1.5)
        return result

    except Exception as e:
        print(f"❌ Error Gemini: {e}")
        return {
            "score_ia": base_score,
            "razon_score": f"Error API, usado score industria: {str(e)[:50]}",
            "consumo_estimado": base_score * 350,
            "sistema_recomendado": round(base_score * 350 / 130, 1),
            "ahorro_mensual": int(base_score * 350 / 130 * 130 * 3.5),
            "mensaje_generado": f"Hola {nombre}, tenemos opciones solares para tu {tipo}."
        }
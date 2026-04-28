import sys
import time
import json
import urllib.parse
import re
from playwright.sync_api import sync_playwright


def normalizar_tipo_negocio(tipo):
    """Normaliza el tipo de negocio para agrupar variaciones similares."""
    if not tipo:
        return "Sin categoría"
    
    tipo_lower = tipo.lower().strip()
    
    # Diccionario de normalización: variaciones → categoría estándar
    normalizaciones = {
        # Lavanderías
        "lavanderia": "Lavandería",
        "lavanderias": "Lavandería",
        "lavandería": "Lavandería",
        "lavanderías": "Lavandería",
        "tintoreria": "Lavandería",
        "tintorerías": "Lavandería",
        
        # Hoteles
        "hotel": "Hotel",
        "hoteles": "Hotel",
        "motel": "Hotel",
        "moteles": "Hotel",
        "posada": "Hotel",
        "posadas": "Hotel",
        
        # Restaurantes
        "restaurante": "Restaurante",
        "restaurantes": "Restaurante",
        "restaurant": "Restaurante",
        "restaurants": "Restaurante",
        "comida": "Restaurante",
        "fonda": "Restaurante",
        "fondas": "Restaurante",
        
        # Casinos
        "casino": "Casino",
        "casinos": "Casino",
        
        # Panaderías
        "panaderia": "Panadería",
        "panaderias": "Panadería",
        "panadería": "Panadería",
        "panaderías": "Panadería",
        
        # Tortillerías
        "tortilleria": "Tortillería",
        "tortillerias": "Tortillería",
        "tortillería": "Tortillería",
        "tortillerías": "Tortillería",
        
        # Gimnasios
        "gimnasio": "Gimnasio",
        "gimnasios": "Gimnasio",
        "gym": "Gimnasio",
        
        # Supermercados
        "supermercado": "Supermercado",
        "supermercados": "Supermercado",
        "super": "Supermercado",
        "tienda": "Supermercado",
        
        # Gasolineras
        "gasolinera": "Gasolinera",
        "gasolineras": "Gasolinera",
        
        # Hospitales/Clínicas
        "hospital": "Hospital",
        "hospitales": "Hospital",
        "clinica": "Hospital",
        "clínica": "Hospital",
        "clinicas": "Hospital",
        "clínicas": "Hospital",
        
        # Escuelas
        "escuela": "Escuela",
        "escuelas": "Escuela",
        "colegio": "Escuela",
        "colegios": "Escuela",
        
        # Oficinas
        "oficina": "Oficina",
        "oficinas": "Oficina",
        
        # Talleres
        "taller": "Taller",
        "talleres": "Taller",
        "mecanico": "Taller",
        "mecánico": "Taller",
    }
    
    # Buscar normalización
    return normalizaciones.get(tipo_lower, tipo.capitalize())


def extraer_ciudad_de_query(query):
    """Extrae la ciudad/ubicación directamente de la query del usuario."""
    q = query.lower()
    
    # Patrón: "en <ciudad>" o "in <ciudad>"
    match = re.search(r'\ben\s+([a-záéíóúüñ][a-záéíóúüñ\s,]+?)(?:\s*$)', q)
    if match:
        ciudad_completa = match.group(1).strip()
        
        # Si hay coma, analizar "ciudad, estado"
        if ',' in ciudad_completa:
            partes = [p.strip() for p in ciudad_completa.split(',')]
            ciudad_parte = partes[0]
            estado_parte = partes[1] if len(partes) > 1 else ""
            
            # Casos especiales: ciudad y estado con mismo nombre
            casos_especiales = {
                "oaxaca": "Oaxaca",
                "veracruz": "Veracruz", 
                "puebla": "Puebla",
                "chihuahua": "Chihuahua",
                "colima": "Colima",
                "durango": "Durango",
                "morelos": "Morelos",
                "zacatecas": "Zacatecas"
            }
            
            ciudad_norm = ciudad_parte.lower().strip()
            estado_norm = estado_parte.lower().strip()
            
            # Si ambos son iguales y están en casos especiales, usar la ciudad
            if ciudad_norm == estado_norm and ciudad_norm in casos_especiales:
                return casos_especiales[ciudad_norm]
            
            # Si la ciudad está en casos especiales, usarla
            if ciudad_norm in casos_especiales:
                return casos_especiales[ciudad_norm]
                
            return ciudad_parte.title()
        
        return ciudad_completa.title()
    
    # Fallback: última palabra(s) significativas
    palabras = query.split()
    if len(palabras) >= 2:
        return ' '.join(palabras[-2:]).title()
    return query.title()


def extraer_estado_de_query(query):
    """Infiere el estado a partir de la ciudad mencionada en la query."""
    ciudad_estado_map = {
        # Ciudades específicas primero (para evitar conflictos con estados)
        "tehuacan": ("Tehuacán", "Pue."),
        "xalapa": ("Xalapa", "Ver."),
        "jalapa": ("Xalapa", "Ver."),
        "coatzacoalcos": ("Coatzacoalcos", "Ver."),
        "poza rica": ("Poza Rica", "Ver."),
        "cordoba": ("Córdoba", "Ver."),
        "minatitlan": ("Minatitlán", "Ver."),
        "boca del rio": ("Boca del Río", "Ver."),
        "oaxaca de juarez": ("Oaxaca de Juárez", "Oax."),
        "salina cruz": ("Salina Cruz", "Oax."),
        "juchitan": ("Juchitán", "Oax."),
        "tuxtepec": ("Tuxtepec", "Oax."),
        "chihuahua capital": ("Chihuahua", "Chih."),
        "ciudad juarez": ("Ciudad Juárez", "Chih."),
        "delicias": ("Delicias", "Chih."),
        "parral": ("Parral", "Chih."),
        "colima capital": ("Colima", "Col."),
        "manzanillo": ("Manzanillo", "Col."),
        "tecoman": ("Tecomán", "Col."),
        "durango capital": ("Durango", "Dgo."),
        "gomez palacio": ("Gómez Palacio", "Dgo."),
        "lerdo": ("Lerdo", "Dgo."),
        "zacatecas capital": ("Zacatecas", "Zac."),
        "fresnillo": ("Fresnillo", "Zac."),
        "guadalupe zac": ("Guadalupe", "Zac."),
        
        # Ciudades principales específicas
        "tapachula": ("Tapachula", "Chis."),
        "tuxtla": ("Tuxtla Gutiérrez", "Chis."),
        "san cristobal": ("San Cristóbal de las Casas", "Chis."),
        "comitan": ("Comitán", "Chis."),
        "pachuca": ("Pachuca de Soto", "Hgo."),
        "mineral de la reforma": ("Mineral de la Reforma", "Hgo."),
        "tulancingo": ("Tulancingo", "Hgo."),
        "tula": ("Tula de Allende", "Hgo."),
        "san luis potosi": ("San Luis Potosí", "S.L.P."),
        
        # Estados/ciudades principales después (menos específicos)
        "puebla": ("Puebla", "Pue."),
        "veracruz": ("Veracruz", "Ver."),
        "oaxaca": ("Oaxaca", "Oax."),
        "chihuahua": ("Chihuahua", "Chih."),
        "colima": ("Colima", "Col."),
        "durango": ("Durango", "Dgo."),
        "zacatecas": ("Zacatecas", "Zac."),
        "mexico": ("Ciudad de México", "CDMX"),
        "cdmx": ("Ciudad de México", "CDMX"),
        "guadalajara": ("Guadalajara", "Jal."),
        "monterrey": ("Monterrey", "N.L."),
        "cancun": ("Cancún", "Q.R."),
        "merida": ("Mérida", "Yuc."),
        "tijuana": ("Tijuana", "B.C."),
        "hermosillo": ("Hermosillo", "Son."),
        "culiacan": ("Culiacán", "Sin."),
        "morelia": ("Morelia", "Mich."),
        "leon": ("León", "Gto."),
        "queretaro": ("Querétaro", "Qro."),
        "aguascalientes": ("Aguascalientes", "Ags."),
        "cuernavaca": ("Cuernavaca", "Mor."),
        "toluca": ("Toluca", "Edomex"),
        "acapulco": ("Acapulco", "Gro."),
    }
    q_norm = query.lower()
    # Remover acentos para comparar
    import unicodedata
    def norm(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    q_norm_clean = norm(q_norm)
    
    # Buscar ciudades específicas primero (más específico)
    for key, val in ciudad_estado_map.items():
        if norm(key) in q_norm_clean:
            return val  # (ciudad, estado_abrev)
    
    return (None, None)


ESTADO_MAP = {
    "Chiapas": "Chis.", "Hidalgo": "Hgo.", "México": "Edomex",
    "Ciudad de México": "CDMX", "Puebla": "Pue.", "Querétaro": "Qro.",
    "Jalisco": "Jal.", "Nuevo León": "N.L.", "Oaxaca": "Oax.",
    "Veracruz": "Ver.", "Guerrero": "Gro.", "Michoacán": "Mich.",
    "Guanajuato": "Gto.", "Tamaulipas": "Tams.", "Yucatán": "Yuc.",
    "Quintana Roo": "Q.R.", "Sonora": "Son.", "Sinaloa": "Sin.",
    "Chihuahua": "Chih.", "Coahuila": "Coah.", "Durango": "Dgo.",
    "Zacatecas": "Zac.", "San Luis Potosí": "S.L.P.", "Morelos": "Mor.",
    "Tlaxcala": "Tlax.", "Nayarit": "Nay.", "Tabasco": "Tab.",
    "Campeche": "Camp.", "Baja California": "B.C.", "Baja California Sur": "B.C.S.",
    "Aguascalientes": "Ags.", "Colima": "Col.", "Estado de México": "Edomex",
}


def scrape_google_maps(query, max_results=5):
    leads = []

    # Extraer ciudad y estado de la query ANTES de scraping
    ciudad_query, estado_query = extraer_estado_de_query(query)
    if not ciudad_query:
        ciudad_query = extraer_ciudad_de_query(query)

    print(f"Ciudad detectada en query: {ciudad_query} | Estado: {estado_query}", file=sys.stderr)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="msedge")
        context = browser.new_context(locale="es-MX")
        page = context.new_page()

        try:
            search_url = f"https://www.google.com/maps/search/{urllib.parse.quote(query)}"
            page.goto(search_url, timeout=60000)
            page.wait_for_selector('div[role="feed"]', timeout=15000)
            time.sleep(3)

            # Scroll para cargar resultados
            for _ in range(3):
                page.mouse.wheel(0, 5000)
                time.sleep(2)

            results = page.query_selector_all('div.Nv2PK')
            if not results:
                results = page.query_selector_all('a.hfpx6c')

            print(f"Encontrados: {len(results)} resultados", file=sys.stderr)

            for res in results[:max_results]:
                try:
                    res.scroll_into_view_if_needed()
                    time.sleep(1)
                    res.click()
                    page.wait_for_selector('h1.DUwDvf', timeout=10000)
                    time.sleep(2)

                    nombre = page.query_selector('h1.DUwDvf').inner_text()

                    direccion = ""
                    telefono = ""
                    website = ""

                    # MÉTODO 1: Botón de dirección específico
                    try:
                        addr_btn = page.query_selector('button[data-item-id="address"]')
                        if addr_btn:
                            direccion = addr_btn.inner_text().strip()
                    except:
                        pass

                    # MÉTODO 2: Fallback por aria-label
                    if not direccion:
                        try:
                            addr_elem = page.query_selector('button[aria-label*="Dirección"]')
                            if addr_elem:
                                direccion = addr_elem.get_attribute('aria-label').replace('Dirección: ', '').strip()
                        except:
                            pass

                    # MÉTODO 3: Divs
                    if not direccion:
                        info_elements = page.query_selector_all('div.Io6YTe')
                        for info in info_elements:
                            text = info.inner_text().strip()
                            if ',' in text and any(c.isdigit() for c in text) and len(text) > 20:
                                if not any(x in text.lower() for x in ['cerrado', 'abierto', 'horario']):
                                    direccion = text
                                    break

                    # Teléfono
                    try:
                        phone_btn = page.query_selector('button[data-item-id^="phone:tel:"]')
                        if phone_btn:
                            telefono = phone_btn.get_attribute('data-item-id').replace('phone:tel:', '')
                    except:
                        pass

                    # Website
                    try:
                        web_btn = page.query_selector('a[data-item-id="authority"]')
                        if web_btn:
                            website = web_btn.get_attribute('href')
                    except:
                        pass

                    # Calificación
                    calif = 0.0
                    try:
                        rating_elem = page.query_selector('div.F7nice span[aria-hidden="true"]')
                        if rating_elem:
                            calif = float(rating_elem.inner_text().replace(',', '.'))
                    except:
                        pass

                    # ── EXTRACCIÓN DE POBLACIÓN Y ESTADO ──────────────────────
                    # Prioridad 1: extraer de la dirección real del negocio
                    poblacion = ""
                    estado_prov = ""

                    if direccion:
                        addr_parts = [p.strip() for p in direccion.split(',')]

                        if len(addr_parts) >= 2:
                            geo_part = addr_parts[-2]
                            poblacion = re.sub(r'^\d{5}\s+', '', geo_part).strip()

                            estado_cp = addr_parts[-1]
                            estado_prov = re.sub(r'^\d{5}\s+', '', estado_cp).strip()

                        if not poblacion and len(addr_parts) >= 3:
                            poblacion = addr_parts[-3].strip()

                        # Limpiar Plus Codes
                        if "+" in poblacion:
                            poblacion = poblacion.split(' ')[-1]

                        # Mapear estado completo → abreviatura
                        estado_prov = ESTADO_MAP.get(estado_prov.strip(), estado_prov.strip())

                    # ── VALIDACIÓN: ¿el resultado es realmente de la ciudad buscada? ──
                    # Si la dirección obtenida no menciona la ciudad de la query,
                    # es probable que Google devolvió resultados de otra ubicación.
                    direccion_lower = direccion.lower() if direccion else ""
                    ciudad_query_lower = ciudad_query.lower() if ciudad_query else ""

                    # Hacer validación más flexible - buscar palabras clave de la ciudad
                    palabras_ciudad = ciudad_query_lower.split() if ciudad_query_lower else []
                    palabras_importantes = [p for p in palabras_ciudad if len(p) > 3]
                    
                    resultado_fuera_de_ciudad = (
                        ciudad_query_lower and
                        len(palabras_importantes) > 0 and
                        not any(
                            palabra in direccion_lower
                            for palabra in palabras_importantes
                        ) and
                        # Verificación adicional: si no hay dirección pero el nombre contiene la ciudad
                        not any(
                            palabra in nombre.lower()
                            for palabra in palabras_importantes
                        )
                    )

                    if resultado_fuera_de_ciudad:
                        print(
                            f"⚠️  DESCARTADO (fuera de {ciudad_query}): {nombre} | Dir: {direccion[:60]}",
                            file=sys.stderr
                        )
                        continue  # Saltar este resultado

                    # Prioridad 2: si no se pudo extraer de la dirección, usar la query
                    if not poblacion:
                        poblacion = ciudad_query or "Sin dato"

                    if not estado_prov or estado_prov in ["Sin dato", ""]:
                        estado_prov = estado_query or "Sin dato"

                    if nombre != "Desconocido":
                        lead_item = {
                            "nombre": nombre,
                            "tipo_negocio": normalizar_tipo_negocio(query.split(' ')[0]),
                            "telefono": telefono,
                            "direccion": direccion if direccion else f"{poblacion}, {estado_prov}",
                            "poblacion": poblacion,
                            "estado": estado_prov,
                            "calificacion": calif,
                            "website": website
                        }
                        print(
                            f"✅ {nombre} | Pob: {poblacion} | Estado: {estado_prov} | Tel: {telefono}",
                            file=sys.stderr
                        )
                        leads.append(lead_item)

                except Exception as e:
                    print(f"Error procesando card: {e}", file=sys.stderr)
                    continue

        except Exception as e:
            print(f"Error general: {e}", file=sys.stderr)
        finally:
            browser.close()

    return leads


if __name__ == '__main__':
    q = ' '.join(sys.argv[1:-1]) if len(sys.argv) > 2 else (sys.argv[1] if len(sys.argv) > 1 else '')
    try:
        m = int(sys.argv[-1]) if len(sys.argv) > 1 and sys.argv[-1].isdigit() else 5
    except Exception:
        m = 5

    if not q:
        print('Usage: python scraper.py "search query" [max_results]', file=sys.stderr)
        sys.exit(0)

    results = scrape_google_maps(q, m)

    try:
        with open('temp_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f'WROTE {len(results)} results to temp_results.json', file=sys.stderr)
    except Exception as e:
        print(f'Error writing temp_results.json: {e}', file=sys.stderr)
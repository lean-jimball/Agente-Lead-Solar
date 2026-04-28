import pywhatkit
import time
import re
import os
from database import get_connection
import urllib.parse
import subprocess
import platform

# Importaciones opcionales
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Importaciones opcionales para Selenium (solo si está disponible)
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

def clean_phone_number(telefono):
    """Limpia y formatea números de teléfono a formato internacional +52"""
    if not telefono or telefono is None:
        return None
    
    # Convertir a string y limpiar
    telefono_str = str(telefono).strip() if telefono else ""
    if not telefono_str:
        return None
        
    telefono_limpio = re.sub(r'\D', '', telefono_str)
    
    if len(telefono_limpio) == 10:
        telefono_limpio = "52" + telefono_limpio
    elif len(telefono_limpio) == 11 and telefono_limpio.startswith("1"):
        telefono_limpio = "52" + telefono_limpio[1:]
    elif len(telefono_limpio) == 12 and telefono_limpio.startswith("52"):
        pass
    else:
        return None
        
    if not telefono_limpio.startswith("+"):
        telefono_limpio = "+" + telefono_limpio
    return telefono_limpio


def extraer_ciudad(direccion):
    """Extrae la ciudad de la dirección completa"""
    if not direccion or direccion is None:
        return "tu zona"
    
    # Convertir a string de forma segura
    direccion_str = str(direccion).strip() if direccion else ""
    if not direccion_str:
        return "tu zona"
        
    partes = direccion_str.split(',')
    if len(partes) >= 2:
        ciudad = partes[-2].strip()
        ciudad = re.sub(r'\d{5}', '', ciudad).strip()
        ciudad = re.sub(r'Los Heroes.*', '', ciudad, flags=re.IGNORECASE).strip()
        return ciudad if ciudad else "tu zona"
    return "tu zona"


def formatear_ahorro(ahorro_raw):
    """
    Convierte el ahorro_mensual real de la BD a texto legible.
    Ejemplos:
        9500  → "$9,500"
        11200 → "$11,200"
        500   → "$500"
    Sin redondeos agresivos — muestra el valor real.
    """
    if ahorro_raw is None:
        return None
        
    try:
        # Manejar diferentes tipos de datos
        if isinstance(ahorro_raw, str):
            ahorro_raw = ahorro_raw.strip() if ahorro_raw else "0"
            
        ahorro = int(float(ahorro_raw))
        if ahorro <= 0:
            return None
        return f"${ahorro:,}"
    except (ValueError, TypeError, AttributeError):
        return None


def generar_mensaje_calificado(lead):
    """
    Genera mensajes personalizados por SCORE posicionándose como ASESOR/ALIADO COMERCIAL
    No como vendedor, sino como consultor que ayuda a optimizar costos
    
    SEGMENTACIÓN POR SCORE (0-10):
    - Score 9-10: 🔥 Mensaje directo/urgente (asesor experto)
    - Score 8-8.9: 🚀 Mensaje persuasivo (aliado comercial)  
    - Score 7-7.9: ⚡ Mensaje educativo (consultor)
    - Score 5-6.9: 🟡 Mensaje suave/nutrir (asesor informativo)
    """
    import random
    
    # Extraer datos del lead
    nombre = lead.get('nombre', '') or ''
    direccion = lead.get('direccion', '') or ''
    ciudad = extraer_ciudad(direccion)
    tipo_negocio = lead.get('tipo_negocio', 'negocio') or 'negocio'
    ahorro_raw = lead.get('ahorro_mensual')
    score_raw = lead.get('score_ia', 0)
    sistema_kwp = lead.get('sistema_recomendado', 0) or 0
    
    # Validar score
    try:
        score = int(score_raw) if score_raw is not None else 0
    except (ValueError, TypeError):
        score = 0
    
    if not ahorro_raw or score < 5:
        return None

    ahorro_txt = formatear_ahorro(ahorro_raw)
    if not ahorro_txt:
        return None

    # Limpiar y preparar tipo de negocio
    tipo_str = str(tipo_negocio).strip() if tipo_negocio else 'negocio'
    tipo_lower = tipo_str.lower()
    
    # Determinar artículo y forma del tipo de negocio
    if 'hotel' in tipo_lower:
        tipo_especifico = 'hoteles'
        sector = 'hotelero'
    elif 'restaurante' in tipo_lower:
        tipo_especifico = 'restaurantes'
        sector = 'restaurantero'
    elif 'lavandería' in tipo_lower or 'lavanderia' in tipo_lower:
        tipo_especifico = 'lavanderías'
        sector = 'de lavanderías'
    elif 'casino' in tipo_lower:
        tipo_especifico = 'casinos'
        sector = 'de entretenimiento'
    elif 'farmacia' in tipo_lower:
        tipo_especifico = 'farmacias'
        sector = 'farmacéutico'
    elif 'supermercado' in tipo_lower:
        tipo_especifico = 'supermercados'
        sector = 'comercial'
    elif 'taller' in tipo_lower:
        tipo_especifico = 'talleres'
        sector = 'industrial'
    elif 'tortillería' in tipo_lower or 'tortilleria' in tipo_lower:
        tipo_especifico = 'tortillerías'
        sector = 'alimenticio'
    else:
        tipo_especifico = tipo_lower + 's' if not tipo_lower.endswith('s') else tipo_lower
        sector = 'comercial'
    
    # Calcular ahorro anual para contexto
    try:
        ahorro_num = int(float(ahorro_raw))
        ahorro_anual = ahorro_num * 12
        ahorro_anual_txt = f"${ahorro_anual:,}"
    except:
        ahorro_anual_txt = None
    
    # SEGMENTACIÓN POR SCORE - DIFERENTES ENFOQUES DE ASESORÍA
    
    if score >= 9:
        # 🔥 SCORE 9-10: ASESOR EXPERTO - MENSAJE DIRECTO/URGENTE
        mensajes_premium = [
            f"""Hola, buen día.

Soy asesor especializado de CySlean. Hemos identificado tu negocio como candidato PRIORITARIO para optimización energética.

Análisis preliminar para {tipo_especifico} en {ciudad}:
• Ahorro potencial: {ahorro_txt}/mes
• ROI proyectado: Excelente para tu sector
• Oportunidad limitada en tu zona

Como experto en el sector {sector}, te recomiendo evaluar esta oportunidad pronto.

¿Podemos agendar una consultoría técnica esta semana?

Responde:
✅ SÍ - Agendemos pronto
⏰ DESPUÉS - Próxima semana
❌ NO - No por ahora

CySlean | Asesoría Especializada
📞 771 661 2061""",

            f"""Hola, buen día.

Te contacto como asesor energético de CySlean. Tu negocio tiene un perfil EXCEPCIONAL para energía renovable.

Datos específicos para tu {tipo_str} en {ciudad}:
• Potencial de ahorro: {ahorro_txt} mensuales
• Sector {sector}: Alta viabilidad técnica
• Análisis: Candidato prioritario

Mi recomendación profesional: Evaluar inmediatamente.

¿Te interesa una consultoría técnica sin costo?

✅ SÍ - Coordinar visita
⏰ DESPUÉS - En unos días  
❌ NO - No me interesa

CySlean Asesoría Técnica
📞 771 661 2061"""
        ]
        return random.choice(mensajes_premium)
    
    elif score >= 8:
        # 🚀 SCORE 8-8.9: ALIADO COMERCIAL - MENSAJE PERSUASIVO
        mensajes_alta_prioridad = [
            f"""Hola, buen día.

Soy tu aliado comercial en CySlean, consultoría energética.

Estamos apoyando a {tipo_especifico} exitosos en {ciudad} a reducir significativamente sus costos operativos.

Tu negocio califica para ahorros de {ahorro_txt}/mes. En el sector {sector}, estos resultados son muy atractivos.

Como tu asesor, te recomiendo conocer las opciones disponibles.

¿Te interesa que te comparta el análisis completo?

Responde:
✅ SÍ - Envíame el análisis
⏰ DESPUÉS - Más adelante
❌ NO - No gracias

CySlean | Tu Aliado Energético
📞 771 661 2061""",

            f"""Hola, buen día.

Te escribo de CySlean como tu consultor en optimización energética.

Hemos identificado una excelente oportunidad para {tipo_especifico} como el tuyo en {ciudad}.

Beneficios proyectados:
• Reducción mensual: {ahorro_txt}
• Sector {sector}: Resultados comprobados
• Sin afectar tu operación

¿Te gustaría que te asesore sobre las mejores opciones?

✅ SÍ - Quiero asesoría
⏰ DESPUÉS - Otro momento
❌ NO - No por ahora

CySlean Consultoría
📞 771 661 2061"""
        ]
        return random.choice(mensajes_alta_prioridad)
    
    elif score >= 7:
        # ⚡ SCORE 7-7.9: CONSULTOR - MENSAJE EDUCATIVO
        mensajes_educativos = [
            f"""Hola, buen día.

Soy consultor de CySlean, especialistas en energía renovable.

Estamos compartiendo información valiosa con {tipo_especifico} de {ciudad} sobre cómo optimizar costos energéticos.

Según nuestros estudios en el sector {sector}, negocios como el tuyo pueden reducir hasta {ahorro_txt} mensuales con las estrategias correctas.

¿Te interesa conocer estas alternativas?

Responde:
✅ SÍ - Envíenme información
⏰ DESPUÉS - En otro momento
❌ NO - No me interesa

CySlean Consultoría Energética
📞 771 661 2061""",

            f"""Hola, buen día.

Te contacto de CySlean para compartir información sobre optimización energética.

Estamos educando a propietarios de {tipo_especifico} en {ciudad} sobre alternativas sustentables para reducir costos.

Tu tipo de negocio tiene potencial de ahorro de {ahorro_txt}/mes según nuestros análisis del sector {sector}.

¿Te gustaría recibir material informativo?

✅ SÍ - Envíenme detalles
⏰ DESPUÉS - Más adelante  
❌ NO - No gracias

CySlean | Educación Energética
📞 771 661 2061"""
        ]
        return random.choice(mensajes_educativos)
    
    else:
        # 🟡 SCORE 5-6.9: ASESOR INFORMATIVO - MENSAJE SUAVE/NUTRIR
        mensajes_suaves = [
            f"""Hola, buen día.

Soy asesor de CySlean. Estamos realizando un estudio sobre consumo energético en {tipo_especifico} de {ciudad}.

Hemos notado que negocios en el sector {sector} están explorando alternativas para optimizar sus costos de electricidad.

Según nuestros datos, hay potencial de ahorro de {ahorro_txt} mensuales en casos similares al tuyo.

¿Te interesaría recibir información general sobre estas alternativas?

Responde cuando gustes:
✅ SÍ - Me interesa saber más
⏰ DESPUÉS - Tal vez después
❌ NO - No por ahora

Saludos,
CySlean Asesoría
📞 771 661 2061""",

            f"""Hola, buen día.

Te saludo de CySlean, consultoría en energía renovable.

Estamos compartiendo información educativa con {tipo_especifico} de {ciudad} sobre tendencias en optimización energética.

Tu sector ({sector}) muestra oportunidades interesantes, con ahorros potenciales de {ahorro_txt}/mes en casos similares.

¿Te gustaría mantenerte informado sobre estas opciones?

Sin presión, responde si te interesa:
✅ SÍ - Información ocasional
⏰ DESPUÉS - Quizás más adelante
❌ NO - No gracias

CySlean | Información Energética
📞 771 661 2061"""
        ]
        return random.choice(mensajes_suaves)


def agregar_columna_si_no_existe(cursor, tabla, columna, tipo):
    cursor.execute(f"PRAGMA table_info({tabla})")
    columnas = [col[1] for col in cursor.fetchall()]
    if columna not in columnas:
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo}")


def detect_whatsapp_desktop():
    """Detecta si WhatsApp Desktop está instalado y ejecutándose"""
    if not PSUTIL_AVAILABLE:
        return False, "psutil no disponible para detección de procesos"
    
    try:
        # Buscar proceso de WhatsApp Desktop
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['name'] and 'whatsapp' in proc.info['name'].lower():
                    return True, proc.info['exe']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Buscar instalación de WhatsApp Desktop
        if platform.system() == "Windows":
            try:
                import winreg
                # Buscar en registro de Windows
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
                for i in range(winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    try:
                        display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                        if "whatsapp" in display_name.lower():
                            return False, "WhatsApp Desktop instalado pero no ejecutándose"
                    except FileNotFoundError:
                        pass
                    winreg.CloseKey(subkey)
                winreg.CloseKey(key)
            except:
                pass
        
        return False, "WhatsApp Desktop no detectado"
    except Exception as e:
        return False, f"Error detectando WhatsApp Desktop: {e}"

def launch_whatsapp_desktop():
    """Intenta abrir WhatsApp Desktop"""
    try:
        if platform.system() == "Windows":
            # Intentar abrir desde ubicaciones comunes
            possible_paths = [
                r"C:\Users\{}\AppData\Local\WhatsApp\WhatsApp.exe".format(os.environ.get('USERNAME', '')),
                r"C:\Program Files\WhatsApp\WhatsApp.exe",
                r"C:\Program Files (x86)\WhatsApp\WhatsApp.exe"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return True, f"WhatsApp Desktop iniciado desde: {path}"
            
            # Intentar con comando del sistema
            try:
                subprocess.Popen(["whatsapp"])
                return True, "WhatsApp Desktop iniciado con comando del sistema"
            except:
                pass
                
        elif platform.system() == "Darwin":  # macOS
            try:
                subprocess.Popen(["open", "-a", "WhatsApp"])
                return True, "WhatsApp Desktop iniciado en macOS"
            except:
                pass
        
        return False, "No se pudo iniciar WhatsApp Desktop"
        
    except Exception as e:
        return False, f"Error iniciando WhatsApp Desktop: {e}"

def send_whatsapp_with_selenium(leads_data, modo_preview=True):
    """
    Función de compatibilidad - redirige a WhatsApp Desktop
    """
    if not SELENIUM_AVAILABLE:
        print("⚠️  Selenium no disponible, usando WhatsApp Desktop...")
        return send_whatsapp_with_desktop_urls(leads_data, modo_preview)
    
    print("⚠️  Función Selenium redirigida a WhatsApp Desktop...")
    return send_whatsapp_with_desktop_urls(leads_data, modo_preview)


def send_whatsapp_with_desktop_urls(leads_data, modo_preview=True):
    """
    Envía mensajes usando URLs de WhatsApp que abren en la app de escritorio
    INCLUYE DELAYS ANTI-SPAM para evitar bloqueos de WhatsApp
    """
    if not leads_data:
        print("❌ No hay leads para enviar")
        return 0

    print(f"\n🚀 Enviando con WhatsApp Desktop - {len(leads_data)} leads")
    print(f"⚠️  IMPORTANTE: Se agregarán delays entre mensajes para evitar spam")
    
    # Detectar WhatsApp Desktop
    is_running, status = detect_whatsapp_desktop()
    
    if not is_running:
        print(f"⚠️  WhatsApp Desktop: {status}")
        print("🔄 Intentando abrir WhatsApp Desktop...")
        
        success, message = launch_whatsapp_desktop()
        if success:
            print(f"✅ {message}")
            print("⏳ Esperando 5 segundos para que se inicie...")
            time.sleep(5)
        else:
            print(f"❌ {message}")
            print("💡 Abre WhatsApp Desktop manualmente y presiona Enter")
            input("   Presiona Enter cuando WhatsApp Desktop esté abierto...")
    else:
        print("✅ WhatsApp Desktop detectado y ejecutándose")
    
    enviados = 0
    omitidos = 0
    
    for idx, lead_data in enumerate(leads_data, 1):
        telefono = lead_data['telefono']
        mensaje = lead_data['mensaje']
        nombre = lead_data['nombre']
        lead_id = lead_data['id']
        
        print(f"\n{'='*50}")
        print(f"LEAD {idx}/{len(leads_data)}: {nombre}")
        print(f"📞 {telefono}")
        
        if modo_preview:
            print(f"\n📝 MENSAJE:")
            print("-" * 30)
            print(mensaje)
            print("-" * 30)
            
            respuesta = input("\n¿Enviar este mensaje? (s=sí / n=no / t=terminar): ")
            respuesta = respuesta.lower().strip() if respuesta else ""
            
            if respuesta == 'n':
                print("⏭️  Omitido por usuario")
                omitidos += 1
                continue
            elif respuesta == 't':
                print("🛑 Proceso detenido por usuario")
                break
        
        try:
            # Limpiar número de teléfono para URL
            phone_clean = telefono.replace('+', '').replace(' ', '')
            
            # Crear URL de WhatsApp
            message_encoded = urllib.parse.quote(mensaje)
            whatsapp_url = f"whatsapp://send?phone={phone_clean}&text={message_encoded}"
            
            print(f"📤 Abriendo chat con {nombre}...")
            print(f"📱 URL: whatsapp://send?phone={phone_clean}")
            
            # Abrir URL en WhatsApp Desktop
            if platform.system() == "Windows":
                os.startfile(whatsapp_url)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", whatsapp_url])
            else:  # Linux
                subprocess.run(["xdg-open", whatsapp_url])
            
            # Esperar a que el usuario confirme el envío
            print(f"\n📋 INSTRUCCIONES:")
            print(f"1. Se abrió el chat con {nombre}")
            print(f"2. El mensaje debería estar pre-cargado")
            print(f"3. Revisa el mensaje y presiona Enter para enviarlo")
            print(f"4. Si el número no existe en WhatsApp, marca como 'No WhatsApp'")
            
            resultado = input("\n¿Mensaje enviado exitosamente? (s=sí / n=no whatsapp / e=error): ")
            resultado = resultado.lower().strip() if resultado else ""
            
            conn = get_connection()
            cursor = conn.cursor()
            
            if resultado == 's':
                # Marcar como enviado exitosamente
                cursor.execute("""
                    UPDATE leads
                    SET estado_pipeline = 'Contactado',
                        enviado = 1,
                        fecha_contacto = datetime('now', 'localtime')
                    WHERE id = ?
                """, (lead_id,))
                conn.commit()
                print(f"✅ Marcado como enviado: {nombre}")
                enviados += 1
                
                # DELAY ANTI-SPAM: Esperar entre mensajes
                if idx < len(leads_data):  # Si no es el último
                    delay_segundos = 15  # 15 segundos entre mensajes
                    print(f"\n⏳ Esperando {delay_segundos} segundos antes del siguiente mensaje...")
                    print(f"   (Esto evita que WhatsApp te marque como spam)")
                    time.sleep(delay_segundos)
                
            elif resultado == 'n':
                # Marcar como No WhatsApp
                cursor.execute("""
                    UPDATE leads
                    SET estado_pipeline = 'No WhatsApp',
                        enviado = -1
                    WHERE id = ?
                """, (lead_id,))
                conn.commit()
                print(f"📵 Marcado como No WhatsApp: {nombre}")
                omitidos += 1
                
            else:
                # Marcar como error
                cursor.execute('UPDATE leads SET enviado = -1 WHERE id = ?', (lead_id,))
                conn.commit()
                print(f"❌ Marcado como error: {nombre}")
                omitidos += 1
            
            conn.close()
            
            # Pausa entre mensajes
            if idx < len(leads_data) and resultado in ['s', 'n']:
                print("⏳ Esperando 2 segundos antes del siguiente...")
                time.sleep(2)
                
        except Exception as e:
            print(f"❌ Error con {nombre}: {e}")
            
            # Marcar como error
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE leads SET enviado = -1 WHERE id = ?', (lead_id,))
            conn.commit()
            conn.close()
            
            omitidos += 1
    
    print(f"\n{'='*50}")
    print(f"✅ PROCESO COMPLETADO")
    print(f"   Enviados: {enviados}")
    print(f"   Omitidos: {omitidos}")
    print(f"{'='*50}")
    
    return enviados
    """
    Envía mensajes de WhatsApp usando Selenium para reutilizar la sesión existente
    """
    if not leads_data:
        print("❌ No hay leads para enviar")
        return 0

    print(f"\n🚀 Iniciando envío con Selenium - {len(leads_data)} leads")
    print("📱 Asegúrate de tener WhatsApp Web abierto y con sesión iniciada")
    
    # Configurar Chrome para usar perfil existente (opcional)
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Intentar conectar a una instancia existente de Chrome o crear nueva
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Ir a WhatsApp Web
        print("🌐 Abriendo WhatsApp Web...")
        driver.get("https://web.whatsapp.com")
        
        # Esperar a que el usuario confirme que está logueado
        input("\n⚠️  IMPORTANTE: \n1. Escanea el código QR si es necesario\n2. Asegúrate de estar logueado en WhatsApp Web\n3. Presiona Enter cuando esté listo...")
        
        enviados = 0
        omitidos = 0
        
        for idx, lead_data in enumerate(leads_data, 1):
            telefono = lead_data['telefono']
            mensaje = lead_data['mensaje']
            nombre = lead_data['nombre']
            lead_id = lead_data['id']
            
            print(f"\n{'='*50}")
            print(f"LEAD {idx}/{len(leads_data)}: {nombre}")
            print(f"📞 {telefono}")
            
            if modo_preview:
                print(f"\n📝 MENSAJE:")
                print("-" * 30)
                print(mensaje)
                print("-" * 30)
                
                respuesta = input("\n¿Enviar este mensaje? (s=sí / n=no / t=terminar): ")
                respuesta = respuesta.lower().strip() if respuesta else ""
                
                if respuesta == 'n':
                    print("⏭️  Omitido por usuario")
                    omitidos += 1
                    continue
                elif respuesta == 't':
                    print("🛑 Proceso detenido por usuario")
                    break
            
            try:
                # Limpiar número de teléfono para URL
                phone_clean = telefono.replace('+', '').replace(' ', '')
                
                # Crear URL de WhatsApp con mensaje
                message_encoded = urllib.parse.quote(mensaje)
                whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_clean}&text={message_encoded}"
                
                print(f"📤 Enviando mensaje a {nombre}...")
                
                # Navegar a la URL de WhatsApp
                driver.get(whatsapp_url)
                
                # Esperar a que cargue la conversación
                try:
                    # Esperar a que aparezca el campo de texto
                    wait = WebDriverWait(driver, 15)
                    
                    # Buscar el botón de enviar o el campo de texto
                    send_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
                    )
                    
                    # Hacer clic en el botón de enviar
                    send_button.click()
                    
                    print(f"✅ Mensaje enviado a {nombre}")
                    
                    # Actualizar base de datos
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE leads
                        SET estado_pipeline = 'Contactado',
                            enviado = 1,
                            fecha_contacto = datetime('now', 'localtime')
                        WHERE id = ?
                    """, (lead_id,))
                    conn.commit()
                    conn.close()
                    
                    enviados += 1
                    
                    # Pausa entre mensajes
                    if idx < len(leads_data):
                        print("⏳ Esperando 3 segundos...")
                        time.sleep(3)
                        
                except Exception as e:
                    print(f"⚠️  No se pudo enviar automáticamente a {telefono}")
                    print(f"   Razón: {e}")
                    print("   El chat se abrió, puedes enviar manualmente si está disponible")
                    
                    # Marcar como no WhatsApp si no se pudo enviar
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute('UPDATE leads SET enviado = -1, estado_pipeline = "No WhatsApp" WHERE id = ?', (lead_id,))
                    conn.commit()
                    conn.close()
                    
                    omitidos += 1
                    
                    # Pausa para que el usuario pueda revisar
                    input("   Presiona Enter para continuar con el siguiente lead...")
                    
            except Exception as e:
                print(f"❌ Error general con {nombre}: {e}")
                
                # Marcar como error
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('UPDATE leads SET enviado = -1 WHERE id = ?', (lead_id,))
                conn.commit()
                conn.close()
                
                omitidos += 1
        
        print(f"\n{'='*50}")
        print(f"✅ PROCESO COMPLETADO")
        print(f"   Enviados: {enviados}")
        print(f"   Omitidos: {omitidos}")
        print(f"{'='*50}")
        
        # Mantener el navegador abierto para revisión
        input("\nPresiona Enter para cerrar el navegador...")
        driver.quit()
        
        return enviados
        
    except Exception as e:
        print(f"❌ Error al inicializar Selenium: {e}")
        print("💡 Asegúrate de tener Chrome instalado y chromedriver en PATH")
        return 0


def send_whatsapp_messages(modo_preview=True, usar_selenium=False, usar_desktop=True):
    """
    Función principal optimizada para WhatsApp Desktop
    """
    conn = get_connection()
    cursor = conn.cursor()

    agregar_columna_si_no_existe(cursor, 'leads', 'enviado', 'INTEGER DEFAULT 0')
    agregar_columna_si_no_existe(cursor, 'leads', 'fecha_contacto', 'TEXT')
    conn.commit()

    cursor.execute("""
        SELECT * FROM leads
        WHERE estado_pipeline = 'Calificado'
        AND telefono IS NOT NULL
        AND telefono != ''
        AND (enviado IS NULL OR enviado = 0)
        AND sistema_recomendado > 0
        AND ahorro_mensual > 0
        AND score_ia >= 5
        ORDER BY score_ia DESC, ahorro_mensual DESC
    """)
    leads_pendientes = [dict(row) for row in cursor.fetchall()]
    conn.close()

    if not leads_pendientes:
        print("❌ No hay leads con teléfono y score >= 5")
        print("\n💡 Revisa que tengas leads con:")
        print("   1. telefono capturado")
        print("   2. score_ia >= 5 (50% para arriba)")
        print("   3. estado = Calificado (usar botón calificación masiva)")
        print("   4. enviado = 0 o NULL")
        return 0

    # Preparar datos para envío
    leads_data = []
    for lead in leads_pendientes:
        telefono_raw = lead.get('telefono')
        telefono = clean_phone_number(telefono_raw)
        
        if not telefono:
            print(f"⚠️  {lead.get('nombre')} - Teléfono inválido: {telefono_raw}")
            # Marcar como teléfono inválido
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE leads SET enviado = -1, estado_pipeline = "Sin teléfono" WHERE id = ?', (lead.get('id'),))
            conn.commit()
            conn.close()
            continue
            
        mensaje = generar_mensaje_calificado(lead)
        if not mensaje:
            print(f"⚠️  {lead.get('nombre')} - No se pudo generar mensaje")
            continue
            
        leads_data.append({
            'id': lead.get('id'),
            'nombre': lead.get('nombre', 'Sin nombre'),
            'telefono': telefono,
            'mensaje': mensaje,
            'lead_data': lead
        })
    
    if not leads_data:
        print("❌ No hay leads válidos para enviar")
        return 0
    
    print(f"\n📋 {len(leads_data)} leads preparados para envío")
    
    # Usar WhatsApp Desktop por defecto
    if usar_desktop or not usar_selenium:
        print("\n📱 Usando WhatsApp Desktop")
        return send_whatsapp_with_desktop_urls(leads_data, modo_preview)
    else:
        print("\n🔧 Usando método Selenium (redirigido a Desktop)")
        return send_whatsapp_with_desktop_urls(leads_data, modo_preview)


def send_whatsapp_messages_pywhatkit(leads_data, modo_preview=True):
    """
    Método original usando PyWhatKit (mantener como respaldo)
    """
    enviados = 0
    omitidos = 0

    for idx, lead_info in enumerate(leads_data, 1):
        lead = lead_info['lead_data']
        telefono = lead_info['telefono']
        mensaje = lead_info['mensaje']
        nombre = lead_info['nombre']
        lead_id = lead_info['id']

        # Preview en consola
        print(f"\n{'='*70}")
        print(f"LEAD {idx}/{len(leads_data)}: {nombre}")
        print(f"{'='*70}")
        print(f"📞 Teléfono : {telefono}")
        print(f"🏢 Tipo     : {lead.get('tipo_negocio', 'N/A')}")
        print(f"📍 Ciudad   : {extraer_ciudad(lead.get('direccion', ''))}")
        print(f"⚡ Sistema  : {lead.get('sistema_recomendado')} kW")
        print(f"💰 Ahorro   : {formatear_ahorro(lead.get('ahorro_mensual'))} / mes")
        print(f"📊 Score IA : {lead.get('score_ia')}")
        print(f"\n📝 MENSAJE A ENVIAR:")
        print("-" * 70)
        print(mensaje)
        print("-" * 70)

        if modo_preview:
            respuesta = input("\n¿Enviar este mensaje? (s=sí / n=no / t=terminar): ")
            respuesta = respuesta.lower().strip() if respuesta else ""
            if respuesta == 's':
                pass
            elif respuesta == 'n':
                print("⏭️  Omitido por usuario")
                omitidos += 1
                continue
            elif respuesta == 't':
                print("🛑 Proceso detenido por usuario")
                break
            else:
                print("⏭️  Omitido - respuesta no válida")
                omitidos += 1
                continue

        try:
            print(f"\n📤 Enviando a {nombre}...")
            pywhatkit.sendwhatmsg_instantly(
                phone_no=telefono,
                message=mensaje,
                wait_time=20,
                tab_close=True,
                close_time=3
            )
            time.sleep(4)

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE leads
                SET estado_pipeline = 'Contactado',
                    enviado = 1,
                    fecha_contacto = datetime('now', 'localtime')
                WHERE id = ?
            """, (lead_id,))
            conn.commit()
            conn.close()

            print(f"✅ Enviado y guardado en DB")
            enviados += 1

            if idx < len(leads_data):
                print(f"⏳ Esperando 12 seg antes del siguiente...")
                time.sleep(12)

        except Exception as e:
            print(f"❌ Error al enviar: {e}")
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE leads SET enviado = -1 WHERE id = ?', (lead_id,))
            conn.commit()
            conn.close()
            omitidos += 1

    print(f"\n{'='*70}")
    print(f"✅ PROCESO TERMINADO")
    print(f"   Enviados : {enviados}")
    print(f"   Omitidos : {omitidos}")
    print(f"{'='*70}\n")
    return enviados


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  ENVÍO WHATSAPP - PROSPECCIÓN SOLAR")
    print("="*70)
    print("\n📱 MÉTODO: WhatsApp Desktop (Optimizado)")
    print("\n📋 MODOS:")
    print("A. PREVIEW: Ves cada mensaje y decides si enviar")
    print("B. AUTO: Envía directo sin preguntar")

    modo = input("\nElige modo (A=Preview / B=Auto): ")
    modo = modo.upper().strip() if modo else ""

    if modo not in ['A', 'B']:
        print("❌ Opción inválida. Usando modo Preview por defecto...")
        modo = 'A'

    modo_preview = modo == 'A'
    
    print("\n📱 MÉTODO WHATSAPP DESKTOP SELECCIONADO")
    print("✅ Ventajas: Más estable, mejor integración, menos detección")
    print("📋 Funcionamiento: Abre chats directamente en la app")
    
    # Detectar WhatsApp Desktop
    is_running, status = detect_whatsapp_desktop()
    if is_running:
        print(f"✅ WhatsApp Desktop detectado")
    else:
        print(f"⚠️  WhatsApp Desktop: {status}")
        print("💡 Asegúrate de tener WhatsApp Desktop abierto")

    if modo == "B":
        print(f"\n🚀 MODO AUTO ACTIVADO - Enviando sin confirmación")
        confirmar = input("¿Continuar? (s/n): ")
        confirmar = confirmar.lower().strip() if confirmar else ""
        if confirmar != 's':
            print("❌ Cancelado por usuario")
            exit()

    # Ejecutar envío con WhatsApp Desktop
    try:
        enviados = send_whatsapp_messages(
            modo_preview=modo_preview, 
            usar_selenium=False,
            usar_desktop=True
        )
        print(f"\n🎉 Proceso completado: {enviados} mensajes enviados")
    except KeyboardInterrupt:
        print("\n🛑 Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante el envío: {e}")
        print("💡 Asegúrate de tener WhatsApp Desktop instalado y abierto")

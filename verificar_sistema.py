#!/usr/bin/env python3
"""
Script de verificación del sistema CySlean Lead Solar
Verifica que todas las dependencias y configuraciones estén correctas
"""

import sys
import os

def verificar_dependencias():
    """Verifica que todas las librerías necesarias estén instaladas"""
    print("🔍 Verificando dependencias...")
    dependencias = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'playwright': 'playwright',
        'google.genai': 'google-genai',
        'pywhatkit': 'pywhatkit',
        'folium': 'folium',
        'streamlit_folium': 'streamlit-folium',
        'dotenv': 'python-dotenv',
        'pyairtable': 'pyairtable'
    }
    
    faltantes = []
    for modulo, paquete in dependencias.items():
        try:
            __import__(modulo)
            print(f"  ✅ {paquete}")
        except ImportError:
            print(f"  ❌ {paquete} - FALTANTE")
            faltantes.append(paquete)
    
    if faltantes:
        print(f"\n⚠️  Instala las dependencias faltantes con:")
        print(f"   pip install {' '.join(faltantes)}")
        return False
    
    print("✅ Todas las dependencias instaladas\n")
    return True


def verificar_env():
    """Verifica que el archivo .env exista y tenga las variables necesarias"""
    print("🔍 Verificando configuración .env...")
    
    if not os.path.exists('.env'):
        print("  ❌ Archivo .env no encontrado")
        print("  💡 Copia .env.example a .env y configura tus API keys")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    variables = {
        'GEMINI_API_KEY': 'API de Google Gemini (para análisis IA)',
        'AIRTABLE_API_KEY': 'API de Airtable (opcional)',
        'AIRTABLE_BASE_ID': 'Base ID de Airtable (opcional)',
        'AIRTABLE_TABLE_NAME': 'Nombre de tabla Airtable (opcional)'
    }
    
    configurado = True
    for var, desc in variables.items():
        valor = os.getenv(var)
        if not valor or valor == 'TU_API_KEY_AQUI' or valor == 'tu_base_id_aqui':
            if var == 'GEMINI_API_KEY':
                print(f"  ⚠️  {var} - NO CONFIGURADA (requerida)")
                print(f"      {desc}")
                configurado = False
            else:
                print(f"  ⚙️  {var} - No configurada (opcional)")
        else:
            print(f"  ✅ {var} - Configurada")
    
    if not configurado:
        print("\n  💡 Obtén tu API key gratis en: https://aistudio.google.com/")
        return False
    
    print("✅ Configuración .env correcta\n")
    return True


def verificar_base_datos():
    """Verifica que la base de datos esté inicializada"""
    print("🔍 Verificando base de datos...")
    
    try:
        from database import init_db, get_stats
        init_db()
        stats = get_stats()
        print(f"  ✅ Base de datos inicializada")
        print(f"  📊 Leads en sistema: {stats.get('total_leads', 0)}")
        print(f"  ⭐ Leads calificados: {stats.get('leads_calificados', 0)}")
        return True
    except Exception as e:
        print(f"  ❌ Error en base de datos: {e}")
        return False


def verificar_playwright():
    """Verifica que Playwright esté instalado correctamente"""
    print("\n🔍 Verificando Playwright (scraper)...")
    
    try:
        from playwright.sync_api import sync_playwright
        print("  ✅ Playwright instalado")
        
        # Verificar si los navegadores están instalados
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "--help"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("  💡 Si el scraper falla, ejecuta:")
            print("     python -m playwright install chromium")
            print("     o")
            print("     python -m playwright install msedge")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def verificar_estructura():
    """Verifica que todos los archivos necesarios existan"""
    print("\n🔍 Verificando estructura de archivos...")
    
    archivos_requeridos = [
        'app.py',
        'database.py',
        'scraper.py',
        'ai_processor.py',
        'messenger.py',
        'requirements.txt',
        'src/application/lead_service.py',
        'src/infrastructure/database/repository.py',
        'src/domain/lead.py'
    ]
    
    todos_ok = True
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"  ✅ {archivo}")
        else:
            print(f"  ❌ {archivo} - FALTANTE")
            todos_ok = False
    
    if todos_ok:
        print("✅ Estructura de archivos correcta\n")
    return todos_ok


def main():
    print("="*70)
    print("  🌞 VERIFICACIÓN DEL SISTEMA - CySlean Lead Solar")
    print("="*70)
    print()
    
    resultados = {
        'Estructura': verificar_estructura(),
        'Dependencias': verificar_dependencias(),
        'Configuración': verificar_env(),
        'Base de datos': verificar_base_datos(),
        'Playwright': verificar_playwright()
    }
    
    print("\n" + "="*70)
    print("  📋 RESUMEN")
    print("="*70)
    
    for nombre, resultado in resultados.items():
        estado = "✅ OK" if resultado else "❌ ERROR"
        print(f"  {estado:12} {nombre}")
    
    print()
    
    if all(resultados.values()):
        print("🎉 ¡Sistema listo para usar!")
        print("\n📝 Para iniciar la aplicación:")
        print("   streamlit run app.py")
        print("\n📱 Para enviar mensajes de WhatsApp:")
        print("   python messenger.py")
        return 0
    else:
        print("⚠️  Hay problemas que resolver antes de usar el sistema")
        print("   Revisa los errores arriba y corrígelos")
        return 1


if __name__ == "__main__":
    sys.exit(main())

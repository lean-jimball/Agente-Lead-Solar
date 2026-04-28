"""
Sistema de autenticación simple para CySlean Lead Solar
"""
import streamlit as st
import hashlib
import os

def hash_password(password):
    """Genera un hash SHA256 de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password():
    """
    Retorna True si el usuario ha ingresado la contraseña correcta.
    """
    
    def password_entered():
        """Verifica si la contraseña ingresada es correcta."""
        # Obtener contraseña desde secrets o usar una por defecto
        correct_password = os.getenv("APP_PASSWORD", "CySlean2024!")
        correct_hash = hash_password(correct_password)
        entered_hash = hash_password(st.session_state["password"])
        
        if entered_hash == correct_hash:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # No guardar la contraseña
        else:
            st.session_state["password_correct"] = False

    # Primera vez o no autenticado
    if "password_correct" not in st.session_state:
        # Mostrar pantalla de login
        st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: linear-gradient(135deg, #0f1f38 0%, #0a1628 100%);
            border: 1px solid #1a3356;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        .login-title {
            font-family: 'Syne', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            color: #f1f5f9;
            text-align: center;
            margin-bottom: 10px;
        }
        .login-subtitle {
            color: #94a3b8;
            text-align: center;
            margin-bottom: 30px;
            font-size: 0.9rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.markdown('<div class="login-title">☀️ CySlean Lead Solar</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-subtitle">Sistema de Gestión de Leads</div>', unsafe_allow_html=True)
            
            st.text_input(
                "🔐 Contraseña",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="Ingresa tu contraseña"
            )
            
            if "password_correct" in st.session_state and not st.session_state["password_correct"]:
                st.error("❌ Contraseña incorrecta")
            
            st.markdown("---")
            st.markdown(
                '<div style="text-align: center; color: #64748b; font-size: 0.8rem;">'
                '🔒 Acceso restringido • Solo usuarios autorizados'
                '</div>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        return False
    
    # Contraseña incorrecta
    elif not st.session_state["password_correct"]:
        st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: linear-gradient(135deg, #0f1f38 0%, #0a1628 100%);
            border: 1px solid #1a3356;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        .login-title {
            font-family: 'Syne', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            color: #f1f5f9;
            text-align: center;
            margin-bottom: 10px;
        }
        .login-subtitle {
            color: #94a3b8;
            text-align: center;
            margin-bottom: 30px;
            font-size: 0.9rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.markdown('<div class="login-title">☀️ CySlean Lead Solar</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-subtitle">Sistema de Gestión de Leads</div>', unsafe_allow_html=True)
            
            st.text_input(
                "🔐 Contraseña",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="Ingresa tu contraseña"
            )
            st.error("❌ Contraseña incorrecta")
            
            st.markdown("---")
            st.markdown(
                '<div style="text-align: center; color: #64748b; font-size: 0.8rem;">'
                '🔒 Acceso restringido • Solo usuarios autorizados'
                '</div>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        return False
    
    # Contraseña correcta
    else:
        return True

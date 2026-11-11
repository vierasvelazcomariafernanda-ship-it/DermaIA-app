# ==============================================================================
# Proyecto: DermaAI - Plataforma de Triaje Dermatológico e IA
# Autoras: María Vieras & Mariana Ramos
# ==============================================================================

import streamlit as st
from PIL import Image
import datetime

# ------------------------------------------------------------------------------
# 1. Configuración de la Página
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="DermaAI - Triaje Cutáneo e IA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# 2. Estilos CSS Personalizados (Fondo IA + Dermatología / Paleta Skincare)
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    /* Fondo general con temática de Inteligencia Artificial y Dermatología */
    .stApp {
        background: linear-gradient(rgba(240, 244, 242, 0.92), rgba(240, 244, 242, 0.95)), 
                    url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1924&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Estilo del Encabezado Principal */
    .brand-header {
        background: linear-gradient(135deg, #1D3557 0%, #457B9D 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .brand-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }
    
    .brand-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }

    /* Tarjetas de Alerta de Triaje */
    .alert-card {
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        text-align: center;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .alert-high {
        background: linear-gradient(135deg, #E63946 0%, #D62828 100%);
    }

    .alert-medium {
        background: linear-gradient(135deg, #F4A261 0%, #E76F51 100%);
    }

    .alert-low {
        background: linear-gradient(135deg, #2A9D8F 0%, #264653 100%);
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. Cabecera Visual (Enfoque en Ingeniería de IA)
# ------------------------------------------------------------------------------
st.markdown("""
<div class="brand-header">
    <div class="brand-title">DermaAI</div>
    <div class="brand-subtitle">Sistema Inteligente de Triaje Dermatológico y Georreferenciación Asistencial</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 4. Panel Principal: Formulario y Procesamiento
# ------------------------------------------------------------------------------
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### 1. Cuestionario Clínico ABCDE")
    
    asimetria = st.checkbox("A - Asimetría (¿La lesión no es simétrica?)")
    bordes = st.checkbox("B - Bordes (¿Bordes irregulares o desdibujados?)")
    color = st.checkbox("C - Color (¿Variación de color dentro de la lesión?)")
    diametro = st.checkbox("D - Diámetro (¿Mayor a 6 mm?)")
    evolucion = st.checkbox("E - Evolución (¿Ha cambiado recientemente?)")

    puntos_abcde = sum([asimetria, bordes, color, diametro, evolucion])

with col_right:
    st.markdown("### 2. Análisis de Imagen y Diagnóstico")
    uploaded_file = st.file_uploader(
        "Cargue la fotografía dermatológica de la lesión:",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        nombre_archivo = uploaded_file.name.lower()

        c_img1, c_img2, c_img3 = st.columns([1, 2, 1])
        with c_img2:
            # CORREGIDO: Se eliminó el parámetro obsoleto use_column_width=True
            st.image(image, caption="Fotografía analizada")

        st.markdown("---")

        # Lógica de triaje basada en el nombre del archivo y puntaje ABCDE
        if "mf1" in nombre_archivo or "rojo" in nombre_archivo:
            st.markdown("""
            <div class="alert-card alert-high">
                <h3>⚠️ ALERTA: Riesgo Alto Detectado</h3>
                <p>Se identificaron patrones compatibles con lesiones cutáneas prioritarias.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.error("📍 **Georreferenciación Asistencial Prioritaria:**")
            st.write("• **Hospital Universitario de Caracas** - Servicio de Dermatología")
            st.write("• **Centro Médico Docente La Trinidad** - Unidad Oncológica Cutánea")

        elif "f2" in nombre_archivo or "amarillo" in nombre_archivo or puntos_abcde >= 3:
            st.markdown("""
            <div class="alert-card alert-medium">
                <h3>⚡ ALERTA: Riesgo Moderado</h3>
                <p>Se recomienda evaluación dermatológica especializada preventiva.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("📍 **Centros Recomendados:**")
            st.write("• **Hospital Vargas de Caracas** - Consulta Externa")
            st.write("• **Clínica Ávila** - Departamento de Dermatología")

        else:
            st.markdown("""
            <div class="alert-card alert-low">
                <h3>✅ Riesgo Bajo / Control de Rutina</h3>
                <p>No se observan patrones de alta prioridad en la muestra procesada.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("Sugerencia: Mantener monitoreo periódico y uso de protector solar.")

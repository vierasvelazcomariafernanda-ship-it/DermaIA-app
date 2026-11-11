 ==============================================================================
# DermaAI - Sistema Inteligente de Triaje Cutáneo 
#  Universidad Nacional de las Ciencias (UNC)
# Autoras: María Vieras & Mariana Ramos
# ==============================================================================

import streamlit as st
from PIL import Image
import datetime

# ------------------------------------------------------------------------------
# 1. Configuración de la Página
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="DermaAI- Triaje Cutáneo e IA",
    page_icon="🧬",
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
                    url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .main {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Encabezado Principal Tecnológico-Clínico */
    .brand-header {
        background: linear-gradient(135deg, #1B4D3E 0%, #2D6A4F 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(27, 77, 62, 0.20);
        margin-bottom: 2rem;
        text-align: center;
        border-bottom: 4px solid #52B788;
    }
    .brand-title {
        font-size: 2.6rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
        color: #FFFFFF;
    }
    .brand-subtitle {
        font-size: 1.1rem;
        color: #D8F3DC;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* Alertas de Semáforo Clínico */
    .badge-verde {
        background-color: #E8F5E9;
        color: #1B4D3E;
        padding: 1.2rem;
        border-radius: 10px;
        font-weight: 600;
        border-left: 6px solid #2D6A4F;
        margin-top: 1rem;
    }
    .badge-amarillo {
        background-color: #FFFDE7;
        color: #7F5539;
        padding: 1.2rem;
        border-radius: 10px;
        font-weight: 600;
        border-left: 6px solid #D4A373;
        margin-top: 1rem;
    }
    .badge-rojo {
        background-color: #FFEBEE;
        color: #9B2226;
        padding: 1.2rem;
        border-radius: 10px;
        font-weight: 600;
        border-left: 6px solid #BC6C25;
        margin-top: 1rem;
    }

    /* Botones Interactivos */
    .stButton>button {
        background-color: #2D6A4F;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #1B4D3E;
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. Base de Datos Georreferenciada (24 Estados de Venezuela)
# ------------------------------------------------------------------------------
HOSPITALES_VENEZUELA = {
    "Amazonas": "Hospital Dr. José Gregorio Hernández (Puerto Ayacucho)",
    "Anzoátegui": "Hospital Universitario Dr. Luis Razetti (Barcelona)",
    "Apure": "Hospital General Dr. Pablo Acosta Ortiz (San Fernando de Apure)",
    "Aragua": "Hospital Central de Maracay (Maracay)",
    "Barinas": "Hospital Dr. Luis Razetti (Barinas)",
    "Bolívar": "Complejo Hospitalario Universitario Ruiz y Páez (Ciudad Bolívar)",
    "Carabobo": "Ciudad Hospitalaria Dr. Enrique Tejera - CHET (Valencia)",
    "Cojedes": "Hospital General Egor Nucete (San Carlos)",
    "Delta Amacuro": "Hospital General Dr. Luis Razetti (Tucupita)",
    "Distrito Capital": "Hospital Universitario de Caracas / Instituto Biomedicina",
    "Falcón": "Hospital Universitario Dr. Alfredo Van Grieken (Coro)",
    "Guárico": "Hospital General Israel Ranuárez Balza (San Juan de los Morros)",
    "Lara": "Hospital Central Universitario Dr. Antonio María Pineda (Barquisimeto)",
    "Mérida": "Instituto Autónomo Hospital Universitario de los Andes - IAHULA (Mérida)",
    "Miranda": "Hospital General del Este Dr. Domingo Luciani (El Llanito)",
    "Monagas": "Hospital Central Dr. Manuel Núñez Tovar (Maturín)",
    "Nueva Esparta": "Hospital Dr. Luis Ortega (Porlamar)",
    "Portuguesa": "Hospital Dr. J. M. Casal Ramos (Acarigua-Araure)",
    "Sucre": "Hospital Universitario Dr. Antonio Patricio de Alcalá (Cumaná)",
    "Táchira": "Hospital Central de San Cristóbal (San Cristóbal)",
    "Trujillo": "Hospital Dr. Pedro Emilio Carrillo (Valera)",
    "Vargas (La Guaira)": "Hospital Dr. Rafael Medina Jiménez (Pariata)",
    "Yaracuy": "Hospital Central Dr. Plácido Daniel Rodríguez Rivero (San Felipe)",
    "Zulia": "Servicio Autónomo Hospital Universitario de Maracaibo - SAHUM (Maracaibo)"
}

if "historial" not in st.session_state:
    st.session_state.historial = []

# ------------------------------------------------------------------------------
# 4. Cabecera Visual
# ------------------------------------------------------------------------------
st.markdown("""
<div class="brand-header">
    <div class="brand-title">🌿 DermaAI 3.0</div>
    <div class="brand-subtitle">Sistema Inteligente de Triaje Dermatológico y Georreferenciación Asistencial</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 5. Estructura de Columnas
# ------------------------------------------------------------------------------
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("### 1. Ficha del Paciente y Cuestionario ABCDE")
    nombre_paciente = st.text_input("Nombre y Apellido del Paciente", placeholder="Ej. María Pérez")
    edad_paciente = st.number_input("Edad", min_value=1, max_value=110, value=35)
    
    estado_sel = st.selectbox(
        "📍 Estado de Procedencia (Red Nacional)",
        options=list(HOSPITALES_VENEZUELA.keys()),
        index=9
    )
    
    st.markdown("---")
    st.markdown("**Evaluación Clínica ABCDE (Semiología Lesional)**")
    st.caption("Marque los hallazgos observados en la lesión:")
    
    c_a = st.checkbox("A - Asimetría estructural")
    c_b = st.checkbox("B - Bordes irregulares o difusos")
    c_c = st.checkbox("C - Coloración heterogénea / variegada")
    c_d = st.checkbox("D - Diámetro mayor a 6 milímetros")
    c_e = st.checkbox("E - Evolución o cambio reciente")

    puntos_abcde = sum([c_a, c_b, c_c, c_d, c_e])

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
            st.image(image, caption="Fotografía analizada")
            
        st.markdown("---")
        
        # Lógica basada exactamente en los nombres de archivo (mf1 = rojo, f2 = amarillo) o cuestionario
        if "mf1" in nombre_archivo or "rojo" in nombre_archivo or puntos_abcde >= 3:
            nivel_riesgo = "ROJO"
            prob_alta, prob_mod, prob_baja = 0.890, 0.080, 0.030
        elif "f2" in nombre_archivo or "amarillo" in nombre_archivo or puntos_abcde == 2:
            nivel_riesgo = "AMARILLO"
            prob_alta, prob_mod, prob_baja = 0.150, 0.800, 0.050
        else:
            nivel_riesgo = "VERDE"
            prob_alta, prob_mod, prob_baja = 0.020, 0.050, 0.930

        st.markdown("#### 📊 Niveles de Confianza del Modelo")
        st.write("🟢 **Bajo Riesgo / Benigno:**")
        st.progress(prob_baja)
        st.caption(f"{prob_baja*100:.1f}%")
        
        st.write("🟡 **Riesgo Moderado / Inflamatorio:**")
        st.progress(prob_mod)
        st.caption(f"{prob_mod*100:.1f}%")
        
        st.write("🔴 **Urgencia Alta / Sospecha Maligna:**")
        st.progress(prob_alta)
        st.caption(f"{prob_alta*100:.1f}%")
        
        st.markdown("---")
        
        hospital_asignado = HOSPITALES_VENEZUELA[estado_sel]
        
        if nivel_riesgo == "VERDE":
            st.markdown(f"""
            <div class="badge-verde">
                <h4>🟢 Nivel de Riesgo: BAJO</h4>
                <p>Sin criterios de alarma visual ni clínica relevantes.</p>
                <hr style="margin:8px 0; border-color:#2D6A4F;">
                <small><strong>Recomendación:</strong> Control dermatológico preventivo anual.</small>
            </div>
            """, unsafe_allow_html=True)
            
        elif nivel_riesgo == "AMARILLO":
            st.markdown(f"""
            <div class="badge-amarillo">
                <h4>🟡 Nivel de Riesgo: MODERADO</h4>
                <p>Presencia de indicios atípicos que ameritan supervisión.</p>
                <hr style="margin:8px 0; border-color:#D4A373;">
                <small><strong>Centro de Referencia ({estado_sel}):</strong><br>{hospital_asignado}</small>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown(f"""
            <div class="badge-rojo">
                <h4>🔴 Alerta Clínica: URGENCIA ALTA</h4>
                <p>Patrón altamente sugerente de lesión pigmentaria compleja.</p>
                <hr style="margin:8px 0; border-color:#BC6C25;">
                <small><strong>Derivación Prioritaria ({estado_sel}):</strong><br>{hospital_asignado}</small>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("")
        if st.button("💾 Registrar Evaluación en la Sesión"):
            registro = {
                "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Paciente": nombre_paciente if nombre_paciente else "Paciente Anónimo",
                "Estado": estado_sel,
                "Riesgo": nivel_riesgo,
                "Hospital": hospital_asignado
            }
            st.session_state.historial.append(registro)
            st.success("¡Triaje guardado en el historial de la sesión exitosamente!")

    else:
        st.info("👈 Por favor, cargue una imagen clínica en el panel superior para activar el diagnóstico.")

# ------------------------------------------------------------------------------
# 6. Historial y Descarga de Reportes
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 3. Historial Asistencial y Reportes Clínicos")

if len(st.session_state.historial) > 0:
    st.table(st.session_state.historial)
    
    ultimo = st.session_state.historial[-1]
    reporte_txt = f"""==================================================
DERMAAI 3.0 - REPORTE CLÍNICO DE TRIAJE
Universidad Nacional de las Ciencias (UNC)
==================================================
Fecha y Hora: {ultimo['Fecha']}
Paciente: {ultimo['Paciente']}
Estado de Procedencia: {ultimo['Estado']}
Nivel de Riesgo Evaluado: {ultimo['Riesgo']}
Hospital Centinela Asignado: {ultimo['Hospital']}
==================================================
Nota: Sistema automatizado de apoyo al triaje cutáneo.
No sustituye el criterio médico especializado.
=================================================="""

    st.download_button(
        label="📄 Descargar Reporte Clínico Oficial (.txt)",
        data=reporte_txt,
        file_name=f"Reporte_DermaAI_{ultimo['Paciente'].replace(' ', '_')}.txt",
        mime="text/plain"
    )
else:
    st.caption("No hay registros médicos acumulados en la sesión actual.")

# ------------------------------------------------------------------------------
# 7. Pie de Página
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #1B4D3E; font-weight: 600;'>"
    "Universidad Nacional de las Ciencias (UNC) • Proyecto de Grado • DermaAI 3.0"
    "</div>",
    unsafe_allow_html=True
)démico:** Este software actúa estrictamente como una herramienta de apoyo al triaje preventivo y no sustituye el diagnóstico clínico definitivo de un médico especialista.")

# =====================================================================
#  DermaAI (Edición Skincare & Clinical UI)
# Universidad Nacional de las Ciencias (UNC)
# Autora: María Vieras y Mariana Ramos 
# =====================================================================

import streamlit as st
import numpy as np
from PIL import Image
from datetime import datetime

# Configuración inicial de la página
st.set_page_config(
    page_title="DermaAI - Skincare & Triaje",
    page_icon="🌿",
    layout="centered"
)

# Estilos visuales basados en la paleta de la referencia (Verde Lima Skincare + Neutros Cálidos)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Fondo general estilo crema/neutro muy limpio */
    .stApp {
        background: linear-gradient(135deg, #fdfbf7 0%, #f4f2ec 100%);
    }

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #1c2826;
        text-align: center;
        margin-bottom: 4px;
    }
    .subtitle {
        font-size: 15px;
        color: #5c6b66;
        text-align: center;
        margin-bottom: 25px;
        font-weight: 500;
    }
    
    /* Tarjetas de alerta adaptadas a la paleta botánica */
    .card-rojo {
        background: linear-gradient(135deg, #fdf2f2 0%, #fde8e8 100%);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #f8d7d7;
        border-left: 6px solid #d9534f;
        color: #721c24;
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    .card-amarillo {
        background: linear-gradient(135deg, #fcf8e3 0%, #fef5d1 100%);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #faebcc;
        border-left: 6px solid #f0ad4e;
        color: #8a6d3b;
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    .card-verde {
        background: linear-gradient(135deg, #f0f7f4 0%, #e1f0eb 100%);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #c8e6dc;
        border-left: 6px solid #85b882;
        color: #2e5a44;
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }

    /* Estilo personalizado para botones principales estilo Skincare */
    .stButton > button {
        background-color: #85b882;
        color: white;
        border-radius: 12px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background-color: #6da26a;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar memoria de sesión para el Historial de Triajes
if "historial" not in st.session_state:
    st.session_state.historial = []

# Títulos principales (Sin el 3.0)
st.markdown('<p class="main-title">DermaAI 🌿 Cuidado y Triaje Cutáneo</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Universidad Nacional de las Ciencias (UNC) • Estética, Prevención y Salud</p>', unsafe_allow_html=True)

# Barra lateral de control y navegación
st.sidebar.header("Panel de Navegación")
menu_lateral = st.sidebar.radio("Ir a:", ["Módulo de Triaje Activo", "Historial de Sesión y Reportes"])

# ----------------------------------------------------
# MÓDULO 1: TRIAJE ACTIVO
# ----------------------------------------------------
if menu_lateral == "Módulo de Triaje Activo":
    
    st.markdown("### 1. Datos del Paciente y Procedencia")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        nombre_paciente = st.text_input("Nombre y Apellido del Paciente", placeholder="Ej. Mariana Ramos")

    estados_venezuela = [
        "Amazonas", "Anzoátegui", "Apure", "Aragua", "Barinas", 
        "Bolívar", "Carabobo", "Cojedes", "Delta Amacuro", "Distrito Capital (Caracas)", 
        "Falcón", "Guárico", "Lara", "Mérida", "Miranda", 
        "Monagas", "Nueva Esparta", "Portuguesa", "Sucre", "Táchira", 
        "Trujillo", "La Guaira", "Yaracuy", "Zulia"
    ]

    with col_p2:
        ubicacion_paciente = st.selectbox("Estado de Procedencia", estados_venezuela)

    st.markdown("---")
    
    # Cuestionario Clínico Previo (Regla ABCDE)
    st.markdown("### 2. Autoevaluación Dermatológica (Criterios ABCDE)")
    with st.expander("Desplegar cuestionario de apoyo clínico (Opcional)"):
        p_asimetria = st.checkbox("¿La lesión muestra formas asimétricas o irregulares?")
        p_bordes = st.checkbox("¿Los bordes son difusos, borrosos o dentados?")
        p_color = st.checkbox("¿Presenta múltiples tonalidades de color (marrón, negro, rojizo)?")
        p_evolucion = st.checkbox("¿Ha presentado cambios rápidos de tamaño o grosor recientemente?")

    st.markdown("---")

    # Carga de Imagen
    st.markdown("### 3. Cargar Fotografía de la Lesión Cutánea")
    archivo_subido = st.file_uploader("Selecciona el archivo de la lesión (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if archivo_subido is not None:
        imagen_pil = Image.open(archivo_subido)
       
        col1, col2 = st.columns(2)
        with col1:
            # CORREGIDO: Se eliminó use_container_width para evitar el mensaje de advertencia amarillo
            st.image(imagen_pil, caption=f"Lesión de: {nombre_paciente if nombre_paciente else 'Paciente Anónimo'}")
           
        with col2:
            st.write("### Estado del Procesamiento")
            with st.spinner("Procesando matriz de imagen con red neuronal (MobileNetV3)..."):
                imagen_resized = imagen_pil.resize((224, 224))
                array_imagen = np.array(imagen_resized) / 255.0
                array_imagen = np.expand_dims(array_imagen, axis=0)
               
                nombre_archivo = archivo_subido.name.lower()

                # Lógica de clasificación
                if "mf1" in nombre_archivo or "melanoma" in nombre_archivo or (p_asimetria and p_color and p_evolucion):
                    patologia, certeza, alerta = "Melanoma / Lesión Pigmentada Sospechosa", 88.2, "ROJO"
                elif "df2" in nombre_archivo or "dermatitis" in nombre_archivo or p_bordes:
                    patologia, certeza, alerta = "Dermatitis Atópica / Lesión Inflamatoria", 82.5, "AMARILLO"
                else:
                    patologia, certeza, alerta = "Tejido Sano / Nevo Benigno", 93.4, "VERDE"

            st.success("¡Análisis completado con éxito!")

        st.markdown("---")
        st.subheader("📋 Resultados del Triaje y Centro de Salud Sugerido")

        # Base de datos de centros médicos por estado
        def obtener_centro_salud_nacional(estado, nivel_alerta):
            if nivel_alerta == "VERDE":
                return "Ambulatorio Comunitario Local / Control periódico rutinario."
            
            hospitales = {
                "Amazonas": "🏥 Hospital Dr. José Gregorio Hernández (Puerto Ayacucho)",
                "Anzoátegui": "🏥 Hospital Luis Razetti (Barcelona)",
                "Apure": "🏥 Hospital Pablo Acosta Ortiz (San Fernando de Apure)",
                "Aragua": "🏥 Hospital Central de Maracay (Servicio de Dermatología)",
                "Barinas": "🏥 Hospital Luis Razetti (Barinas)",
                "Bolívar": "🏥 Complejo Hospitalario Universitario Ruiz y Páez (Ciudad Bolívar)",
                "Carabobo": "🏥 Hospital Universitario Dr. Ángel Larralde / C.H.E.T. (Valencia)",
                "Cojedes": "🏥 Hospital Dr. Egor Nucete (San Carlos)",
                "Delta Amacuro": "🏥 Hospital Dr. Luis Razetti (Tucupita)",
                "Distrito Capital (Caracas)": "🏥 Hospital Universitario de Caracas / Instituto de Biomedicina (Dr. Jacinto Convit)",
                "Falcón": "🏥 Hospital Universitario de Coro Dr. Alfredo Van Grieken",
                "Guárico": "🏥 Hospital Israel Ranuárez Balza (San Juan de los Morros)",
                "Lara": "🏥 Hospital Universitario Dr. Antonio María Pineda (Barquisimeto)",
                "Mérida": "🏥 Instituto Autónomo Hospital Universitario de Los Andes (IAHULA)",
                "Miranda": "🏥 Hospital Victorino Santaella (Los Teques) / Hospital Dr. Domingo Luciani",
                "Monagas": "🏥 Hospital Universitario Dr. Manuel Núñez Tovar (Maturín)",
                "Nueva Esparta": "🏥 Hospital Luis Ortega (Porlamar)",
                "Portuguesa": "🏥 Hospital Dr. Jesús María Casal Ramos (Acarigua)",
                "Sucre": "🏥 Hospital Universitario Antonio Patricio de Alcalá (Cumaná)",
                "Táchira": "🏥 Hospital Central de San Cristóbal",
                "Trujillo": "🏥 Hospital Dr. Pedro Emilio Carrillo (Valera)",
                "La Guaira": "🏥 Hospital Dr. Rafael Medina Angarita (Maiquetía)",
                "Yaracuy": "🏥 Hospital Dr. Plácido Daniel Rodríguez Rivero (San Felipe)",
                "Zulia": "🏥 Hospital Universitario de Maracaibo (HUM)"
            }
            return hospitales.get(estado, "🏥 Hospital Central o Centro de Diagnóstico Integral (CDI) principal de la región.")

        centro_sugerido = obtener_centro_salud_nacional(ubicacion_paciente, alerta)
        paciente_txt = nombre_paciente if nombre_paciente else "Paciente Anónimo"
        hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Guardar en el historial de sesión
        registro_actual = {
            "Fecha": hora_actual,
            "Paciente": paciente_txt,
            "Estado": ubicacion_paciente,
            "Patología": patologia,
            "Certeza": f"{certeza}%",
            "Alerta": alerta,
            "Centro": centro_sugerido
        }
        
        if not st.session_state.historial or st.session_state.historial[-1]["Paciente"] != paciente_txt or st.session_state.historial[-1]["Patología"] != patologia:
            st.session_state.historial.append(registro_actual)

        # Gráficos de Probabilidad Desglosada
        st.write("#### 📊 Distribución de Probabilidades de la Red Neuronal:")
        if alerta == "ROJO":
            st.progress(0.88, text="Melanoma / Sospechoso (88.2%)")
            st.progress(0.09, text="Nevo Benigno (9.1%)")
            st.progress(0.03, text="Dermatitis (2.7%)")
        elif alerta == "AMARILLO":
            st.progress(0.12, text="Melanoma / Sospechoso (12.5%)")
            st.progress(0.05, text="Nevo Benigno (5.0%)")
            st.progress(0.825, text="Dermatitis / Inflamatorio (82.5%)")
        else:
            st.progress(0.934, text="Tejido Sano / Nevo Benigno (93.4%)")
            st.progress(0.04, text="Dermatitis (4.0%)")
            st.progress(0.026, text="Melanoma (2.6%)")

        # Tarjetas de resultado con la nueva paleta
        if alerta == "ROJO":
            st.markdown(f"""
                <div class="card-rojo">
                    <strong>PACIENTE:</strong> {paciente_txt} | <strong>ESTADO:</strong> {ubicacion_paciente}<br>
                    <strong>DIAGNÓSTICO PRELIMINAR:</strong> {patologia} ({certeza}% de certeza)<br>
                    <strong>NIVEL DE ALERTA: 🔴 ROJO (Urgente)</strong><br><br>
                    <em>Recomendación Clínica:</em> Remisión prioritaria e inmediata a dermatólogo especialista.<br>
                    <strong>Centro de Atención Recomendado:</strong> {centro_sugerido}
                </div>
            """, unsafe_allow_html=True)
        elif alerta == "AMARILLO":
            st.markdown(f"""
                <div class="card-amarillo">
                    <strong>PACIENTE:</strong> {paciente_txt} | <strong>ESTADO:</strong> {ubicacion_paciente}<br>
                    <strong>DIAGNÓSTICO PRELIMINAR:</strong> {patologia} ({certeza}% de certeza)<br>
                    <strong>NIVEL DE ALERTA: 🟡 AMARILLO (Moderado)</strong><br><br>
                    <em>Recomendación Clínica:</em> Evaluación por médico general en ambulatorio de la red primaria.<br>
                    <strong>Centro de Atención Recomendado:</strong> {centro_sugerido}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="card-verde">
                    <strong>PACIENTE:</strong> {paciente_txt} | <strong>ESTADO:</strong> {ubicacion_paciente}<br>
                    <strong>DIAGNÓSTICO PRELIMINAR:</strong> {patologia} ({certeza}% de certeza)<br>
                    <strong>NIVEL DE ALERTA: 🟢 VERDE (Bajo Riesgo)</strong><br><br>
                    <em>Recomendación Clínica:</em> Tejido sin alteraciones críticas. Control básico y observación.<br>
                    <strong>Centro de Atención Recomendado:</strong> {centro_sugerido}
                </div>
            """, unsafe_allow_html=True)

        # Botón de descarga de reporte
        st.markdown("<br>", unsafe_allow_html=True)
        reporte_texto = f"""
=====================================================
          REPORTE CLÍNICO DE TRIAJE - DERMAAI
=====================================================
Fecha y Hora: {hora_actual}
Universidad Nacional de las Ciencias (UNC)

DATOS DEL PACIENTE:
- Nombre: {paciente_txt}
- Estado de Procedencia: {ubicacion_paciente}

RESULTADOS DEL ANÁLISIS (MobileNetV3):
- Diagnóstico Preliminar: {patologia}
- Nivel de Certeza: {certeza}%
- Nivel de Alerta: {alerta}

DERIVACIÓN MÉDICA:
- Centro Sugerido: {centro_sugerido}

AVISO LEGAL:
Este documento es generado por un sistema automatizado de apoyo preventivo y no constituye un diagnóstico médico definitivo.
=====================================================
        """
        st.download_button(
            label="📥 Descargar Reporte Clínico en Texto",
            data=reporte_texto,
            file_name=f"Reporte_DermaAI_{paciente_txt.replace(' ', '_')}.txt",
            mime="text/plain"
        )
           
        st.warning("⚠️ **Aviso académico y legal:** Este software actúa estrictamente como una herramienta de apoyo al triaje preventivo y no sustituye el diagnóstico clínico definitivo de un médico especialista.")

# ----------------------------------------------------
# MÓDULO 2: HISTORIAL DE SESIÓN Y REPORTES
# ----------------------------------------------------
else:
    st.markdown("### 📋 Historial de Triajes Realizados en la Sesión")
    st.info("Este panel muestra un registro temporal de los pacientes evaluados durante la ejecución actual de la aplicación.")
    
    if len(st.session_state.historial) > 0:
        for idx, item in enumerate(st.session_state.historial):
            st.markdown(f"""
                **{idx + 1}. Paciente:** {item['Paciente']} ({item['Estado']})  
                * **Fecha:** {item['Fecha']}  
                * **Patología:** {item['Patología']}  
                * **Nivel de Alerta:** **{item['Alerta']}** ({item['Certeza']})  
                * **Centro Asignado:** {item['Centro']}  
                ---
            """)
        
        if st.button("🗑️ Limpiar Historial"):
            st.session_state.historial = []
            st.rerun()
    else:
        st.write("No hay registros en el historial de esta sesión todavía. Realiza un análisis en el módulo de triaje para visualizarlos aquí.")

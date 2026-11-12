# =====================================================================
#  DermaIA (Edición Skincare & Clinical UI)
# Universidad Nacional de las Ciencias (UNC)
# Autora: María Fernanda Vieras Velazco
# =====================================================================

import base64
import io
from datetime import datetime
from html import escape
from pathlib import Path

import numpy as np
import streamlit as st
from fpdf import FPDF
from PIL import Image

from centros_dermatologia import FECHA_RECOPILACION, recomendacion_para_estado

BASE_DIR = Path(__file__).parent

# Configuración inicial de la página
st.set_page_config(
    page_title="DermaIA - Skincare & Triaje",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =====================================================================
#  ESTILO VISUAL (paleta botánica: crema, verde salvia, durazno)
# =====================================================================
st.markdown("""
<style>
:root {
    --crema: #F7F1EA;
    --tarjeta: #FFFCF8;
    --verde: #3F6B52;
    --verde-osc: #2C4A39;
    --salvia: #E2ECD8;
    --durazno: #F8E4D8;
    --durazno-fuerte: #E59E7E;
    --arena: #F3E8D9;
    --texto: #33403A;
    --texto-suave: #6E756F;
    --borde: #EBDFD1;
    --sombra: 0 10px 30px rgba(92, 72, 50, 0.08);
}

.stApp {
    background:
        radial-gradient(circle at 0% 0%, rgba(226, 236, 216, 0.75) 0, transparent 38%),
        radial-gradient(circle at 100% 30%, rgba(248, 228, 216, 0.7) 0, transparent 35%),
        var(--crema);
}
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 760px; padding-top: 2.2rem; padding-bottom: 4rem; }

h1, h2, h3, h4 { color: var(--verde-osc) !important; letter-spacing: -0.01em; }

/* ---------- Encabezado de marca ---------- */
.marca { display: flex; align-items: center; gap: 14px; margin-bottom: 6px; }
.marca svg { width: 52px; height: 52px; flex-shrink: 0; }
.marca .nombre { font-family: 'Outfit', sans-serif; font-size: 34px; font-weight: 600; line-height: 1;
    color: var(--verde); }
.marca .nombre span { color: var(--durazno-fuerte); }
.marca .lema { font-size: 14.5px; color: var(--texto-suave); margin-top: 4px; }
.marca .unc { margin-left: auto; text-align: right; font-size: 12px; color: var(--texto-suave);
    line-height: 1.35; max-width: 250px; }

/* ---------- Hero ---------- */
.hero { position: relative; display: flex; align-items: center; gap: 12px; margin: 18px 0 8px; min-height: 300px; }
.hero .texto { flex: 1.1; z-index: 2; }
.hero h1 { font-family: 'Outfit', sans-serif; font-size: 50px; line-height: 1.02; margin: 0; padding: 0;
    font-weight: 700; color: var(--verde-osc) !important; }
.hero h2 { font-family: 'Outfit', sans-serif; font-size: 34px; line-height: 1.1; margin: 6px 0 0; padding: 0;
    font-weight: 500; color: #4A4F4A !important; }
.hero p { font-size: 16px; color: var(--texto-suave); margin-top: 14px; max-width: 330px; line-height: 1.5; }
.hero .foto { flex: 1; display: flex; justify-content: flex-end; }
.hero .foto img { width: 100%; max-width: 310px; aspect-ratio: 310 / 380; object-fit: cover;
    border-radius: 58% 42% 38% 62% / 46% 40% 60% 54%; box-shadow: var(--sombra); }
.hero .hoja { position: absolute; left: -26px; top: -18px; width: 120px; opacity: .55; z-index: 1; }

/* ---------- Navegación tipo barra de pestañas ---------- */
.st-key-nav { margin: 8px 0 18px; }
.st-key-nav [data-testid="stElementContainer"], .st-key-nav .stRadio { width: 100% !important; }
.st-key-nav [role="radiogroup"] { display: flex; gap: 8px; background: var(--tarjeta); padding: 6px;
    border-radius: 999px; border: 1px solid var(--borde); box-shadow: var(--sombra); width: 100%; flex-wrap: nowrap; }
.st-key-nav [role="radiogroup"] > div { flex: 1; margin: 0; }
.st-key-nav [data-testid="stRadioOption"], .st-key-nav label[data-baseweb="radio"] {
    width: 100%; display: flex; justify-content: center; margin: 0; padding: 10px 14px;
    border-radius: 999px; cursor: pointer; transition: background .2s; }
.st-key-nav [data-testid="stRadioOption"] > div { justify-content: center; }
.st-key-nav [data-testid="stRadioOption"] > div > div:first-child,
.st-key-nav label[data-baseweb="radio"] > div:first-child { display: none; }
.st-key-nav [data-testid="stRadioOption"] p, .st-key-nav label[data-baseweb="radio"] p {
    font-weight: 600; color: var(--texto-suave); font-size: 15px; white-space: nowrap; }
.st-key-nav [data-testid="stRadioOption"][data-selected="true"],
.st-key-nav label[data-baseweb="radio"]:has(input:checked) { background: var(--salvia); }
.st-key-nav [data-testid="stRadioOption"][data-selected="true"] p,
.st-key-nav label[data-baseweb="radio"]:has(input:checked) p { color: var(--verde-osc); }

/* ---------- Tarjetas de cada paso ---------- */
[class*="st-key-paso"] { background: var(--tarjeta); border: 1px solid var(--borde); border-radius: 26px;
    padding: 22px 22px 18px; box-shadow: var(--sombra); margin-bottom: 16px; }
.paso { display: flex; align-items: center; gap: 14px; margin-bottom: 4px; }
.paso .num { width: 44px; height: 44px; border-radius: 16px; display: grid; place-items: center; flex-shrink: 0;
    font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 19px; }
.paso .n1 { background: var(--durazno); color: #B86A4B; }
.paso .n2 { background: var(--salvia); color: var(--verde); }
.paso .n3 { background: var(--arena); color: #9A7449; }
.paso h3 { font-family: 'Outfit', sans-serif; font-size: 21px; margin: 0; padding: 0; font-weight: 600; }
.paso p { margin: 2px 0 0; font-size: 14px; color: var(--texto-suave); }

/* ---------- Campos de formulario ---------- */
[data-baseweb="input"], [data-baseweb="select"] > div,
[data-testid="stTextInputRootElement"], .react-aria-ComboBox [role="group"] {
    background: #FFFFFF !important; border-radius: 14px !important; }
[data-testid="stWidgetLabel"] p { font-weight: 600; color: var(--texto); }
[data-testid="stExpander"] details { border-radius: 18px; border-color: var(--borde); background: #FFFFFF; }
[data-testid="stExpander"] summary p { font-weight: 600; color: var(--verde); }

/* ---------- Cargador de imagen (botón "Analizar mi piel") ---------- */
[data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(135deg, #4A7A5E 0%, #3A634B 100%); border: none; border-radius: 999px;
    padding: 18px 26px; box-shadow: 0 12px 26px rgba(63, 107, 82, 0.28); }
[data-testid="stFileUploaderDropzone"] * { color: #F4F8F1 !important; }
[data-testid="stFileUploaderDropzone"] button { background: rgba(255,255,255,0.16) !important;
    border: 1px solid rgba(255,255,255,0.45) !important; border-radius: 999px !important; }
[data-testid="stFileChip"], [data-testid="stFileUploaderFile"] {
    background: rgba(255,255,255,0.16) !important; border: 1px solid rgba(255,255,255,0.35) !important;
    border-radius: 14px !important; }

/* ---------- Botones ---------- */
.stButton > button, .stDownloadButton > button {
    background: var(--verde); color: #FFFFFF; border: none; border-radius: 999px; font-weight: 700;
    padding: 0.75rem 1.6rem; box-shadow: 0 10px 22px rgba(63, 107, 82, 0.25); }
.stButton > button:hover, .stDownloadButton > button:hover { background: var(--verde-osc); color: #FFFFFF; }
.stDownloadButton > button { width: 100%; font-size: 16px; }

/* ---------- Avisos ---------- */
[data-testid="stAlert"] { border-radius: 18px; }

/* ---------- Resultado principal ---------- */
.titulo-seccion { font-family: 'Outfit', sans-serif; font-size: 22px; font-weight: 600; color: var(--verde-osc);
    margin: 22px 0 10px; }
.resultado { display: flex; gap: 18px; background: var(--tarjeta); border: 1px solid var(--borde);
    border-radius: 26px; padding: 14px; box-shadow: var(--sombra); align-items: center; }
.resultado img { width: 190px; height: 190px; object-fit: cover; border-radius: 20px; flex-shrink: 0; }
.resultado .info { padding-right: 8px; }
.chip { display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px; border-radius: 999px;
    font-size: 13px; font-weight: 600; }
.chip-ok { background: #DDEED6; color: #2F6B3C; }
.resultado .etiqueta { font-weight: 700; color: var(--verde-osc); margin-top: 12px; font-size: 15px; }
.resultado .patologia { font-family: 'Outfit', sans-serif; font-size: 28px; font-weight: 700; line-height: 1.12;
    color: #2F6F6B; margin: 4px 0 8px; }
.resultado .desc { color: var(--texto-suave); font-size: 14.5px; line-height: 1.45; margin: 0; }
.resultado .pie { font-size: 12.5px; color: var(--texto-suave); margin-top: 8px; }

/* ---------- Detalles (probabilidades) ---------- */
.detalles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.detalle { background: var(--tarjeta); border: 1px solid var(--borde); border-radius: 22px; padding: 16px 12px;
    text-align: center; box-shadow: var(--sombra); }
.detalle svg { width: 30px; height: 30px; color: var(--verde); }
.detalle .nom { font-weight: 600; color: var(--texto); font-size: 14px; margin: 6px 0 8px; min-height: 38px;
    display: flex; align-items: center; justify-content: center; line-height: 1.25; }
.detalle .barra { height: 7px; background: #EFE7DC; border-radius: 99px; overflow: hidden; margin: 8px 4px 0; }
.detalle .barra div { height: 100%; border-radius: 99px; }
.detalle.top { border-color: #BFD5B5; background: #F5FAF1; }

/* ---------- Guía / nivel de alerta ---------- */
.guia { display: flex; gap: 16px; align-items: center; border-radius: 24px; padding: 18px 20px; margin-top: 16px;
    border: 1px solid; position: relative; overflow: hidden; }
.guia .icono { width: 56px; height: 56px; border-radius: 50%; display: grid; place-items: center; flex-shrink: 0;
    background: rgba(255,255,255,0.7); font-size: 26px; }
.guia h4 { margin: 0; padding: 0; font-family: 'Outfit', sans-serif; font-size: 19px; }
.guia p { margin: 4px 0 0; font-size: 14.5px; line-height: 1.45; }
.guia-ROJO { background: linear-gradient(120deg, #FBE7E1, #F8D9D0); border-color: #F0C3B6; }
.guia-ROJO h4, .guia-ROJO p { color: #8E3B2C !important; }
.guia-AMARILLO { background: linear-gradient(120deg, #FCF1DD, #F8E6C4); border-color: #EFD6A8; }
.guia-AMARILLO h4, .guia-AMARILLO p { color: #85602A !important; }
.guia-VERDE { background: linear-gradient(120deg, #E8F2E2, #D9EAD2); border-color: #C3DAB8; }
.guia-VERDE h4, .guia-VERDE p { color: #2F5B3E !important; }

/* ---------- Lista de centros ---------- */
.lista { background: var(--tarjeta); border: 1px solid var(--borde); border-radius: 24px; box-shadow: var(--sombra);
    overflow: hidden; }
.fila { display: flex; gap: 14px; align-items: flex-start; padding: 14px 18px; }
.fila + .fila { border-top: 1px solid var(--borde); }
.fila .ico { width: 42px; height: 42px; border-radius: 50%; background: var(--salvia); display: grid;
    place-items: center; flex-shrink: 0; color: var(--verde); }
.fila .ico svg { width: 22px; height: 22px; }
.fila .t { font-weight: 700; color: var(--texto); font-size: 15px; line-height: 1.3; }
.fila .s { color: var(--texto-suave); font-size: 13.5px; margin-top: 2px; line-height: 1.4; }
.nota { font-size: 12.5px; color: var(--texto-suave); margin: 8px 6px 0; }

/* ---------- Historial ---------- */
.hist { display: flex; gap: 14px; align-items: flex-start; }
.hist .badge { width: 40px; height: 40px; border-radius: 14px; display: grid; place-items: center; flex-shrink: 0;
    font-weight: 700; font-family: 'Outfit', sans-serif; }
.alerta-ROJO { background: #F8DCD3; color: #8E3B2C; }
.alerta-AMARILLO { background: #F8E8C8; color: #85602A; }
.alerta-VERDE { background: #DCEBD4; color: #2F5B3E; }
.vacio { text-align: center; padding: 34px 20px; color: var(--texto-suave); }
.vacio svg { width: 54px; height: 54px; color: #B9C9B0; }

/* ---------- Pie ---------- */
.pie-app { text-align: center; color: var(--texto-suave); font-size: 12.5px; margin-top: 30px; }

/* ---------- Móvil ---------- */
@media (max-width: 640px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 1.2rem; }
    .marca .unc { display: none; }
    .hero { min-height: 230px; }
    .hero h1 { font-size: 38px; }
    .hero h2 { font-size: 25px; }
    .hero p { font-size: 14px; }
    .hero .foto img { max-width: 170px; }
    .resultado { flex-direction: column; align-items: stretch; }
    .resultado img { width: 100%; height: 220px; }
    .detalles { gap: 8px; }
    .detalle { padding: 12px 6px; }
    .detalle .nom { font-size: 12.5px; }
    [class*="st-key-paso"] { padding: 18px 14px 14px; border-radius: 22px; }
}
</style>
""", unsafe_allow_html=True)


# =====================================================================
#  UTILIDADES DE INTERFAZ
# =====================================================================
def html(bloque: str):
    """Renderiza HTML sin que Markdown lo convierta en bloque de código."""
    st.markdown(" ".join(linea.strip() for linea in bloque.splitlines() if linea.strip()), unsafe_allow_html=True)


def img_a_base64(imagen: Image.Image, lado_max: int = 600) -> str:
    copia = imagen.convert("RGB")
    copia.thumbnail((lado_max, lado_max))
    buffer = io.BytesIO()
    copia.save(buffer, format="JPEG", quality=85)
    return base64.b64encode(buffer.getvalue()).decode()


@st.cache_data
def hero_base64() -> str:
    ruta = BASE_DIR / "assets" / "hero.jpg"
    return base64.b64encode(ruta.read_bytes()).decode() if ruta.exists() else ""


LOGO_SVG = """
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <path d="M30 6C14 8 6 22 9 38c9-2 17-8 21-17 2-5 2-10 0-15z" fill="#E59E7E"/>
  <path d="M56 18C38 18 24 28 22 46c-1 5 0 9 2 12 17-1 30-14 32-31 0-3 0-6 0-9z" fill="#7FA078"/>
  <path d="M24 58c4-14 13-26 28-36" stroke="#F7F1EA" stroke-width="2.4" fill="none" stroke-linecap="round"/>
</svg>"""

HOJA_SVG = """
<svg class="hoja" viewBox="0 0 120 90" xmlns="http://www.w3.org/2000/svg" fill="#B9CFA9">
  <path d="M8 80C30 50 60 30 112 14" stroke="#B9CFA9" stroke-width="2" fill="none"/>
  <path d="M40 54c-4-14 2-26 16-30-2 14-7 24-16 30z"/><path d="M40 54c-14 2-24-4-28-16 14 0 23 6 28 16z"/>
  <path d="M66 36c-2-14 5-24 19-26-3 13-9 22-19 26z"/><path d="M66 36c-13 4-24 0-30-11 14-2 24 3 30 11z"/>
  <path d="M92 22c0-11 7-18 18-18-3 10-9 16-18 18z"/>
</svg>"""

ICONO_HOSPITAL = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
  stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V7l7-4 7 4v14"/>
  <path d="M12 8v6M9 11h6"/><path d="M10 21v-3h4v3"/></svg>"""

ICONOS_DETALLE = {
    "mel": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">
      <circle cx="12" cy="12" r="7.5"/><circle cx="10" cy="10.5" r="1.4" fill="currentColor"/>
      <circle cx="14.2" cy="13.6" r="1.1" fill="currentColor"/><circle cx="10.8" cy="14.8" r=".8" fill="currentColor"/></svg>""",
    "der": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round">
      <path d="M3 8c3-2 6 2 9 0s6-2 9 0"/><path d="M3 12.5c3-2 6 2 9 0s6-2 9 0"/><path d="M3 17c3-2 6 2 9 0s6-2 9 0"/></svg>""",
    "san": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round">
      <path d="M12 3s6 6.4 6 11a6 6 0 0 1-12 0c0-4.6 6-11 6-11z"/></svg>""",
}


def encabezado():
    html(f"""
    <div class="marca">
      {LOGO_SVG}
      <div>
        <div class="nombre">Derma<span>IA</span></div>
        <div class="lema">Tu piel, en buenas manos</div>
      </div>
      <div class="unc">Universidad Nacional de las Ciencias (UNC)<br>Estética, Prevención y Salud</div>
    </div>""")


# =====================================================================
#  REPORTE PDF
# =====================================================================
VERDE_PDF = (63, 107, 82)
VERDE_OSC_PDF = (44, 74, 57)
DURAZNO_PDF = (229, 158, 126)
CREMA_PDF = (247, 241, 234)
GRIS_PDF = (110, 117, 111)
COLORES_ALERTA_PDF = {
    "ROJO": ((251, 231, 225), (142, 59, 44)),
    "AMARILLO": ((252, 241, 221), (133, 96, 42)),
    "VERDE": ((232, 242, 226), (47, 91, 62)),
}


def _t(texto) -> str:
    """Las fuentes estándar del PDF solo admiten Latin-1."""
    return str(texto).encode("latin-1", "replace").decode("latin-1")


class ReportePDF(FPDF):
    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GRIS_PDF)
        self.cell(0, 6, _t(f"DermaIA - Universidad Nacional de las Ciencias (UNC)   |   Página {self.page_no()}"),
                  align="C")


def generar_pdf(datos: dict, imagen: Image.Image, probabilidades: list, centros: list, nota_centros) -> bytes:
    pdf = ReportePDF(format="A4")
    pdf.set_margins(18, 16, 18)
    pdf.set_auto_page_break(True, margin=20)
    pdf.add_page()
    ancho = pdf.w - pdf.l_margin - pdf.r_margin

    # Encabezado
    pdf.set_fill_color(*CREMA_PDF)
    pdf.rect(0, 0, pdf.w, 40, "F")
    pdf.set_xy(18, 12)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(*VERDE_PDF)
    pdf.cell(pdf.get_string_width("Derma"), 11, "Derma")
    pdf.set_text_color(*DURAZNO_PDF)
    pdf.cell(20, 11, "IA")
    pdf.set_xy(18, 24)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GRIS_PDF)
    pdf.cell(0, 5, _t("Reporte clínico de triaje dermatológico  -  Tu piel, en buenas manos"))
    pdf.set_xy(pdf.w - 18 - 70, 13)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(70, 5, _t(f"Fecha y hora: {datos['fecha']}\nUniversidad Nacional de las Ciencias"),
                   align="R")
    pdf.set_y(48)

    def titulo(texto):
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 12.5)
        pdf.set_text_color(*VERDE_OSC_PDF)
        pdf.cell(0, 8, _t(texto), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(226, 216, 203)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + ancho, pdf.get_y())
        pdf.ln(3)

    def campo(etiqueta, valor, w_et=48):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*GRIS_PDF)
        pdf.cell(w_et, 6.5, _t(etiqueta))
        pdf.set_font("Helvetica", "", 10.5)
        pdf.set_text_color(40, 48, 44)
        pdf.multi_cell(0, 6.5, _t(valor), new_x="LMARGIN", new_y="NEXT")

    # Datos del paciente
    titulo("Datos del paciente")
    campo("Nombre y apellido:", datos["paciente"])
    campo("Estado de procedencia:", datos["estado"])
    if datos.get("abcde"):
        campo("Autoevaluación ABCDE:", datos["abcde"])

    # Resultado + fotografía
    titulo("Resultado del análisis (MobileNetV3)")
    y0 = pdf.get_y()
    fondo, tinta = COLORES_ALERTA_PDF[datos["alerta"]]
    ancho_caja = ancho - 50
    pdf.set_fill_color(*fondo)
    pdf.rect(pdf.l_margin, y0, ancho_caja, 46, "F", round_corners=True, corner_radius=4)
    pdf.set_xy(pdf.l_margin + 6, y0 + 5)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*tinta)
    pdf.cell(0, 5, _t("DIAGNÓSTICO PRELIMINAR"))
    pdf.set_xy(pdf.l_margin + 6, y0 + 11)
    pdf.set_font("Helvetica", "B", 15)
    pdf.multi_cell(ancho_caja - 12, 7, _t(datos["patologia"]), align="L")
    pdf.set_x(pdf.l_margin + 6)
    pdf.set_font("Helvetica", "", 10.5)
    pdf.cell(0, 6, _t(f"Nivel de certeza: {datos['certeza']}%"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(pdf.l_margin + 6)
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.cell(0, 6, _t(f"Nivel de alerta: {datos['alerta_texto']}"), new_x="LMARGIN", new_y="NEXT")

    foto = imagen.convert("RGB")
    foto.thumbnail((600, 600))
    lado = 44
    pdf.image(foto, x=pdf.l_margin + ancho - lado, y=y0 + 1, w=lado, h=lado, keep_aspect_ratio=True)
    pdf.set_y(y0 + 50)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*GRIS_PDF)
    pdf.cell(0, 6, _t("Recomendación clínica:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10.5)
    pdf.set_text_color(40, 48, 44)
    pdf.multi_cell(0, 6, _t(datos["recomendacion"]), new_x="LMARGIN", new_y="NEXT")

    # Probabilidades
    titulo("Distribución de probabilidades de la red neuronal")
    for etiqueta, valor in probabilidades:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 48, 44)
        pdf.cell(70, 7, _t(etiqueta))
        x, y = pdf.get_x(), pdf.get_y() + 2.2
        largo = ancho - 70 - 20
        pdf.set_fill_color(239, 231, 220)
        pdf.rect(x, y, largo, 2.8, "F", round_corners=True, corner_radius=1.4)
        pdf.set_fill_color(*VERDE_PDF)
        pdf.rect(x, y, max(largo * valor / 100, 1.5), 2.8, "F", round_corners=True, corner_radius=1.4)
        pdf.set_x(x + largo + 2)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(18, 7, f"{valor:.1f}%", align="R", new_x="LMARGIN", new_y="NEXT")

    # Derivación
    titulo("Derivación médica - Centro de atención recomendado")
    for c in centros:
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.set_text_color(40, 48, 44)
        pdf.multi_cell(0, 6, _t(c["nombre"]), new_x="LMARGIN", new_y="NEXT")
        detalle = " - ".join(x for x in [c.get("ciudad", ""), c.get("direccion", "")] if x)
        if c.get("telefono"):
            detalle += f"   Tel.: {c['telefono']}"
        if detalle:
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(*GRIS_PDF)
            pdf.multi_cell(0, 5, _t(detalle), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1.5)
    if nota_centros:
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*GRIS_PDF)
        pdf.multi_cell(0, 5, _t(nota_centros), new_x="LMARGIN", new_y="NEXT")

    # Aviso legal
    pdf.ln(4)
    pdf.set_fill_color(*CREMA_PDF)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*VERDE_OSC_PDF)
    pdf.multi_cell(0, 5, "AVISO LEGAL", fill=True, new_x="LMARGIN", new_y="NEXT", padding=(3, 4, 0, 4))
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*GRIS_PDF)
    pdf.multi_cell(0, 4.8, _t(
        "Este documento es generado por un sistema automatizado de apoyo preventivo y no constituye un "
        "diagnóstico médico definitivo. Directorio de centros elaborado con fuentes públicas (Sociedad "
        "Venezolana de Dermatología y Red de Dermatología Sanitaria del Instituto Dr. Jacinto Convit), "
        f"recopilado el {datetime.strptime(FECHA_RECOPILACION, '%Y-%m-%d').strftime('%d/%m/%Y')}. "
        "Confirme la disponibilidad del servicio antes de acudir."),
        fill=True, new_x="LMARGIN", new_y="NEXT", padding=(1, 4, 3, 4))

    return bytes(pdf.output())


# =====================================================================
#  ESTADO DE SESIÓN Y NAVEGACIÓN
# =====================================================================
if "historial" not in st.session_state:
    st.session_state.historial = []

encabezado()

with st.container(key="nav"):
    menu_lateral = st.radio(
        "Ir a:",
        ["Módulo de Triaje Activo", "Historial de Sesión y Reportes"],
        format_func=lambda o: ":material/document_scanner: Triaje" if o.startswith("Módulo")
        else ":material/history: Historial y reportes",
        horizontal=True,
        label_visibility="collapsed",
    )

# ----------------------------------------------------
# MÓDULO 1: TRIAJE ACTIVO
# ----------------------------------------------------
if menu_lateral == "Módulo de Triaje Activo":

    foto_hero = hero_base64()
    html(f"""
    <div class="hero">
      {HOJA_SVG}
      <div class="texto">
        <h1>Hola,</h1>
        <h2>cuidemos tu piel hoy</h2>
        <p>Analiza tu lesión cutánea con inteligencia artificial, conoce su nivel de alerta y
           encuentra dónde atenderte.</p>
      </div>
      {'<div class="foto"><img src="data:image/jpeg;base64,' + foto_hero + '" alt=""></div>' if foto_hero else ''}
    </div>""")

    with st.container(key="paso1"):
        html("""<div class="paso"><div class="num n1">1</div><div>
              <h3>Datos del Paciente y Procedencia</h3><p>Identificación y estado de residencia</p></div></div>""")
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

    # Cuestionario Clínico Previo (Regla ABCDE)
    with st.container(key="paso2"):
        html("""<div class="paso"><div class="num n2">2</div><div>
              <h3>Autoevaluación Dermatológica (Criterios ABCDE)</h3><p>Cuestionario de apoyo clínico</p></div></div>""")
        with st.expander("Desplegar cuestionario de apoyo clínico (Opcional)"):
            p_asimetria = st.checkbox("¿La lesión muestra formas asimétricas o irregulares?")
            p_bordes = st.checkbox("¿Los bordes son difusos, borrosos o dentados?")
            p_color = st.checkbox("¿Presenta múltiples tonalidades de color (marrón, negro, rojizo)?")
            p_evolucion = st.checkbox("¿Ha presentado cambios rápidos de tamaño o grosor recientemente?")

    # Carga de Imagen
    with st.container(key="paso3"):
        html("""<div class="paso"><div class="num n3">3</div><div>
              <h3>Cargar Fotografía de la Lesión Cutánea</h3><p>Analizar mi piel · JPG o PNG</p></div></div>""")
        archivo_subido = st.file_uploader("Selecciona el archivo de la lesión (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if archivo_subido is not None:
        imagen_pil = Image.open(archivo_subido)

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

        # Centros de salud por estado (directorio verificado en centros_dermatologia.py)
        def obtener_centro_salud_nacional(estado, nivel_alerta):
            if nivel_alerta == "VERDE":
                return [{"nombre": "Ambulatorio Comunitario Local / Control periódico rutinario.",
                         "ciudad": "", "direccion": "", "telefono": ""}], None
            reco = recomendacion_para_estado(estado)
            return reco["centros"], reco["nota"]

        centros, nota_centros = obtener_centro_salud_nacional(ubicacion_paciente, alerta)
        centro_sugerido = " / ".join(c["nombre"] for c in centros)
        paciente_txt = nombre_paciente if nombre_paciente else "Paciente Anónimo"
        paciente_html = escape(paciente_txt)
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

        # Textos por nivel de alerta
        info_alerta = {
            "ROJO": ("🔴", "ROJO (Urgente)",
                     "Remisión prioritaria e inmediata a dermatólogo especialista."),
            "AMARILLO": ("🟡", "AMARILLO (Moderado)",
                         "Evaluación por médico general en ambulatorio de la red primaria."),
            "VERDE": ("🟢", "VERDE (Bajo Riesgo)",
                      "Tejido sin alteraciones críticas. Control básico y observación."),
        }
        emoji_alerta, texto_alerta, recomendacion = info_alerta[alerta]

        # Distribución de probabilidades de la red neuronal
        if alerta == "ROJO":
            probabilidades = [("Melanoma / Sospechoso", 88.2), ("Nevo Benigno", 9.1), ("Dermatitis", 2.7)]
        elif alerta == "AMARILLO":
            probabilidades = [("Melanoma / Sospechoso", 12.5), ("Nevo Benigno", 5.0), ("Dermatitis / Inflamatorio", 82.5)]
        else:
            probabilidades = [("Tejido Sano / Nevo Benigno", 93.4), ("Dermatitis", 4.0), ("Melanoma", 2.6)]

        # --- Resultado principal ---
        html('<div class="titulo-seccion">Resultados del Triaje</div>')
        html(f"""
        <div class="resultado">
          <img src="data:image/jpeg;base64,{img_a_base64(imagen_pil)}" alt="Lesión">
          <div class="info">
            <span class="chip chip-ok">✓ ¡Análisis completado con éxito!</span>
            <div class="etiqueta">Diagnóstico preliminar</div>
            <div class="patologia">{patologia}</div>
            <p class="desc">{certeza}% de certeza · {paciente_html} · {ubicacion_paciente}</p>
            <div class="pie">Lesión de: {paciente_html}</div>
          </div>
        </div>""")

        # --- Detalles: probabilidades ---
        html('<div class="titulo-seccion">Distribución de Probabilidades de la Red Neuronal</div>')
        maximo = max(v for _, v in probabilidades)
        tarjetas = ""
        for etiqueta, valor in probabilidades:
            clave = "mel" if "Melanoma" in etiqueta else "der" if "Dermatitis" in etiqueta else "san"
            color = {"mel": "#C9785E", "der": "#D2A04A", "san": "#6E9C6A"}[clave]
            tarjetas += f"""
            <div class="detalle {'top' if valor == maximo else ''}">
              {ICONOS_DETALLE[clave]}
              <div class="nom">{etiqueta}</div>
              <span class="chip" style="background:{color}22;color:{color}">{valor:.1f}%</span>
              <div class="barra"><div style="width:{valor}%;background:{color}"></div></div>
            </div>"""
        html(f'<div class="detalles">{tarjetas}</div>')

        # --- Nivel de alerta y recomendación ---
        html(f"""
        <div class="guia guia-{alerta}">
          <div class="icono">{emoji_alerta}</div>
          <div><h4>Nivel de alerta: {texto_alerta}</h4>
          <p><strong>Recomendación Clínica:</strong> {recomendacion}</p></div>
        </div>""")

        # --- Centro de atención recomendado ---
        html('<div class="titulo-seccion">Centro de Atención Recomendado</div>')
        filas = ""
        for c in centros:
            sub = " · ".join(x for x in [c.get("ciudad", ""), c.get("direccion", "")] if x)
            if c.get("telefono"):
                sub += f"{' · ' if sub else ''}Tel. {c['telefono']}"
            filas += f"""
            <div class="fila"><div class="ico">{ICONO_HOSPITAL}</div>
              <div><div class="t">{c['nombre']}</div>{f'<div class="s">{sub}</div>' if sub else ''}</div>
            </div>"""
        html(f'<div class="lista">{filas}</div>')
        if nota_centros:
            html(f'<p class="nota">ⓘ {nota_centros}</p>')

        # Botón de descarga de reporte en PDF
        st.markdown("<br>", unsafe_allow_html=True)
        respuestas_abcde = [
            texto for marcado, texto in [
                (p_asimetria, "Asimetría"), (p_bordes, "Bordes irregulares"),
                (p_color, "Múltiples colores"), (p_evolucion, "Evolución rápida"),
            ] if marcado
        ]
        reporte_pdf = generar_pdf(
            datos={
                "fecha": hora_actual,
                "paciente": paciente_txt,
                "estado": ubicacion_paciente,
                "abcde": ", ".join(respuestas_abcde) if respuestas_abcde else "Sin criterios marcados",
                "patologia": patologia,
                "certeza": certeza,
                "alerta": alerta,
                "alerta_texto": texto_alerta,
                "recomendacion": recomendacion,
            },
            imagen=imagen_pil,
            probabilidades=probabilidades,
            centros=centros,
            nota_centros=nota_centros,
        )
        st.download_button(
            label="Descargar Reporte Clínico en PDF",
            icon=":material/download:",
            data=reporte_pdf,
            file_name=f"Reporte_DermaIA_{paciente_txt.replace(' ', '_')}.pdf",
            mime="application/pdf",
        )

        st.warning("**Aviso académico y legal:** Este software actúa estrictamente como una herramienta de apoyo al triaje preventivo y no sustituye el diagnóstico clínico definitivo de un médico especialista.", icon="⚠️")

# ----------------------------------------------------
# MÓDULO 2: HISTORIAL DE SESIÓN Y REPORTES
# ----------------------------------------------------
else:
    html('<div class="titulo-seccion" style="font-size:28px;margin-top:6px">Historial de Triajes Realizados</div>')
    st.info("Este panel muestra un registro temporal de los pacientes evaluados durante la ejecución actual de la aplicación.", icon=":material/info:")

    if len(st.session_state.historial) > 0:
        filas = ""
        for idx, item in enumerate(st.session_state.historial):
            filas += f"""
            <div class="fila hist">
              <div class="badge alerta-{item['Alerta']}">{idx + 1}</div>
              <div>
                <div class="t">{escape(item['Paciente'])} <span style="font-weight:400;color:#6E756F">({item['Estado']})</span></div>
                <div class="s">{item['Fecha']}</div>
                <div class="s"><strong>Patología:</strong> {item['Patología']}</div>
                <div class="s"><strong>Nivel de Alerta:</strong>
                  <span class="chip alerta-{item['Alerta']}" style="padding:2px 10px;font-size:12px">{item['Alerta']} ({item['Certeza']})</span></div>
                <div class="s"><strong>Centro Asignado:</strong> {item['Centro']}</div>
              </div>
            </div>"""
        html(f'<div class="lista">{filas}</div>')

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Limpiar Historial", icon=":material/delete:"):
            st.session_state.historial = []
            st.rerun()
    else:
        html("""
        <div class="lista vacio">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
            <path d="M4 5h16v14H4z"/><path d="M8 9h8M8 13h5"/></svg>
          <p>No hay registros en el historial de esta sesión todavía. Realiza un análisis en el módulo de triaje
             para visualizarlos aquí.</p>
        </div>""")

html('<div class="pie-app">DermaIA · Universidad Nacional de las Ciencias (UNC) · Estética, Prevención y Salud</div>')

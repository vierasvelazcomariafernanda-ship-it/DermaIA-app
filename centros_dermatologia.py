"""
Centros de atención dermatológica en Venezuela, agrupados por estado.

Recopilado el 2026-11-11 a partir de fuentes públicas:
  [SVD]    Sociedad Venezolana de Dermatología Médica, Quirúrgica y Estética
           https://www.svderma.org/sociedad/servicios
  [CONVIT] Red Nacional de Dermatología Sanitaria - Instituto de Biomedicina "Dr. Jacinto Convit"
           https://www.jacintoconvit.org.ve/red-dermatologica/
  [MPPS]   Ministerio del Poder Popular para la Salud (nota de prensa)
  [INSALUD] Instituto de Salud de Carabobo (nota de prensa)
  [SJD]    Hospital San Juan de Dios Caracas (web oficial)

IMPORTANTE: ninguna de estas fuentes trae fecha de actualización. Los teléfonos
y responsables pueden haber cambiado. Confirmar antes de mostrarlos como definitivos.

Campo "verificacion":
  "directorio"  -> aparece en el directorio oficial de SVD o de la Red Convit
  "prensa"      -> confirmado por nota de prensa oficial (MPPS / gobernación)
  "referencia"  -> no se encontró servicio confirmado en el estado; se indica a dónde
                   acudir/consultar para ser referido
"""

FECHA_RECOPILACION = "2026-11-11"

FUENTES = {
    "SVD": "https://www.svderma.org/sociedad/servicios",
    "CONVIT": "https://www.jacintoconvit.org.ve/red-dermatologica/",
    "MPPS": "https://mpps.gob.ve/servicio-de-dermatologia-del-hcm-garantizo-atencion-gratuita-a-mas-de-4-mil-pacientes-en-el-primer-semestre-del-ano/",
    "INSALUD": "https://insalud.gob.ve/?p=9321",
    "SJD": "https://hospitalcaracas.sanjuandedios.com.ve/nuestros-servicios/consulta-externa/dermatologia/",
}

ESTADOS = [
    "Amazonas", "Anzoátegui", "Apure", "Aragua", "Barinas", "Bolívar", "Carabobo",
    "Cojedes", "Delta Amacuro", "Distrito Capital", "Falcón", "Guárico", "La Guaira",
    "Lara", "Mérida", "Miranda", "Monagas", "Nueva Esparta", "Portuguesa", "Sucre",
    "Táchira", "Trujillo", "Yaracuy", "Zulia",
]

# Centro nacional de referencia (para estados sin servicio verificado)
REFERENCIA_NACIONAL = {
    "nombre": 'Instituto de Biomedicina "Dr. Jacinto Convit" - Hospital Vargas de Caracas',
    "ciudad": "Caracas",
    "direccion": "Monte Carmelo a Providencia, San José, Caracas",
    "telefono": "",
    "tipo": "Público - centro nacional de referencia",
    "fuente": "SVD",
}

CENTROS = [
    # ---------------- Distrito Capital ----------------
    {"estado": "Distrito Capital", "ciudad": "Caracas",
     "nombre": "Hospital Universitario de Caracas - Servicio de Dermatología",
     "direccion": "Piso 8, Ciudad Universitaria UCV, Los Chaguaramos",
     "telefono": "", "tipo": "Público", "fuente": "SVD", "verificacion": "directorio"},
    {"estado": "Distrito Capital", "ciudad": "Caracas",
     "nombre": 'Hospital Vargas de Caracas - Instituto de Biomedicina "Dr. Jacinto Convit"',
     "direccion": "Monte Carmelo a Providencia, San José",
     "telefono": "", "tipo": "Público", "fuente": "SVD", "verificacion": "directorio"},
    {"estado": "Distrito Capital", "ciudad": "Caracas",
     "nombre": 'Hospital Militar "Dr. Carlos Arvelo" - Dermatología',
     "direccion": "Piso 2, Av. José Ángel Lamas, Parroquia San Juan",
     "telefono": "", "tipo": "Público (militar)", "fuente": "SVD", "verificacion": "directorio"},
    {"estado": "Distrito Capital", "ciudad": "Caracas",
     "nombre": 'Hospital de Niños "J.M. de los Ríos" - Dermatología pediátrica',
     "direccion": "Torre Pérez Guanipa, Av. Vollmer, Torre de Consulta Externa piso 4",
     "telefono": "", "tipo": "Público (pediátrico)", "fuente": "SVD", "verificacion": "directorio"},
    {"estado": "Distrito Capital", "ciudad": "Caracas",
     "nombre": "Hospital San Juan de Dios - Consulta de Dermatología",
     "direccion": "",
     "telefono": "", "tipo": "Privado sin fines de lucro", "fuente": "SJD", "verificacion": "directorio"},

    # ---------------- Anzoátegui ----------------
    {"estado": "Anzoátegui", "ciudad": "Barcelona",
     "nombre": 'Hospital Universitario "Dr. Luis Razetti" - Servicio de Dermatología',
     "direccion": "Consulta externa, Edificio de Inmunología 1er piso (frente a Central de Citas)",
     "telefono": "0416-4805665", "tipo": "Público", "fuente": "SVD, CONVIT", "verificacion": "directorio"},

    # ---------------- Aragua ----------------
    {"estado": "Aragua", "ciudad": "Maracay",
     "nombre": "Hospital Central de Maracay - Servicio de Dermatología",
     "direccion": "",
     "telefono": "", "tipo": "Público", "fuente": "MPPS", "verificacion": "prensa"},

    # ---------------- Barinas ----------------
    {"estado": "Barinas", "ciudad": "Barinas",
     "nombre": "Servicio de Salud Pública - Dermatología Sanitaria",
     "direccion": "Calle Miranda con San Luis",
     "telefono": "0414-5692208 / 0414-5670460", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Bolívar ----------------
    {"estado": "Bolívar", "ciudad": "Ciudad Bolívar",
     "nombre": "Módulo El Perú - Servicio de Dermatología Sanitaria",
     "direccion": "Urbanización El Perú, Módulo El Perú, 1er piso",
     "telefono": "0424-9163691", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Carabobo ----------------
    {"estado": "Carabobo", "ciudad": "Valencia",
     "nombre": "Ciudad Hospitalaria Dr. Enrique Tejera (CHET) - Servicio de Dermatología",
     "direccion": "",
     "telefono": "", "tipo": "Público", "fuente": "INSALUD", "verificacion": "prensa"},
    {"estado": "Carabobo", "ciudad": "Naguanagua",
     "nombre": "Hospital Rafael González Plaza - Dermatología Sanitaria",
     "direccion": "Bárbula, Naguanagua",
     "telefono": "0241-9894924 / 0414-0407270", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Cojedes ----------------
    {"estado": "Cojedes", "ciudad": "San Carlos",
     "nombre": "Ambulatorio Augusto Malavé Villalba - Dermatología Sanitaria",
     "direccion": 'Av. Ricaurte, al lado de la Ferretería San Rafael "La Morena"',
     "telefono": "0426-5445424", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Guárico ----------------
    {"estado": "Guárico", "ciudad": "San Juan de los Morros",
     "nombre": "Hospital Israel Ranuárez Balza - Servicio de Dermatología",
     "direccion": "Módulo 1",
     "telefono": "0414-1460560 / 0424-3034030", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},
    {"estado": "Guárico", "ciudad": "Calabozo",
     "nombre": "Hospital Francisco Torrealba - Dermatología Sanitaria",
     "direccion": "Calle Libertad con Sixto Sosa",
     "telefono": "0416-6433041", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},
    {"estado": "Guárico", "ciudad": "Zaraza",
     "nombre": "Dermatología Sanitaria Zaraza",
     "direccion": "",
     "telefono": "0412-4102325", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Mérida ----------------
    {"estado": "Mérida", "ciudad": "Mérida",
     "nombre": "Hospital Universitario de Los Andes (IAHULA) - Dermatología Sanitaria",
     "direccion": "",
     "telefono": "0274-2521160 / 0274-2403233", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Miranda ----------------
    {"estado": "Miranda", "ciudad": "San José de Barlovento",
     "nombre": "Distrito Sanitario N° 5 - Servicio de Dermatología",
     "direccion": "Final Av. Bolívar con calle La Línea",
     "telefono": "0414-3995091 / 0426-8045045", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Monagas ----------------
    {"estado": "Monagas", "ciudad": "Maturín",
     "nombre": "Hospital General José Antonio Serres - Servicio de Dermatología",
     "direccion": "Zona Industrial Las Cocuizas",
     "telefono": "0424-9588792", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Portuguesa ----------------
    {"estado": "Portuguesa", "ciudad": "Guanare",
     "nombre": "Servicio de Dermatología Sanitaria Guanare",
     "direccion": "Av. Mariscal Sucre, entrada al Aeropuerto",
     "telefono": "0257-2517565 / 0426-4528700", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},
    {"estado": "Portuguesa", "ciudad": "Biscucuy",
     "nombre": "Ambulatorio Diego Briceño - Servicio de Dermatología",
     "direccion": "",
     "telefono": "0426-4528700", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Sucre ----------------
    {"estado": "Sucre", "ciudad": "Cumaná",
     "nombre": "Ambulatorio Arquímedes Serrano - Servicio de Dermatología",
     "direccion": "Av. Perimetral",
     "telefono": "0412-9412911 / 0414-8391125", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},
    {"estado": "Sucre", "ciudad": "Carúpano",
     "nombre": "Hospital de Carúpano - Servicio de Dermatología",
     "direccion": "Av. Universitaria",
     "telefono": "0294-4052768", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Trujillo ----------------
    {"estado": "Trujillo", "ciudad": "Valera",
     "nombre": "Hospital Central Pedro Emilio Carrillo - Dermatología Sanitaria",
     "direccion": "Al lado de Traumatología",
     "telefono": "0416-8714946 / 0424-7241476", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},
    {"estado": "Trujillo", "ciudad": "Trujillo",
     "nombre": "Unidad Sanitaria - Servicio de Dermatología",
     "direccion": "Piso 1, frente al Hospital José Gregorio Hernández",
     "telefono": "0414-7238206", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},
    {"estado": "Trujillo", "ciudad": "Boconó",
     "nombre": "Unidad Sanitaria - Dermatología Sanitaria",
     "direccion": "Av. Rotaria cruce con Av. Los Leones",
     "telefono": "0414-0796591 / 0416-0781593", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Yaracuy ----------------
    {"estado": "Yaracuy", "ciudad": "San Felipe",
     "nombre": "Servicio de Dermatología Sanitaria San Felipe",
     "direccion": "Av. La Patria entre 3ra y 4ta Avenida",
     "telefono": "0414-5466115 / 0412-6928177", "tipo": "Público", "fuente": "CONVIT", "verificacion": "directorio"},

    # ---------------- Zulia ----------------
    {"estado": "Zulia", "ciudad": "Maracaibo",
     "nombre": "Servicio Autónomo Hospital Universitario de Maracaibo (SAHUM) - Dermatología",
     "direccion": "Av. 16 Guajira, vía a Ziruma, frente al antiguo Rectorado LUZ",
     "telefono": "", "tipo": "Público", "fuente": "SVD", "verificacion": "directorio"},
    {"estado": "Zulia", "ciudad": "Maracaibo",
     "nombre": 'Hospital Militar de Maracaibo "Dr. Francisco Valbuena" - Dermatología',
     "direccion": "PB, Av. Fuerzas Armadas, al lado del Colegio Los Robles",
     "telefono": "", "tipo": "Público (militar)", "fuente": "SVD", "verificacion": "directorio"},
]

# Estados sin servicio de dermatología confirmado en las fuentes consultadas.
# Se sugiere al paciente acudir al hospital central del estado o a la Dirección
# Regional de Salud para ser referido.
#   Amazonas y Delta Amacuro: según la Red Convit, los cubren las "Unidades para el
#   control y la investigación de las enfermedades endémicas".
SIN_SERVICIO_VERIFICADO = {
    "Amazonas": "Hospital Dr. José Gregorio Hernández (Puerto Ayacucho) o Unidad de control de enfermedades endémicas",
    "Apure": "Hospital Dr. Pablo Acosta Ortiz (San Fernando de Apure)",
    "Delta Amacuro": "Hospital Dr. Luis Razetti (Tucupita) o Unidad de control de enfermedades endémicas",
    "Falcón": "Hospital Universitario Dr. Alfredo Van Grieken (Coro)",
    "La Guaira": "Dirección Regional de Salud de La Guaira o centros de Distrito Capital",
    "Lara": "Hospital Central Universitario Dr. Antonio María Pineda (Barquisimeto)",
    "Nueva Esparta": "Hospital Dr. Luis Ortega (Porlamar)",
    "Táchira": "Hospital Central de San Cristóbal",
}

NOTA_CONFIRMAR = "Servicio de dermatología no confirmado en fuentes públicas: confirme la consulta antes de acudir."


def _normalizar_estado(estado: str) -> str:
    # La app usa "Distrito Capital (Caracas)"
    return estado.split(" (")[0].strip()


def centros_por_estado(estado: str) -> list[dict]:
    """Centros verificados del estado (lista vacía si no hay)."""
    estado = _normalizar_estado(estado)
    return [c for c in CENTROS if c["estado"] == estado]


def recomendacion_para_estado(estado: str) -> dict:
    """
    Devuelve lo que se debe mostrar al paciente (app o PDF):
      {"centros": [...], "nota": str | None, "referencia_nacional": dict}
    """
    centros = centros_por_estado(estado)
    nota = None
    if not centros:
        est = _normalizar_estado(estado)
        nombre = SIN_SERVICIO_VERIFICADO.get(
            est, "Hospital central o Centro de Diagnóstico Integral (CDI) principal de la región"
        )
        centros = [{"estado": est, "ciudad": "", "nombre": nombre, "direccion": "",
                    "telefono": "", "tipo": "Público", "fuente": "", "verificacion": "referencia"}]
        nota = NOTA_CONFIRMAR
    return {"centros": centros, "nota": nota, "referencia_nacional": REFERENCIA_NACIONAL}


if __name__ == "__main__":
    import csv, sys
    out = sys.argv[1] if len(sys.argv) > 1 else "centros_dermatologia.csv"
    campos = ["estado", "ciudad", "nombre", "direccion", "telefono", "tipo", "fuente", "verificacion"]
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(CENTROS)
        for est, nota in SIN_SERVICIO_VERIFICADO.items():
            w.writerow({"estado": est, "nombre": nota, "verificacion": "referencia"})
    con = {c["estado"] for c in CENTROS}
    print(f"{len(CENTROS)} centros en {len(con)} estados; "
          f"{len(SIN_SERVICIO_VERIFICADO)} estados sin servicio verificado -> {out}")
    faltan = set(ESTADOS) - con - set(SIN_SERVICIO_VERIFICADO)
    print("Estados sin cubrir:", faltan or "ninguno")

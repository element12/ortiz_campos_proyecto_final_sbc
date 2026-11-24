PREDICADOS = {
    "Incendio": "El incidente involucra fuego",
    "Estructural": "El fuego afecta una estructura",
    "Forestal": "El fuego afecta vegetación o terreno forestal",
    "HumoIntenso": "Se observa humo intenso",
    "PersonaAtrapada": "Hay una persona reportada como atrapada",
    "RiesgoElectrico": "Hay equipos o líneas eléctricas energizadas en riesgo",
    "VientoCambiante": "El viento es cambiante",
    "PropagacionRapida": "Se observa propagación rápida del fuego",
    "RutaEscapeComprometida": "La ruta de escape está comprometida",
    "RecursosInsuficientes": "Los recursos presentes no parecen suficientes",
}

CONCLUSIONES = {
    "EvaluarRiesgos": "Evaluar los riesgos y las condiciones de la escena antes de actuar.",
    "ReevaluarEstrategia": "Reevaluar la estrategia de atención según las condiciones.",
    "PriorizarRescate": "Priorizar la evaluación de un rescate seguro.",
    "EvitarIngreso": "Evitar el ingreso mientras existan condiciones no controladas.",
    "SolicitarApoyo": "Solicitar apoyo adicional (personal, máquinas o recursos).",
    "EstablecerMando": "Confirmar el mando del incidente y las comunicaciones.",
    "CoordinarCorteEnergia": "Coordinar el corte de energía con la empresa de servicio.",
    "RescateCondicionado": "Hacer el rescate solo cuando el riesgo esté controlado o desde el exterior.",
    "ReubicarPersonal": "Reubicar al personal en una zona segura y buscar otra ruta de escape.",
}


def crear_regla(nombre, descripcion, condiciones, conclusion, certeza):

    if not 0 <= certeza <= 1:
        raise ValueError("La certeza debe estar entre 0 y 1.")

    return {
        "nombre": nombre,
        "descripcion": descripcion,
        "condiciones": condiciones,
        "conclusion": conclusion,
        "certeza": certeza,
    }


def formula_logica(regla):

    partes = [condicion + "(i)" for condicion in regla["condiciones"]]

    if len(partes) == 1:
        antecedente = partes[0]
    else:
        antecedente = "(" + " ∧ ".join(partes) + ")"

    return "∀i [" + antecedente + " → " + regla["conclusion"] + "(i)]"


REGLAS = [
    crear_regla("R1", "Incendio estructural",
                ["Incendio", "Estructural"], "EvaluarRiesgos", 0.95),
    crear_regla("R2", "Incendio forestal",
                ["Incendio", "Forestal"], "ReevaluarEstrategia", 0.90),
    crear_regla("R3", "Humo intenso",
                ["HumoIntenso"], "EvaluarRiesgos", 0.90),

    crear_regla("R4", "Persona atrapada",
                ["PersonaAtrapada"], "PriorizarRescate", 0.99),
    crear_regla("R5", "Riesgo eléctrico",
                ["RiesgoElectrico"], "EvitarIngreso", 0.99),
    crear_regla("R6", "Ruta de escape comprometida",
                ["RutaEscapeComprometida"], "EvitarIngreso", 0.99),
    crear_regla("R7", "Corte de energía",
                ["RiesgoElectrico"], "CoordinarCorteEnergia", 0.95),

    crear_regla("R8", "Propagación rápida",
                ["PropagacionRapida"], "SolicitarApoyo", 0.95),
    crear_regla("R9", "Recursos insuficientes",
                ["RecursosInsuficientes"], "SolicitarApoyo", 0.95),
    crear_regla("R10", "Viento cambiante",
                ["VientoCambiante"], "ReevaluarEstrategia", 0.90),

    crear_regla("R11", "Evaluación de riesgos y mando",
                ["EvaluarRiesgos"], "EstablecerMando", 0.90),
    crear_regla("R12", "Solicitud de apoyo y reevaluación",
                ["SolicitarApoyo"], "ReevaluarEstrategia", 0.90),
    crear_regla("R13", "Rescate sin poder ingresar",
                ["PriorizarRescate", "EvitarIngreso"], "RescateCondicionado", 0.90),
    crear_regla("R14", "Forestal con viento y sin ruta de escape",
                ["Forestal", "VientoCambiante", "RutaEscapeComprometida"],
                "ReubicarPersonal", 0.95),
]

CATEGORIAS = {
    "Identificación y evaluación de riesgos": ["R1", "R2", "R3"],
    "Seguridad y rescate": ["R4", "R5", "R6", "R7"],
    "Propagación y solicitud de apoyo": ["R8", "R9", "R10"],
    "Coordinación y seguimiento": ["R11", "R12", "R13", "R14"],
}

from datetime import datetime

from base_conocimiento import REGLAS, formula_logica
from motor_inferencia import (
    encadenamiento_adelante,
    explicar_razonamiento,
    porque,
    calcular_certezas,
    validar_hechos,
)
from textos import HECHOS_SIMPLES, ACCIONES_SIMPLES, EJEMPLOS


def nivel_confianza(certeza):
    if certeza >= 0.97:
        return "Muy segura"
    if certeza >= 0.93:
        return "Segura"
    return "Bastante segura"


def causas(conclusion, hechos_iniciales, reglas_aplicadas):
    if conclusion in hechos_iniciales:
        return {conclusion}
    encontradas = set()
    for regla in reglas_aplicadas:
        if regla["conclusion"] == conclusion:
            for condicion in regla["condiciones"]:
                encontradas |= causas(condicion, hechos_iniciales, reglas_aplicadas)
    return encontradas


def ordenar_acciones(certezas):
    prioridad = list(ACCIONES_SIMPLES)
    return sorted(certezas, key=lambda c: (-certezas[c], prioridad.index(c)))


def crear_informe(hechos_iniciales, reglas_aplicadas, certezas, orden):
    partes = [
        "INFORME DE EVALUACIÓN INICIAL DE INCENDIO",
        "Fecha: " + datetime.now().strftime("%d/%m/%Y %H:%M"),
        "",
        "Si hay fuego, llame a la línea 123.",
        "",
        "1. LO QUE SE OBSERVÓ",
    ]
    for hecho in HECHOS_SIMPLES:
        if hecho in hechos_iniciales:
            partes.append(f"   - {HECHOS_SIMPLES[hecho][0]} ({hecho})")

    partes += ["", "2. QUÉ HACER (en orden)"]
    if len(orden) == 0:
        partes.append("   Con lo observado no fue posible dar una recomendación.")
    for numero, conclusion in enumerate(orden, start=1):
        titulo, detalle = ACCIONES_SIMPLES[conclusion]
        partes.append(f"   {numero}. {titulo}")
        partes.append(f"      {detalle}")
        partes.append(f"      Confianza: {nivel_confianza(certezas[conclusion])} "
                      f"({certezas[conclusion]:.0%})")

    partes += ["", "3. POR QUÉ SE RECOMIENDA CADA ACCIÓN"]
    for conclusion in orden:
        partes.append(f"   {ACCIONES_SIMPLES[conclusion][0]} ({conclusion}):")
        for renglon in porque(conclusion, hechos_iniciales, reglas_aplicadas).splitlines():
            partes.append("      " + renglon)

    partes += ["", "4. REGLAS APLICADAS (encadenamiento hacia adelante)"]
    for renglon in explicar_razonamiento(reglas_aplicadas).splitlines():
        partes.append("   " + renglon)

    partes += ["", "5. REGLAS EN LÓGICA DE PREDICADOS"]
    for regla in reglas_aplicadas:
        partes.append(f"   {regla['nombre']}: {formula_logica(regla)}")
    if len(reglas_aplicadas) == 0:
        partes.append("   Ninguna.")

    return "\n".join(partes)


def obtener_datos():
    hechos = [
        {"id": hecho, "titulo": titulo, "explicacion": explicacion,
         "gif": f"gifs/{hecho}.gif"}
        for hecho, (titulo, explicacion) in HECHOS_SIMPLES.items()
    ]
    ejemplos = [{"nombre": nombre, "hechos": lista} for nombre, lista in EJEMPLOS.items()]
    return {"hechos": hechos, "ejemplos": ejemplos}


def evaluar(lista_hechos):
    hechos_iniciales = set(lista_hechos)

    if len(hechos_iniciales) == 0:
        return {"error": "Marque al menos una casilla para continuar."}

    try:
        validar_hechos(hechos_iniciales)
    except ValueError as error:
        return {"error": str(error)}

    hechos_finales, reglas_aplicadas = encadenamiento_adelante(REGLAS, hechos_iniciales)
    certezas = calcular_certezas(reglas_aplicadas)
    orden = ordenar_acciones(certezas)

    acciones = []
    for conclusion in orden:
        titulo, detalle = ACCIONES_SIMPLES[conclusion]
        origen = causas(conclusion, hechos_iniciales, reglas_aplicadas)
        acciones.append({
            "id": conclusion,
            "titulo": titulo,
            "detalle": detalle,
            "certeza": certezas[conclusion],
            "nivel": nivel_confianza(certezas[conclusion]),
            "gif": f"gifs/accion_{conclusion}.gif",
            "causas": [HECHOS_SIMPLES[h][0] for h in HECHOS_SIMPLES if h in origen],
        })

    return {
        "acciones": acciones,
        "informe": crear_informe(hechos_iniciales, reglas_aplicadas, certezas, orden),
    }

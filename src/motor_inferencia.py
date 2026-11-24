import logging

from base_conocimiento import REGLAS, PREDICADOS

logging.basicConfig(level=logging.INFO, format="%(message)s")

MAX_ITERACIONES = 50

def se_cumple(regla, hechos):
    return all(
        condicion in hechos
        for condicion in regla["condiciones"]
    )


def validar_hechos(hechos_iniciales):
    for hecho in hechos_iniciales:
        if hecho not in PREDICADOS:
            raise ValueError(f"El hecho '{hecho}' no existe en la base de conocimiento.")


def encadenamiento_adelante(base_conocimiento, hechos_iniciales):

    hechos = set(hechos_iniciales)
    reglas_aplicadas = []
    ya_usadas = []
    iteracion = 0
    hubo_cambios = True

    logging.info(f"Hechos iniciales: {sorted(hechos)}")

    while hubo_cambios:
        iteracion += 1
        hubo_cambios = False

        if iteracion > MAX_ITERACIONES:
            logging.warning("Se alcanzó el límite de iteraciones. Puede haber un ciclo.")
            break

        for regla in base_conocimiento:
            if regla["nombre"] in ya_usadas:
                continue

            if se_cumple(regla, hechos):
                hechos.add(regla["conclusion"])
                reglas_aplicadas.append(regla)
                ya_usadas.append(regla["nombre"])
                hubo_cambios = True
                logging.info(f"Iteración {iteracion}: se activa {regla['nombre']} "
                             f"-> {regla['conclusion']}")

    if len(reglas_aplicadas) == 0:
        logging.info("No se activó ninguna regla.")

    return hechos, reglas_aplicadas


def calcular_certezas(reglas_aplicadas):
    certezas = {}

    for regla in reglas_aplicadas:
        conclusion = regla["conclusion"]
        if conclusion not in certezas or regla["certeza"] > certezas[conclusion]:
            certezas[conclusion] = regla["certeza"]

    return certezas


def explicar_razonamiento(reglas_aplicadas):
    if len(reglas_aplicadas) == 0:
        return "No se activó ninguna regla. Con estos hechos no se puede dar una recomendación."

    texto = ""
    conclusiones_vistas = []

    for paso, regla in enumerate(reglas_aplicadas, start=1):
        condiciones = " Y ".join(regla["condiciones"])
        texto += (f"{paso}. {regla['nombre']} ({regla['descripcion']}): "
                  f"SI {condiciones} ENTONCES {regla['conclusion']} "
                  f"(certeza {regla['certeza']})")

        if regla["conclusion"] in conclusiones_vistas:
            texto += " - confirma una conclusión anterior"

        conclusiones_vistas.append(regla["conclusion"])
        texto += "\n"

    return texto


def porque(conclusion, hechos_iniciales, reglas_aplicadas, nivel=0):
    
    sangria = "    " * nivel

    if conclusion in hechos_iniciales:
        return f"{sangria}- {conclusion}: hecho inicial\n"

    reglas_origen = [r for r in reglas_aplicadas if r["conclusion"] == conclusion]

    if len(reglas_origen) == 0:
        return f"{sangria}- {conclusion}: no se pudo deducir con los hechos ingresados\n"

    texto = ""
    for regla in reglas_origen:
        texto += (f"{sangria}- {conclusion}: por la regla {regla['nombre']} "
                  f"({regla['descripcion']})\n")

        for condicion in regla["condiciones"]:
            texto += porque(condicion, hechos_iniciales, reglas_aplicadas, nivel + 1)

    return texto


if __name__ == "__main__":
    hechos_iniciales = {"Incendio", "RiesgoElectrico", "PersonaAtrapada", "HumoIntenso"}

    hechos_finales, reglas_aplicadas = encadenamiento_adelante(REGLAS, hechos_iniciales)

    print("\nHECHOS Y CONCLUSIONES FINALES:")
    print(", ".join(sorted(hechos_finales)))

    print("\nCERTEZAS:")
    print(calcular_certezas(reglas_aplicadas))

    print("\nEXPLICACIÓN DEL RAZONAMIENTO:")
    print(explicar_razonamiento(reglas_aplicadas))

    print("¿POR QUÉ SE RECOMIENDA UN RESCATE CONDICIONADO?")
    print(porque("RescateCondicionado", hechos_iniciales, reglas_aplicadas))

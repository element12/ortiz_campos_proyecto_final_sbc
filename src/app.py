import streamlit as st

from base_conocimiento import PREDICADOS, CONCLUSIONES, REGLAS, CATEGORIAS, formula_logica
from motor_inferencia import (
    encadenamiento_adelante,
    explicar_razonamiento,
    porque,
    calcular_certezas,
    validar_hechos,
)

CASOS = {
    "Caso 1 - Incendio estructural":
        ["Incendio", "Estructural", "HumoIntenso", "PropagacionRapida"],
    "Caso 2 - Incendio forestal":
        ["Incendio", "Forestal", "VientoCambiante", "RutaEscapeComprometida",
         "RecursosInsuficientes"],
    "Caso 3 - Riesgo eléctrico y rescate":
        ["Incendio", "RiesgoElectrico", "PersonaAtrapada", "HumoIntenso"],
    "Caso 4 - Sin conclusión":
        ["Incendio"],
    "Caso 5 - Emergencia compleja":
        ["Incendio", "Estructural", "HumoIntenso", "PersonaAtrapada",
         "RiesgoElectrico", "PropagacionRapida", "RecursosInsuficientes"],
    "Caso 6 - Prueba caso 2":
            ["Incendio", "Forestal", "HumoIntenso", "PersonaAtrapada",
            "PropagacionRapida", "RecursosInsuficientes", "VientoCambiante"],
}


def cargar_caso():
    hechos_del_caso = CASOS.get(st.session_state["caso"], [])
    for hecho in PREDICADOS:
        st.session_state[hecho] = hecho in hechos_del_caso
    st.session_state["resultado"] = None


def limpiar():
    for hecho in PREDICADOS:
        st.session_state[hecho] = False
    st.session_state["caso"] = "Ninguno"
    st.session_state["resultado"] = None


st.set_page_config(page_title="Evaluación inicial de incendios")

if "resultado" not in st.session_state:
    st.session_state["resultado"] = None

st.title("Evaluación inicial de incendios")
st.write("Marque lo que observa en la escena y presione Evaluar.")

st.selectbox("Cargar un caso de prueba", ["Ninguno"] + list(CASOS.keys()),
             key="caso", on_change=cargar_caso)

st.subheader("Hechos observados")

lista_hechos = list(PREDICADOS.items())
mitad = (len(lista_hechos) + 1) // 2
columna_1, columna_2 = st.columns(2)

for posicion, (hecho, texto) in enumerate(lista_hechos):
    if posicion < mitad:
        columna_1.checkbox(texto, key=hecho)
    else:
        columna_2.checkbox(texto, key=hecho)

boton_1, boton_2 = st.columns(2)
evaluar = boton_1.button("Evaluar", type="primary", width="stretch")
boton_2.button("Limpiar", on_click=limpiar, width="stretch")

if evaluar:
    hechos_iniciales = {h for h in PREDICADOS if st.session_state.get(h)}

    if len(hechos_iniciales) == 0:
        st.error("Debe marcar al menos un hecho.")
        st.session_state["resultado"] = None
    else:
        try:
            validar_hechos(hechos_iniciales)
            with st.spinner("Evaluando..."):
                hechos_finales, reglas_aplicadas = encadenamiento_adelante(
                    REGLAS, hechos_iniciales
                )
            st.session_state["resultado"] = (hechos_iniciales, reglas_aplicadas)
        except ValueError as error:
            st.error(str(error))

if st.session_state["resultado"] is not None:
    hechos_iniciales, reglas_aplicadas = st.session_state["resultado"]
    certezas = calcular_certezas(reglas_aplicadas)

    st.subheader("Recomendaciones")

    if len(certezas) == 0:
        st.warning("No se pudo llegar a ninguna recomendación. "
                   "Agregue más información de la escena.")
    else:
        st.success(f"Se encontraron {len(certezas)} recomendaciones.")

        for conclusion in sorted(certezas, key=certezas.get, reverse=True):
            with st.container(border=True):
                st.write(f"**{CONCLUSIONES[conclusion]}**")
                st.progress(certezas[conclusion],
                            text=f"Certeza: {certezas[conclusion]:.0%}")
                with st.expander("¿Por qué?"):
                    st.text(porque(conclusion, hechos_iniciales, reglas_aplicadas))

    st.subheader("Reglas aplicadas")
    st.text(explicar_razonamiento(reglas_aplicadas))

st.divider()

with st.expander("Ver las reglas del sistema"):
    for categoria, nombres in CATEGORIAS.items():
        st.write(f"**{categoria}**")
        for regla in REGLAS:
            if regla["nombre"] in nombres:
                st.write(f"{regla['nombre']} - {regla['descripcion']} "
                         f"(certeza {regla['certeza']})")
                st.code(formula_logica(regla), language=None)

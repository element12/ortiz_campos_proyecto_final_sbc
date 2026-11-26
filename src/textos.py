HECHOS_SIMPLES = {
    "Incendio": ("Hay fuego",
                 "Se ven llamas en el lugar."),
    "Estructural": ("Se quema una construcción",
                    "Lo que arde es una casa, edificio, bodega u otra construcción."),
    "Forestal": ("Se quema vegetación",
                 "Lo que arde es pasto, árboles o monte."),
    "HumoIntenso": ("Hay mucho humo",
                    "Sale mucho humo oscuro y cuesta ver o respirar."),
    "PersonaAtrapada": ("Alguien no puede salir",
                        "Una persona quedó adentro y no puede salir por su cuenta."),
    "RiesgoElectrico": ("Hay electricidad cerca del fuego",
                        "Hay cables de luz, postes o aparatos eléctricos cerca de las llamas."),
    "VientoCambiante": ("El viento cambia de dirección",
                        "El viento sopla hacia un lado y luego hacia otro, y mueve el fuego."),
    "PropagacionRapida": ("El fuego crece rápido",
                          "En pocos minutos las llamas se hacen más grandes y llegan a nuevos lugares."),
    "RutaEscapeComprometida": ("La salida está bloqueada",
                               "La puerta o el camino para salir tiene fuego o está cerrado."),
    "RecursosInsuficientes": ("Las personas que hay no alcanzan",
                              "El fuego es más grande de lo que pueden apagar las personas "
                              "y equipos que ya están ahí. Hace falta que llegue más gente."),
}

ACCIONES_SIMPLES = {
    "PriorizarRescate": ("Avise que hay alguien atrapado",
                         "Al llamar al 123, diga primero que hay una persona atrapada "
                         "y en qué lugar está. Es lo más urgente."),
    "EvitarIngreso": ("No entre al lugar",
                      "Aunque quiera ayudar, entrar puede costarle la vida. Quédese afuera."),
    "ReubicarPersonal": ("Aléjese a un lugar seguro",
                         "Muévase lejos del fuego y del humo, y busque otro camino "
                         "si la salida está bloqueada."),
    "SolicitarApoyo": ("Llame al 123 y pida ayuda",
                       "Cuente lo que ve: si el fuego crece rápido o si hay pocas "
                       "personas para ayudar."),
    "CoordinarCorteEnergia": ("No toque cables y avise que hay electricidad",
                              "No eche agua cerca de cables. Al llamar, diga que hay "
                              "riesgo eléctrico para que corten la luz."),
    "RescateCondicionado": ("No intente sacar a la persona usted mismo",
                            "Háblele desde afuera para calmarla y dígale que la ayuda "
                            "ya viene. El rescate lo hacen los bomberos."),
    "EvaluarRiesgos": ("Mire bien antes de acercarse",
                       "Fíjese en el humo, los cables y por dónde puede salir. "
                       "Si tiene dudas, no se acerque."),
    "EstablecerMando": ("Que una sola persona hable con los bomberos",
                        "Pónganse de acuerdo: una persona da la información y las "
                        "demás siguen sus indicaciones."),
    "ReevaluarEstrategia": ("Esté atento a los cambios",
                            "Si el viento cambia o el fuego crece, aléjese más y "
                            "vuelva a llamar para avisar."),
}

EJEMPLOS = {
    "Ejemplo 1: incendio en un edificio":
        ["Incendio", "Estructural", "HumoIntenso", "PropagacionRapida"],
    "Ejemplo 2: incendio en el monte":
        ["Incendio", "Forestal", "VientoCambiante", "RutaEscapeComprometida",
         "RecursosInsuficientes"],
    "Ejemplo 3: cables eléctricos y una persona atrapada":
        ["Incendio", "RiesgoElectrico", "PersonaAtrapada", "HumoIntenso"],
    "Ejemplo 4: solo se ve fuego":
        ["Incendio"],
    "Ejemplo 5: emergencia grande":
        ["Incendio", "Estructural", "HumoIntenso", "PersonaAtrapada",
         "RiesgoElectrico", "PropagacionRapida", "RecursosInsuficientes"],
    "Ejemplo 6: incendio en el monte con una persona atrapada":
        ["Incendio", "Forestal", "HumoIntenso", "PersonaAtrapada",
         "PropagacionRapida", "RecursosInsuficientes", "VientoCambiante"],
}

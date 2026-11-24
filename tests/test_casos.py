import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from base_conocimiento import REGLAS, PREDICADOS
from motor_inferencia import (encadenamiento_adelante, calcular_certezas,
                              explicar_razonamiento, porque, validar_hechos)

CASOS = [
    ("Caso 1 - Incendio estructural",
     {"Incendio", "Estructural", "HumoIntenso", "PropagacionRapida"},
     ["R1", "R3", "R8", "R11", "R12"],
     {"EvaluarRiesgos", "SolicitarApoyo", "EstablecerMando", "ReevaluarEstrategia"}),

    ("Caso 2 - Incendio forestal",
     {"Incendio", "Forestal", "VientoCambiante", "RutaEscapeComprometida",
      "RecursosInsuficientes"},
     ["R2", "R6", "R9", "R10", "R12", "R14"],
     {"ReevaluarEstrategia", "EvitarIngreso", "SolicitarApoyo", "ReubicarPersonal"}),

    ("Caso 3 - Riesgo eléctrico y rescate",
     {"Incendio", "RiesgoElectrico", "PersonaAtrapada", "HumoIntenso"},
     ["R3", "R4", "R5", "R7", "R11", "R13"],
     {"EvaluarRiesgos", "PriorizarRescate", "EvitarIngreso",
      "CoordinarCorteEnergia", "EstablecerMando", "RescateCondicionado"}),

    ("Caso 4 - Sin conclusión",
     {"Incendio"},
     [],
     set()),

    ("Caso 5 - Emergencia compleja",
     {"Incendio", "Estructural", "HumoIntenso", "PersonaAtrapada",
      "RiesgoElectrico", "PropagacionRapida", "RecursosInsuficientes"},
     ["R1", "R3", "R4", "R5", "R7", "R8", "R9", "R11", "R12", "R13"],
     {"EvaluarRiesgos", "PriorizarRescate", "EvitarIngreso", "CoordinarCorteEnergia",
      "SolicitarApoyo", "EstablecerMando", "ReevaluarEstrategia", "RescateCondicionado"}),
]


class PruebasCasos(unittest.TestCase):

    def test_cinco_casos(self):
        for nombre, hechos, reglas_esperadas, conclusiones_esperadas in CASOS:
            hechos_finales, reglas_aplicadas = encadenamiento_adelante(REGLAS, hechos)
            reglas = [regla["nombre"] for regla in reglas_aplicadas]
            conclusiones = hechos_finales - hechos

            self.assertEqual(reglas, reglas_esperadas, nombre)
            self.assertEqual(conclusiones, conclusiones_esperadas, nombre)


class PruebasDeBorde(unittest.TestCase):

    def test_hay_14_reglas(self):
        self.assertEqual(len(REGLAS), 14)

    def test_sin_hechos(self):
        hechos_finales, reglas_aplicadas = encadenamiento_adelante(REGLAS, set())
        self.assertEqual(reglas_aplicadas, [])
        self.assertIn("No se activó ninguna regla", explicar_razonamiento(reglas_aplicadas))

    def test_hecho_que_no_existe(self):
        with self.assertRaises(ValueError):
            validar_hechos({"Incendio", "Inundacion"})

    def test_todos_los_hechos(self):
        hechos_finales, reglas_aplicadas = encadenamiento_adelante(REGLAS, set(PREDICADOS))
        self.assertEqual(len(reglas_aplicadas), 14)

    def test_estructural_sin_incendio(self):
        hechos_finales, reglas_aplicadas = encadenamiento_adelante(REGLAS, {"Estructural"})
        self.assertEqual(reglas_aplicadas, [])

    def test_certeza_mas_alta(self):
        hechos_finales, reglas_aplicadas = encadenamiento_adelante(REGLAS, CASOS[0][1])
        certezas = calcular_certezas(reglas_aplicadas)
        self.assertEqual(certezas["EvaluarRiesgos"], 0.95)

    def test_ciclo(self):
        reglas_ciclo = [
            {"nombre": "C1", "descripcion": "", "condiciones": ["A"],
             "conclusion": "B", "certeza": 1.0},
            {"nombre": "C2", "descripcion": "", "condiciones": ["B"],
             "conclusion": "A", "certeza": 1.0},
        ]
        hechos_finales, reglas_aplicadas = encadenamiento_adelante(reglas_ciclo, {"A"})
        self.assertEqual(hechos_finales, {"A", "B"})

    def test_porque_no_deducido(self):
        texto = porque("ReubicarPersonal", {"Incendio"}, [])
        self.assertIn("no se pudo deducir", texto)

    def test_porque_llega_a_hechos_iniciales(self):
        hechos = CASOS[2][1]
        hechos_finales, reglas_aplicadas = encadenamiento_adelante(REGLAS, hechos)
        texto = porque("RescateCondicionado", hechos, reglas_aplicadas)
        self.assertIn("R13", texto)
        self.assertIn("PersonaAtrapada: hecho inicial", texto)


if __name__ == "__main__":
    unittest.main()

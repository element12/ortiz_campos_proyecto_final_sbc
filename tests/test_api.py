import logging
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import app

logging.disable(logging.CRITICAL)


class PruebasApi(unittest.TestCase):

    def setUp(self):
        self.cliente = app.test_client()

    def test_pagina_principal(self):
        respuesta = self.cliente.get("/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b"id=\"app\"", respuesta.data)
        respuesta.close()

    def test_datos(self):
        datos = self.cliente.get("/api/datos").get_json()
        self.assertEqual(len(datos["hechos"]), 10)
        self.assertEqual(len(datos["ejemplos"]), 6)

    def test_gifs_existen(self):
        datos = self.cliente.get("/api/datos").get_json()
        for hecho in datos["hechos"]:
            respuesta = self.cliente.get("/" + hecho["gif"])
            self.assertEqual(respuesta.status_code, 200, hecho["gif"])
            respuesta.close()

    def test_evaluar_caso_3(self):
        hechos = ["Incendio", "RiesgoElectrico", "PersonaAtrapada", "HumoIntenso"]
        datos = self.cliente.post("/api/evaluar", json={"hechos": hechos}).get_json()
        ids = [accion["id"] for accion in datos["acciones"]]
        self.assertEqual(len(ids), 6)
        self.assertEqual(ids[0], "PriorizarRescate")
        self.assertIn("R13", datos["informe"])
        self.assertIn("∀i", datos["informe"])

    def test_sin_hechos(self):
        respuesta = self.cliente.post("/api/evaluar", json={"hechos": []})
        self.assertEqual(respuesta.status_code, 400)

    def test_hecho_invalido(self):
        respuesta = self.cliente.post("/api/evaluar", json={"hechos": ["Inundacion"]})
        self.assertEqual(respuesta.status_code, 400)

    def test_sin_recomendacion(self):
        datos = self.cliente.post("/api/evaluar", json={"hechos": ["Incendio"]}).get_json()
        self.assertEqual(datos["acciones"], [])


if __name__ == "__main__":
    unittest.main()

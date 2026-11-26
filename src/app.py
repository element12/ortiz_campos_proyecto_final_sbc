import os

from flask import Flask, jsonify, request

import servicio

app = Flask(__name__, static_folder="static", static_url_path="")


@app.get("/")
def inicio():
    return app.send_static_file("index.html")


@app.get("/api/datos")
def datos():
    return jsonify(servicio.obtener_datos())


@app.post("/api/evaluar")
def evaluar():
    cuerpo = request.get_json(silent=True) or {}
    resultado = servicio.evaluar(cuerpo.get("hechos", []))

    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado)


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    print(f"Abra http://localhost:{puerto} en el navegador")
    app.run(port=puerto)

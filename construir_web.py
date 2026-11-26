import os
import shutil

RAIZ = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(RAIZ, "src")
DESTINO = os.path.join(RAIZ, "web")
ARCHIVOS_PYTHON = ["base_conocimiento.py", "motor_inferencia.py", "textos.py", "servicio.py"]

if os.path.exists(DESTINO):
    shutil.rmtree(DESTINO)

shutil.copytree(os.path.join(SRC, "static"), DESTINO)
os.makedirs(os.path.join(DESTINO, "py"))
for archivo in ARCHIVOS_PYTHON:
    shutil.copy(os.path.join(SRC, archivo), os.path.join(DESTINO, "py", archivo))

print("Versión estática lista en:", DESTINO)

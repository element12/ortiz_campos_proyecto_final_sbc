# Sistema experto: evaluación inicial de incendios

Proyecto final de **Inteligencia Artificial II**, Fundación Universitaria Los Libertadores.

**Autor:** Jeisson Steven Ortiz Campos· 

## Descripción

Sistema basado en conocimiento con interfaz web. Apoya la **evaluación inicial de un incendio**: el usuario marca lo que observa en la escena (tipo de incendio, personas atrapadas, riesgo eléctrico, viento, recursos…) y el sistema:

- aplica **14 reglas de producción** con **encadenamiento hacia adelante**;
- genera recomendaciones accionables, cada una con su **factor de certeza**;
- explica el razonamiento: muestra las reglas aplicadas en orden y tiene un botón **"¿Por qué?"** para cada conclusión.

## Estructura

```
├── README.md
├── requirements.txt
├── src/
│   ├── base_conocimiento.py   # Predicados, conclusiones y 14 reglas
│   ├── motor_inferencia.py    # Encadenamiento adelante, explicación, porque()
│   └── app.py                 # Interfaz web (Streamlit)
├── tests/
│   ├── casos_prueba.md        # Tabla de los 5 casos y casos de borde
│   └── test_casos.py          # Pruebas automáticas
└── docs/
    ├── documentacion_tecnica.pdf
    └── manual_usuario.pdf
```

## Instalación

Requisitos: **Python 3.10 o superior**.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

```powershell
streamlit run src/app.py
```

La aplicación se abre en `http://localhost:8501`.

Para probar solo el motor desde la consola:

```powershell
python src/motor_inferencia.py
```

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

Se prueban los 5 casos documentados y los casos de borde: sin hechos, hecho que no existe, todos los hechos, ciclos, entre otros.

## Cómo agregar una regla

1. En `src/base_conocimiento.py`, agrega una línea a `REGLAS` con `crear_regla("R15", "descripción", ["Condicion1", "Condicion2"], "Conclusion", 0.90)`.
2. Agrega el nombre de la regla a una de las listas de `CATEGORIAS`.
3. Si la conclusión es nueva, agrégala a `CONCLUSIONES` con el texto que verá el usuario.
4. Si usa un hecho de entrada nuevo, agrégalo a `PREDICADOS`. La casilla aparece sola en la interfaz.


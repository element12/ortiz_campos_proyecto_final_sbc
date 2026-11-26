# Sistema experto: evaluación inicial de incendios

Proyecto final de **Inteligencia Artificial II**, Fundación Universitaria Los Libertadores.

**Autor:** Jeisson Steven Ortiz Campos· 

## Descripción

Sistema basado en conocimiento con interfaz web, pensado para personas que **no saben nada de bomberos**. En 3 pasos, el usuario marca lo que ve en el lugar (cada situación tiene un GIF animado que la explica) y el sistema:

- aplica **14 reglas de producción** con **encadenamiento hacia adelante**;
- muestra las acciones a seguir en orden, en lenguaje sencillo, cada una con su **nivel de confianza**;
- explica por qué recomienda cada acción;
- permite **descargar un informe** con el razonamiento completo: la función `porque`, las reglas aplicadas y las fórmulas en lógica de predicados.

## Arquitectura

- **Backend:** Python con Flask (`src/app.py`). Expone una API JSON que usa el motor de inferencia.
- **Frontend:** Vue 3 y Bootstrap 5 (`src/static/`). Se cargan desde CDN, así que no hay que instalar Node ni compilar nada.

| Ruta | Método | Qué hace |
|---|---|---|
| `/` | GET | Página web |
| `/api/datos` | GET | Situaciones, textos, GIF y ejemplos |
| `/api/evaluar` | POST | Recibe `{"hechos": [...]}` y devuelve las acciones y el informe |

## Estructura

```
├── README.md
├── requirements.txt
├── src/
│   ├── base_conocimiento.py   # Predicados, conclusiones y 14 reglas
│   ├── motor_inferencia.py    # Encadenamiento adelante, explicación, porque()
│   ├── textos.py              # Textos sencillos para el usuario final
│   ├── servicio.py            # Lógica de la aplicación (sirve a Flask y a Pyodide)
│   ├── app.py                 # Backend Flask (API)
│   └── static/
│       ├── index.html         # Frontend Vue 3 + Bootstrap 5
│       ├── app.js             # Lógica de la interfaz (Vue)
│       ├── estilos.css
│       └── gifs/              # GIF animados de situaciones y acciones
├── tests/
│   ├── casos_prueba.md        # Tabla de los 5 casos y casos de borde
│   ├── test_casos.py          # Pruebas del motor
│   └── test_api.py            # Pruebas de la API
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
python src/app.py
```

Luego abra `http://localhost:5000` en el navegador. Se necesita internet para cargar Vue, Bootstrap y la tipografía desde el CDN.

Para probar solo el motor desde la consola:

```powershell
python src/motor_inferencia.py
```

## Versión publicada

La aplicación está en línea en **https://incendios.bomberosmadridb31.com**.

El hosting web compartido no ejecuta Python, así que la versión publicada es estática: el mismo código Python (`base_conocimiento.py`, `motor_inferencia.py`, `textos.py` y `servicio.py`) se ejecuta en el navegador con **Pyodide**. El frontend detecta si hay un backend Flask: si lo hay, usa la API; si no, carga Python en el navegador.

Para generar la versión estática:

```powershell
python construir_web.py
```

Esto crea la carpeta `web/`, lista para subir al hosting. Para probarla en local:

```powershell
python -m http.server 5600 --directory web
```

### Actualizar la versión publicada en Hostinger

Cada vez que se cambie algo en `src/`, hay que volver a publicar:

1. Generar la versión estática:

   ```powershell
   python construir_web.py
   ```

2. Comprimir el **contenido** de `web/` (no la carpeta):

   ```powershell
   Compress-Archive -Path web\* -DestinationPath incendios.zip -Force
   ```

3. En [hPanel](https://hpanel.hostinger.com), ir a **Sitios web** → **bomberosmadridb31.com** → **Administrador de archivos** y abrir la carpeta `public_html/incendios`.
4. Subir `incendios.zip`, hacer clic derecho → **Extraer** y aceptar reemplazar los archivos.
5. Borrar `incendios.zip` del servidor para que no quede descargable.
6. Abrir https://incendios.bomberosmadridb31.com y recargar con **Ctrl + F5**.

> Trabaje solo dentro de `public_html/incendios`. Subir o extraer archivos directamente en `public_html` puede dañar el sitio principal.

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

Se prueban los 5 casos documentados, los casos de borde (sin hechos, hecho que no existe, todos los hechos, ciclos, entre otros) y la API: datos, evaluación, errores y GIF.

## Cómo agregar una regla

1. En `src/base_conocimiento.py`, agrega una línea a `REGLAS` con `crear_regla("R15", "descripción", ["Condicion1", "Condicion2"], "Conclusion", 0.90)`.
2. Agrega el nombre de la regla a una de las listas de `CATEGORIAS`.
3. Si la conclusión es nueva, agrégala a `CONCLUSIONES` y, en `src/textos.py`, a `ACCIONES_SIMPLES` con el texto para el usuario. Agrega también su GIF en `src/static/gifs/accion_<Conclusion>.gif`.
4. Si usa un hecho de entrada nuevo, agrégalo a `PREDICADOS`, a `HECHOS_SIMPLES` y su GIF en `src/static/gifs/<Hecho>.gif`. La tarjeta aparece sola en la interfaz.


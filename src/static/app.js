const { createApp } = Vue;

const ARCHIVOS_PYTHON = ["base_conocimiento.py", "motor_inferencia.py", "textos.py", "servicio.py"];
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";

const backend = {
  modo: "servidor",
  python: null,

  async iniciar() {
    try {
      const respuesta = await fetch("api/datos");
      const tipo = respuesta.headers.get("content-type") || "";
      if (respuesta.ok && tipo.includes("json")) return;
    } catch (error) {}

    this.modo = "navegador";
    await new Promise((listo, fallo) => {
      const script = document.createElement("script");
      script.src = PYODIDE;
      script.onload = listo;
      script.onerror = fallo;
      document.head.appendChild(script);
    });
    this.python = await loadPyodide();
    for (const archivo of ARCHIVOS_PYTHON) {
      const codigo = await (await fetch("py/" + archivo)).text();
      this.python.FS.writeFile(archivo, codigo);
    }
    this.python.runPython("import json, servicio");
  },

  async datos() {
    if (this.modo === "servidor") {
      return (await fetch("api/datos")).json();
    }
    return JSON.parse(this.python.runPython("json.dumps(servicio.obtener_datos())"));
  },

  async evaluar(hechos) {
    if (this.modo === "servidor") {
      const respuesta = await fetch("api/evaluar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hechos }),
      });
      return respuesta.json();
    }
    this.python.globals.set("hechos_js", JSON.stringify(hechos));
    return JSON.parse(this.python.runPython("json.dumps(servicio.evaluar(json.loads(hechos_js)))"));
  },
};

createApp({
  data() {
    return {
      pasos: ["Lo que ve", "Revisar", "Qué hacer"],
      paso: 1,
      hechos: [],
      ejemplos: [],
      ejemplo: "",
      marcados: [],
      acciones: [],
      informe: "",
      aviso: "",
      cargando: false,
      iniciando: true,
      errorCarga: "",
      abiertos: [],
    };
  },

  computed: {
    hechosMarcados() {
      return this.hechos.filter((h) => this.marcados.includes(h.id));
    },
  },

  async mounted() {
    try {
      await backend.iniciar();
      const datos = await backend.datos();
      this.hechos = datos.hechos;
      this.ejemplos = datos.ejemplos;
    } catch (error) {
      this.errorCarga = "No se pudo cargar el sistema. Revise su conexión a internet y recargue la página.";
    }
    this.iniciando = false;
  },

  methods: {
    estadoPaso(numero) {
      if (numero < this.paso) return "hecho";
      if (numero === this.paso) return "actual";
      return "pendiente";
    },

    irArriba() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    },

    cargarEjemplo() {
      const elegido = this.ejemplos.find((e) => e.nombre === this.ejemplo);
      this.marcados = elegido ? [...elegido.hechos] : [];
      this.aviso = "";
      this.irArriba();
    },

    siguiente() {
      if (this.marcados.length === 0) {
        this.aviso = "Marque al menos una casilla para continuar.";
        return;
      }
      this.aviso = "";
      this.paso = 2;
      this.irArriba();
    },

    atras() {
      this.paso = 1;
      this.irArriba();
    },

    async evaluar() {
      this.cargando = true;
      const datos = await backend.evaluar(this.marcados);
      this.cargando = false;

      if (datos.error) {
        this.aviso = datos.error;
        this.paso = 1;
        return;
      }
      this.acciones = datos.acciones;
      this.informe = datos.informe;
      this.abiertos = [];
      this.paso = 3;
      this.irArriba();
    },

    porcentaje(certeza) {
      return Math.round(certeza * 100) + "%";
    },

    alternarPorque(id) {
      if (this.abiertos.includes(id)) {
        this.abiertos = this.abiertos.filter((a) => a !== id);
      } else {
        this.abiertos.push(id);
      }
    },

    descargarInforme() {
      const archivo = new Blob(["﻿" + this.informe], { type: "text/plain;charset=utf-8" });
      const enlace = document.createElement("a");
      enlace.href = URL.createObjectURL(archivo);
      enlace.download = "informe_incendio.txt";
      enlace.click();
      URL.revokeObjectURL(enlace.href);
    },

    empezarDeNuevo() {
      this.marcados = [];
      this.ejemplo = "";
      this.acciones = [];
      this.informe = "";
      this.paso = 1;
      this.irArriba();
    },
  },
}).mount("#app");

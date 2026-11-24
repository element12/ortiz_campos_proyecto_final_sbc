# Casos de prueba

Para correr las pruebas automáticas:

```
python -m unittest discover -s tests -v
```

`R3*` quiere decir que la regla se activó, pero su conclusión ya había salido antes con otra regla. Es decir, la regla confirma esa conclusión. Cuando varias reglas llegan a la misma conclusión, se toma la certeza más alta.

## Tabla de casos

| Caso | Descripción | Hechos iniciales | Reglas esperadas | Conclusión esperada | Resultado obtenido | Estado |
|---|---|---|---|---|---|---|
| 1 | Incendio estructural con humo y propagación rápida | Incendio, Estructural, HumoIntenso, PropagacionRapida | R1, R3*, R8, R11, R12 | EvaluarRiesgos, SolicitarApoyo, EstablecerMando, ReevaluarEstrategia | EvaluarRiesgos (0.95), SolicitarApoyo (0.95), EstablecerMando (0.90), ReevaluarEstrategia (0.90) | ✓ |
| 2 | Incendio forestal con viento cambiante, ruta de escape comprometida y pocos recursos | Incendio, Forestal, VientoCambiante, RutaEscapeComprometida, RecursosInsuficientes | R2, R6, R9, R10*, R12*, R14 | ReevaluarEstrategia, EvitarIngreso, SolicitarApoyo, ReubicarPersonal | EvitarIngreso (0.99), SolicitarApoyo (0.95), ReubicarPersonal (0.95), ReevaluarEstrategia (0.90) | ✓ |
| 3 | Riesgo eléctrico, persona atrapada y humo | Incendio, RiesgoElectrico, PersonaAtrapada, HumoIntenso | R3, R4, R5, R7, R11, R13 | EvaluarRiesgos, PriorizarRescate, EvitarIngreso, CoordinarCorteEnergia, EstablecerMando, RescateCondicionado | PriorizarRescate (0.99), EvitarIngreso (0.99), CoordinarCorteEnergia (0.95), EvaluarRiesgos (0.90), EstablecerMando (0.90), RescateCondicionado (0.90) | ✓ |
| 4 | Sin conclusión: solo se sabe que hay fuego | Incendio | Ninguna | Ninguna | No se activó ninguna regla | ✓ |
| 5 | Emergencia compleja que activa la mayoría de reglas | Incendio, Estructural, HumoIntenso, PersonaAtrapada, RiesgoElectrico, PropagacionRapida, RecursosInsuficientes | R1, R3*, R4, R5, R7, R8, R9*, R11, R12, R13 (10 de 14) | EvaluarRiesgos, PriorizarRescate, EvitarIngreso, CoordinarCorteEnergia, SolicitarApoyo, EstablecerMando, ReevaluarEstrategia, RescateCondicionado | Las 8 conclusiones esperadas | ✓ |

## Casos de borde

| Caso | Entrada | Qué debe pasar | Estado |
|---|---|---|---|
| B1 | Ningún hecho marcado | No se activa ninguna regla y la interfaz pide marcar un hecho | ✓ |
| B2 | Un hecho que no existe (`Inundacion`) | `validar_hechos` muestra un error | ✓ |
| B3 | Los 10 hechos marcados | Se activan las 14 reglas | ✓ |
| B4 | `Estructural` sin `Incendio` | R1 no se activa porque le falta una condición | ✓ |
| B5 | Reglas con ciclo A → B → A | El motor termina, porque cada regla se activa una sola vez y hay un límite de iteraciones | ✓ |
| B6 | Preguntar `porque()` por algo que no se dedujo | Responde "no se pudo deducir" | ✓ |

## Análisis

- **Caso 1:** EvaluarRiesgos sale de dos reglas (R1 y R3), y la explicación muestra las dos.
- **Caso 2:** ReevaluarEstrategia sale de tres reglas (R2, R10 y R12). La R14 detecta la situación más peligrosa del incendio forestal.
- **Caso 3:** muestra el encadenamiento. R4 y R5 producen las condiciones que necesita R13.
- **Caso 4:** el sistema no da recomendaciones cuando no hay información suficiente.
- **Caso 5:** se activan 10 de las 14 reglas. Las que faltan (R2, R6, R10 y R14) se prueban en el Caso 2.

# Cámara: cómo se mueve y por qué
La cámara es lo que da profundidad y lo que guía la mirada. Regla madre (Ayrton): **cámara de película, siempre al servicio de que se entienda.** Vocabulario con ejemplos por segundo: `GLOSARIO-EDICION.md`. Cómo se escribe en código: `docs/5-tecnica/THREEJS.md`. Recetas medidas en las referencias: `docs/4-referencias/CATALOGO-MOVIMIENTOS.md`.

## El modelo: un set, estaciones, una cámara
- **Un solo set 3D por reel.** Cada idea del guion vive en una **estación** (un lugar del espacio con sus objetos).
- Las estaciones se ordenan **en diagonal hacia un lado y al fondo** (por defecto: izquierda y atrás; p. ej. A (0, 0, 0) · B (−1,8, 0, −3,5) · C (−3,6, 0, −7)). Así todos los viajes van en la **misma dirección** (la "corriente" del reel) y se usa el eje z.
- **Una cámara continua** las recorre: plano secuencia, sin cortes. El único corte es al CTA.
- Cada reel elige **su propio recorrido** (otra corriente, otras alturas, otro orden de ángulos): no calcar el anterior.

## Las 9 reglas
1. **Mover solo cuando cambia la idea.** Un movimiento por concepto nuevo (≈ 1,5 a 5 movimientos notorios cada 10 s; en la práctica, uno cada 3–6 s).
2. **Quieta cuando se nombra.** Mientras la voz nombra un objeto, la cámara está **inmóvil** (≥ 1,5 s) y el objeto entero y legible. La quietud es lo que lo resalta. En una retención **no hay** push-in, flotación ni deriva.
3. **Viajes rápidos, retenciones largas.** Un viaje entre estaciones dura **0,8–0,9 s** (pico 800–3000 px/s). Al menos el 25 % de los cuadros del reel están quietos.
4. **Plano general para relacionar.** Cuando la idea es "esto y esto van juntos", la cámara sube y se aleja hasta verlos juntos y retiene ≥ 2,5 s.
5. **Variar el ángulo.** No llegar a todas las estaciones de frente: alternar frontal, tres cuartos, **picado** (desde arriba: muestra el conjunto) y **contrapicado** (desde abajo: agranda, da importancia). No terminar dos planos seguidos igual.
6. **Nunca desenfocar ni recortar lo que se explica.** El acercamiento no puede dejar cortado un objeto que hay que leer.
7. **Lo que no se nombró todavía no distrae.** Los objetos de la estación siguiente aparecen cuando la cámara viaja hacia ellos (`E.pop`), no asoman detrás del texto.
8. **Temblor solo al aterrizar.** Chiquito (0,006 m) y decreciente, al llegar a una estación. Nunca en una pausa.
9. **Las metas son una alarma, no un objetivo** (`docs/4-referencias/metas.json`). Si el ojo dice que confunde, gana el ojo.

**Actualización 11-17 (Ayrton):** las referencias de Instagram que más le gustan (9 reels medidos en `docs/4-referencias/material/2026-11-17-refs-instagram-dinamismo/`) mueven la cámara en el 69–88 % de los cuadros. Por eso la regla 2 ("quieta cuando se nombra") se relaja: en una retención hay **deriva orbital lenta** (≈ 10° y 8 % de acercamiento, < 100 px/s) que no mueve el texto de lugar; los viajes siguen siendo rápidos. Ver el recurso en `videos/2026-11-python-variables/assets/set.js` (`orb`).

## Planos y movimientos: recetas
Posiciones relativas a la estación, en metros (objeto de ≈ 0,3–0,5 m apoyado en el piso). `p` = dónde está la cámara, `l` = a dónde mira. Son puntos de partida: confirmar con `python engine/reel.py encuadre` y con los cuadros.
| Plano / ángulo | `p` (x, y, z) | `l` | Para qué |
|---|---|---|---|
| Medio en tres cuartos, leve picado (portada) | (1,7 · 1,6 · 3,0) | (0 · 0,6 · 0) | presentar el objeto protagonista |
| Medio frontal | (0,3 · 0,4 · 1,3) | (0 · 0,03 · 0) | leer una pantalla o un objeto chico |
| Contrapicado | (0,8 · 0,2 · 2,3) | (0 · 0,02 · 0) | darle importancia a un objeto |
| Picado | (−0,5 · 2,2 · 3,4) | (0 · 0,6 · 0) | varias cosas apiladas o en fila |
| Detalle | a 1,6–1,7 m del punto, misma altura | el punto | una parte chica (un cuadradito, un puerto) |
| General en picado | 5–11 m arriba y 8–10 m atrás | un punto bajo el centro del set | todas las estaciones juntas |

Truco de encuadre: **mirar a un punto más bajo sube el objeto en pantalla** (lo saca de la franja de subtítulos); alejar la cámara lo achica.

| Movimiento | Duración | Curva (`e`) | Cuándo | Sonido |
|---|---|---|---|---|
| **Travelling** entre estaciones | 0,8–0,9 s | `io` | cambia la idea | `P.viaje(t)` en la mitad del viaje |
| **Dolly in** (acercarse) | 0,5–1,2 s | `io` u `out` | "mirá este detalle" | viaje corto o `zoom-click` |
| **Dolly out** (alejarse) | 0,6–0,9 s | `io` | volver al contexto | viaje suave |
| **Grúa** (subir o bajar) | 0,4–1,1 s | `in` al salir, `out` al llegar | pasar por encima; plano general | viaje largo (`d=0.9`) |
| **Push-in lento** | 2–3 s | `lin` | **solo en el gancho**, mientras se lee el título | — |
| **Retención** | ≥ 1,5 s | misma pose dos veces | la voz nombra | — |
| **Latigazo** | 0,25–0,3 s | `io` | cambio brusco de tema (raro) | whoosh corto |

Curvas: `io` arranca y frena suave (viajes) · `out` llega frenando (aterrizajes) · `in` sale acelerando · `expo` llegada con cola larga (el CTA) · `lin` constante (retención, push-in).
**Llegar lento, irse limpio**: las llegadas tienen cola; las salidas son más cortas y aceleran. Usar la misma curva y duración en todo es lo que hace que un video "se sienta generado".

## Tiempos: la cámara sigue a la voz
- El viaje **termina justo antes** de que la voz nombre lo nuevo: si la frase empieza en `tC = cuando('l03')`, el viaje va de `tC − 0,45` a `tC + 0,45` y el pico cae en `tC`.
- **Quietud antes del clímax**: 0,3–0,75 s de pausa entre la acción y el resultado.
- Lo que aparece, aparece **en la palabra** que lo nombra (`cuando('l03', 'router')`), nunca "un ratito después".
- Lectura: un rótulo queda al menos 0,5 s + 0,3 s por palabra.
- Variar: que el plano más largo dure ≥ 4 veces el más corto; no reencuadrar con el mismo intervalo cada vez (metrónomo).

## Límites entre escenas
En un plano secuencia los límites entre escenas de `video.json` no se ven: son el mismo set en tiempo continuo. Aun así:
- **El viaje cruza el límite** (empieza antes y termina después), en la dirección de la corriente.
- **Algo sobrevive**: el objeto de una estación sigue visible, más chico, mientras se llega a la siguiente; o se transforma (la fila crece a planilla, la planilla se apila en bloque).
- Se mide con `arrastre.py` (lo corre `reel.py medir`): medio ≥ 0,5; un 0,0 solo en el corte al CTA. Ojo: en medio de una grúa rápida puede dar bajo sin que haya corte.
- **Corte al CTA**: hit metálico + boom → el CTA aterriza con el chinn. Está en la plantilla.

## Significado de las direcciones (gastarlas con motivo)
| Dirección | Significa |
|---|---|
| la corriente (p. ej. izquierda y al fondo) | "lo que sigue" |
| hacia arriba (grúa) | conclusión, ver el conjunto |
| adelante (dolly in) | ir más hondo en la misma idea |
| atrás (dolly out) | contexto; algo grande aterriza |
Nunca dos viajes seguidos en direcciones opuestas (ping-pong): se lee como error.

## Señales de "video hecho por IA" (evitarlas)
Todas las llegadas iguales · todo aparece con fundido + deslizamiento hacia arriba · títulos que siguen moviéndose después de aterrizar · loops de flotar/respirar/pulsar · vacío oscuro con cositas flotando · tres tarjetas en fila · rebote en interfaz.

## Qué se mide (lo hace `python engine/reel.py medir`)
| Métrica | Rango (alarma) | Reel de referencia (tokens v2) |
|---|---|---|
| Cuadros con cámara en movimiento | 25–75 % | 38 % |
| Movimientos notorios cada 10 s | 1,5–5 | 3,2 |
| Pico de un movimiento notorio | 800–3000 px/s | 1374 |
| Retención entre movimientos | 1–4 s | 1,4 s |
| Continuidad (arrastre medio) | ≥ 0,5 | 0,61 |
| Render | ≤ 3 s por segundo de video | ≈ 2 |

## Biblioteca de movimiento (`assets/movimiento.js`)
Funciones puras del tiempo para animar **piezas** (no hace falta para la cámara, que usa `E.ruta`): `resorte`, `entra`, `popIn`, `letra`, `sale` (entradas y salidas con carácter), `impacto`, `estirar`, `temblor` (solo aterrizajes), `latigazo`, `morfar` (un rectángulo se vuelve otro), `salto`, `juntar`. Uso: `import * as M from './movimiento.js'`.

## Errores ya cometidos (no repetir)
- Mover la cámara todo el tiempo y hacer zoom de más: confunde (banco de prueba, 2026-11-15).
- Desenfocar lo que se explica.
- Un decorado que pasa por detrás del texto (la cinta de la fábrica).
- Calcar la puesta en escena del reel anterior.
- Cables que no llegan al objeto; ondas dibujadas por tramos que no empalman (la fase se calcula con la posición global: `E.onda` ya lo hace).
- Rótulos debajo del objeto: pisan los subtítulos.
- Escribir la duración de una escena dentro de su composición: al cambiar la voz, el final quedó congelado. Hoy los tiempos salen solos de `assets/tiempos.js`.

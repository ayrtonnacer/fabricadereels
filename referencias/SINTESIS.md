# Síntesis de las referencias de motion graphics

Qué se repite en los videos analizados (2026-11-09). Fuente: los cinco desgloses de esta carpeta. Es la «biblioteca» de la que se elige al armar la estructura técnica de un reel (docs/FLUJO.md, paso 3). Se amplía con cada referencia nueva.

| Video | Duración | Planos | Cortes/min | LUFS | Golpes medidos | Qué enseña |
|---|---|---|---|---|---|---|
| [Motion Templates](motion-templates-after-effects/analisis.md) | 15 s | 16 | 60 | −13,4 | 25 | cursor que dispara, tarjetas 3D con paralaje, montaje sobre el ritmo, pila de capas, silencio antes del clic |
| [Promo de marca (50 s)](pinterest-791437334567656517/analisis.md) | 50 s | 14 | 16 | −14,5 | 75 | estructura problema→solución→prueba→CTA; fondo rojo líquido; rojo↔blanco; wipe con forma de objeto |
| [Instagram strategy](motion-inspiration-frames/analisis.md) | 18 s | 15 | 47 | −14,5 | 9 | una frase por beat; oscuro/claro; una palabra en el acento; sonido escaso |
| [Nokia collage](motion-inspiration-nokia/analisis.md) | 20 s | 13 | 36 | −14,7 | 14 | cortes en la grilla del ritmo (≈125 BPM); barridos y formas como transición; disco giratorio |
| [Glitch cyber](pinterest-999095498641347187/analisis.md) | 9 s | 11 | 69 | −9,7 | 0 | POV caminando + interfaz de error; mosaico de píxeles; duotono; teselas |

## Lo que todos tienen en común
1. **Una sola idea por video** y una frase corta por beat (4–6 palabras, 1–1,5 s). Nada se explica con párrafos.
2. **El corte es la transición.** Casi ninguno usa un fundido encadenado: el cambio de color de fondo, una forma que barre, un barrido con desenfoque, un flash o un zoom a través de un objeto reemplazan al corte. (Coincide con la ley del vector de `docs/MOVIMIENTO.md`.)
3. **Ritmo rápido pero con contraste.** Planos medios de 0,8–1,5 s en los reels de 9–20 s; 3,6 s en el de 50 s. Siempre hay un tramo más largo o una pausa antes del momento clave (silencio de 0,45 s antes del clic; 3–4 s de cierre quieto).
4. **Un color de acento por video** y una palabra por frase en ese color; el resto, neutro. (Nuestra regla 2: lo que se debe recordar, en `var(--acc)`.)
5. **Objetos concretos como metáfora**: tacho, ojo, bombilla, maletín, disco, carpetas, farol. Uno por beat.
6. **Cierre legible y quieto** (≈3–4 s) con el nombre/URL, salvo el que termina abierto.
7. **Dos filosofías de sonido**: golpes frecuentes que marcan cada corte (Motion Templates, promo de marca, Nokia) y sonido escaso con un impacto por idea (Instagram strategy). El glitch usa una pista continua muy comprimida.

## Sincronía con el ritmo (medida)
- Motion Templates: golpes cada ≈0,32 s; los cortes caen a ±0,1 s de un golpe.
- Nokia: golpes cada ≈0,48 s (≈125 BPM); cortes a ±0,07 s de un golpe; planos de 2, 4 u 8 beats.
- **Regla para Claqueta:** decidir la música y su BPM ANTES del guion técnico; los `t0/t1` de las tomas y los cortes van en múltiplos del beat (a 125 BPM, un beat = 0,48 s), y los golpes de `sfx_events.py` caen en esos mismos instantes. Un reel hablado no puede llevar golpes cada 0,3 s: ahí se usa la opción «sonido escaso» (un impacto por idea) y el ritmo lo lleva la voz.

## Catálogo de transiciones observadas y cómo se hacen en Claqueta
| Transición (dónde se vio) | Qué es | En Claqueta |
|---|---|---|
| Latigazo de tarjetas / barrido con desenfoque (Templates, Nokia) | Dos planos unidos por un movimiento rápido borroso | **Hay:** `costuras` `latigazo`, `rig.transicion(i,'latigazo')` + `MotionBlur` |
| Zoom a través de un objeto (Templates P5) | Un objeto crece hasta llenar el cuadro y es la escena siguiente | **Hay:** toma `mover` con ease `entrada` + `destello`/corte |
| Flash blanco corto (Nokia 11 s, glitch) | 0,1 s de blanco en el corte | **Hay:** `destello()` de camara3d.js |
| Fundido por negro / dip (Frames, Nokia, glitch) | La imagen se oscurece antes del corte | **Hay:** `costuras` `oscuro` |
| Rack focus (Nokia) | Pico de desenfoque que tapa un corte | **Hay:** `costuras` `foco` |
| Cámara baja por una pila de capas (Templates P9) | Tilt down atravesando tarjetas en Z | **A armar:** set 3D de planos apilados + toma `mover` |
| Flip de color de fondo (promo, Frames) | Rojo↔blanco / oscuro↔claro en cada beat | **A armar:** dos fondos por tema + `salida:"corte"` |
| Iris / círculo que crece desde un punto (promo, Frames) | Un círculo lo cubre todo | **Falta:** costura `iris` (clip-path circular) |
| Wipe con la forma de un objeto o color (promo tacho, Nokia) | Una forma barre la pantalla | **Falta:** costura `forma` |
| Mosaico de píxeles / bloques desplazados / teselas (glitch) | La imagen se rompe en bloques | **Falta:** costura `glitch` / `teselas` (canvas) |
| Estallido radial (Nokia 3,6 s) | Rayos que giran + zoom | **Falta:** efecto radial (shader o abanico de planos) |
| Ola líquida blanca (promo 25–32 s) | Una ola sube y empuja | **Falta:** `clip-path` animado con curva |

## Qué agregar al motor (en orden de utilidad para reels educativos)
1. **`iris` y `forma`** (costuras): las dos más usadas y simples (clip-path). 
2. **`glitch` / `teselas`**: encajan con ciberseguridad; hacer con canvas sobre el 3D.
3. **Set de «tarjetas en pila»** para camara3d.js: cámara que recorre capas (Templates).
4. **Cuadrícula de beats**: `beats(bpm, t0)` en camara3d/costuras para que cada toma y cada golpe caigan en el beat, y que `revisar.py` avise si un corte queda a más de 0,1 s del beat.
5. **Contadores y olas** (`data-count`, `clip-path` ondulado) para cifras de un reel.
Todo esto es para ELEGIR por reel (regla de variedad de `docs/CAMARA-3D.md`), no para usar junto.

## Lo que NO sirve de estos videos para nosotros
Fotos de stock y marcas de terceros, retratos de personas, paletas ajenas (rojo/blanco, amarillo/rojo/crema, azul eléctrico), tono publicitario («Download», KPIs de marketing), formato 1:1 con barras negras (Nokia) y loudness de −9,7 LUFS que ahoga una voz.

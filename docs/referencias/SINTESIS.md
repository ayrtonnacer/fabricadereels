# Síntesis de las referencias de motion graphics

Qué se repite en los videos analizados (2026-11-09; 10 referencias). Fuente: los desgloses de esta carpeta. Es la «biblioteca» de la que se elige al armar la estructura técnica de un reel (docs/FLUJO.md, paso 3). Se amplía con cada referencia nueva.

| Video | Duración | Planos | Cortes/min | LUFS | Golpes medidos | Qué enseña |
|---|---|---|---|---|---|---|
| [Motion Templates](externos/motion-templates-after-effects/ANALISIS.md) | 15 s | 16 | 60 | −13,4 | 25 | cursor que dispara, tarjetas 3D con paralaje, montaje sobre el ritmo, pila de capas, silencio antes del clic |
| [Promo de marca (50 s)](externos/pinterest-791437334567656517/ANALISIS.md) | 50 s | 14 | 16 | −14,5 | 75 | estructura problema→solución→prueba→CTA; fondo rojo líquido; rojo↔blanco; wipe con forma de objeto |
| [Instagram strategy](externos/motion-inspiration-frames/ANALISIS.md) | 18 s | 15 | 47 | −14,5 | 9 | una frase por beat; oscuro/claro; una palabra en el acento; sonido escaso |
| [Nokia collage](externos/motion-inspiration-nokia/ANALISIS.md) | 20 s | 13 | 36 | −14,7 | 14 | cortes en la grilla del ritmo (≈125 BPM); barridos y formas como transición; disco giratorio |
| [Glitch cyber](externos/pinterest-999095498641347187/ANALISIS.md) | 9 s | 11 | 69 | −9,7 | 0 | POV caminando + interfaz de error; mosaico de píxeles; duotono; teselas |
| [Sting ilustrado](externos/motion-ref-1/ANALISIS.md) | 9 s | 8 | 45 | −14,2 | 0 | objeto portador (estrella) entre cortes; parpadeo A/B; destello como puente; color = significado |
| [Lente explosionada 3D](externos/motion-ref-2/ANALISIS.md) | 20 s (16:9) | 1 | 0 | −16,0 | 4 | **vista explosionada con etiquetas y tooltip al hover; cámara mover-retener-mover; cierre en bucle** |
| [Anuncio con tarjetas de vidrio](externos/motion-ref-3/ANALISIS.md) | 25 s | 1 | 0 | −14,2 | 6 | un solo plano continuo; texto cinético por palabra; tarjetas de vidrio 3D; contadores; silencio final |
| [Miedo y codicia](externos/motion-ref-4/ANALISIS.md) | 32 s | 6 | 10 | −14,2 | 36 | rojo/verde con significado; una palabra por tic de sonido; objeto que cruza como transición |
| [Explicador largo (agentes de IA)](externos/motion-ref-5/ANALISIS.md) | 104 s | 6 | 3 | −11,7 | 46+ | mascota-guía, tarjetas de producto, subtítulos por palabra; ejemplo de lo que hay que partir en serie |

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

## Patrones nuevos (referencias 6 a 10)
1. **Explicación técnica en 3D = vista explosionada + etiquetas + hover** (la referencia «Lente»). Es el patrón más cercano a lo que Ayrton quiere para reels técnicos: un solo plano de cámara 3D, la pieza se abre en capas a lo largo de un eje, cada parte lleva un cartel con línea guía, y una frase de definición aparece al resaltar una pieza con el cursor. La frase del tooltip es la que dice la voz. En un reel de redes, el switch o el router abiertos mostrarían puertos, controlador y memoria; en un reel de redes en capas, las capas del modelo separándose.
2. **La cámara «mueve–retiene–mueve».** En la lente: retenciones de 2 a 4 s para leer, reencuadres de 0,5 a 0,7 s con pico de velocidad ≈2,2. En los 25 s del anuncio, 7 reencuadres rápidos (pico 2,3–3,9) entre retenciones. Regla: **cada movimiento tiene un motivo (cambiar de pieza) y cada retención deja leer**; nunca movimiento constante. En Claqueta: `rig.toma` cortas con ease `suave` y `MotionBlur`, separadas por retenciones largas.
3. **Un plano continuo es posible sin cortes.** Dos de las diez referencias (lente, anuncio) no tienen un solo corte: la cámara se reencuadra y los elementos entran y salen. Ahorra transiciones y se ve más «3D».
4. **Una palabra por tic de sonido** (miedo y codicia, explicador): cada palabra del texto entra con un clic corto, y el espectador lee al ritmo del sonido. En el 4 se miden 36 tics en 25 s.
5. **Color con un solo significado** (miedo y codicia: rojo = miedo, verde = codicia; sting: azul = calma, rojo = peligro). Coincide con la regla 1 de CLAUDE.md.
6. **Un objeto portador cruza los cortes** (la estrella del sting, la cápsula de miedo y codicia, la mascota del explicador): el ojo sigue al objeto, no a la escena.
7. **Cierre en bucle** (la lente termina en el cuadro con el que empieza; el sting vuelve a un cuadro parecido al inicial).
8. **Silencio de cierre** (anuncio: 1,2 s sin música en el logo).
9. **Lo largo se parte.** El explicador de 104 s, con una sola idea por tramo, serían dos o tres reels.

## Transiciones y recursos nuevos del catálogo
| Recurso (dónde) | En Claqueta |
|---|---|
| Vista explosionada de un grupo 3D (lente) | **A armar:** grupo con piezas en posición «ensamblada» y «explosionada», `lerp` escalonado; helper `explosionar(g, t0, dur)` |
| Etiqueta con línea guía + tooltip al hover (lente) | **Hay en parte:** `cartel()` y el billboard del reel de redes; falta la línea guía y la tarjeta de dos líneas con resalte |
| Rayos/haces de luz atravesando piezas (lente) | **Hay en parte:** paquetes y tubos con `drawRange`; falta un helper de haces |
| Flicker A/B (sting) | `visible` alternando cada 9 cuadros |
| Estrella/objeto portador (sting) | un paquete o llave que cruza las escenas |
| Cápsula que cruza a toda velocidad (miedo y codicia) | costura `latigazo` con objeto |
| Contador y anillo de progreso (anuncio) | `custom(id, lt)` con `eo()` |
| Tarjetas de vidrio con perspectiva (anuncio, explicador) | `MeshPhysicalMaterial` con transmisión o plano con borde/brillo |
| Texto por palabra con tic (miedo y codicia, explicador, anuncio) | `data-a` escalonado + `tick()` en `sfx_events.py` |

## Qué agregar al motor ahora (orden de utilidad)
1. **`explosionar()` + etiquetas con línea guía + tooltip** (patrón 1): sirve a cualquier reel técnico con un objeto físico (USB, notebook, switch, router).
2. **Helper `retener(rig, [...])`** para armar la secuencia mover-retener-mover sin calcular tiempos a mano.
3. **`iris` y `forma`**, **`glitch`/`teselas`** y la **cuadrícula de beats** (lista anterior).

## Lo que NO sirve de estos videos para nosotros
Fotos de stock y marcas de terceros (incluidos productos y empresas de las referencias nuevas: lente de cámara, trading, Glasser.AI), retratos de personas, paletas ajenas (rojo/blanco, amarillo/rojo/crema, azul eléctrico), tono publicitario («Download», KPIs de marketing), formato 1:1 con barras negras (Nokia) y 16:9 horizontal (lente: hay que reencuadrar en 9:16), loudness de −9,7 o −11,7 LUFS que ahoga una voz, CTAs de «guardá/comentá la palabra» (nuestra regla 3) y promesas de ganancias.

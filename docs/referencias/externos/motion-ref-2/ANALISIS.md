# Desglose de referencia — Vista explosionada de una lente de cámara (3D interactivo, 16:9)

> Referencia de motion graphics que pasó Ayrton (2026-11-09), guardada en `assets/referencias/motion-ref-2.mp4`. Cortes, ritmo y volumen: **medidos** por `engine/analisis/previo/analizar_video.py` (histórico; hoy `engine/analisis/medir.py`). Planos, movimientos y transiciones: **leídos mirando los cuadros** (en motion graphics 2D las etiquetas automáticas de movimiento no sirven: se mueven los elementos, no una cámara). Vocabulario: `docs/GLOSARIO-EDICION.md` y `docs/MOVIMIENTO.md`. Hojas de cuadros locales en `docs/referencias/analisis/motion-ref-2/` (no van a git; se regeneran con `./reel analizar`).

## Ficha
- **Archivo:** `assets/referencias/motion-ref-2.mp4` · 1280x720 · 30 fps · 20 s
- **Fuente:** Pinterest (archivo adjuntado por Ayrton; sin link directo)
- **Qué queremos aprender:** estructura técnica: planos, transiciones, movimientos de cámara, ritmo y sonido, para usarlos en próximos reels.

## 1. En una frase
Una explicación técnica de cómo funciona una lente: un solo plano de cámara 3D que se pega al sensor, retrocede, abre la lente en capas, resalta una pieza con el cursor y vuelve a armarla, terminando donde empezó.

## 2. Estructura narrativa
| Bloque | Tiempo | Qué pasa |
|---|---|---|
| Hook | 0–2,2 s | Sensor de imagen en azul con rayos de luz que convergen y tooltip «Image Sensor» |
| Contexto | 2,2–5,5 s | La cámara retrocede: se ve la lente completa en corte, con rayos |
| Desarrollo | 5,5–9,9 s | Hover sobre el grupo de enfoque; se aprieta «Explode» y las piezas se separan a lo largo del eje, cada una con su etiqueta |
| Detalle | 9,9–14 s | Push-in al diafragma: resaltado en azul y tooltip «Nine blades open and close to set the f-stop: how much light, how much blur.» |
| Payoff | 14–18,5 s | Pull-out, «Assemble»: las piezas vuelven a su lugar |
| Cierre | 18,5–20 s | Push-in al sensor otra vez: el último cuadro se parece al primero (bucle) |

## 3. Guion técnico (planos y transiciones)
| # | Tiempo | Qué se ve | Movimiento / transición de salida | Texto |
|---|---|---|---|---|
| P1a | 0–2,2 | Cámara pegada al sensor azul mirando por el eje; haces de luz de colores atraviesan los lentes; cursor y tooltip | Plano casi quieto (retención ≈2 s para leer el tooltip) | «Image Sensor — The camera chip where every beam meets and the picture is recorded» |
| P1b | 2,2–2,9 | La cámara se aleja y gira un poco; aparece otra pieza resaltada en azul | Pull-out rápido (≈0,7 s, pico de velocidad alto con ease suave) | Tooltip de «Rear Element Group» |
| P1c | 2,9–5,5 | Vista lateral de la lente en corte con rayos; gira lento y aparece el botón «Explode» abajo | Giro horario lento (órbita de 10°) | Botón «Explode» |
| P1d | 5,5–9,9 | Retención en vista lateral; cursor pasa por «Focus Group» (azul); luego «Explode»: las piezas se separan en cadena desde el sensor y aparecen las etiquetas con línea guía | Retención 4 s; explosión escalonada de ≈1,5 s | «Focus Group» y 10 etiquetas (Image Sensor, Rear Element Group, Ultrasonic Focus Motor…) |
| P1e | 9,9–14 | Push-in a la zona del diafragma; el cursor lo resalta y abre un tooltip con la definición | Push-in rápido ≈0,7 s y retención 3,4 s | «Aperture Diaphragm» |
| P1f | 14–18,5 | Pull-out al plano general explosionado; el botón pasa a «Assemble» y las piezas convergen; la lente armada con rayos | Pull-out rápido 0,5 s; ensamblado ≈1,5 s | — |
| P1g | 18,5–20 | Push-in al sensor otra vez con tooltip de «Rear Element Group» | Push-in rápido ≈0,7 s; el cuadro final repite el inicial | — |

## 4. Ritmo (medido)
- 1 planos · **0.0 cortes/min** · plano medio 20.03 s (mediana 20.03 s; más corto 20.03 s, más largo 20.03 s) → ritmo **contemplativo**.

## 5. Sonido
- Volumen **−16 LUFS**, rango ≈11 dB. **Solo 4 golpes graves** (0,08; 2,58; 5,58; 12,58 s): impactos suaves cuando la cámara se mueve o cambia de pieza; el resto es una cama muy baja.
- Sin voz en este corte (la información va en los tooltips). Un video hablado lo narraría con una frase por pieza.

## 6. Técnicas para tomar
| Técnica | Cómo se hace | Cómo la hacemos en Claqueta |
|---|---|---|
| Vista explosionada | Las piezas se separan a lo largo del eje con escalonado desde un extremo; antes la cámara se aleja para que entren todas | Grupo 3D con piezas a posiciones «ensambladas» y «explosionadas»; `lerp` escalonado por pieza; toma `mover` que se aleja antes de explotar |
| Corte seccional + rayos de luz | Una lente abierta en corte y haces de color atravesándola muestran la función, no solo la forma | Cutaway = mitad de cada pieza; rayos = tubos finos con `drawRange` o paquetes de luz (como los paquetes del reel de redes) |
| Etiquetas con línea guía | Cada pieza tiene un cartel pequeño y una línea con un punto que apunta a ella | `cartel()` + línea fina en el espacio; billboard hacia la cámara (ya se hace en el reel de redes) |
| Hover con tooltip | El cursor resalta la pieza en el acento y abre una tarjeta con título y una frase de definición | `dinamismo.cursor` + material emisivo del acento + `cartel` de dos líneas; la frase es la misma que dice la voz |
| Mover-retener-mover | La cámara se queda quieta 3–4 s (leer) y se reencuadra en 0,5–0,7 s con pico de velocidad alto | Tomas `mover` cortas con ease `suave` + `MotionBlur`; ver patrón en `../../SINTESIS.md` |
| Cierre en bucle | El último cuadro repite el primero (sensor azul con rayos) | `musica_ventana` y empalme como en el Parrot-bucle (docs/GUION.md) |
| Botón de estado | «Explode» ↔ «Assemble» muestra que el usuario manda | Chip HTML que cambia con `data-a`; opcional |

## 7. Qué NO copiar
El producto (lente de cámara), la interfaz oscura con tipografía de ellos y el formato 16:9 (nuestro reel es 9:16: hay que reencuadrar vertical, con el eje de la pieza en vertical o en diagonal).

## 8. Ideas para nuestros reels
- **Switch / router abiertos en vista explosionada:** puerto, controlador, memoria… cada uno con su tooltip (mismo lenguaje que este reel).
- **Una red como vista explosionada:** capas apiladas (aplicación → transporte → red → enlace) que se separan.
- **Paquete de datos que atraviesa piezas** en corte, con luz que cambia de color en cada capa.

## Datos crudos
- `INFORME.md` y `metricas.json` de esta carpeta (medidos con `medir.py`). Resumen de patrones de todas las referencias: `referencias/SINTESIS.md`.

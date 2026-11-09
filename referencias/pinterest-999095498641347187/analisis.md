# Desglose de referencia — Glitch cyber sobre calle real («system shutdown»)

> Referencia de motion graphics que pasó Ayrton (2026-11-09), guardada en `assets/referencias/pinterest-999095498641347187.mp4`. Cortes, ritmo y volumen: **medidos** por `engine/analizar_video.py`. Planos, movimientos y transiciones: **leídos mirando los cuadros** (en motion graphics 2D las etiquetas automáticas de movimiento no sirven: se mueven los elementos, no una cámara). Vocabulario: `docs/GLOSARIO-EDICION.md` y `docs/MOVIMIENTO.md`. Hojas de cuadros locales en `referencias/pinterest-999095498641347187/` (no van a git; se regeneran con `./reel analizar`).

## Ficha
- **Archivo:** `assets/referencias/pinterest-999095498641347187.mp4` · 720x1280 · 60 fps · 8,8 s
- **Fuente:** Pinterest (archivo adjuntado por Ayrton; sin link directo)
- **Qué queremos aprender:** estructura técnica: planos, transiciones, movimientos de cámara, ritmo y sonido, para usarlos en próximos reels.

## 1. En una frase
Metraje real de una calle nevada, caminado en primera persona, con un «sistema» que se rompe encima: ventanas de error, bloques azules, píxeles y recortes digitales; todo con cortes de ≈0,8 s y una pista de música muy comprimida.

## 2. Estructura narrativa
| Bloque | Tiempo | Qué pasa |
|---|---|---|
| Hook | 0–1,7 s | Panel de señales con «File.exe» y calavera, «sky is loading» |
| Desarrollo | 1,7–5,2 s | Cámara caminando; jinete (BLOCKED), error de sistema con barra de carga, glitches |
| Payoff | 5,2–7,3 s | Catedral con ventanas de error, luz de farol que pasa de azul a cálido |
| Cierre | 7,3–8,8 s | Tramas de código sobre la catedral («PFN_LIST_CORRUPT») |

## 3. Guion técnico (planos y transiciones)
| # | Tiempo | Qué se ve | Movimiento / transición de salida | Texto |
|---|---|---|---|---|
| P1 | 0–1,2 | Calle con señales cubiertas de interfaz azul (File.exe, Retry/Cancel, calavera) y una persona caminando | Paneo a la derecha lento; glitch de bloques en la salida | «File.exe» «Retry Cancel» |
| P2–P3 | 1,2–2,4 | POV hacia un cruce con ventanas de ordenador flotando («sky is loading», máscara de Anonymous); barra de carga | Corte con bloques horizontales desplazados (glitch) | «sky is loading» |
| P4 | 2,4–3,2 | Un jinete a caballo cruza; el cuadro se pixela en bloques y aparece «ENEMY DETECTED» | Mosaico de píxeles como transición | «ENEMY DETECTED» |
| P5 | 3,2–3,8 | Mancha blanca que se come al jinete: «BLOCKED»; luego pared de edificio | Recorte tipo máscara blanca que se llena de ruido | «BLOCKED» |
| P6–P7 | 3,8–4,8 | POV caminando por una calle de edificios; un cuadrado de la imagen se reemplaza por blanco y vuelve; rasgado de líneas de escaneo | Walk-through en primera persona con cortes por bloques | — |
| P8 | 4,8–5,2 | La calle se convierte en dos tonos azul/blanco de alto contraste (umbral); aparece un cuadro «ERROR / SYSTEM SHUTDOWN» con barra de progreso | Posterizado a duotono azul + diálogo de error | «ERROR SYSTEM SHUTDOWN» |
| P9–P10 | 5,2–7,3 | Catedral nevada; ventanas de error de Windows («A problem has been detected…»); sobre blanco con ruido; farol que se pinta azul | Walk-through / push-in lento hacia la catedral; flash de blanco entre planos | «A problem has been detected» «Windows has been shut down» |
| P11 | 7,3–8,8 | El farol azul se reemplaza por una versión cálida con una grilla de cuadros y trama de líneas; catedral con texto de código | Reveal por grilla de teselas; luego trama de puntos y texto «text_00…» | «PFN_LIST_CORRUPT» «text_02» |

## 4. Ritmo (medido)
- 11 planos · **68.7 cortes/min** · plano medio 0.79 s (mediana 0.7 s; más corto 0.37 s, más largo 1.47 s) → ritmo **vertiginoso**.

## 5. Sonido
- Volumen **−9,7 LUFS** (muy fuerte), rango dinámico de solo **3,4 dB**: pista densa y comprimida; **no se detectaron golpes aislados** (el ritmo lo lleva la música continua; los glitches probablemente van pegados al audio, a confirmar escuchando).
- Lección: este nivel es 4–5 LU más fuerte que nuestro objetivo de −14 LUFS; es un estilo de reel de efectos, no un tutorial hablado (la voz se perdería).

## 6. Técnicas para tomar
| Técnica | Cómo se hace | Cómo la hacemos en Claqueta |
|---|---|---|
| Walk-through en primera persona | Cámara caminando por un lugar real; encima, interfaz | Toma `fpv` de camara3d.js: un pasillo, una calle o una placa madre en 3D; interfaz como `cartel()` en el espacio |
| Interfaz de error como capa | Ventanas «ERROR / SYSTEM SHUTDOWN», barras de carga, «BLOCKED» sobre la imagen | HTML encima del canvas 3D con `data-a`; paleta de error del tema (rojo relleno con ✕, regla 1) |
| Mosaico de píxeles / bloques desplazados | La imagen se rompe en bloques y salta al siguiente plano | Costura nueva «glitch» (canvas con bloques; a implementar) |
| Duotono de umbral | La imagen se convierte en dos colores de alto contraste | Filtro SVG/CSS sobre el canvas con colores del tema |
| Reveal por grilla de teselas | Un cuadrado de la imagen se cambia por otro en grilla | Costura «teselas» (a implementar) |
| Texto de código al final | Líneas tipo `text_00`, `0xC0000098` como textura | `data-type` con texto de código del propio reel |

## 7. Qué NO copiar
El metraje de Rusia/San Petersburgo y la persona (identidad de terceros), el azul eléctrico, el nivel de loudness (−9,7 LUFS) que ahoga la voz y la idea de «sistema que mata» con referencias a Windows. Es el estilo más cercano a ciberseguridad, pero se hace con 3D propio.

## 8. Ideas para nuestros reels
- **Reel de ciberseguridad (ataque / bloqueo):** pasillo de servidores en primera persona (toma `fpv`) que se corrompe a medida que avanza el ataque.
- **Reveal por grilla** al pasar de «sistema vulnerable» a «sistema parcheado» (el farol azul → cálido).

## Datos crudos
- `referencias/pinterest-999095498641347187/planos.json` y `audio.json` (medidos). Resumen de patrones de todas las referencias: `referencias/SINTESIS.md`.

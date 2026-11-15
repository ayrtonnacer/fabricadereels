# onetake (feitangyuan/onetake) — estudio, 2026-11-15
Fuente: https://github.com/feitangyuan/onetake (skill de Claude para films de producto, ~4,2 k estrellas, licencia PolyForm Noncommercial 1.0.0). **Solo se leyó** (README, SKILL.md, references/rhythm, 3d, motion-library); **no se instaló ni se copió código**. Licencia: no comercial → tomamos **ideas y umbrales**, no su código (`lib/motion.js`, `probe.py`). Su tier "Pro" es de pago: no se usa.

## Qué hace bien (y es lo que le interesa a Ayrton)
Una película = **una sola cámara continua**; en cada límite entre escenas **algo sobrevive y se transforma en lo siguiente** (una barra de texto se abre y es la ventana de la app; una tarjeta crece hasta ser la página). Un script (`probe.py`) lo mide ANTES de que un humano lo vea: **puntaje de arrastre** por límite. Versiones: 0,00 (diapositivas, rechazada) → 0,40 (rechazada) → 0,75 (aceptada) → 0,83 (su film final).

## Qué tomamos (ya aplicado)
1. **Medir el arrastre**: `engine/analisis/arrastre.py` (código propio, solo numpy/PIL/ffmpeg). Mide en cada corte cuánto de lo que había sigue en lo que viene. Umbral de ellos: puntaje medio ≥ 0,5 aceptado; < 0,5 en un límite = diapositiva.
2. **Tipos de arrastre** para diseñar cada límite (a escribir en el plan, columna "qué sobrevive"): (a) el objeto sigue y pasa a la escena siguiente; (b) un contenedor se transforma en la escena siguiente (la tarjeta → la página; el bloque → la planilla); (c) la cámara empuja hasta que el objeto ocupa todo el cuadro y ESO es la escena siguiente (zoom through); (d) un círculo se abre desde un punto; (e) un grupo se junta en uno (el cierre/lockup); (f) metáfora física/superficie continua. "Si nada sobrevive al límite, es un cambio de diapositiva, por más ritmo que tenga."
3. **Cámara**: *lead* (la cámara apunta ~0,1 s por delante del objeto con `sineInOut`, lo sigue), *anticipate* (antes de un golpe se fija el punto de aterrizaje con `expoInOut` y se "latiguea" hasta él), *shake* decreciente y determinista **solo en los aterrizajes**, flotación de mano lenta **en cero durante las pausas**, y **una retícula tenue lejana** para que el movimiento se note sobre un fondo vacío (= nuestro piso de líneas, ya lo tenemos).
4. **Ritmo (umbrales aceptados por ellos)**: planos con **variación ≥ 4×** entre el más corto y el más largo y coeficiente de variación ≥ 0,25 ("metrónomo = diapositivas"); **≥ 25 % de cuadros quietos** y al menos un tramo ≥ 1 s; los reposos son de verdad quietos (un push-in durante la pausa cuenta como movimiento); nunca terminar dos planos seguidos igual (alternar resorte / desenfoque / corte); una "ráfaga" (≥ 3 cambios grandes en 1,5 s) solo si el concepto tiene golpes.
5. **Cámara que recalcula en cada beat = metrónomo**: saltos del mismo tamaño cada 0,86 s fueron rechazados; alternar lados cada beat invierte la dirección de pantalla (mantener una dirección en todo el tramo). Mismo criterio que la "corriente" de `docs/MOVIMIENTO.md`.
6. **Legibilidad en 3D**: texto plano en el mundo se aplasta con el ángulo (sen de la elevación); medir **alto en px ≥ 24 y aplastamiento ≥ 0,6**; se arregla con la cámara de frente a esa línea, no con letra más grande. Alturas: evitar vistas cenitales (una cadena que cae se lee como cambio de color); ≤ 35° bajo-3/4.
7. **Desenfoque de movimiento real** (obturador de 180°, promediando varias capturas por cuadro, en luz lineal): sin obturador, un movimiento de > 80 px/cuadro "estroboscopea" (ellos lo marcan como falla). Sirve de alarma para nuestros whips.
8. **Reglas duras que coinciden con las nuestras**: nada de partículas/confeti/chispas decorativas; render determinista (`Math.random` prohibido, semilla fija); fondo grande y elementos chicos (≈ 70 % vacío en su estilo claro); no cargar el look del film anterior al siguiente; sonido con **menos eventos que beats** y un solo "cuarto" (reverb) para todos; master −16 LUFS / pico real −3,5 dBTP (nosotros: −14 LUFS, pico ≥ −3).
9. **Flujo**: antes de escribir, **3 conceptos distintos** (no 3 variantes de tarjetas), cada uno con su cuadro-gancho, su arrastre por límite y qué descarta; el humano elige. Planilla de ritmo (t · beat · duración · movimiento: quieto/chico/tipeo/ráfaga/pausa/golpes) **sin huecos**, más una columna "qué sobrevive" en cada límite; "un PASS sobre menos límites que los de la planilla no es evidencia".

## Qué NO tomamos
- Su motor (Playwright + captura por cuadro, 4K60, GPU) y su `lib/motion.js`: nuestro render ya es HyperFrames + three.js y funciona. Ellos mismos notan que WebGL sin GPU es ~4× más lento (coincide con nuestro costo medido).
- Estética de fondo blanco de sus films; sus voz/TTS (Kokoro) y música; sus services Pro.
- Su "pared de 70 % blanco": nuestro fondo es negro puro (Scale).
- Su meta "cámara siempre persiguiendo": una cámara quieta fue rechazada por ellos por poco "viva", pero **Ayrton ya dijo lo contrario para el banco v4 (demasiado movimiento confunde)**. Gana Ayrton: se toma la parte de pausas verdaderas (≥ 25 % quieto) y del seguimiento *anticipado* (no más movimiento, mejor movimiento).

## Choque con nuestras metas
`metas.json` pide `camara.pct_cuadros_en_movimiento` 60–90 %; onetake exige ≥ 25 % de cuadros quietos (es decir ≤ 75 % en movimiento) y Ayrton pidió pausas. **Propuesta (pendiente de su OK, no se cambió)**: pasar esa meta a 40–75 % y agregar `arrastre_medio ≥ 0,5` y `pct_cuadros_quietos ≥ 25`.

## Primera medición propia
`python engine/analisis/arrastre.py docs/referencias/propios/2026-11-tensores-scale-oscuro/final-960.mp4 --escenas videos/2026-11-tensores-scale-oscuro/video.json`:
arrastre medio **0,51**; límites en 0,00 (t = 36,8 s y 50,9 s → diapositiva), 0,35 (42,9 s), 0,45 (0,1 s, la portada) y 0,62–1,00 el resto. Planos con CV 0,45 (×104 entre el más corto y el más largo, pero por la portada de 0,1 s). Cuadros quietos 72 % (la diferencia está medida a 108 px de ancho: movimientos lentos de cámara cuentan como quietos, así que el número es un máximo). **Heurística: 1,00 no prueba continuidad si el piso/fondo persiste; mirar siempre los cuadros.**
Lectura: el cierre (50,9 s) es un corte a otra composición (CTA) y el cambio en 36,8 s es el paso a "usos/payoff"; son los dos límites donde conviene diseñar una transformación.

## Ampliación (2026-11-15): todo lo que se copió/adaptó al repo
Pedido de Ayrton: "copiá todo lo útil". Criterio: **no se copió código** (licencia PolyForm Noncommercial: el canal puede monetizarse y el repo es compartible); se **reescribió con código propio** lo que sirve, porque las fórmulas son matemática estándar.
| De onetake | En nuestro repo |
|---|---|
| `lib/motion.js` (resortes, impact, shake, whip, camera log-zoom, zoomThrough, morphRect, iris, hop, gather) | `videos/_plantilla/assets/movimiento.js` (probado con node) |
| `probe.py` (arrastre), energy map, estilo de rhythm.md | `engine/analisis/arrastre.py` (+ mapa de energía) |
| sound.md (materiales, un cuarto, menos eventos, barro, efecto rana) | `docs/AUDIO.md` (sección nueva) + `engine/analisis/barro.py` |
| rhythm.md / SKILL.md (planilla, CV ≥ 0,25, ≥ 25 % quieto, no terminar dos planos igual) | `videos/_plantilla/plan.md` (metas + tabla de límites), `docs/CAMARA.md` reglas 7–9 |
| composition.md: **pausa = byte-idéntica** (un push 1→1,05 ya falla), `handEnv` apaga la mano; ruido fijo 256² (alfa ≤ 7/255) sobre gradientes oscuros para evitar bandas tras el codificado | regla 9 de CAMARA.md; **idea pendiente**: probar el ruido anti-bandas en el fondo Scale (negro con gradiente) |
| 3d.md: legibilidad de texto en el mundo (≥ 24 px de alto, aplastamiento ≥ 0,6), ≤ 35° de elevación, vista cenital = se lee como cambio de color | pendiente: chequeo automático de legibilidad en `escena3d.js` |
| SKILL.md flujo: 3 conceptos distintos, no arrastrar el look de un film a otro, segundo idioma sin bifurcar la composición (`?lang=` + deformación de tiempo) | `docs/FLUJO.md` (ángulos); el segundo idioma queda como idea para reels en inglés |
**No sirve para nosotros**: render 4K60 y captura por cuadro con Playwright (tenemos HyperFrames), `record_footage.py`/UI reconstruida (no hacemos demos de producto), Kokoro/faster-whisper (tenemos Piper y `subtitulos.py`), galería de 12 films (solo el Pro de pago trae el código fuente completo).


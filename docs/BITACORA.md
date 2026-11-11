# Bitácora de indicaciones de Ayrton
Todo lo que Ayrton dice y pasa se guarda acá (y el material en `docs/material/`), para aprovecharlo en videos futuros: criterios de diseño, cómo dibujar y graficar, sonido, flujo. **Regla: cada vez que Ayrton da una indicación o pasa un archivo, se agrega acá y se lleva a la doc que corresponda.** Las correcciones puntuales de un video van además a `docs/DECISIONES.md`.

## 2026-11-09 — replanteo del proyecto
- Trabajar con **HyperFrames** (más probado que el motor propio); renderizar 3D tardaba muchísimo y quiere **reels rápidos**. Estilo: **motion graphics**; muchos motion graphics son 2D y el **movimiento de cámara** da la profundidad. Revisar todo el repo y sacar lo que sobra. → `docs/CAMARA.md`, `CLAUDE.md`.
- Referencias de movimientos de cámara: las va a pasar a medida que trabajemos. → `docs/referencias/`.
- Sonido "chinn" (cristal) mejor para el cierre. Repo `code-reel-studio`: tipeo real de teclado y otras lógicas. → `docs/AUDIO.md`.
- En el cierre el **foco es el CTA**, no su usuario (la demo hacía zoom a la firma). → `docs/DECISIONES.md`.
- Flujo: link + breve explicación → guion (según lineamientos y público) → **script técnico** (planos, sfx, perspectiva de cámara) → video. A futuro: **publicar automáticamente** en sus redes. → `docs/FLUJO.md`.
- Público: **técnicos, principiantes y reclutadores**; los reels son portfolio y tienen que demostrar que sabe. → `docs/GUION.md`.
- Pidió un reel que explique **qué es el WiFi y cómo funciona** para cualquier público (fuentes: HowStuffWorks, Wikipedia, Cisco). → `videos/2026-11-wifi`.

## 2026-11-09 (tarde) — correcciones sobre el reel de WiFi
- **Subtítulos**: muchas personas ven los reels en silencio (hay estadísticas); respetar los **espacios seguros**. → `docs/SUBTITULOS.md`.
- **Ondas cortadas**: las ondas de 2,4 y 5 GHz se cortaban en la pared, sin continuidad (los dos tramos reiniciaban la fase). Ahora comparten fase. → `docs/CAMARA.md`. (Captura: `docs/material/2026-11-09-wifi-correcciones/1-ondas-cortadas.png`.)
- **Cable que no llegaba al router**: el cable quedaba flotando sobre el router. (`2-cable-no-llega-al-router.png`.) Regla: lo que se conecta tiene que tocarse.
- **Palabra sola** ("llega") en la bajada del gancho. (`3-palabra-sola-llega.png`.) Pasó el artículo de Adobe sobre viudas y huérfanas. → `docs/TIPOGRAFIA.md`.
- **Escuchar el audio**: sugirió usar earshot o Whisper para "escuchar" y verificar. Desde la nube no se pueden bajar modelos (Hugging Face y OpenAI bloqueados; earshot ya se había intentado y no corrió). Solución: los tiempos por palabra salen del propio Piper (exactos) y se verifican dibujando la onda. → `docs/SUBTITULOS.md`. Si quiere Whisper de verdad: correrlo en su compu.
- **Sonido grave** (`boom-cinematico.mp3`, "cinematic impact boom 05" de Universfield): al **inicio y al final**. → `docs/AUDIO.md`.
- **Fondo**: le gustan las **líneas que dan perspectiva** (el piso de grilla) y el **gradiente**. Los **puntitos verdes** de fondo no le encontraba sentido: **sacados**. → `docs/ESTILO.md`.
- **Eje z / three.js**: siente que no se aprovecha la profundidad (z). Se puede usar three.js **si no demora mucho el render**; si demora, no lo quiere. Medido: ver `docs/CAMARA.md` (≈ +1 s de render por segundo de video para una escena simple). Se hizo un piloto en el payoff.
- **Guardar todo en el repo**: indicaciones, materiales, cómo dibujar/graficar, sonido. → esta bitácora y `docs/material/`.

## 2026-11-09 (noche) — segunda tanda de correcciones sobre el reel de WiFi
- **Sonido limpio**: preguntó si la voz tenía efecto de radio (no: `efecto: "ninguno"`). Causas probables del aire "sucio": zumbido de 50 Hz con ruido de fondo (ambiente), `glitch()` (estática), normalización dinámica que comprimía la voz dos veces y el ancho de banda propio de Piper (22 kHz). Quedó: sin ambiente ni glitch por defecto, voz con compresión leve y ganancia lineal, nivel final lineal + limitador. → `docs/AUDIO.md`.
- **Un "1" sin sentido** (captura `docs/material/2026-11-09-wifi-correcciones/4-uno-sin-sentido.png`): los bits desenfocados de fondo se sacaron todos. Regla: nada decorativo sin significado. → `docs/PREFERENCIAS.md`.
- **Todo con three.js**: le gustó la perspectiva de los teléfonos; quiere la explicación de la compu, la antena, etc. también en three.js, "como venimos trabajando en otros proyectos". Hecho: librería `assets/escena3d.js` y todas las escenas en 3D (notebook, router, globo, cable, ondas, pared). Render del reel completo: ~66 s para 33 s. → `docs/CAMARA.md`.
- **"WiFi" mal pronunciado**: "guifi" se leía "gifi". Se cambió a "uaifai" y se dejaron 3 variantes para elegir de oído (`docs/material/pronunciacion/wifi-variantes.mp3`: 1 uaifai, 2 güifi, 3 uifi).
- **Texto del cierre ≠ voz**: el texto debe decir lo mismo que la voz: "Dale like y seguime para aprender más de redes". → `docs/GUION.md`.
- **Guardar notas siempre y sin que se lo pida**: pidió confirmación. Respuesta: la bitácora ya existía; se agregó `docs/PREFERENCIAS.md` (resumen de gustos y errores) que se repasa antes de cada video, y la regla 10 de `CLAUDE.md` pide actualizar ambos en cada tanda.

## 2026-11-09 (noche, 3) — tercera tanda sobre el reel de WiFi + investigación de three.js
- Pasó una **guía de three.js** (r187, `docs/material/2026-11-threejs-guia-profesional-r187.md`) y el artículo de Utsubo (100 consejos de rendimiento) + el link de la doc oficial (bloqueado desde la nube). Pidió investigar por mi cuenta, guardar los consejos en el repo y mejorar los objetos y la lógica **siempre dentro de la estética HackTheBox**. → `docs/THREEJS.md`; la librería pasó a r187 con tone mapping Neutral, entorno procedural, biseles, sombras de contacto y contraluz.
- **"uaifai" aprobado** para WiFi. **"router" sonaba "RRUter"** → se prueba "ráuter" (todas las grafías empiezan con la r vibrada del español; "ráuter" da el diptongo "au").
- **Notebook sin antena**: las notebooks no tienen una antena literal; la onda sale de la tapa y se expande por el piso. **Bits más chicos** y dentro de la pantalla. (Capturas 5 a 8 en `docs/material/2026-11-09-wifi-correcciones/`.)
- **Los cables tocan los objetos**: en internet el cable debe ir al centro del globo (no quedar al borde), y salir del router; en ethernet, de la notebook al router. Las señales de radio no necesitan encajar justo.
- **Etiqueta "pared" sobra**: "el espectador no es idiota". Regla: rótulos solo si aportan.
- **Sonidos nuevos** (guardados en `assets/sfx/propios/`): `interface-texto-digital` (tipeo de 0 y 1; el teclado queda para tipear código), `modem-conexion` (handshake de módem al conectarse a internet), `hit-metal` (en vez del whoosh suave antes del cierre, ~0:28; "probemos, tenés oídos").
- **CTA**: duda entre "aprender más DE X" y "SOBRE X" → se usa "de" para temas de una palabra (más corto y natural en rioplatense) y "sobre" para temas largos o frases ("sobre cómo funciona internet").

## 2026-11-10 — medición de videos (de "se siente" a números)
- Ayrton vio un video de *Crea con LuisPa* sobre medir en vez de opinar ("una opinión no la puedes recrear, un número sí") y pasó el repo `luispablovillasenor-afk/shorts-animados-claude` (MIT; no le gusta su estética, sí su **enfoque de medir**): hojas de contacto de 60 cuadros, correlación de fase para la cámara, cortes, brillo/contraste/saturación, tirón (*jerk*), 2,77 palabras/s en la referencia.
- Lo que él quería desde el principio: **analizar videos de referencia de motion graphics** (transiciones, movimientos de cámara, planos, sonido) para usarlos de inspiración con parámetros; no sabía cómo pasarlos: por eso había pensado en el shooting script. → `docs/MEDICION.md`: se adjunta el .mp4 y se mide; sale un script técnico medido.
- Duda: "¿grabamos a 30 FPS?": sí, es el estándar; medido que alcanza para nuestro movimiento (p95 ≈ 4,7 px/cuadro). → `docs/MEDICION.md`.
- Hecho: `engine/analisis/medir.py` (propio, calibrado con autotest) y `comparar.py`; primer análisis del reel de WiFi y del ejemplo del repo en `docs/referencias/medidas/`; `docs/referencias/PARAMETROS.md`.

## 2026-11-10 (2) — una sola rama
- Ayrton: **quiere trabajar con una sola rama** (`main`); no conoce bien GitHub y se le mezclan las ramas. → todo se commitea y sube **directo a `main`**; no se crean ramas ni pull requests salvo que él lo pida (regla 13 de `CLAUDE.md`).
- Al revisar el repo apareció una rama de otra sesión (`claude/3d-camera-video-effects-9j1wwx`, 14 commits del 9/11 sobre el motor viejo) con **10 referencias de motion graphics que él había pasado** + análisis + un guion de "redes". Una unión directa daba 16 conflictos; se **rescató a `main`** el contenido útil (`referencias/`, `assets/referencias/`, 4 docs, el guion) y se midieron las 10 referencias con `medir.py` → `docs/referencias/PARAMETROS.md`.

## 2026-11-10 (3) — análisis solo con números
- Ayrton: el "script técnico / shooting script" lo pidió **por desconocimiento, antes de ver la herramienta de medición del repo de LuisPa**. Quiere que el análisis y el resumen de los videos sean **como en ese repo: con números**, para decirle a Claude con precisión qué funciona, qué no y cómo son las transiciones, y poder **comparar nuestros reels con otros**. Pidió **eliminar lo que no se use** y ver **todos los análisis en un solo lugar**.
- Hecho: `docs/referencias/BIBLIA-DE-ESTILO.md` (hallazgos + tablas de los 12 videos, regeneradas por `engine/analisis/biblia.py`), `docs/referencias/metas.json` (rangos objetivo), `medir.py` ahora mide transiciones (velocidad previa, golpe de sonido más cercano) y mover–retener–mover (picos, retenciones, ataque/liberación); `comparar.py propio.json` compara contra las metas. `plan.md` (numérico) reemplaza a `script-tecnico.md`.
- Borrado: analizador viejo (`previo/`), `SCRIPT-TECNICO-REFERENCIA.md`, `ANALISIS.md` cualitativos, `SINTESIS.md`, `PARAMETROS.md`, `INDICE.md`, `ANALISIS-REFERENCIAS.md`, `script-tecnico.md` (plantilla y WiFi). Todo sigue en el historial de git.

## 2026-11-10 (4) — últimas correcciones del reel de WiFi (v5)
- Ayrton: "el video está casi perfecto". Capturas en `docs/material/2026-11-09-wifi-correcciones/v4-9…13.png` (rojo = sacar, verde = OK).
  1. **Sacar la onda ondulada** (notebook "y las emite por su antena", router "y de vuelta, igual", ethernet "WiFi es Ethernet sin cable"). Cuando se habla de la onda de radio en la computadora, etc., mostrar **ondas/círculos** (anillos). **Dejar las ondas sinusoidales solo en las frecuencias** (2,4 y 5 GHz): esas están OK.
  2. **Sonido de la sección del router** ("el router las recibe, las decodifica y las manda a internet"): que sea el **sonido de router/módem**, no el tipeo digital sobre los 0/1 del router. El **tipeo digital queda solo cuando se escriben los 0 y 1 en la computadora**.
- Pidió que el proceso a futuro sea **más dinámico y gaste menos tokens**: solo pasar el material y que se generen los videos bien (se gastó ~50 % del cupo semanal en esta serie de cambios).
- Hecho: `envia`, `router` y `ethernet` usan anillos (`E.anillo`); ondas sinusoidales solo en `bandas`; `sfx_events.py`: módem en todo el router.

## 2026-11-10 — Prueba A/B: estética hairline vs HackTheBox (reel del WiFi)
- Ayrton pasó `@lucasmarkes/hairline` (npm, MIT, 33 figuras isométricas SVG de línea fina, responden al puntero) para ver si le gusta más que HackTheBox en el reel del WiFi.
- Hecho: copia `videos/2026-11-wifi-hairline/` (el original no se toca). El paquete en sí no se usa en el render (son SVG interactivos por puntero, no se pueden buscar por tiempo); se replicó el **look** en three.js: placas planas del color del fondo + aristas finas (LineSegments2, 2,2 px), gris sobre casi negro, lima solo para señal/énfasis, sin luces/IBL/glow. Se activa con `--estilo: hairline` en `marca.css` (`escena3d.js` lo lee).
- Render mudo 63 s para 33 s (≈1,9 s/s; el original con IBL ≈ 2 min). Pendiente: que Ayrton elija.
- 2026-11-10 (2): Ayrton: "me gusta cómo va" (hairline). Pidió probar **rojo en vez de verde** como acento: `--acc: #FF2E3F` en `videos/2026-11-wifi-hairline/assets/marca.css` (render `out/mudo-rojo.mp4`; el lima queda en `out/mudo.mp4`). Ojo: el rojo ya significa error (`--err`); si gana, mover el error a otro código.
- 2026-11-11: Ayrton aprobó el **rojo hairline** ("todo encaja en una estética hacker") y pasó música: Jenkins, *Palladio – I. Allegretto* → `assets/musica/palladio-allegretto.mp3` (desde 0 s, −8 dB, fades). Entregado `videos/2026-11-wifi-hairline/final.mp4` (−14,0 LUFS). l07 corrida a 20,95 s para no pisar a l06 con esta voz.
- 2026-11-11 (2): "la música casi no se escucha" → Palladio estaba ~14 dB bajo la voz (fuente −21,9 LUFS, −8 dB, ducking ×4). Ahora `musica_db: 4` y `musica_duck: 2` (nuevo parámetro opcional en `video.json`, lo lee `mezcla.py`). Para música de fuente baja, medir antes de fijar dB.
- 2026-11-11 (3): Ayrton pidió **medir el audio y ajustar la velocidad de Daniela**. Medido en `final.mp4` (medir.py): −14,0 LUFS, pico −1,8 dBTP, silencio 0,4 %, ataques 2,87/s. Habla: 101 palabras en 33,1 s = 3,05 pal/s total (meta 2,6–2,9; hablando ≈ 3,7). Cambios: `length_scale` 0,92 → **1,05**; guion recortado a **96 palabras (2,90 pal/s)**: l02 sin "por su antena", l05 "WiFi es Ethernet…" (sin "el"), l07 "Más frecuencia…" (sin "Cuanta"); líneas l03/l04/l08 corridas unas décimas. Música: medida contra la voz por línea (sidechain); Palladio sube de volumen con el tiempo, así que se agregó nivelado (`musica_nivelar: [-30, 6]`, opcional en `mezcla.py`) y `musica_db: 11`, `musica_duck: 2` → música ≈ 8–15 dB bajo la voz mientras habla.
- Ojo: Piper no es determinista (`noise_scale`); cada corrida de `voz.py` cambia las duraciones ±0,1 s. Revisar la tabla de `voz.py` tras regenerar.

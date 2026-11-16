# Fábrica de reels — manual de operación

Repo de @ayrtonnacer para producir reels verticales (1080×1920, ~30–60 s) explicativos de programación, matemática, ciberseguridad y Linux.
Flujo: **el usuario pega una fuente (link o tema, a veces con lo que quiere o no) → Claude escribe el guion → el usuario lo aprueba → Claude arma el plan numérico (metas de la biblia de estilo: cámara, cortes, ritmo, sonido) → se anima con HyperFrames (three.js r187 con cámara que se mueve en profundidad) → voz Piper (Daniela es_AR) + efectos + música → mp4.**

Cuando el usuario diga "hacé un reel de <fuente>" (o `/reel`), seguí `docs/5-tecnica/FLUJO.md` paso a paso. Mapa de todos los documentos: `docs/BIBLIA.md`. Leé antes: `docs/1-canal/PREFERENCIAS.md`, `docs/2-estilo/ESTILO.md`, `docs/2-estilo/CAMARA.md` (cómo la cámara da profundidad), `docs/5-tecnica/THREEJS.md` (criterios y costos de three.js), `docs/2-estilo/SUBTITULOS.md`, `docs/2-estilo/TIPOGRAFIA.md`, `docs/1-canal/BITACORA.md` (todo lo que dijo Ayrton), `docs/3-guion/GUION.md` (Hook→Payoff→CTA/bucle, 2,3 palabras/s; investigación en `docs/3-guion/INVESTIGACION-GUIONES.md`), `docs/5-tecnica/MEDICION.md`, `docs/2-estilo/AUDIO.md`, `engine/audio/pronunciacion.json` **`docs/1-canal/DECISIONES.md`** (cada corrección de Ayrton; no repetir esos errores), **`docs/1-canal/PUBLICO.md`** (para quién es y qué dijo la gente de cada reel) y **`docs/1-canal/CANAL.md`** (quién es Ayrton, inspiraciones, qué se repite en cada reel para que lo reconozcan, próximas mejoras).
Para todo lo de HyperFrames (contrato de las composiciones, CLI, bloques del registro) usá las skills `/hyperframes`, `/hyperframes-cli`, `/hyperframes-registry` y `/media-use` que están en `.claude/skills/`. Donde choquen con este manual (voz, audio, estética), gana este manual.

## Estructura
- `videos/<AAAA-MM-tema>/` — un video = un proyecto HyperFrames:
  - `video.json` — única fuente de verdad de tiempos: escenas (`id`, `d`), líneas de voz con su tiempo, audio.
  - `index.html` — raíz: monta una composición por escena (duraciones escritas por `engine/tiempos.py`).
  - `compositions/<escena>.html` — cada escena: su set 3D (three.js), su cámara y su timeline GSAP.
  - `assets/` — `marca.css` (identidad; otros temas en `engine/themes/`), `escena3d.js` + `three.module.js` (librería 3D), `movimiento.js` (resortes, temblor, límites con arrastre: `docs/2-estilo/CAMARA.md`), `gsap.min.js` y `fonts/` locales (nada de CDN: el render no usa la red).
  - `sfx_events.py` (efectos), `guion.md`, `plan.md` (plan numérico); salidas `out/`, `audio/`, `final.mp4` (ignoradas por git).
- `videos/_plantilla/` — punto de partida (3 escenas de ejemplo: gancho, explica, cierre). Se copia con `engine/nuevo.sh`.
- `engine/` — lo nuestro alrededor de HyperFrames: `nuevo.sh`, `tiempos.py` y `audio/` (`voz.py`, `sfx.py`, `sfxlib.py`, `mezcla.py`, `radio.py`, `cortar_teclas.py`, `pronunciacion.json`).
- `videos/LEEME.md` — qué es cada carpeta de video y en qué estado está (publicado, prueba, solo guion).
- `docs/4-referencias/material/` — archivos que pasa Ayrton (artículos, capturas con correcciones, referencias); `docs/1-canal/BITACORA.md` — registro de sus indicaciones.
- `docs/4-referencias/` — TODO el análisis, con números, en un solo lugar: `BIBLIA-DE-ESTILO.md` (qué funciona, con cifras; LEER antes de armar el plan), `metas.json` (rangos objetivo), `externos/<video>/` (`INFORME.md` + `metricas.json` de cada referencia) y `propios/<reel>/` (nuestros reels medidos). Los 10 mp4 originales están en `assets/referencias/`.
- `assets/voces/` (modelo Piper partido en 3), `assets/musica/`, `assets/sfx/propios/` (tipeo real, chinn, clicks).
- El motor anterior (three.js propio) y los videos de Parrot quedaron en el historial de git: commit `ae9a888`.

## Comandos
```
bash engine/nuevo.sh AAAA-MM-tema                     # video nuevo desde la plantilla
node engine/fisica.mjs videos/X/fisica.mjs        # (si el reel tiene física) hornea la simulación Rapier → assets/fisica.json; ver docs/5-tecnica/FISICA.md
python engine/audio/voz.py videos/X                   # voz + chequeo de tiempos y palabras prohibidas
python engine/tiempos.py videos/X                     # duraciones de video.json → index.html
python engine/subtitulos.py videos/X                  # subtítulos con tiempos exactos por palabra
(cd videos/X && npx hyperframes check)                # contrato y layout: sin errores
(cd videos/X && npx hyperframes snapshot --at 0,1.5,4) # cuadros sueltos: MIRARLOS SIEMPRE antes de renderizar
python engine/audio/sfx.py videos/X                   # efectos desde sfx_events.py
(cd videos/X && npx hyperframes render --workers 4 -o out/mudo.mp4)   # ~2,5 s por segundo de video en CPU
python engine/audio/mezcla.py videos/X                # mezcla −14 LUFS + out/mudo.mp4 → final.mp4
python engine/audio/escuchar.py final.mp4 --video videos/X   # Whisper "escucha" la voz y la compara con el guion: % entendido por línea y palabras que suenan mal
python engine/analisis/medir.py video.mp4 salida/ [--transcripcion t.txt]   # mide cámara, cortes, color, audio → números (cámara, cortes, transiciones, ritmo, audio)
python engine/analisis/comparar.py ref/metricas.json propio/metricas.json  # qué parámetro se aleja (sin 2.º archivo: contra la biblia de estilo)
python engine/analisis/encuadre.py video.mp4 [otro.mp4 …]   # encuadre: ancho/alto del contenido y nitidez relativa
python engine/analisis/arrastre.py final.mp4 --escenas videos/X/video.json   # continuidad: qué sobrevive en cada corte (medio ≥ 0,5), % quieto, variación de planos, mapa de energía
python engine/analisis/barro.py final.mp4                                    # graves-medios acumulados en la mezcla (alarma > 35 %)
```
**Las sesiones de la nube se preparan solas** (gancho `.claude/hooks/session-start.sh`, registrado en `.claude/settings.json`: instala ffmpeg, Python y `node_modules` solo si cambió algo). Si algo falta igual (otro entorno): `bash engine/preparar.sh`. Instalación a mano: `npm install` (HyperFrames fijado en 0.9.26) y `pip install -r requirements.txt`; requiere Node ≥ 22 y ffmpeg.

## Reglas que nunca se rompen (detalle en docs/)
1. **Estilo motion graphics en 3D**: todos los objetos en **three.js r187** con `assets/escena3d.js` (guía: `docs/5-tecnica/THREEJS.md`) (notebook, router, ondas, cables…), cámara que se mueve en el eje z, piso de líneas en perspectiva; el texto es HTML sobre el 3D. Escenas simples (reel completo ≈ 2 s de render por segundo de video; si pasa de ~3, simplificar). **Nada decorativo sin significado** (sin puntitos ni bits de fondo).
2. Estética (por defecto desde 2026-11-14): tema **Scale** de `assets/marca.css` (inspirado en la marca de Scale AI): negro puro, **objetos 3D de línea gris** (relleno negro), **un solo acento Foundry Tan** `--acc #A8927C`, texto blanco/gris, **Host Grotesk + Geist Mono**, subtítulos con barra negra. Los colores de marca van como acento, nunca de fondo. **Color = significado** (paleta en `docs/2-estilo/ESTILO.md`): énfasis = `--acc`, verde+✓ ok, ⚠ aviso, error = bloque rojo RELLENO+✕. Temas anteriores (línea roja, cyber) en `engine/themes/`. Sin scanlines, sin HUD/esquinas, sin mayúsculas espaciadas, sin texto de fuente al final. Paso = "Paso 1 de 7" en sans. Siempre `var(--…)`, nunca colores fijos.
3. Firma `@ayrtonnacer` al inicio y al final, **con el acento del tema (tan)**, sola (sin punto ni adornos). En el cierre **el foco es el CTA**: la firma va debajo, más chica, sin zoom sobre ella. Chinn (`propio('chinn')`) cuando aterriza el CTA. El inicio y el cierre se mantienen entre reels; el medio cambia.
4. CTA multiplataforma: texto "Dale like y seguime para aprender más de <tema>" / voz "dale me gusta y seguime para aprender más de <tema>" (**el texto coincide con la voz**). Nunca "guardalo".
5. Voz: Daniela (Piper) por ahora (voz clonada de Ayrton pendiente: `docs/2-estilo/AUDIO.md` → Voz propia). **Público mixto, la mayoría no es de IT** (`docs/1-canal/PUBLICO.md`): que se entienda sin saber nada de antemano y sin errores que un experto pueda marcar; vocabulario del área sí, cada término nuevo con una imagen o ejemplo cotidiano; no leer la terminal ni los carteles; "memoria", no "pendrive"; "me gusta", no "like". Pronunciación por diccionario, no a ojo.
6. Audio (`docs/2-estilo/AUDIO.md`): 4 capas (voz, música, efectos, ambiente), −14 LUFS, efectos audibles pero bajo la voz (ducking), música con fades ajustada al largo, **whoosh en el pico de cada movimiento de cámara**, silencio como recurso. HyperFrames renderiza mudo; el audio lo mezcla `mezcla.py`.
7. **Guion**: una idea por reel, loop abierto en el hook y cerrado en el payoff, hook ≤ 3 s sin muletillas de IA, ≤ duración × 2,3 palabras. El cuadro 0 ya muestra la idea (es la miniatura).
7b. **Checkpoint**: mostrar el guion (voz + una línea por escena con su movimiento de cámara) y esperar aprobación ANTES de animar.
8. Cambiar UNA cosa por vez y mostrar cuadros (`snapshot`) antes de renderizar. **Subtítulos siempre** (se ve mucho en silencio): `docs/2-estilo/SUBTITULOS.md`; zona segura: imagen hasta y ≈ 1100, subtítulos en 1120–1320. Nada de palabras sueltas en la última línea (`docs/2-estilo/TIPOGRAFIA.md`).
9. Contrato HyperFrames (`/hyperframes`): timeline pausado registrado en `window.__timelines`, nada de `Date.now()`/`Math.random()`/red, `fromTo` en escenas, ids únicos con prefijo por escena, posiciones de cámara por `data-x/y/z` (nunca `transform` en CSS).
10. **Guardar todo en el repo, siempre y sin que Ayrton lo pida**: cada indicación va a `docs/1-canal/BITACORA.md` (detalle) y se destila en `docs/1-canal/PREFERENCIAS.md` (gustos y errores); cada archivo que pase va a `docs/4-referencias/material/` (o `assets/`, `videos/X/fuentes/`). **Repasar `docs/1-canal/PREFERENCIAS.md` al empezar y antes de entregar cada video.**
11. **Medir en vez de opinar** (`docs/5-tecnica/MEDICION.md`): ante un video de referencia que pase Ayrton, primero `medir.py` y recién después proponer; antes de entregar un reel, medirlo y contrastarlo con `docs/4-referencias/BIBLIA-DE-ESTILO.md` (`comparar.py`). Render a **30 fps**.
12. **Una sola rama: `main`.** Ayrton no usa ramas ni pull requests: commitear y subir **directo a `main`** (`git push origin main`); no crear ramas ni PR salvo que él lo pida. Hablarle de GitHub en palabras simples.
13. Terminar cada video agregando a `docs/1-canal/DECISIONES.md` lo que el usuario corrigió y a `pronunciacion.json` cada palabra nueva.

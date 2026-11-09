# Fábrica de reels — manual de operación

Repo de @ayrtonnacer para producir reels verticales (1080×1920, ~30–60 s) explicativos de programación, matemática, ciberseguridad y Linux.
Flujo: **el usuario pega una fuente (link o tema) → Claude escribe el guion → el usuario lo aprueba → se anima con HyperFrames (motion graphics 2D + cámara 2.5D) → voz Piper (Daniela es_AR) + efectos + música → mp4.**

Cuando el usuario diga "hacé un reel de <fuente>" (o `/reel`), seguí `docs/FLUJO.md` paso a paso. Leé antes: `docs/ESTILO.md`, `docs/CAMARA.md` (cómo la cámara da profundidad), `docs/GUION.md` (Hook→Payoff→CTA/bucle, 2,3 palabras/s; investigación en `docs/INVESTIGACION-GUIONES.md`), `docs/AUDIO.md`, `engine/audio/pronunciacion.json` y **`docs/DECISIONES.md`** (cada corrección de Ayrton; no repetir esos errores).
Para todo lo de HyperFrames (contrato de las composiciones, CLI, bloques del registro) usá las skills `/hyperframes`, `/hyperframes-cli`, `/hyperframes-registry` y `/media-use` que están en `.claude/skills/`. Donde choquen con este manual (voz, audio, estética), gana este manual.

## Estructura
- `videos/<AAAA-MM-tema>/` — un video = un proyecto HyperFrames:
  - `video.json` — única fuente de verdad de tiempos: escenas (`id`, `d`), líneas de voz con su tiempo, audio.
  - `index.html` — raíz: monta una composición por escena (duraciones escritas por `engine/tiempos.py`).
  - `compositions/<escena>.html` — cada escena: su set 2.5D, su cámara y su timeline GSAP.
  - `assets/` — `marca.css` (identidad), `camara.js` (cámara 2.5D), `gsap.min.js` y `fonts/` locales (nada de CDN: el render no usa la red).
  - `sfx_events.py` (efectos), `guion.md`; salidas `out/`, `audio/`, `final.mp4` (ignoradas por git).
- `videos/_plantilla/` — punto de partida (3 escenas de ejemplo: gancho, explica, cierre). Se copia con `engine/nuevo.sh`.
- `engine/` — lo nuestro alrededor de HyperFrames: `nuevo.sh`, `tiempos.py` y `audio/` (`voz.py`, `sfx.py`, `sfxlib.py`, `mezcla.py`, `radio.py`, `cortar_teclas.py`, `pronunciacion.json`).
- `assets/voces/` (modelo Piper partido en 3), `assets/musica/`, `assets/sfx/propios/` (tipeo real, chinn, clicks).
- El motor anterior (three.js propio) y los videos de Parrot quedaron en el historial de git: commit `ae9a888`.

## Comandos
```
bash engine/nuevo.sh AAAA-MM-tema                     # video nuevo desde la plantilla
python engine/audio/voz.py videos/X                   # voz + chequeo de tiempos y palabras prohibidas
python engine/tiempos.py videos/X                     # duraciones de video.json → index.html
(cd videos/X && npx hyperframes check)                # contrato y layout: sin errores
(cd videos/X && npx hyperframes snapshot --at 0,1.5,4) # cuadros sueltos: MIRARLOS SIEMPRE antes de renderizar
python engine/audio/sfx.py videos/X                   # efectos desde sfx_events.py
(cd videos/X && npx hyperframes render --workers 4 -o out/mudo.mp4)   # ~2,5 s por segundo de video en CPU
python engine/audio/mezcla.py videos/X                # mezcla −14 LUFS + out/mudo.mp4 → final.mp4
```
Instalación: `npm install` (HyperFrames fijado en 0.9.26) y `pip install -r requirements.txt`; requiere Node ≥ 22 y ffmpeg.

## Reglas que nunca se rompen (detalle en docs/)
1. **Estilo motion graphics**: 2D (tipografía, tarjetas, terminal, diagramas que se arman) con **profundidad dada por la cámara** (`docs/CAMARA.md`: capas a distinta z, paralaje, piso en perspectiva). Sin three.js como base: tarda mucho en renderizar; 3D real solo para un plano puntual si se pide.
2. Estética: tema cyber/HackTheBox de `assets/marca.css` (azul-negro + lima). **Color = significado**: énfasis = `--acc`, verde+✓ ok, ámbar+⚠ aviso, error = bloque rojo relleno+✕. IBM Plex Sans/Mono. Sin scanlines, sin HUD/esquinas, sin mayúsculas espaciadas, sin texto de fuente al final. Paso = "Paso 1 de 7" en sans. Siempre `var(--…)`, nunca colores fijos.
3. Firma `@ayrtonnacer` al inicio y al final, **con el acento del tema**, sola (sin punto ni adornos). Lo resaltado es lo que se debe recordar.
4. CTA multiplataforma: "Dale like" (texto) / "dale me gusta" (voz) + "Seguime para aprender más de <tema>". Nunca "guardalo".
5. Voz: Daniela (Piper). Palabras simples, no leer la terminal ni los carteles; "memoria", no "pendrive"; "me gusta", no "like". Pronunciación por diccionario, no a ojo.
6. Audio (`docs/AUDIO.md`): 4 capas (voz, música, efectos, ambiente), −14 LUFS, efectos audibles pero bajo la voz (ducking), música con fades ajustada al largo, **whoosh en el pico de cada movimiento de cámara**, silencio como recurso. HyperFrames renderiza mudo; el audio lo mezcla `mezcla.py`.
7. **Guion**: una idea por reel, loop abierto en el hook y cerrado en el payoff, hook ≤ 3 s sin muletillas de IA, ≤ duración × 2,3 palabras. El cuadro 0 ya muestra la idea (es la miniatura).
7b. **Checkpoint**: mostrar el guion (voz + una línea por escena con su movimiento de cámara) y esperar aprobación ANTES de animar.
8. Cambiar UNA cosa por vez y mostrar cuadros (`snapshot`) antes de renderizar. Subtítulos solo si Ayrton los pide.
9. Contrato HyperFrames (`/hyperframes`): timeline pausado registrado en `window.__timelines`, nada de `Date.now()`/`Math.random()`/red, `fromTo` en escenas, ids únicos con prefijo por escena, posiciones de cámara por `data-x/y/z` (nunca `transform` en CSS).
10. Terminar cada video agregando a `docs/DECISIONES.md` lo que el usuario corrigió y a `pronunciacion.json` cada palabra nueva.

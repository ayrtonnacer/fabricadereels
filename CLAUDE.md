# Fábrica de reels — manual de operación

Repo de @ayrtonnacer para producir reels verticales (1080×1920, 30 fps, 30–60 s) que explican programación, matemática, ciberseguridad y Linux **sin mostrar la cara**.
Flujo: **Ayrton pega una fuente (link o tema) → Claude escribe el guion → Ayrton lo aprueba → plan → se anima (HyperFrames + three.js: un set 3D recorrido por una cámara continua) → voz Piper (Daniela) + efectos + música → mp4.**

Cuando Ayrton diga "hacé un reel de <fuente>" (o `/reel`): seguí **`docs/5-tecnica/FLUJO.md`** paso a paso. Cada paso dice qué leer, qué comando correr y cuándo está terminado.

## Qué leer (solo lo vigente; nada más hace falta para hacer un reel)
| Cuándo | Documento |
|---|---|
| Siempre, al empezar y antes de entregar | `docs/1-canal/PREFERENCIAS.md` — gustos y errores de Ayrton, por tema (lo vigente, sin historia) |
| Al escribir el guion | `docs/3-guion/GUION.md` · `docs/1-canal/PUBLICO.md` |
| Al planear y animar | `docs/2-estilo/ESTILO.md` (look, portada, texto, subtítulos) · `docs/2-estilo/CAMARA.md` (gramática de cámara y recetas) · `docs/5-tecnica/THREEJS.md` (funciones de la librería 3D) |
| Al hacer el sonido | `docs/2-estilo/AUDIO.md` |
| Para HyperFrames (contrato, CLI, bloques) | skills `/hyperframes`, `/hyperframes-cli`, `/hyperframes-registry`. Donde choquen con este manual (voz, audio, estética), **gana este manual** |

Solo de consulta (no leer de corrido): `docs/BIBLIA.md` (mapa de todo), `docs/1-canal/CANAL.md` (visión), `BITACORA.md` y `DECISIONES.md` (historial: contienen decisiones viejas ya reemplazadas), `docs/4-referencias/` (mediciones), `docs/2-estilo/GLOSARIO-EDICION.md` (vocabulario de cine para hablar con Ayrton), `docs/5-tecnica/MEDICION.md`, `FISICA.md`, `MANIM.md`.
**Si dos documentos se contradicen**, el orden es: lo que Ayrton diga en la conversación → este archivo → `PREFERENCIAS.md` → el resto. Y se corrige el documento equivocado en el mismo commit.

## Estructura
- `videos/<AAAA-MM-tema>/` — un video = un proyecto HyperFrames. **Se escriben a mano solo 5 cosas:**
  - `guion.md` y `plan.md` — el guion aprobado y el plan de cámara.
  - `video.json` — **única fuente de verdad de los tiempos**: escenas (`id`, `d`), líneas de voz (`t`, `texto`), audio, `estado`.
  - `assets/set.js` — **el set 3D del reel**: estaciones, objetos, rótulos y la cámara, todo en tiempo global del video.
  - `compositions/cierre.html` — el CTA (solo se cambia el tema).
  - `sfx_events.py` — los efectos, por significado.
  - Se generan solos (no editar): `index.html`, `assets/tiempos.js`, `compositions/<escena>.html` (un "plano" por escena), `compositions/subtitulos.html`. Salidas ignoradas por git: `out/`, `audio/`, `final.mp4`.
  - Librería (copiada de la plantilla, igual en todos): `assets/escena3d.js`, `movimiento.js`, `marca.css`, `three.*.js`, `gsap.min.js`, `fonts/`. Nada de CDN: el render no usa la red.
- `videos/_plantilla/` — punto de partida que **ya cumple todas las reglas** (portada, gancho, set de 3 estaciones, cierre). `videos/2026-11-tokens-1-v2/` — el reel de referencia del estilo aprobado. `videos/_archivo/` — versiones viejas: **no copiar de ahí**. Estado de cada video: `videos/LEEME.md`.
- `engine/` — `reel.py` (un comando por etapa), `verificar.py` (reglas del canal), `tiempos.py`, `subtitulos.py`, `audio/` (voz, efectos, mezcla, `pronunciacion.json`), `analisis/` (medición), `fisica.mjs`, `themes/` (temas viejos).
- `docs/` — ver tabla de arriba. `docs/4-referencias/material/` — lo que pasa Ayrton. `docs/media-kit/` — sistema de diseño de la marca.
- `assets/` — `voces/` (Piper, partido en 3), `musica/`, `sfx/propios/` (sonidos de marca), `referencias/` (videos de referencia).

## Comandos (desde la raíz del repo)
```
python engine/reel.py nuevo AAAA-MM-tema      # video nuevo desde la plantilla
python engine/reel.py guion videos/X          # revisa guion y voz (ritmo, gancho, CTA, palabras prohibidas) ANTES del OK de Ayrton
python engine/reel.py voz videos/X            # voz + subtítulos + tiempos (correr cada vez que cambia video.json)
python engine/reel.py revisar videos/X        # reglas del canal + contrato HyperFrames: 0 errores antes de seguir
python engine/reel.py cuadros videos/X        # cuadros clave en una hoja: MIRARLA SIEMPRE antes de renderizar
python engine/reel.py encuadre "cámara" "mira" "punto" …   # dónde cae en pantalla un punto 3D (sin renderizar)
python engine/reel.py render videos/X         # efectos + render mudo + mezcla → final.mp4  (≈ 2 s por segundo de video)
python engine/reel.py audio videos/X          # solo efectos + mezcla
python engine/reel.py medir videos/X          # mide final.mp4 contra las metas (agregar --escuchar para la pronunciación)
python engine/reel.py entregar videos/X       # copia liviana + portada + lista de cierre
python engine/reel.py estado                  # en qué etapa está cada video
```
Las sesiones de la nube se preparan solas (`.claude/hooks/session-start.sh`: ffmpeg, Python, `node_modules`, banco de efectos). En otro entorno: `bash engine/preparar.sh` (Node ≥ 22, ffmpeg; HyperFrames fijado en 0.9.26).
Herramientas sueltas (las usa `reel.py`): `engine/audio/voz.py`, `sfx.py`, `mezcla.py`, `escuchar.py`; `engine/analisis/medir.py`, `comparar.py`, `arrastre.py`, `barro.py`, `encuadre.py`, `movimientos.py`, `biblia.py`; `node engine/fisica.mjs` (física horneada).

## Reglas que nunca se rompen
`python engine/reel.py revisar` chequea solo las marcadas con ⚙; las demás se miran en los cuadros.
1. **Un set 3D, una cámara continua.** Todo objeto en three.js r187 con `assets/escena3d.js`; el texto es HTML encima. El reel es un plano secuencia: la cámara **viaja rápido (≈ 0,8 s) y se queda QUIETA mientras la voz nombra algo**. Único corte: al CTA. Nada decorativo sin significado; nada detrás del texto. Render ≤ 3 s por segundo de video.
2. **Estética Scale** (`assets/marca.css`): negro puro, objetos de **línea gris**, **un solo acento Foundry Tan** `--acc`, blanco solo para texto/cables/señal, Host Grotesk + Geist Mono. Color = significado (verde ✓ ok, ⚠ aviso, error = bloque rojo relleno ✕). ⚙ Siempre `var(--…)` / `P.acc`, nunca colores escritos a mano. ⚙ Sin scanlines, HUD, mayúsculas espaciadas, ni texto de fuente al final.
3. **Marca fija en todos los reels** (no se toca sin que Ayrton lo pida): ⚙ portada de 0,1 s; gancho con firma + título de 3–5 palabras (una en tan); ⚙ firma `@ayrtonnacer` sola, en tan, al inicio y al final; ⚙ boom grave en 0 s y antes del CTA, chinn cuando aterriza el CTA; música firma; voz Daniela limpia. **Lo que cambia entre reels es el medio** (set, objetos, recorrido): no calcar el reel anterior.
4. ⚙ **CTA**: pantalla "Dale like y seguime para aprender más de <tema>" · voz "Dale me gusta y seguime para aprender más de <tema>" (mismo tema; "sobre" si el tema es una frase). El foco es el CTA: firma chica debajo, sin zoom. Nunca "guardalo".
5. **Público**: la mayoría no es de IT. Se entiende sin saber nada y no tiene errores que un experto pueda marcar. Cada término nuevo llega con una imagen o ejemplo cotidiano. Datos verificados contra la fuente primaria (medir, no citar de memoria).
6. ⚙ **Guion**: una idea por reel; gancho ≤ 3 s y ≤ 10 palabras, sin muletillas de IA; loop abierto en el gancho y cerrado en el payoff; **2,4–2,8 palabras por segundo** del video completo (máximo 2,9); voz: "me gusta" no "like", "memoria" no "pendrive", no leer terminal ni carteles. Pronunciación por `pronunciacion.json`, nunca a ojo.
7. **✋ Checkpoint**: mostrar el guion (voz + una línea por escena con su plano y movimiento de cámara, en vocabulario de cine) y **esperar el OK de Ayrton antes de animar**. Salvo que él pida explícitamente "hacelo directo".
8. **Subtítulos siempre**, con barra negra, en y 1120–1320. La imagen que se lee va entre y 200 y 1100. Sin palabras sueltas en la última línea. **Mirar los cuadros antes de renderizar** y cambiar una cosa por vez.
9. ⚙ **Contrato HyperFrames**: todo es función del tiempo (sin `Math.random()`, `Date.now()`, temporizadores ni red); timeline pausado registrado en `window.__timelines`; sin `transform` en CSS; sin `<audio>` (el sonido lo mezcla `mezcla.py`: 4 capas, −14 LUFS, efectos bajo la voz, sonido del viaje de cámara en el pico de velocidad).
10. ⚙ **Los tiempos salen de la voz.** Nunca escribir segundos a mano en `set.js` ni en `sfx_events.py`: usar `cuando('l03', 'palabra')` y `ESC.<escena>.t0`. Si cambia `video.json`, correr `reel.py voz`.
11. **Medir en vez de opinar**: ante una referencia, `medir.py` primero. Antes de entregar, `reel.py medir`. Las metas (`docs/4-referencias/metas.json`) son una alarma, no un objetivo: si el ojo de Ayrton dice otra cosa, gana el ojo.
12. **Guardar todo en el repo, sin que Ayrton lo pida**: cada indicación → `docs/1-canal/BITACORA.md` (una línea con fecha) y, si cambia cómo se trabaja, → `PREFERENCIAS.md` en la sección de su tema (reemplazando lo viejo, no agregando al final). Cada archivo que pase → `docs/4-referencias/material/`. Cada palabra nueva → `pronunciacion.json`. Correcciones de un video terminado → `DECISIONES.md`.
13. **Una sola rama: `main`.** Ayrton no usa ramas ni pull requests: commitear y subir directo a `main`. Hablarle de GitHub en palabras simples y explicarle lo que se hizo con vocabulario de cine (`GLOSARIO-EDICION.md`).
14. **No publicar nada en redes** sin que Ayrton lo pida en ese momento.

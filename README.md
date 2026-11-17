# fabricadereels — el estudio de reels de @ayrtonnacer
Reels verticales (1080×1920, 30 fps, 30–60 s) que explican programación, matemática, ciberseguridad y Linux sin mostrar la cara. Un set 3D de línea gris sobre negro (three.js dentro de [HyperFrames](https://github.com/heygen-com/hyperframes)), una cámara de película que lo recorre sin cortes, voz Piper (Daniela es_AR), efectos, música firma y subtítulos.

## Cómo se trabaja
Abrí una sesión de Claude Code sobre este repo y pegá una fuente: `/reel https://…` o "hacé un reel sobre …". Claude escribe el guion, **espera tu OK**, anima, mide y te entrega el mp4. Las reglas están en `CLAUDE.md` y el paso a paso en `docs/5-tecnica/FLUJO.md`: están escritos para que cualquier modelo (también Sonnet) llegue al mismo resultado.

## Los comandos
```
python engine/reel.py nuevo AAAA-MM-tema    # video nuevo
python engine/reel.py guion videos/X        # revisa el guion antes de tu OK
python engine/reel.py voz videos/X          # voz + subtítulos + tiempos
python engine/reel.py revisar videos/X      # reglas del canal + contrato técnico
python engine/reel.py cuadros videos/X      # hoja de cuadros para mirar antes de renderizar
python engine/reel.py render videos/X       # final.mp4
python engine/reel.py medir videos/X        # números contra las metas
python engine/reel.py entregar videos/X     # copia liviana, portada y lista de cierre
python engine/reel.py estado                # en qué etapa está cada video
```
Vista previa a mano: `cd videos/X && npx hyperframes preview`.

## Instalación (fuera de la nube)
```
bash engine/preparar.sh     # Node ≥ 22 y ffmpeg instalados antes; instala HyperFrames 0.9.26, Python y el banco de efectos
```
Las sesiones de Claude Code en la nube se preparan solas.

## Mapa
- `CLAUDE.md` — reglas y comandos. `docs/BIBLIA.md` — mapa de todos los documentos.
- `videos/` — un video = una carpeta. `_plantilla/` es el punto de partida; `videos/LEEME.md` dice el estado de cada uno; `_archivo/` guarda versiones viejas.
- `engine/` — `reel.py` (comandos), `verificar.py` (reglas), voz, subtítulos, efectos, mezcla, medición.
- `assets/` — voces, música, sonidos de marca, videos de referencia.
- `docs/` — canal, estilo, guion, referencias medidas, técnica. Lo que se ordenó el 17/11/2026: `docs/REFACTOR-2026-11-17.md`.

## GitHub, en simple
Hay una sola línea de trabajo, `main`. Todo se guarda y se sube ahí; no hace falta usar ramas ni pull requests.

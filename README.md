# fabricadereels — fábrica de reels de @ayrtonnacer
Reels verticales (1080×1920, 30 fps, 30–60 s) que explican programación, matemática, ciberseguridad y Linux. Objetos 3D con three.js dentro de [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP renderizado a video), cámara que viaja en profundidad, voz Piper (Daniela es_AR), efectos, música y subtítulos.

## Instalación
```
npm install                       # HyperFrames 0.9.26 (Node ≥ 22)
pip install -r requirements.txt   # voz, audio y medición; también hace falta ffmpeg
```
El modelo de voz está partido en `assets/voces/`; `voz.py` lo arma solo.

## Cómo se trabaja
Abrí una sesión de Claude Code sobre este repo: carga `CLAUDE.md`. Pegá una fuente (`/reel https://…` o "hacé un reel sobre …"). Claude escribe el guion, espera tu OK, arma el script técnico y genera el video.
Vista previa a mano: `cd videos/X && npx hyperframes preview`.

## Mapa del repo
- `CLAUDE.md` — reglas y comandos (empezar acá). `docs/LEEME.md` — mapa de todos los documentos.
- `videos/` — un video = una carpeta (`_plantilla/` es el punto de partida; `2026-11-wifi/` el primero).
- `engine/` — scripts: voz, subtítulos, efectos, mezcla, medición.
- `assets/` — voces, música, sonidos propios (`sfx/propios/`) y los 10 videos de referencia (`referencias/`).
- `docs/` — manual, preferencias, bitácora, referencias medidas (`docs/referencias/`).

## GitHub, en simple
Hay una sola rama: `main`. Todo se guarda y se sube ahí; no hace falta usar ramas ni pull requests.

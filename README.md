# fabricadereels — fábrica de reels de @ayrtonnacer
Reels verticales de motion graphics hechos con [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP renderizado a video), con una cámara 2.5D que da profundidad sin 3D, voz Piper (Daniela es_AR), efectos y música.

## Instalación
```
npm install                       # HyperFrames 0.9.26 (Node ≥ 22)
pip install -r requirements.txt   # voz y audio; también hace falta ffmpeg
```
El modelo de voz está partido en `assets/voces/` y `voz.py` lo arma solo. Música en `assets/musica/fondo.mp3`.

## Uso con Claude Code
Abrí una sesión sobre este repo: carga `CLAUDE.md`, el comando `/reel` y las skills de HyperFrames (`.claude/skills/`). Pegá una fuente: `/reel https://…` o "hacé un reel sobre …". Claude escribe el guion, espera tu OK y genera el video.

Para editar a mano con vista previa en vivo: `cd videos/X && npx hyperframes preview` (o la app de escritorio de HyperFrames).

## Manual
`CLAUDE.md` (reglas y comandos) → `docs/FLUJO.md` (paso a paso) → `docs/CAMARA.md` (movimientos de cámara).

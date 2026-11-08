# fabricadereels — fábrica de reels de @ayrtonnacer
Reels verticales animados con HTML + three.js, voz Piper (Daniela es_AR), efectos sintéticos y música.

## Instalación
```
npm install && npx playwright install chromium
pip install -r requirements.txt        # y tener ffmpeg instalado
```
Copiar el modelo de voz a `assets/voces/` y la música a `assets/musica/fondo.mp3` (ver sus LEEME.md).

## Uso con Claude Code
Se trabaja desde Claude Code en la web (sin instalar nada local): abrí una sesión sobre este repo, que carga `CLAUDE.md` y el comando `/reel`. Pegá una fuente: `/reel https://…` o "hacé un reel sobre …". Claude escribe el guion, espera tu OK, y genera el video. Docs en `docs/`; empezá por `docs/PARTES.md`.

## Manual
Un video nuevo: `cp -r videos/_plantilla videos/AAAA-MM-tema`. Comandos en `CLAUDE.md`.

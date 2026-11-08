# fabricadereels — framework de reels de @ayrtonnacer

Framework propio para crear reels verticales (1080×1920, 45–60 s) explicativos de programación, matemática, ciberseguridad y Linux. Cada video es una página HTML (con three.js para el 3D) que se dibuja cuadro por cuadro de forma determinística y se convierte en mp4, con voz en off Piper (Daniela, es_AR), efectos y música.
Cómo funciona por dentro y en qué se parece a HyperFrames y Remotion: [`docs/FRAMEWORK.md`](docs/FRAMEWORK.md).

## Instalación
```
npm install && npx playwright install chromium
pip install -r requirements.txt        # y tener ffmpeg instalado
```
Modelo de voz en `assets/voces/` y música en `assets/musica/fondo.mp3` (ver sus `LEEME.md`; no van a git).

## Uso
Con Claude Code: abrir una sesión sobre este repo y pedir `/reel <link o tema>`. Claude escribe el guion, espera tu OK y arma el video siguiendo `CLAUDE.md` y `docs/`.

A mano:
```
./reel nuevo permisos-linux --titulo "Permisos en Linux"
./reel revisar 2026-11-permisos-linux
./reel ver 2026-11-permisos-linux          # visor en el navegador
./reel render 2026-11-permisos-linux       # → videos/2026-11-permisos-linux/final.mp4
./reel ayuda
```

## Mapa
- `engine/` — el motor (render, tiempo y escenas, transiciones, cámara 3D, dinamismo, temas, audio, revisor, visor, CLI).
- `videos/` — un video por carpeta; `_plantilla` es el punto de partida, `2026-11-parrot-usb` el video de referencia, `_demo-camara3d` la demo de cámara.
- `docs/` — reglas y guías: estilo, guion, audio, movimiento, cámara 3D, dinamismo, análisis de referencias, y `DECISIONES.md` (cada corrección de Ayrton).
- `referencias/` — un análisis por cada video de referencia estudiado.

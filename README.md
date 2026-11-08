# Claqueta

**Framework para crear reels verticales con código.** Cada video es una página HTML (con three.js para el 3D) que se dibuja cuadro por cuadro de forma determinística y se convierte en mp4, con voz en off, efectos y música. Hecho para los reels educativos de [@ayrtonnacer](https://github.com/ayrtonnacer) sobre programación, matemática, ciberseguridad y Linux.

> Una *claqueta* es la tablilla que se golpea al empezar cada toma de un rodaje.

## Qué trae
- **Render determinístico:** el mismo instante `t` da siempre el mismo cuadro (Chromium + FFmpeg), en paralelo por escenas.
- **3D con cámara estilo After Effects:** dron en primera persona, órbitas, cenital, vértigo, latigazos, desenfoque de movimiento real.
- **Transiciones con velocidad igualada** entre escenas y una guía de movimiento para que no parezcan diapositivas.
- **Audio en 4 capas:** voz Piper (es_AR, local y gratis), efectos, música y ambiente, con ducking y −14 LUFS.
- **Revisor** que chequea reglas de estilo, guion, voz y determinismo antes de renderizar.
- **Visor en el navegador:** reproduce, salta de escena en escena y avanza cuadro a cuadro.
- **Análisis de videos de referencia:** cortes, movimiento de cámara, ritmo y sonido, con un documento por video.

Cómo funciona por dentro, y en qué se parece a HyperFrames y Remotion: [`docs/FRAMEWORK.md`](docs/FRAMEWORK.md).

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
- `engine/` — el motor (render, escenas, transiciones, cámara 3D, dinamismo, temas, audio, revisor, visor, CLI).
- `videos/` — un video por carpeta; `_plantilla` es el punto de partida, `2026-11-parrot-usb` el video de referencia, `_demo-camara3d` la demo de cámara.
- `docs/` — reglas y guías: estilo, guion, audio, movimiento, cámara 3D, dinamismo, análisis de referencias, y `DECISIONES.md` (cada corrección de Ayrton).
- `referencias/` — un análisis por cada video de referencia estudiado.

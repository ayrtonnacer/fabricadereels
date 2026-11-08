# El video como un auto: partes y cómo encajan

Un reel se arma como un motor: cada parte tiene una función, una entrada, una salida y un lugar en el orden. Esta es la "ficha técnica" para describirle un video a una IA (o a una persona) con precisión.

| # | Parte | Función | Archivo / herramienta | Depende de |
|---|-------|---------|----------------------|-----------|
| 1 | **Brief** | Tema, público, objetivo, duración, tono | `videos/X/guion.md` (cabecera) | — |
| 2 | **Guion** | Texto de voz en estructura Hook→Payoff→CTA/bucle | `guion.md`, `video.json` (líneas) | Brief |
| 3 | **Imagen** | Lo que se ve, ver capas abajo | `index.html`, `engine/themes/` | Guion |
| 4 | **Sonido** | Voz, música, SFX, ambiente, mezcla | `engine/audio/*` | Guion + Tiempo |
| 5 | **Tiempo** | Duración de escenas, ritmo, cues (qué pasa en qué segundo) | `video.json` | Guion |
| 6 | **Entrega** | Render, mezcla −14 LUFS, `final.mp4`, publicación | `engine/render.mjs`, `mezcla.py` | Todo |

## Capas de la Imagen (de atrás hacia adelante)
1. **Fondo** (`bg(T)`, color, gradiente, partículas).
2. **Espacio 3D** (three.js: objetos, luces, materiales, cámara).
3. **Interfaz/diagramas** (cajas, flechas, terminal).
4. **Tipografía** (títulos, palabra gigante, subrayados que se dibujan).
5. **Overlays** (color drama, viñeta, glitch, grano).
6. **Transiciones** (entre escenas: zoom, push, whip, glitch — siempre motivadas).

## Sonido en 4 capas
Voz (−14 LUFS) · Música (con ventana y fades) · SFX (whoosh en el pico del movimiento) · Ambiente. Ducking: la voz manda.

## Cómo describir cada plano (plantilla mínima)
`escena · segundos · qué se ve · cámara (plano + movimiento) · texto en pantalla · voz · sfx · transición de salida`
Ver `docs/SHOOTING-SCRIPT.md`.

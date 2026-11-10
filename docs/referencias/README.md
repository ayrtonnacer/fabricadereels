# Referencias de movimientos de cámara y planos

Acá se guardan los scripts técnicos de reels de referencia que pasa Ayrton (uno por archivo: `AAAA-MM-<nombre>.md`), para copiar movimientos de cámara, ritmos y transiciones. Se van sumando a medida que trabajamos.

Por archivo: de dónde sale (link o descripción), y por plano: segundos, qué se ve, **movimiento de cámara** (con el nombre de `docs/CAMARA.md` si existe; si es nuevo, describirlo y agregarlo allá), transición y sonido. Al final, "qué tomamos" en una línea.

Si la referencia es un video: YouTube está bloqueado en la nube; pasarlo como archivo adjunto o describir los planos. Con el archivo, `npx hyperframes snapshot --against ref.mp4` o extraer cuadros con ffmpeg para analizarlo plano por plano.

## Cómo se analiza una referencia
Ahora no hace falta describir los planos a mano: Ayrton adjunta el **.mp4** y se corre `python engine/analisis/medir.py` (ver `docs/MEDICION.md`). Sale un script técnico **medido** (`SCRIPT-TECNICO-REFERENCIA.md`) y números comparables; se guardan en `docs/referencias/medidas/` y se resumen en `PARAMETROS.md`.

## Índice
- `medidas/` — informes medidos (`propios/` y `externos/`); `PARAMETROS.md` — tabla viva de parámetros.
- `2026-11-code-reel-studio.md` — recorrido de código (repo propio de Ayrton).

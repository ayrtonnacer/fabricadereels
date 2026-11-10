# Referencias de movimientos de cámara y planos

Acá se guardan los scripts técnicos de reels de referencia que pasa Ayrton (uno por archivo: `AAAA-MM-<nombre>.md`), para copiar movimientos de cámara, ritmos y transiciones. Se van sumando a medida que trabajamos.

Por archivo: de dónde sale (link o descripción), y por plano: segundos, qué se ve, **movimiento de cámara** (con el nombre de `docs/CAMARA.md` si existe; si es nuevo, describirlo y agregarlo allá), transición y sonido. Al final, "qué tomamos" en una línea.

Si la referencia es un video: YouTube está bloqueado en la nube; pasarlo como archivo adjunto o describir los planos. Con el archivo, `npx hyperframes snapshot --against ref.mp4` o extraer cuadros con ffmpeg para analizarlo plano por plano.

## Cómo se analiza una referencia
Ahora no hace falta describir los planos a mano: Ayrton adjunta el **.mp4** y se corre `python engine/analisis/medir.py` (ver `docs/MEDICION.md`). Sale un script técnico **medido** (`SCRIPT-TECNICO-REFERENCIA.md`) y números comparables; se guardan en `docs/referencias/medidas/` y se resumen en `PARAMETROS.md`.

## Índice
- `medidas/` — informes medidos (`propios/` y `externos/`); `PARAMETROS.md` — tabla viva de parámetros.
- `2026-11-code-reel-studio.md` — recorrido de código (repo propio de Ayrton).

## Referencias que ya pasó Ayrton (10 videos)
Análisis cualitativo y síntesis: `analisis/` (ver `analisis/LEEME-MIGRACION.md`). Números medidos: `medidas/externos/` y `PARAMETROS.md`. Videos originales: `assets/referencias/`.

## Cómo trabajan juntas las tres piezas (no se superponen)
1. **`medir.py`** (herramienta, la única vigente) → *mide*: números y un script técnico medido por video (`medidas/`).
2. **Script técnico del reel** (`videos/X/script-tecnico.md`, el "shooting script") → *decide*: es el plan de planos, cámara y sfx de NUESTRO reel; se arma mirando `PARAMETROS.md` y `analisis/SINTESIS.md`.
3. **`analisis/`** → *interpreta*: qué hace cada referencia y qué patrón copiar (lo cualitativo; lo escribe Claude mirando cuadros).
Ciclo: medir la referencia → tomar parámetros → escribir el script técnico → renderizar → `medir.py` sobre nuestro video → `comparar.py`.
`engine/analisis/previo/analizar_video.py` es el analizador viejo (flujo óptico): historial, no se usa.

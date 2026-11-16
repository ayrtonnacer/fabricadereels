# Referencias y mediciones — todo con números, en esta carpeta
| Qué | Dónde |
|---|---|
| **Biblia de estilo**: qué funciona, con cifras, y las tablas de todos los videos | `BIBLIA-DE-ESTILO.md` |
| Rangos objetivo para nuestros reels (los usan la biblia y `comparar.py`) | `metas.json` |
| Una carpeta por video de referencia | `externos/<video>/` |
| Una carpeta por reel nuestro | `propios/<reel>/` |
| Videos originales (mp4) | `../../assets/referencias/` (los nuevos se dejan en `assets/referencias/_nuevas/` y `engine/analisis/analizar_lote.py` los mide y archiva) |

Cada carpeta de video tiene: `INFORME.md` (lectura en español: cortes y transiciones, cámara, audio), `metricas.json` (los números), `hoja_resumen.jpg` (un cuadro por segundo).

## Dos usos de una referencia (Ayrton, 2026-11-16)
1. **Cómo se explica** (ej. 3Blue1Brown): analogías, orden, qué se muestra y cuándo. Se resume en `../3-guion/` y no se copia hook ni objetos.
2. **Técnica de cámara** (los reels más virales): paneos, dolly, grúa, latigazos, curvas y ritmo; ahí **el tema no importa**. `python engine/analisis/movimientos.py <externos/slug>` escribe `MOVIMIENTOS.md` (cada movimiento con nombre de cine, duración, distancia, pico, curva y 3 cuadros) y `--catalogo` junta todos en `CATALOGO-MOVIMIENTOS.md` (la receta típica de cada tipo). Límite: mide el movimiento global de la imagen; cuando el OBJETO se mueve (una vista explosionada que se separa), parece zoom de cámara. Por eso cada movimiento trae sus cuadros: se confirma mirando.

## Flujo (una sola herramienta, una sola fuente de verdad)
1. `python engine/analisis/medir.py <video> docs/4-referencias/externos/<slug>` (o `propios/<reel>` con `--transcripcion`).
2. `python engine/analisis/biblia.py` regenera las tablas de `BIBLIA-DE-ESTILO.md`.
3. Se ajusta `metas.json` si las referencias nuevas lo piden.
4. Para un reel nuestro: `python engine/analisis/comparar.py videos/X/analisis/metricas.json` dice qué número cae fuera de la meta.

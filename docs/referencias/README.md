# Referencias y mediciones — todo con números, en esta carpeta
| Qué | Dónde |
|---|---|
| **Biblia de estilo**: qué funciona, con cifras, y las tablas de todos los videos | `BIBLIA-DE-ESTILO.md` |
| Rangos objetivo para nuestros reels (los usan la biblia y `comparar.py`) | `metas.json` |
| Una carpeta por video de referencia | `externos/<video>/` |
| Una carpeta por reel nuestro | `propios/<reel>/` |
| Videos originales (mp4) | `../../assets/referencias/` |

Cada carpeta de video tiene: `INFORME.md` (lectura en español: cortes y transiciones, cámara, audio), `metricas.json` (los números), `hoja_resumen.jpg` (un cuadro por segundo).

## Flujo (una sola herramienta, una sola fuente de verdad)
1. `python engine/analisis/medir.py <video> docs/referencias/externos/<slug>` (o `propios/<reel>` con `--transcripcion`).
2. `python engine/analisis/biblia.py` regenera las tablas de `BIBLIA-DE-ESTILO.md`.
3. Se ajusta `metas.json` si las referencias nuevas lo piden.
4. Para un reel nuestro: `python engine/analisis/comparar.py videos/X/analisis/metricas.json` dice qué número cae fuera de la meta.

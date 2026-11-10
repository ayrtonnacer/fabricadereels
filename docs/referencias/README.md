# Referencias y mediciones — todo en esta carpeta
Acá está TODO lo que analizamos: videos de referencia que pasó Ayrton y nuestros propios reels.

| Qué | Dónde |
|---|---|
| Patrones aprendidos (leer antes de armar un script técnico) | `SINTESIS.md` |
| Tabla de parámetros y metas (cámara, ritmo, audio) | `PARAMETROS.md` |
| Índice de las 10 referencias | `INDICE.md` |
| Una carpeta por referencia | `externos/<video>/` |
| Una carpeta por reel nuestro | `propios/<reel>/` (+ comparaciones) |
| Recorrido de código de un repo de Ayrton | `2026-11-code-reel-studio.md` |
| Videos originales (mp4) | `../../assets/referencias/` |

Cada carpeta `externos/<video>/` o `propios/<reel>/` tiene lo mismo:
- `INFORME.md` — lectura en español de las medidas (cámara, cortes, ritmo, voz, volumen).
- `SCRIPT-TECNICO-REFERENCIA.md` — un renglón por plano, medido.
- `ANALISIS.md` — lo cualitativo (qué técnica usa y qué copiar; lo escribe Claude mirando los cuadros). Solo en las 10 referencias de Ayrton.
- `metricas.json` + `hoja_resumen.jpg` — números y hoja de cuadros.

## Cómo se combinan (no se superponen)
1. **`medir.py`** (única herramienta de medición) → genera `INFORME`, `SCRIPT-TECNICO-REFERENCIA` y `metricas.json`.
2. **`ANALISIS.md`** → interpreta qué patrón sirve. Las cifras vigentes son las de `INFORME.md`/`metricas.json`; las que pudieran quedar escritas en `ANALISIS.md` son aproximadas, de un método anterior.
3. **Script técnico del reel** (`videos/X/script-tecnico.md`) → decide planos, cámara y efectos de NUESTRO reel, usando `PARAMETROS.md` y `SINTESIS.md`.
Ciclo: medir referencia → elegir parámetros → script técnico → render → `medir.py` sobre nuestro video (se guarda en `propios/`) → `comparar.py`.

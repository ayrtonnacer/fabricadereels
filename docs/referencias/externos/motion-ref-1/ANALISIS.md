# Desglose de referencia — Mini-historia ilustrada: casa → fuego → ojo → espada → coronas (9 s)

> Referencia de motion graphics que pasó Ayrton (2026-11-09), guardada en `assets/referencias/motion-ref-1.mp4`. Cortes, ritmo y volumen: **medidos** por `engine/analisis/previo/analizar_video.py` (histórico; hoy `engine/analisis/medir.py`). Planos, movimientos y transiciones: **leídos mirando los cuadros** (en motion graphics 2D las etiquetas automáticas de movimiento no sirven: se mueven los elementos, no una cámara). Vocabulario: `docs/GLOSARIO-EDICION.md` y `docs/MOVIMIENTO.md`. Hojas de cuadros locales en `docs/referencias/analisis/motion-ref-1/` (no van a git; se regeneran con `./reel analizar`).

## Ficha
- **Archivo:** `assets/referencias/motion-ref-1.mp4` · 720x1278 · 30 fps · 9,4 s
- **Fuente:** Pinterest (archivo adjuntado por Ayrton; sin link directo)
- **Qué queremos aprender:** estructura técnica: planos, transiciones, movimientos de cámara, ritmo y sonido, para usarlos en próximos reels.

## 1. En una frase
Un sting cinematográfico sin texto: una estrella de cuatro puntas viaja de escena en escena (casa, ojo, espada, coronas) y cada corte es un destello o un parpadeo entre dos estados del mismo cuadro.

## 2. Estructura narrativa
| Bloque | Tiempo | Qué pasa |
|---|---|---|
| Hook | 0–1,5 s | Casa verde de neón bajo una estrella de cuatro puntas, fondo azul con degradado |
| Conflicto | 1,5–2,3 s | Parpadeo azul ↔ rojo: la misma casa en llamas, tres alternancias de 0,3 s |
| Giro | 2,3–4,7 s | Destello blanco: la estrella se abre y se vuelve el ojo que sangra |
| Desarrollo | 4,7–6,9 s | Una espada brillante cae del cielo hasta clavarse en la piedra |
| Payoff | 6,9–9,3 s | Manos tiran de la espada; el plano siguiente son coronas rotas que giran |
| Cierre | 9,3–9,4 s | Push-in a una corona (corte casi en el cuadro final: sirve de bucle) |

## 3. Guion técnico (planos y transiciones)
| # | Tiempo | Qué se ve | Movimiento / transición de salida | Texto |
|---|---|---|---|---|
| P1 | 0–1,5 | Casa de neón verde sobre el horizonte con reflejo; estrella de cuatro puntas que brilla arriba | Cámara casi quieta; la estrella parpadea. Corte con parpadeo a rojo | — |
| P2–P4 | 1,5–2,3 | La misma casa en dos estados: azul (calma) y rojo en llamas; se alternan tres veces en 0,3 s | Flicker A/B (corte cada ≈0,3 s); el último estado (rojo) se queda | — |
| P5 | 2,3–4,7 | Casa en llamas sostenida; luego un destello blanco llena el cuadro y la estrella crece desde el centro | Destello blanco (≈0,1 s) como puente: la estrella se convierte en el ojo | — |
| P6 | 4,7–6,9 | Ojo estilizado con sangre y un brillo de cuatro puntas en la pupila; la pupila se cierra | Match cut por forma: estrella → pupila; cae a negro | — |
| P7 | 6,9–9,3 | Espada que desciende con luces de colores; manos que la sujetan, grietas en el suelo; luego coronas que giran y se rompen | Corte seco a mitad de movimiento (la espada sigue bajando en el cuadro siguiente) | — |
| P8 | 9,3–9,4 | Corona gigante que llena el cuadro | Push-in final; el último cuadro vuelve a algo parecido al inicio (bucle) | — |

## 4. Ritmo (medido)
- 8 planos · **45.0 cortes/min** · plano medio 1.17 s (mediana 0.88 s; más corto 0.03 s, más largo 2.37 s) → ritmo **vertiginoso**.

## 5. Sonido
- Volumen **−14,2 LUFS**, rango ≈10 dB; **no hay golpes aislados** detectados: es música continua que lleva el ritmo y los parpadeos A/B caen sobre su pulso (a confirmar escuchando).
- Sin voz ni texto: el relato es solo visual.

## 6. Técnicas para tomar
| Técnica | Cómo se hace | Cómo la hacemos en Claqueta |
|---|---|---|
| Objeto portador entre cortes | La estrella de cuatro puntas aparece en la escena 1 y sigue en la escena del ojo: el espectador sigue el objeto, no la escena | Portador de `docs/MOVIMIENTO.md` §3: un mismo objeto 3D (el paquete de datos, la llave) cruza todos los cortes |
| Parpadeo A/B | Dos estados del mismo cuadro alternan cada 0,3 s antes del giro: tensión sin cambio de plano | Dos materiales/luces por escena (calma/peligro) y alternar `visible` por tiempo, en cortes de 9 cuadros |
| Destello como puente | 0,1 s de blanco une dos mundos | `destello()` de camara3d.js (ya existe) |
| Match por forma | Estrella → pupila: la forma se reutiliza | Costura «forma/iris» (a implementar) o toma `mover` hacia un círculo y corte en el centro |
| Color = significado | Azul/verde = calma, rojo = peligro, siempre | Regla 1 de CLAUDE.md: verde ok, rojo error |

## 7. Qué NO copiar
Todo el contenido (casa, espada, ojo, coronas): es una pieza de ilustración sin relación con redes ni programación; el degradado neón y el brillo de cuatro puntas son el estilo de otro autor.

## 8. Ideas para nuestros reels
- **Alerta de seguridad:** una red en calma (verde) que parpadea a rojo cuando entra un atacante, con el paquete malicioso como portador entre escenas.
- **Reel de 9 s como bucle** (hook de otra serie): el último cuadro empalma con el primero.

## Datos crudos
- `INFORME.md` y `metricas.json` de esta carpeta (medidos con `medir.py`). Resumen de patrones de todas las referencias: `referencias/SINTESIS.md`.

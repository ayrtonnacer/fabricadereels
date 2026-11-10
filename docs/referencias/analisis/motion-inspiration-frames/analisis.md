# Desglose de referencia — «Instagram doesn't reward effort, it rewards strategy»

> Referencia de motion graphics que pasó Ayrton (2026-11-09), guardada en `assets/referencias/motion-inspiration-frames.mp4`. Cortes, ritmo y volumen: **medidos** por `engine/analisis/previo/analizar_video.py` (histórico; hoy `engine/analisis/medir.py`). Planos, movimientos y transiciones: **leídos mirando los cuadros** (en motion graphics 2D las etiquetas automáticas de movimiento no sirven: se mueven los elementos, no una cámara). Vocabulario: `docs/GLOSARIO-EDICION.md` y `docs/MOVIMIENTO.md`. Hojas de cuadros locales en `docs/referencias/analisis/motion-inspiration-frames/` (no van a git; se regeneran con `./reel analizar`).

## Ficha
- **Archivo:** `assets/referencias/motion-inspiration-frames.mp4` · 720x1280 · 25 fps · 17,9 s
- **Fuente:** Pinterest (archivo adjuntado por Ayrton; sin link directo)
- **Qué queremos aprender:** estructura técnica: planos, transiciones, movimientos de cámara, ritmo y sonido, para usarlos en próximos reels.

## 1. En una frase
Un tip de redes en 18 s, narrado con una frase por beat: cada beat alterna fondo oscuro y claro, una palabra en rojo y un objeto o emoji como remate visual.

## 2. Estructura narrativa
| Bloque | Tiempo | Qué pasa |
|---|---|---|
| Hook | 0–3,2 s | «You've got the ideas and content» (foco en una bombilla) → «But your growth? still stuck» |
| Problema | 3,2–10,3 s | «Because content without an audience is just noise», «And the audience is the real money», nota «Value / No eyeballs / No impact / No earnings» |
| Giro | 10,3–12,7 s | «Instagram doesn't reward effort» → «It rewards strategy» |
| Payoff | 12,7–16,3 s | Perfil de Instagram (la solución) y «Your content's working hard, but not smart» |
| Cierre | 16,3–17,9 s | Negro, «to fix»: corte abierto (invita a seguir) |

## 3. Guion técnico (planos y transiciones)
| # | Tiempo | Qué se ve | Movimiento / transición de salida | Texto |
|---|---|---|---|---|
| P1 | 0–1,4 | Foto de bombilla sobre papel crema; «You've got the ideas and content» con «ideas» y «content» en negrita roja; mariposa | Entra con escala + giro leve; sale con atenuado | «You've got the ideas and content» |
| P2 | 1,4–3,2 | Hombre de traje con cabeza-bombilla blanca, halftone; «But your growth?» y «still stuck» abajo | Fundido por negro (la imagen se oscurece 0,3 s) hacia el siguiente | «But your growth? still stuck» |
| P3 | 3,2–4,9 | Negro puro; «Because content» con «content» en rojo brillante con resplandor | Aparece letra por letra con resplandor; luz de fondo viva | «Because content without an audience» |
| P4 | 4,9–6,0 | Fondo claro con cinta gris curva; emoji de payaso grande («is just noise») | Corte oscuro → claro (flip de fondo) | «is just noise» |
| P5 | 6,0–7,5 | Negro: maletín de dinero rotando; «And the audience / is the real money» | Corte claro → oscuro | «the real money» |
| P6 | 7,5–10,3 | Claro: nota gris con chinche roja que se llena («Value», «No eyeballs», «No impact», «No earnings»), cinta gris curva de fondo | Elementos que aparecen con rebote leve; la cinta cruza el cuadro | «Value No eyeballs No impact No earnings» |
| P7–P11 | 10,3–11,6 | Wordmark de Instagram; un círculo rojo nace de un punto y crece hasta llenar todo (revelado); «doesn't reward effort» aparece palabra por palabra | Iris desde un punto (wipe circular) y texto escalonado cada 0,3 s | «Instagram doesn't reward effort» |
| P12 | 11,6–13,1 | Fondo casi blanco: «It rewards strategy» con «strategy» en rojo | Texto por palabra; corte a oscuro | «It rewards strategy» |
| P13–P14 | 13,1–15,6 | Tarjeta de perfil de Instagram sobre negro con inclinación 3D leve; luego teclado y «Your content's working hard / But not smart» con emoji de lentes y mano | Tilt 3D de la tarjeta; objeto real (teclado) entra desde abajo | «Your content's working hard but not smart» |
| P15 | 15,6–17,9 | Negro, «to fix» con resplandor rojo | Cierre abierto sin firma | «to fix» |

## 4. Ritmo (medido)
- 15 planos · **47.2 cortes/min** · plano medio 1.19 s (mediana 1.4 s; más corto 0.28 s, más largo 2.84 s) → ritmo **vertiginoso**.

## 5. Sonido
- Volumen **−14,5 LUFS**, rango ≈15 dB: sin silencios largos. **Solo 9 golpes** medidos (3,5; 4,9; 6,1; **7,5 grave** en «the real money»; 9,7; 11,5; 12,7; 15,7; 16,5 s): poca cosa, bien puesta, sobre una cama de música.
- Un impacto por beat de contenido, no por cada elemento. Es un patrón opuesto al de los videos con golpes cada 0,3 s: acá el sonido enfatiza la idea.

## 6. Técnicas para tomar
| Técnica | Cómo se hace | Cómo la hacemos en Claqueta |
|---|---|---|
| Una frase por beat (~1,4 s) | Cada beat cambia de fondo y trae 4–6 palabras que se leen cómodas | Respetar `docs/GUION.md` (≈2,3 palabras/s) y planificar una escena corta por frase |
| Alternar oscuro/claro por beat | El contraste de fondo marca el cambio de idea sin transición elaborada | Dos fondos por tema (`--bg` y uno claro) y `salida: "corte"` |
| Una palabra en el acento por frase | «content», «growth», «noise», «money», «strategy»… | Exactamente la regla 2 de CLAUDE.md |
| Objeto/emoji como remate | Cada frase termina en una imagen concreta (payaso, dinero, teclado) | Un objeto 3D real por beat clave, no íconos genéricos |
| Resplandor en negro | El texto rojo brilla sobre negro (glow suave) | `text-shadow` con `var(--acc)`; evitar glow en loop (señal de video generado) |
| Iris desde un punto | Un círculo crece desde donde empieza la acción | Costura nueva «iris» (a implementar) |

## 7. Qué NO copiar
Los emojis y fotos de stock, la marca Instagram, el rojo/crema, el tono de «tip de marketing» y el cierre abierto «to fix» sin firma (nosotros cerramos con firma y CTA, salvo bucle).

## 8. Ideas para nuestros reels
- **Mito → realidad** (plantilla (b) de la investigación): el mismo patrón «lo que creés / es solo ruido / lo que sí funciona», una frase por beat.
- **Reel con muy poca cámara:** casi todo tipografía y un objeto por beat; sirve para temas abstractos (matemática).

## Datos crudos
- `docs/referencias/analisis/motion-inspiration-frames/planos.json` y `audio.json` (medidos). Resumen de patrones de todas las referencias: `referencias/SINTESIS.md`.

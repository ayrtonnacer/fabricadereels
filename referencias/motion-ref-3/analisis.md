# Desglose de referencia — Anuncio de prop trading: tarjetas de vidrio 3D y texto cinético (25 s)

> Referencia de motion graphics que pasó Ayrton (2026-11-09), guardada en `assets/referencias/motion-ref-3.mp4`. Cortes, ritmo y volumen: **medidos** por `engine/analizar_video.py`. Planos, movimientos y transiciones: **leídos mirando los cuadros** (en motion graphics 2D las etiquetas automáticas de movimiento no sirven: se mueven los elementos, no una cámara). Vocabulario: `docs/GLOSARIO-EDICION.md` y `docs/MOVIMIENTO.md`. Hojas de cuadros locales en `referencias/motion-ref-3/` (no van a git; se regeneran con `./reel analizar`).

## Ficha
- **Archivo:** `assets/referencias/motion-ref-3.mp4` · 720x1280 · 24 fps · 24,8 s
- **Fuente:** Pinterest (archivo adjuntado por Ayrton; sin link directo)
- **Qué queremos aprender:** estructura técnica: planos, transiciones, movimientos de cámara, ritmo y sonido, para usarlos en próximos reels.

## 1. En una frase
Un anuncio hecho como un solo plano continuo: frases cortas que cambian de palabra clave en azul, tarjetas de vidrio 3D con contadores y gráficos que entran y salen, y un logo que cierra.

## 2. Estructura narrativa
| Bloque | Tiempo | Qué pasa |
|---|---|---|
| Hook | 0–4,5 s | «What if you could trade with… without putting your own money on the line»: figura oscura, saldo que sube de $96,907 a $100,000 |
| Desarrollo | 4,5–15 s | «You got the Skills» + gráfico de barras; «They give you the funds»; «All you do is pass a simple challenge» |
| Prueba | 15–19 s | «You're trading a real funded account» con gráfico de velas |
| Payoff | 19–21 s | «You keep up to 32 % … 90 % of the profits» con anillo de progreso |
| CTA | 21–24,8 s | Logo y «All starting from $99»; 1,2 s de silencio final |

## 3. Guion técnico (planos y transiciones)
| # | Tiempo | Qué se ve | Movimiento / transición de salida | Texto |
|---|---|---|---|---|
| 0–4,5 | 0–4,6 | Figura redonda sobre semicírculo azul con una ciudad de barras detrás; la tarjeta «Balance» cuenta de $96,907 a $100,000; el texto se arma por palabras debajo | Cámara quieta con micro-paralaje; las palabras entran de a una | «What if you could trade with / without / your own money» |
| 4,6–8 | 4,6–8 | La figura sale; una tarjeta de vidrio inclinada entra con barras azules que suben y monedas; «Prop Firms come in» | Corte de elementos: lo anterior se desvanece, la tarjeta entra con perspectiva 3D | «You got the Skills» |
| 8–12 | 8–13 | Vuelve la figura; «The funds» en azul grande; una tarjeta con una curva y un círculo; la palabra «pass» se destaca | Reencuadre rápido hacia la derecha (pico de velocidad 2,3–3,9) y la tarjeta se desliza | «They give you The funds» · «All you do is pass a simple challenge» |
| 13–19 | 13–19 | Tarjeta de vidrio con una marca de verificación y luego un gráfico de velas; un anillo de luz gira alrededor | Tilt hacia abajo + acercamiento; la tarjeta rota en 3D | «to prove you can manage risk» · «You're trading a real funded account» |
| 19–21 | 19–21 | Anillo de progreso que sube 32 % → 77 % y «90 % of the profits» en azul grande | Contador animado; push-in leve | «You keep up to 90 % of the profits» |
| 21–24,8 | 21–24,8 | Fondo negro; logo de escudo azul que se dibuja; «All starting from $99» con el precio que entra con rebote | Corte a negro y logo quieto; silencio final | «All starting from $99» |

## 4. Ritmo (medido)
- 1 planos · **0.0 cortes/min** · plano medio 24.75 s (mediana 24.75 s; más corto 24.75 s, más largo 24.75 s) → ritmo **contemplativo**.

## 5. Sonido
- Volumen **−14,2 LUFS**, rango ≈13 dB; golpes medios sobre los cambios (0,7; 4,3; 5,8; 11,3; 14,6; 15,5 s).
- **Silencio de 23,3 a 24,6 s** al final: el logo se queda solo con la cola de la música (silencio como recurso).

## 6. Técnicas para tomar
| Técnica | Cómo se hace | Cómo la hacemos en Claqueta |
|---|---|---|
| Texto cinético por palabra | Una frase aparece palabra por palabra, con la clave en el acento y de tamaño mayor | `data-a` + `up` escalonado en `index.html`; palabra gigante de `dinamismo.golpe` |
| Tarjetas de vidrio 3D con perspectiva | Planos translúcidos inclinados con brillo y borde fino; contienen gráficos, contadores o iconos | `cartel()` con `MeshPhysicalMaterial` (transmisión) o plano con borde y brillo; inclinar con `rotation.y/x` |
| Un solo plano continuo | No hay cortes: los elementos entran y salen y la cámara solo se reencuadra | `rig` con tomas encadenadas sin escena nueva; `costuras` innecesarias |
| Contador animado | El saldo y el porcentaje suben de un valor a otro | `custom(id, lt)` con `Math.round(lerp(a,b,eo(u)))` |
| Silencio final | El cierre queda quieto y casi sin sonido | Regla 6 de CLAUDE.md: silencio como recurso (+ firma) |

## 7. Qué NO copiar
El tema (trading, cuentas fondeadas, precios), la paleta azul sobre negro, el logo y las promesas de ganancias: son de una empresa financiera. No usar cifras de rendimiento ni lenguaje de «gané $».

## 8. Ideas para nuestros reels
- **Contador de latencia o de puertos** como el saldo: «ping 120 ms → 12 ms» al pasar de Wi-Fi a cable.
- **Tarjeta de vidrio con el resultado de un comando** (reel de CTF): la terminal flota en 3D mientras entra el texto.

## Datos crudos
- `referencias/motion-ref-3/planos.json` y `audio.json` (medidos). Resumen de patrones de todas las referencias: `referencias/SINTESIS.md`.

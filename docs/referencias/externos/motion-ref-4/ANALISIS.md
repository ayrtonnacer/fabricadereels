# Desglose de referencia — «Los mercados corren con miedo y codicia» — psicología del trader (32 s)

> Referencia de motion graphics que pasó Ayrton (2026-11-09), guardada en `assets/referencias/motion-ref-4.mp4`. Cortes, ritmo y volumen: **medidos** por `engine/analisis/previo/analizar_video.py` (histórico; hoy `engine/analisis/medir.py`). Planos, movimientos y transiciones: **leídos mirando los cuadros** (en motion graphics 2D las etiquetas automáticas de movimiento no sirven: se mueven los elementos, no una cámara). Vocabulario: `docs/GLOSARIO-EDICION.md` y `docs/MOVIMIENTO.md`. Hojas de cuadros locales en `docs/referencias/analisis/motion-ref-4/` (no van a git; se regeneran con `./reel analizar`).

## Ficha
- **Archivo:** `assets/referencias/motion-ref-4.mp4` · 720x1278 · 30 fps · 31,6 s
- **Fuente:** Pinterest (archivo adjuntado por Ayrton; sin link directo)
- **Qué queremos aprender:** estructura técnica: planos, transiciones, movimientos de cámara, ritmo y sonido, para usarlos en próximos reels.

## 1. En una frase
Una historia en seis planos con color como significado: rojo = miedo, verde = codicia; cada palabra del texto llega con un golpe de sonido y los gráficos y siluetas explican la emoción.

## 2. Estructura narrativa
| Bloque | Tiempo | Qué pasa |
|---|---|---|
| Hook | 0–2,1 s | Saldo $40,294 que se vuelve $14,118 y llega a $0 en rojo |
| Problema | 2,1–7 s | «They misunderstand one thing: their emotions»; la figura con emociones de colores |
| Desarrollo | 7–14 s | «Markets run on fear and greed»; multitud que festeja en verde / entra en pánico en rojo |
| Giro | 12–14 s | Cápsula verde que cruza la pantalla: «this planning» |
| Solución | 14–27 s | «Know your targets. Know your risk.»; curvas de euforia y miedo; figura meditando («master the mindset»); monedas |
| CTA | 27–31,6 s | «No matter the trend» y «Save this post…» (lo que no copiamos) |

## 3. Guion técnico (planos y transiciones)
| # | Tiempo | Qué se ve | Movimiento / transición de salida | Texto |
|---|---|---|---|---|
| P1 | 0–2,1 | Barra de saldo con $40,294 en verde y otra en rojo con $14,118 que baja a $2,775, $157 y $0; figura diminuta en la barra | Corte entre verde y rojo; el número cae en picado | «traders because…» |
| P2 | 2,1–7 | Fondo negro; cabeza redonda con sombra de busto; aparecen luces de colores (emociones) sobre la cabeza; el texto escribe una palabra a la vez | Fundido por negro; las palabras entran una por una a ≈0,7 s cada una | «They misunderstand one thing / their emotions» |
| P3 | 7–12 | Titular «Markets run on fear and greed» con «fear» en rojo y «greed» en verde (gráfica tipográfica); luego multitud de siluetas con una curva que sube (verde) o cae (rojo) y la luz de fondo cambia de color | Corte seco entre verde y rojo según la emoción | «climb / everyone's euphoric / drop / panics» |
| P4 | 12–14 | Cápsula negra con una esfera verde que pasa a toda velocidad con rayas de velocidad | Paso veloz de un objeto como transición (≈0,3 s) | «this planning» |
| P5 | 14–26,9 | Frase «Know your targets. Know your risk.»; gráfico con dos curvas (euforia en verde, miedo en rojo) que se cruzan; botones «Buy Quality / Profit» se encienden; figura sentada meditando con anillos orbitando; pilas de monedas | Fundidos por negro entre bloques; las curvas se dibujan; los anillos giran | «when spikes / quality / euphoria / profits» · «master the mindset» · «this dividends» |
| P6 | 26,9–31,6 | Texto «no matter the trend.» en tipografía pesada y un llamado final a guardar la publicación | Cierre con fundido; texto que entra desde abajo | «Save this post, your future self will thank you.» |

## 4. Ritmo (medido)
- 6 planos · **9.5 cortes/min** · plano medio 5.26 s (mediana 4.77 s; más corto 1.97 s, más largo 12.83 s) → ritmo **contemplativo**.

## 5. Sonido
- Volumen **−14,2 LUFS**, rango ≈17 dB. **36 golpes medidos**, casi todos sobre la aparición de cada palabra (de 14,5 a 25 s, cada ≈0,3–0,7 s): tics de interfaz que marcan el ritmo de lectura.
- Un golpe grave en cada cambio de bloque (6,7; 9,0 s) y un brillante en el cierre de sección (12,5; 24,7 s).

## 6. Técnicas para tomar
| Técnica | Cómo se hace | Cómo la hacemos en Claqueta |
|---|---|---|
| Color = significado | Rojo y verde representan miedo y codicia en todo el video y nada más | Regla 1 de CLAUDE.md: verde ok, ámbar aviso, rojo error; en este reel el rojo = error/ataque |
| Una palabra por tic | Cada palabra entra con un clic corto; el espectador lee al ritmo del sonido | `data-a="up"` escalonado + `tick()` de sfxlib en el mismo instante |
| Titular tipográfico con dos colores | «fear» rojo y «greed» verde en un mismo titular | `<span class="rd">` y `<span class="cy">` del tema |
| Objeto que cruza como transición | Una cápsula con una esfera pasa a toda velocidad | Costura `latigazo` con un objeto portador (el paquete) |
| Curvas que se dibujan | Dos curvas se trazan y se cruzan en el gráfico | `TubeGeometry` con `drawRange` (cables de `index.html` del reel de redes) |
| Fundido por negro entre bloques | El negro separa las ideas | `salida: "oscuro"` de costuras.js |

## 7. Qué NO copiar
El CTA «Save this post, your future self will thank you»: nuestra regla 3 prohíbe «guardalo» porque no funciona en todas las plataformas. También el tema financiero, las siluetas de multitud y la paleta verde/rojo (para nosotros el verde es «ok» y el rojo «error»).

## 8. Ideas para nuestros reels
- **Mito vs realidad** con dos colores: lo que se cree (rojo ✕) y lo que pasa (verde ✓) en un reel de ciberseguridad.
- **Una palabra por tic** para un reel con voz lenta: cada término técnico entra con su clic.

## Datos crudos
- `INFORME.md` y `metricas.json` de esta carpeta (medidos con `medir.py`). Resumen de patrones de todas las referencias: `referencias/SINTESIS.md`.

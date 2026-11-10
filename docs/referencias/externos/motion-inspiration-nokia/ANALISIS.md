# Desglose de referencia — Nokia — «Who's callin' my phone?» (collage retro)

> Referencia de motion graphics que pasó Ayrton (2026-11-09), guardada en `assets/referencias/motion-inspiration-nokia.mp4`. Cortes, ritmo y volumen: **medidos** por `engine/analisis/previo/analizar_video.py` (histórico; hoy `engine/analisis/medir.py`). Planos, movimientos y transiciones: **leídos mirando los cuadros** (en motion graphics 2D las etiquetas automáticas de movimiento no sirven: se mueven los elementos, no una cámara). Vocabulario: `docs/GLOSARIO-EDICION.md` y `docs/MOVIMIENTO.md`. Hojas de cuadros locales en `docs/referencias/analisis/motion-inspiration-nokia/` (no van a git; se regeneran con `./reel analizar`).

## Ficha
- **Archivo:** `assets/referencias/motion-inspiration-nokia.mp4` · 720x1280 · 30 fps · 20 s
- **Fuente:** Pinterest (archivo adjuntado por Ayrton; sin link directo)
- **Qué queremos aprender:** estructura técnica: planos, transiciones, movimientos de cámara, ritmo y sonido, para usarlos en próximos reels.

## 1. En una frase
Un collage tipográfico retro (amarillo, rojo, crema, negro, halftone y titulares de diario) donde cada corte es un barrido o una forma que se convierte en la siguiente, todo sobre el ritmo.

## 2. Estructura narrativa
| Bloque | Tiempo | Qué pasa |
|---|---|---|
| Hook | 0–1,8 s | Póster «Who's callin' my phone?» con el 25 de Nokia |
| Desarrollo | 1,8–9,4 s | Cortes de ≈0,9 s: collages con retratos, disco giratorio de anillos, manos |
| Giro | 9,4–12,6 s | Portada de diario «Is it Keisha?», flash blanco, tablero de corcho con fotos |
| Payoff | 12,6–15,8 s | Letras gigantes «WAS IT» y «IS IT PARTY» llenan el cuadro |
| Cierre | 15,8–20 s | Negro con un ícono pixelado girando, 4 s |

## 3. Guion técnico (planos y transiciones)
| # | Tiempo | Qué se ve | Movimiento / transición de salida | Texto |
|---|---|---|---|---|
| P1 | 0–1,8 | Póster con letras apiladas; la cámara se aleja (pull-out) descubriendo «25» y el borde de Nokia | Pull-out rápido, corte en barrido con desenfoque direccional de ~0,1 s | «WHO'S CALLIN' MY PHONE?» |
| P2 | 1,8–2,8 | Bandas roja y amarilla; imagen en blanco y negro dentro; el título sube desde abajo | Inclinación hacia arriba; corte con una forma amarilla que barre | «WHO'S» |
| P3 | 2,8–3,6 | Retrato con recorte, línea roja discontinua que se dibuja alrededor, texto NOKIA / DRAKE | Rotación leve + línea que se dibuja; corte con forma negra y roja que invade | «NOKIA» |
| P4 | 3,6–7,1 | Retrato con rayos radiales (sunburst) que giran al entrar; letras gigantes «STACY» y «S A L» rotando; círculo central con el logo | Estallido radial (zoom con rayos) → travelling a la derecha → letras que giran | «STACY» |
| P5–P6 | 7,1–9,0 | Disco concéntrico (vinilo) con retratos que giran a distinta velocidad y un centro que se achica; al final una mano con anillos entra desde un lado | Giro continuo y zoom hacia el centro; el centro del disco se vuelve el siguiente plano (match por forma) | «ME FLYER TITLE» |
| P7–P8 | 9,0–9,8 | Letras rojas gigantes cortadas por el borde, mano estrechándose; después la portada de diario «THE Daily News» | Corte con las letras como cortinilla | «IS IT KEISHA?» |
| P9 | 9,8–11,0 | Diario con titular; se inclina y se acerca; destello blanco/amarillo en el corte de salida | Flash a blanco (≈0,1 s) como transición | «The Nokia edit was made by Zresin» |
| P10–P11 | 11,0–14,5 | Tablero de corcho con fotos instantáneas; letras rojas enormes «OAS IT» detrás; círculo rojo que barre; pull-out con travelling | Barrido de forma circular roja y alejamiento | «WAS IT» |
| P12 | 14,5–15,8 | Retrato sobre amarillo y bloque de texto «WAS»; push-in con travelling | Push-in + paneo | «WAS IT» |
| P13 | 15,8–20,1 | Cuadro crema vacío y luego negro con un ícono rojo pixelado pequeño que gira lento | Giro lento sostenido, fundido por negro | — |

## 4. Ritmo (medido)
- 13 planos · **35.9 cortes/min** · plano medio 1.54 s (mediana 1.27 s; más corto 0.27 s, más largo 4.3 s) → ritmo **dinámico**.

## 5. Sonido
- Volumen **−14,7 LUFS**, pico −3,3 dBFS, rango ≈16 dB. 14 golpes medios medidos.
- **Los cortes caen sobre la grilla del ritmo**: golpes a 1,76 / 2,24 / 2,72 / 3,22 / 3,67 s (≈cada 0,48 s ≈ 125 BPM) y cortes a 1,83 / 2,77 / 3,60 s: los cortes quedan a ±0,07 s de un golpe, y los planos duran 2, 4 u 8 beats.
- Entre 4,4 y 8,2 s no hay golpes de contenido: el disco giratorio corre sobre la cama musical (tensión sostenida).

## 6. Técnicas para tomar
| Técnica | Cómo se hace | Cómo la hacemos en Claqueta |
|---|---|---|
| Cortes en la grilla del ritmo | Planos de 2/4/8 beats a ≈125 BPM; el corte nunca cae entre golpes | Decidir BPM de la música antes del guion técnico; `rig.toma` con t0/t1 múltiplos del beat (ver `../../SINTESIS.md`) |
| Barrido con desenfoque direccional | Un cuadro desenfocado a lo largo del movimiento une dos planos | `costuras` `latigazo` (ya existe) + `MotionBlur` en 3D |
| Forma que barre la pantalla | Una forma de color (amarilla, negra, roja) cubre y descubre | Costura «forma/iris» (a implementar) |
| Estallido radial | Rayos que giran y la imagen entra con zoom | Shader de rayos o abanico de planos con rotación; usar como payoff, no repetirlo |
| Objeto circular que se convierte en la siguiente escena | El centro del disco se vuelve el plano siguiente | Toma `mover` hacia un objeto circular + corte en el centro (match por forma) |
| Flash blanco corto | 0,1 s de blanco en el corte hacia una escena clara | `destello()` de camara3d.js (ya existe) |

## 7. Qué NO copiar
Todo el look: paleta amarillo/rojo/crema, halftone, titulares de diario, retratos de personas reales y marca Nokia (contenido de terceros), y el recuadro 1:1 con barras negras: nuestro formato es 9:16 a pantalla completa.

## 8. Ideas para nuestros reels
- **Montaje a 125 BPM** para un reel de «5 errores» o «top de comandos»: un plano por compás.
- **Disco concéntrico** como animación del cifrado César (la rueda gira y cada anillo es un alfabeto).

## Datos crudos
- `INFORME.md` y `metricas.json` de esta carpeta (medidos con `medir.py`). Resumen de patrones de todas las referencias: `referencias/SINTESIS.md`.

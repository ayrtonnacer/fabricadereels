# El framework (cómo funciona por dentro)

Este repo es un **framework propio para hacer reels**: el mismo modelo que HyperFrames y Remotion (una página web que Chrome dibuja cuadro por cuadro y FFmpeg convierte en video), pero hecho a medida de los reels educativos de @ayrtonnacer: formato 1080×1920, voz Piper en español rioplatense, estética HackTheBox, 3D con three.js, reglas de guion y de movimiento, y un revisor que conoce las correcciones de Ayrton.

## Comparación
| | Remotion | HyperFrames | Este framework |
|---|---|---|---|
| Qué se escribe | componentes React | HTML + timeline GSAP | HTML + `video.json` + funciones de `t` (`custom`, `pose`) |
| Cómo se mueve el tiempo | la función lee el número de cuadro | el motor pausa y "salta" la animación | el motor llama `__render(t)` con `t = cuadro / 30` |
| 3D | con librerías aparte | bloques del catálogo | three.js integrado + cámara estilo After Effects (`camara3d.js`) |
| Voz, efectos, música | aparte | modelos de HeyGen (pagos) o pistas propias | Piper local (gratis) + efectos sintéticos y propios + mezcla con ducking a −14 LUFS |
| Reglas de estilo | no | genéricas (`check`) | las de Ayrton (`revisar.py`: firma, CTA, palabras prohibidas, colores del tema…) |
| Licencia / costo | paga desde 4 personas | Apache 2.0, servicios pagos aparte | propio, todo local |

## Contrato de una composición
Un video es una carpeta `videos/<AAAA-MM-tema>/` con:
- **`video.json`**: la única fuente de verdad (escenas, duraciones, voz, audio). Esquema abajo; `reel revisar` lo valida.
- **`index.html`**: lo visual. Carga un tema (`/engine/themes/cyber.css`), declara una `<section class="scene" id="sN">` por escena y llama a `installRender({SC, TOTAL, custom, pose, gl})` de `engine/lib.js`.
- **`sfx_events.py`**: los efectos, con `build(T, S)` (T = pista, S = segundo de inicio de cada escena).

`installRender` publica en la página:
- `window.__render(t)`: dibuja el instante `t` (segundos). **Tiene que ser una función pura de `t`**: el mismo `t` da siempre el mismo cuadro, y los `t` se pueden pedir en cualquier orden.
- `window.__scenes`, `window.__total`: escenas con su inicio y duración, y la duración total.
- `window.__ready = true`: cuando ya cargaron las fuentes, texturas y modelos. Nada se carga después de eso.

### Reglas de determinismo (las chequea `reel revisar`)
- Nada de reloj: ni `Date.now`, ni `performance.now`, ni `requestAnimationFrame`, ni `setTimeout`. El tiempo es `t`.
- Nada de azar sin semilla: `hash(n)` de lib.js en vez de `Math.random()`.
- Nada de transiciones ni animaciones CSS (`transition`, `@keyframes`): corren con el reloj. Se anima con `data-a` o en `custom(id, lt)`.
- Nada de cargar cosas a mitad del render.
- `id="gl"` está reservado para el canvas 3D; `.ln` es para líneas de terminal con `data-show`.

## Las piezas
| Pieza | Qué hace |
|---|---|
| `engine/lib.js` | Tiempo y escenas (`timeline`, `installRender`), animaciones declarativas `data-a="up|left|pop|fade:inicio:duración"`, `data-show`, tipeo `data-type`, barra "Paso N de M", fondo. Easings `eo`, `eio`, `eb`; `hash` para azar determinístico. |
| `engine/costuras.js` | Transiciones entre escenas con velocidad igualada (`"salida"` en video.json). `docs/MOVIMIENTO.md`. |
| `engine/dinamismo.js` | Capa opcional de dinamismo: palabra gigante con blur, sello, resalte que se dibuja, zoom lento, cursor con clic. `docs/DINAMISMO.md`. |
| `engine/camara3d.js` | Cámara 3D por tomas (dron FPV, órbita, cenital, vértigo, mover), transiciones automáticas, desenfoque de movimiento real, temblor, speed ramp, carteles 3D. `docs/CAMARA-3D.md`. |
| `engine/themes/` | Estética: `cyber.css` (por defecto), `redteam.css` (opcional), `estados.css` (chips ok/aviso/error). Todo color por variables CSS. |
| `engine/render.mjs` | Render: abre la página en Chromium (Playwright), llama `__render(t)` por cuadro, captura directo de Chrome (CDP) y codifica con FFmpeg. En paralelo por escenas. |
| `engine/servidor.mjs` | Servidor estático del repo (render y visor). |
| `engine/visor.html` | Visor en el navegador (`reel ver`): reproducir, barra de tiempo con los cortes, saltar a una escena, cuadro a cuadro, con el audio de la mezcla. |
| `engine/revisar.py` | Revisor antes de renderizar: esquema, determinismo, reglas de Ayrton, voz, costuras, tramos quietos. |
| `engine/audio/` | `voz.py` (Piper + diccionario de pronunciación), `sfxlib.py` + `sfx.py` (efectos), `mezcla.py` (4 capas con ducking, −14 LUFS; mezcla las capas que haya), `radio.py`, `cortar_teclas.py`. |
| `engine/analizar_video.py` | Desglose de un video de referencia (cortes, cámara, ritmo, sonido). `docs/ANALISIS-REFERENCIAS.md`. |
| `engine/cli.mjs` (`./reel`) | Un solo punto de entrada para todo. |

## CLI
```
./reel nuevo <tema> [--titulo "…"]     # copia la plantilla a videos/AAAA-MM-<tema>
./reel revisar <video> [--quietud]     # chequeos (rápido; --quietud renderiza un cuadro cada 0,5 s)
./reel ver <video>                     # visor en el navegador (http://127.0.0.1:8080)
./reel preview <video> 1 12 30         # cuadros sueltos → <video>/frames/
./reel render <video> [escenas…]       # revisar → voz → efectos → escenas → unir → mezcla → final.mp4
./reel voz | efectos | mezcla <video>
./reel analizar ref.mp4 --nombre x
```
`<video>` acepta la carpeta o solo su nombre (`2026-11-parrot-usb`). Variables: `WORKERS` (por defecto, los núcleos entre 2 y 4), `GPU=1`.

## Esquema de `video.json`
| Clave | Tipo | Qué es |
|---|---|---|
| `titulo` | texto | nombre del video |
| `fecha`, `fuente` | texto | AAAA-MM(-DD) y link o tema de origen |
| `steps` | número | total de pasos para la barra "Paso N de M" (0 = sin barra) |
| `scenes[]` | lista | `{id, d, gl?, plano?, salida?}`: id (`s1`…), duración en s, `gl: true` si usa 3D, `plano` (nota del guion técnico), `salida` (transición hacia la siguiente) |
| `voz` | objeto | `lineas[]` = `{id, escena, t, texto}` (t en s del video); `length_scale`, `noise_scale`, `noise_w_scale`; `efecto: "radio"` + `radio_fuerza` opcionales |
| `audio` | objeto | `musica`, `musica_desde`, `musica_db`, `sfx_gain`, `loudness`; `musica_ventana: [ini, fin]` en videos en bucle |
| `bucle` | sí/no | video en bucle (sin firma ni CTA al final) |
| `ev` | objeto | tiempos de eventos que comparten el visual y `sfx_events.py` (clics, palabras gigantes) |

## Rendimiento (medido en esta máquina, 4 núcleos, sin GPU)
- Captura: ~175 ms por cuadro en escenas HTML y ~320 ms en 3D (antes 205 y 410 con `page.screenshot`).
- El desenfoque de movimiento de la cámara 3D multiplica el costo por las muestras (hasta 12) solo en los cuadros rápidos.
- Con GPU real (`GPU=1`) el 3D baja mucho. Renderizar solo las escenas que cambiaron: `./reel render <video> s3 s5`.

## Pendiente / ideas
- Render en Docker para que el resultado sea idéntico en cualquier máquina (fuentes y Chrome fijos).
- Pruebas automáticas del motor (render de la plantilla y comparación de cuadros).
- Captura con `HeadlessExperimental.beginFrame` (lo que usa HyperFrames) si hace falta más velocidad.

# Cámara 3D estilo After Effects (recorridos, cenital, latigazos)

Pedido de Ayrton (2026-11-08): videos con **recorrido en 3D**, cambios de plano (cenital, órbita, dron en primera persona) y transiciones de video viral de IG, como se hace en After Effects, pero hechos con Claude.
Motor: `engine/camara3d.js`. Demo de referencia: `videos/_demo-camara3d/` (17 s, sin voz).

## La idea (cómo lo hace After Effects y cómo lo traducimos)
En AE se arma una **composición 3D**: capas 3D (texto, imágenes, formas) repartidas en el espacio, una **cámara** con *point of interest* y a menudo un **null** que la arrastra; se animan posición y orientación con keyframes y *Easy Ease*, se activa **motion blur** y profundidad de campo, y las transiciones salen del movimiento de la cámara (latigazo, atravesar un objeto, corte en el pico de velocidad).
El **3D Camera Tracker** de AE es otra cosa: analiza un video filmado para pegarle capas 3D encima. No lo necesitamos: nuestra escena ya es 3D (three.js), la cámara la escribimos nosotros.

| After Effects | Acá (three.js + `camara3d.js`) |
|---|---|
| Composición 3D | `THREE.Scene` con el "set" (racks, piso, objetos a escala real) |
| Capa 3D de texto | `cartel(THREE, lineas, {ancho})` — plano con texto en las fuentes y colores del tema |
| Cámara + null + keyframes | `Rig` con `toma()`s en tiempo GLOBAL: una sola cámara continua para todo el video |
| Easy Ease / gráfico de velocidad | `ease`: `suave`, `salida`, `entrada`, `latigazo`, `lineal`, `llegada` (expo.out), `acelera`/`frena` (las dos mitades de un corte), `empujon` o una función. Qué curva para qué rol: `docs/MOVIMIENTO.md` §5 |
| Auto Bézier del camino | curvas Catmull-Rom con velocidad constante (`fpv`, `mover` con `via`) |
| Motion blur (obturador 180°) | `MotionBlur`: promedia sub-cuadros reales, solo cuando la cámara va rápido |
| Wiggle de cámara en mano | `temblor(T, amp, frec)` en `rig.extra` |
| Time remapping / speed ramp | `rampa(T, [[t, vel], ...])` |
| Flash/transición de luz | `destello(T, tCorte)` sobre un `<div>` a pantalla completa |
| Profundidad / atmósfera | `scene.fog` del color del fondo (ajustado a la altura de cámara) |

## Tipos de toma (`rig.toma({...})`)
- **`fpv`** (dron en primera persona): `curva:[[x,y,z],...]`, mira hacia adelante sobre la curva y se **inclina en las curvas** (`banking`). Es el efecto del artefacto del dron. Ease `lineal` = velocidad de crucero.
- **`orbita`** (arc shot): `centro`, `radio→radioFin` (acercamiento mientras gira), `desde/hasta` en grados, `alto→altoFin`, `fov→fovFin`.
- **`cenital`** (top-down): `centro`, `alto→altoFin`, `giro:[a,b]` (rotación lenta, muy de reel). En formato 9:16 el ancho visible es chico: con `fov 50` y alto 30 entran ≈16 m de ancho.
- **`vertigo`** (dolly zoom, Hitchcock): `centro`, `de`→`a` (distancia al sujeto), `fov` inicial, `direccion`. El fov compensa la distancia (d·tan(fov/2) constante): el sujeto queda igual y el fondo se estira o se aplasta. Necesita fondo con profundidad.
- **`mover`**: dolly, truck, grúa, push-in, picada… de una pose `de:{pos,look,fov,roll}` a otra `a:{...}`, opcional `via:[...]` para curvar el camino.
- **Hueco entre tomas = transición automática**: la cámara viaja sola desde el final de una toma al comienzo de la siguiente con el ease de `rig.transicion(i, ease)`.
  - Hueco corto (0,4–0,6 s) + mucho giro + `latigazo` = **whip pan** (con el motion blur queda el barrido).
  - Hueco largo (1,5–2 s) + `suave` desde una órbita a un cenital = **grúa**.

## Recetario de transiciones "virales" (catálogo para ELEGIR, no una secuencia fija)
Es un menú. Cada reel usa solo 2–4 de estos recursos, elegidos por lo que pide SU idea; la demo `_demo-camara3d` los junta todos a propósito para mostrarlos y NO es una plantilla.

1. **Latigazo (whip pan)**: hueco de 0,5 s con ease `latigazo` + MotionBlur + whoosh en el pico (mitad del hueco). Se puede cortar de escena justo en el pico: el desenfoque tapa el corte.
2. **Zoom through (atravesar)**: `mover` con ease `entrada` hacia un objeto (fov que se cierra: 50→28), `destello` en el instante en que lo atraviesa, corte al set nuevo del otro lado. Impacto + riser antes.
3. **Grúa a cenital**: de un plano a la altura de los ojos a mirar desde arriba; ideal para "mostrar el mapa" (red, arquitectura, árbol de directorios). Dibujar algo en el piso mientras sube.
4. **Órbita + push-in**: presentar un objeto (USB, notebook, servidor) girando alrededor y acercándose.
5. **Dron FPV**: recorrido por un "lugar" de la idea (pasillo de servidores, placa madre, ciudad de datos) con temblor y banking.
6. **Travelling con paralaje**: carteles a distintas profundidades; lo cercano pasa rápido y lo lejano lento. Para cierres y listas.
7. **Match cut**: terminar una toma con una forma (círculo de un nodo, pantalla) y empezar la siguiente con la misma forma en el mismo lugar del cuadro.
8. **Speed ramp**: `rampa()` para cámara lenta en el momento clave y aceleración hacia el corte.

## Variedad entre reels (regla de la fábrica)
Lo que es IGUAL en todos los reels: la voz (Daniela), la música de fondo y la estética visual (tema, tipografía, firma). Todo lo demás cambia de un reel a otro:
- **El mundo 3D** lo dicta el tema (pasillo de servidores, placa madre, árbol de carpetas, plano cartesiano, ciudad de datos, un objeto único sobre fondo limpio…). Nunca reutilizar el mismo set en dos reels seguidos.
- **El plan de cámara** se elige por intención, no por posición en el guion. Guía de elección (opciones, no obligaciones):

| Si la idea es… | Conviene… |
|---|---|
| un lugar o recorrido ("qué hay adentro") | dron FPV |
| un objeto físico | órbita + push-in |
| un mapa, red, estructura, árbol | cenital / grúa |
| un cambio de estado o un giro | latigazo o zoom through |
| una lista o comparación | travelling con paralaje, o cámara casi quieta con cortes |
| algo abstracto (matemática) | cámara casi fija, el movimiento lo hacen los objetos |

- **Un reel puede no tener casi movimiento de cámara.** El movimiento es una herramienta, no un requisito; si la idea se entiende mejor quieta, queda quieta.
- Antes de armar el plan, mirar el del reel anterior (`rig.toma` en su `index.html`) y **no repetir la misma secuencia de tomas ni el mismo tipo de transición de salida**.
- Variar también el ritmo: un reel puede ser pausado (2 tomas largas) y otro vertiginoso (6 tomas cortas).

## Reglas (además de las de CLAUDE.md)
- **Una intención por movimiento**; cada toma acompaña UNA frase de la voz. El latigazo/corte cae entre frases.
- **Escala real** (metros): rack 0,6 × 2 m, notebook ≈0,32 m, USB ≈0,055 m. La cámara de dron va a ~1 m de altura.
- 9:16 es angosto: probar el encuadre con `preview`; los objetos tienden a quedar cortados a los costados.
- El texto que se tiene que leer va en HTML (nítido, encima) o en un `cartel` quieto/lento; nunca leer texto durante un latigazo.
- Motion blur cuesta: `max` 8–12 muestras, `umbral` alto para que solo actúe en movimientos rápidos.
- Probar SIEMPRE con `./reel preview videos/X t1 t2…` en el pico de cada transición antes de renderizar.
- Colores: `colorTema('--acc')`, nunca hex fijos de acento.

## Esqueleto mínimo
```js
import { Rig, MotionBlur, temblor, cartel, colorTema, destello } from '/engine/camara3d.js';
const rig = new Rig(THREE, cam);
rig.toma({ t0:0, t1:3.9, tipo:'fpv', curva:[[0,1,12],[0.5,1.1,4],[0,1.2,-8]], ease:x=>x });
rig.transicion(0, 'latigazo');
rig.toma({ t0:4.45, t1:8, tipo:'orbita', centro:[7,1.4,-14], radio:5, radioFin:4, desde:-60, hasta:40 });
const blur = new MotionBlur(renderer, scene, cam, { max:12, umbral:2.5 });
const colocar = t => { animarSet(t); return rig.aplicar(t); };
installRender({ SC, TOTAL, custom, pose:(id,lt,T)=>blur.render(T, colocar), gl:{renderer,scene,cam} });
```
En `video.json` todas las escenas que usan la cámara llevan `"gl": true`. La cámara usa el tiempo global `T`, así que cortar en escenas (para renderizar por partes) no rompe la continuidad.

## Pendiente / ideas
- Profundidad de campo real (BokehPass) para rack focus: cara en SwiftShader; probar con `GPU=1`.
- Sonido: whoosh en el pico de cada latigazo y riser + impacto en el zoom through (`sfx_events.py` leyendo los tiempos de las tomas).
- Referencias de Ayrton (YouTube) no se pudieron ver: el proxy de la sesión bloquea YouTube. Si hace falta analizarlas cuadro a cuadro, pasarlas como archivo o transcripción.

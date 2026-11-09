# Cámara 2.5D: profundidad sin 3D

Decisión de 2026-11-09: el estilo es **motion graphics 2D**; la profundidad la da **el movimiento de cámara** (paralaje), no modelos three.js. Renderiza en CPU ~9× más rápido que el motor 3D anterior (15 s de video en ~36 s).

## Cómo funciona
Cada escena (`compositions/<id>.html`) arma un set de piezas HTML planas a distintas profundidades y una cámara con perspectiva las recorre. Lo hace `assets/camara.js` con GSAP sobre el timeline pausado de la escena (determinístico: cada cuadro sale igual).

```
.vista  (perspectiva 1600 px, recorta)
 └ .cam    (dolly z + giros rx/ry/rz; pivote en el centro de pantalla)
    └ .mundo  (traslación x/y = a dónde mira la cámara)
       ├ fondo lejano   data-z="-1400"   → se mueve poco
       ├ estaciones     data-x/data-y, z = 0  → donde está lo que se lee
       ├ piso de grilla data-rx="90" data-y="700" → plano acostado, da perspectiva
       └ primer plano   data-z="500"     → pasa rápido delante
```
Las piezas se ubican con atributos (`data-x`, `data-y`, `data-z`, `data-rx`, `data-ry`, `data-rz`, `data-s`), nunca con `transform` en CSS (lo prohíbe HyperFrames y rompe la cámara). Lo que no debe moverse con la cámara (firma del inicio, "Paso N de M") va **fuera** de `.vista`.

```js
const cam = Camara(root, tl);                  // root = el div de la escena, tl = su timeline
cam.poner({ z: -520, rx: 20 });                // pose al cuadro 0
cam.ir(0, { z: 0, rx: 6 }, 1.6, 'expo.out');   // ir(t, pose, duración, ease)
cam.mirar(2.6, '#e-b', { z: 40, ry: -7 }, 1.0, 'power3.inOut');  // centrar una estación
```
Pose: `x`, `y` (px del mundo; 0,0 = centro), `z` (+ acerca / − aleja), `rx` (inclina), `ry` (órbita alrededor del plano z = 0), `rz` (rola).

## Movimientos (vocabulario)
| Movimiento | Pose | Para qué |
|---|---|---|
| **Aterrizaje** | de `z:-500, rx:20` a `z:0` con `expo.out` | entrada del gancho; el cuadro 0 ya muestra el titular |
| **Push-in / dolly** | `z` sube 50–200 en 1,5–3 s, `none` | mantener vida mientras se lee (sin pasarse: el titular no debe "flotar") |
| **Pan entre estaciones** | `mirar()` a otra estación, `power3.inOut`, 0,8–1,2 s, con `ry: -6…-8` que vuelve a 0 | pasar de un paso al siguiente sin cortar; el paralaje hace la profundidad |
| **Órbita** | `ry` ±6–12 alrededor de una estación | mostrar que algo es un objeto, revelar un costado |
| **Inclinar (tilt)** | `rx` 6–20 | mostrar el piso, sensación de "mirar desde arriba" |
| **Zoom through** | `z` hasta +1500 en 0,6 s, `power3.in` | transición: atravesar un objeto; la escena siguiente arranca en `z:900` y se asienta |
| **Pull-back (revelar)** | de `z:+700` pegado a un detalle a `z:0` | revelar el contexto de un dato (no en el cierre: ahí el foco es el CTA) |
| **Recorrido de código** | estación = bloque de código; zoom `z:+400…600`, después `y` = alto de línea × n.º de línea, pausa de lectura por línea, y vuelta a `z:0` | explicar un fragmento línea por línea (de code-reel-studio, `docs/referencias/`) con `zoom-click` en el zoom in/out |
| **Aterrizaje en el CTA** | desde `z:-700, rx:14` a `z:0, rx:5`, expo.out 1,1 s, y queda quieta | cierre: el foco es el llamado; la firma aparece después, chica, sin zoom |

Reglas: un movimiento = una intención. Llegadas lentas con cola larga (`expo.out`), viajes `power2/3.inOut`, salidas que aceleran (`power3.in`). En el corte entre escenas, misma dirección y velocidad a ambos lados. **El whoosh va en el pico de velocidad** (la mitad de un `inOut`, el final de un `in`). Nada de "flotar/respirar" en loop ni temblores sin motivo.

## Profundidad: qué la vende
1. Capas a distintas `z` que se cruzan en paralaje cuando la cámara se mueve en x/y (fondo de puntos lejos, glifos `{ } # $` cerca).
2. Piso de grilla acostado (`data-rx="90"`): con cualquier `rx` se ve la perspectiva.
3. Sombras largas en tarjetas (`.tarjeta`) y viñeta.
4. Desenfoque: en entradas de texto (blur → 0). Para un rack focus real entre dos planos, usar el bloque del registro (`npx hyperframes catalog --tag camera`).

## Referencias
Scripts técnicos de reels de referencia en `docs/referencias/` (Ayrton los va pasando). Cuando una referencia trae un movimiento nuevo, se agrega a la tabla de arriba.

## Profundidad en el eje z (lo que se hace en cada escena)
Para que no quede todo plano en z = 0:
- **Objetos que se conectan** (cable, onda entre dos piezas, fila de nodos): **mismo plano z**; si no, con la órbita se despegan.
- **Piezas sueltas a otra z**: rótulos, chips y títulos al frente (`data-z` 60–140); fondos lejanos (`data-z` −200 a −600).
- **Unos y ceros en primer plano** (`.bit`, `data-z` 450–700, desenfocados, en los bordes): dan paralaje y tienen sentido con el tema. Sustituyen a los puntitos de fondo (sacados el 2026-11-09).
- **Órbita leve** (`ry` ±6) en cada escena: es lo que hace visible la profundidad.
- **Escena 3D real (three.js)** cuando el espacio es el protagonista (un departamento, una sala, un objeto que se mira desde varios lados). Piloto: `videos/2026-11-wifi/compositions/payoff.html`.

## three.js: costo medido (2026-11-09, CPU sin GPU, 4 workers)
| Prueba | Tiempo de render por segundo de video |
|---|---|
| Escena CSS 3D mínima (3 tarjetas) | 0,8 s |
| Escena three.js simple (piso, grilla, notebook, router, pared, 5 anillos, luces; sin sombras ni post) | 1,8 s |
| Reel de WiFi completo, solo CSS | 1,65 s (54,6 s para 33 s) |
| Reel de WiFi con payoff en three.js (3,9 s de 3D) | 1,75 s (57,6 s para 33 s) |
El motor anterior tardaba ~20 s por segundo: no era por three.js sino por escenas pesadas y render con SwiftShader. **Regla**: three.js sí, en 1–2 escenas por reel, **simple** (sin sombras, sin postproceso, ≤ ~30 mallas, luces hemisféricas + una direccional, `setPixelRatio(1)`). Si el render de un reel pasa de ~3 s por segundo de video, simplificar o pasar esa escena a CSS.

### Cómo se integra
- `assets/three.module.js` (r160, local) y en la composición: `import('./assets/three.module.js').then(THREE => {...})` dentro del script de la escena. **El timeline se registra al final del callback** (`window.__timelines[id] = tl`).
- Canvas 1080×1920 con `alpha: true` detrás del `.vista` (chips y bits siguen siendo HTML). Todo es función del tiempo local `t` (`tl.to(st, { t: D, duration: D, ease: 'none', onUpdate: draw })`); sin `Math.random` ni reloj.
- Colores del tema leídos de las variables CSS (`getComputedStyle`), nunca fijos.
- Composición: en retrato la profundidad va "hacia arriba" de la pantalla (cámara cenital inclinada); ubicar el plano arriba de y 1100 (franja de subtítulos) apuntando la cámara a un punto más cercano que el centro del plano.

## Rendimiento
- Lo caro en CPU es el área enorme de capas con máscara o `filter`: piso ≤ 3000×3000, fondo de puntos ≤ 2200×3000. Si crece el tiempo de render, achicar esas capas antes que nada.
- `npx hyperframes render --workers 4` usa todos los núcleos.
- ¿3D de verdad? Sí, con three.js en escenas puntuales y simples (ver arriba el costo medido).

## Registro de HyperFrames (bloques listos)
Antes de construir un efecto a mano: `npx hyperframes catalog --tag camera --json` (push-in, pull-back-reveal, pan-stations, focus-rack, camera-shake, parallax-device-dive…), `--tag transition`, `--tag motion-primitive`. Se instalan como código editable con `npx hyperframes add <nombre>` y hay que adaptarlos a `marca.css`.

## Errores a no repetir al armar piezas
- **Ondas por tramos**: si una onda se dibuja en varios tramos (antes y después de una pared), la **fase se calcula con la x global**, no desde el inicio de cada tramo; si no, se corta y no hay continuidad (error marcado por Ayrton).
- **Lo que se conecta se toca**: el cable llega hasta el cuerpo del objeto (no queda flotando).
- **Una clase de pieza NO debe poner `position`** (ni `relative`): `.mundo > *` ya las pone `absolute` y la cámara las ubica con `data-x/y/z`. Una clase con `position: relative` definida después gana y la pieza cae al flujo normal, desalineada (pasó con `.laptop`/`.router` en el reel de WiFi).
- **Anillos y ondas expansivas**: no escalar un div con borde (el trazo se engorda con el zoom); usar un `<svg>` de 2×2 px con `overflow: visible` y animar `attr: { r }` del círculo.
- **Primer cuadro de cada escena**: el contenido tiene que estar ya a medias visible (opacity ≥ 0,4 y blur) en t = 0; si no, el corte muestra el fondo vacío 0,2 s y parpadea.
- **Zona segura**: todo lo que se lee entre 200 y 1330 px de alto; con la cámara en `y` positivo las piezas de abajo bajan: verificar con `snapshot`.

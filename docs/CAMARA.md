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

## Rendimiento
- Lo caro en CPU es el área enorme de capas con máscara o `filter`: piso ≤ 3000×3000, fondo de puntos ≤ 2200×3000. Si crece el tiempo de render, achicar esas capas antes que nada.
- `npx hyperframes render --workers 4` usa todos los núcleos.
- ¿3D de verdad (un objeto físico creíble)? Sigue siendo posible con three.js dentro de una escena (ver `/hyperframes` → `references/types/3d.md`), pero solo para un plano puntual: no como base del video.

## Registro de HyperFrames (bloques listos)
Antes de construir un efecto a mano: `npx hyperframes catalog --tag camera --json` (push-in, pull-back-reveal, pan-stations, focus-rack, camera-shake, parallax-device-dive…), `--tag transition`, `--tag motion-primitive`. Se instalan como código editable con `npx hyperframes add <nombre>` y hay que adaptarlos a `marca.css`.

## Errores a no repetir al armar piezas
- **Una clase de pieza NO debe poner `position`** (ni `relative`): `.mundo > *` ya las pone `absolute` y la cámara las ubica con `data-x/y/z`. Una clase con `position: relative` definida después gana y la pieza cae al flujo normal, desalineada (pasó con `.laptop`/`.router` en el reel de WiFi).
- **Anillos y ondas expansivas**: no escalar un div con borde (el trazo se engorda con el zoom); usar un `<svg>` de 2×2 px con `overflow: visible` y animar `attr: { r }` del círculo.
- **Primer cuadro de cada escena**: el contenido tiene que estar ya a medias visible (opacity ≥ 0,4 y blur) en t = 0; si no, el corte muestra el fondo vacío 0,2 s y parpadea.
- **Zona segura**: todo lo que se lee entre 200 y 1330 px de alto; con la cámara en `y` positivo las piezas de abajo bajan: verificar con `snapshot`.

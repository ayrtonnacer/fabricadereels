# Profundidad: cámara y 3D
> **Estándar actual (2026-11-09 noche): todos los objetos van en three.js (r187)** con la librería `assets/escena3d.js` (ver "Librería 3D" abajo y la guía completa en `docs/5-tecnica/THREEJS.md`). El sistema CSS 2.5D (`camara.js`) queda como alternativa para piezas puramente tipográficas, pero ya no se usa en los reels. Pedido de Ayrton: aprovechar el eje z y la perspectiva de los objetos 3D, siempre que el render no se vuelva lento (medido abajo).

## Gramática de cámara (2026-11-15, después del banco de prueba)
Lo que pidió Ayrton: cámara de película, **siempre al servicio de que se entienda**. Lo que falló en el banco v4: moverse todo el tiempo y hacer zoom de más.
1. **Mover solo en los cambios de idea.** Un movimiento clave por concepto nuevo (≈ 1 cada 5–8 s), dinámico (llegada con cola larga), con whoosh en el pico.
2. **Retener cuando se nombra.** Cuando la voz nombra un objeto, la cámara está **quieta** (≥ 1,5 s) y el objeto entero y legible. La quietud es lo que lo resalta.
3. **Plano general para relacionar.** Cuando la idea es "estas cosas son lo mismo", la cámara se aleja hasta verlas juntas y retiene (≥ 2,5 s).
4. **Plano continuo en vez de corte.** Dentro de una misma idea no se corta: el objeto se transforma en el siguiente (el píxel sale de la foto, la fila crece a planilla, la planilla se apila en bloque). Se corta solo al cambiar de tema.
5. **Nunca desenfocar ni recortar lo que se explica.** El zoom no puede dejar el objeto cortado si hay que leerlo.
6. **Las metas de `metas.json` son una alarma, no un objetivo.** Si el ojo dice que confunde, gana el ojo.
7. **Seguir anticipando (de onetake, `docs/4-referencias/material/2026-11-onetake.md`)**: la cámara apunta ~0,1 s por DELANTE del objeto (`sineInOut`) y, antes de un golpe, fija el punto de aterrizaje y va hasta él con `expoInOut`; así sigue al sujeto sin perderlo. Menos movimiento, mejor puesto.
8. **Un límite = algo que sobrevive.** En cada cambio de escena, un objeto (o un contenedor, o la cámara que empuja hasta llenar el cuadro) tiene que seguir y transformarse en lo siguiente. Se anota en el plan (columna "qué sobrevive") y se mide con `engine/analisis/arrastre.py` (meta: medio ≥ 0,5; ningún límite en 0,0 salvo el cambio de tema o el cierre del CTA).
9. **Pausas de verdad quietas**: ≥ 25 % de los cuadros sin movimiento y al menos un tramo ≥ 1 s; en una pausa no hay push-in ni flotación. **Temblor** decreciente y determinista solo en los aterrizajes. Variación de planos ≥ 4× (el más largo contra el más corto); no terminar dos planos seguidos igual; no reencuadrar con saltos iguales cada beat (metrónomo).

### Biblioteca de movimientos `assets/movimiento.js` (2026-11-15)
Funciones puras del tiempo local (sin azar ni reloj), copiadas con la plantilla por `nuevo.sh`; en una composición: `import * as M from './assets/movimiento.js'`.
| Función | Para qué |
|---|---|
| `resorte(tau, z, w)`, `entra(t, t0)`, `popIn`, `letra(t, t0, i)`, `sale(t, t1)` | entradas con carácter (la opacidad se adelanta al movimiento), escalonadas por letra, salidas que levantan y desenfocan |
| `impacto(t, tGolpe)`, `estirar(vx, vy)` | aplastar y vibrar al aterrizar; estirar según la velocidad |
| `temblor(t, tGolpe)` | temblor decreciente y determinista, cero antes del golpe: SOLO en aterrizajes |
| `latigazo`, `empuje`, `mano`/`envMano`, `camara(t, claves)`, `mirarAdelantado` | whip, empuje lento (no en pausas), flotación de mano apagable, cámara por claves con zoom logarítmico, seguimiento con adelanto |
| `morfar`, `atravesar`, `iris`, `salto`, `juntar` | **límites con arrastre**: un rect se vuelve otro; la cámara empuja hasta que un objeto llena el cuadro; un círculo se abre; un salto en arco; un grupo converge |
Probada con `node` (resorte → 1, temblor 0 antes del golpe, zoom logarítmico, `atravesar` llena el cuadro). Integrada en la plantilla: `E.ruta(t, claves, golpes)` acepta `golpes = [[tGolpe, amplitud_m, semilla], …]` (p. ej. `[[1.2, 0.012]]` para un aterrizaje con temblor de ~1 cm que decae en ~0,4 s). Sin `golpes`, se comporta igual que antes; los videos ya publicados no se tocaron. Probado en render real (2026-11-15): con amplitud 0,06 m el cuadro del golpe difiere 9 niveles de gris del cuadro sin golpe y a los 0,5 s la diferencia es ≈ 0,3 (el temblor decae solo). 0,06 es exagerado para probar; usar ~0,01–0,02 y mirar `snapshot`.

## (histórico) Cámara 2.5D sin 3D

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
| **Recorrido de código** | estación = bloque de código; zoom `z:+400…600`, después `y` = alto de línea × n.º de línea, pausa de lectura por línea, y vuelta a `z:0` | explicar un fragmento línea por línea (de code-reel-studio, `docs/4-referencias/material/2026-11-code-reel-studio.md`) con `zoom-click` en el zoom in/out |
| **Aterrizaje en el CTA** | desde `z:-700, rx:14` a `z:0, rx:5`, expo.out 1,1 s, y queda quieta | cierre: el foco es el llamado; la firma aparece después, chica, sin zoom |

Reglas: un movimiento = una intención. Llegadas lentas con cola larga (`expo.out`), viajes `power2/3.inOut`, salidas que aceleran (`power3.in`). En el corte entre escenas, misma dirección y velocidad a ambos lados. **El whoosh va en el pico de velocidad** (la mitad de un `inOut`, el final de un `in`). Nada de "flotar/respirar" en loop ni temblores sin motivo.

## Profundidad: qué la vende
1. Capas a distintas `z` que se cruzan en paralaje cuando la cámara se mueve en x/y (fondo de puntos lejos, glifos `{ } # $` cerca).
2. Piso de grilla acostado (`data-rx="90"`): con cualquier `rx` se ve la perspectiva.
3. Sombras largas en tarjetas (`.tarjeta`) y viñeta.
4. Desenfoque: en entradas de texto (blur → 0). Para un rack focus real entre dos planos, usar el bloque del registro (`npx hyperframes catalog --tag camera`).

## Referencias
Scripts técnicos de reels de referencia en `docs/4-referencias/` (Ayrton los va pasando). Cuando una referencia trae un movimiento nuevo, se agrega a la tabla de arriba.

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

## Librería 3D (`assets/escena3d.js`) — cómo se arma una escena
- Cada escena: `<canvas class="canvas3d">` + `.hud` (texto HTML) + `import('./assets/escena3d.js').then(async M => { const E = await M.crear(root); ... })`; el timeline se registra **al final**.
- Objetos listos: `E.laptop()` (sin antena; pantalla con texto de varias líneas: `.userData.pantalla.texto('1011\n0110')`; `.userData.emisor` = de dónde sale la onda), `E.router()` (con `.userData.puertoTrasero/puertoLado/puntaAntena` para conectar cables), `E.caja()` (caja biselada), `E.sombra()`, `E.antena()`, `E.globo()`, `E.pared(w,h,d)`, `E.paquete()`, `E.cable(A,B)` (crece con `.set(p)`), `E.onda({A,B,amp,lambda,s0,s1})` (senoide con brillo; **fase global**: tramos distintos empalman), `E.anillo(color, normal)` (`.emitir(p, rmax, centro)`, trazo de grosor constante). Piso de líneas con ancho real que convergen en perspectiva (automático).
- Cámara: `E.ruta(t, [{ t, p:[x,y,z], l:[x,y,z], e:'io'|'out'|'expo'|'lin'|'in' }, ...])`. Dibujo por cuadro: `E.animar(tl, duración, (t) => {...})`; todo es función del tiempo local.
- Texto sobre objetos 3D: `E.label(elemento, punto3D)` ubica un `.ancla` (HTML) sobre un punto del 3D; **actualiza la matriz de cámara antes de proyectar** (ya lo hace). El texto animado va en el hijo del `.ancla`, nunca en el `.ancla` mismo.
- Zona segura: la librería sube la imagen 170 px (`dy`) para dejar libre la franja de subtítulos (y 1120–1320).
- Composición en retrato: la profundidad va "hacia arriba" de la pantalla; cadenas de objetos en el eje z (notebook cerca → router → internet lejos) con la cámara siguiendo los datos; piezas conectadas en el mismo trazo.
- Costo: reel de WiFi 100 % en 3D = 66 s de render para 33 s (≈ 2 s por segundo de video, CPU). Regla: ≤ ~3 s por segundo; si pasa, simplificar (menos mallas, sin sombras ni postproceso).

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

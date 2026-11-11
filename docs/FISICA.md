# Física en las escenas 3D (estudio de react-three-rapier, 2026-11-11)

Ayrton pasó `github.com/pmndrs/react-three-rapier` (el wrapper de React de **Rapier**, motor de física en Rust/WASM) para entender la física con three.js. Se estudió el código (`Physics.tsx`, `RigidBody.tsx`, `utils-collider.ts`, readme). **El paquete en sí no se usa** (es React/R3F; nosotros no tenemos React ni bucle de tiempo real); **sí se usa el motor que hay debajo**, `@dimforge/rapier3d-compat` 0.19.2 (WASM embebido en el JS, sin red), y varias ideas.

## Qué problema tiene la física para nosotros
Nuestras escenas se dibujan **como función del tiempo `t`** (render determinista, `docs/THREEJS.md`): HyperFrames puede pedir el cuadro 3,2 s antes que el 1,0 s, o repetirlo. Una simulación avanza paso a paso y guarda estado, así que no se puede correr "en vivo" dentro del render.

## Solución: **hornear** la simulación
1. `videos/X/fisica.mjs` describe el mundo (piso, cuerpos, rebote, fricción). Ejemplo: `videos/_plantilla/fisica.ejemplo.mjs`.
2. `node engine/fisica.mjs videos/X/fisica.mjs` simula a paso fijo (60 Hz) y escribe `videos/X/assets/fisica.json` con posición + rotación de cada cuerpo por cuadro y la lista de **choques** `{t, a, b, v}`.
3. La escena crea `const poner = E.fisica(datos, { cubo0: malla0, … })` y en `E.animar` llama `poner(t)`: interpola entre cuadros (lerp posición, slerp rotación). Sin reloj ni azar.
4. **Los choques alimentan `sfx_events.py`**: el tiempo `t` de cada golpe es el instante exacto del efecto y `v` (m/s) da el volumen. Es lo que hace creíble el sonido sin ajustar a ojo.

Medido: 20 cubos × 5 s → 43 ms, dos corridas dan resultados **idénticos** (verificado). El costo es despreciable frente al render (≈ 2–4 s por segundo de video).

## Lo que se toma del repo
| Idea de react-three-rapier | Cómo queda acá |
|---|---|
| **Paso fijo + interpolación** (`timeStep = 1/60`, acumulador, `lerp/slerp` entre el estado previo y el actual) | El horneado usa paso fijo; `E.fisica` interpola entre cuadros. Física estable aunque el video sea a 30 fps. |
| **Autocolliders por forma** (`cuboid`, `ball`, `convexHull`, `trimesh`) | Collider simple a mano: cubo/esfera/cápsula. **Nunca `trimesh` en cuerpos que se mueven** (Rapier lo pide fijo) y casi nunca hace falta `convexHull`; un cubo con bisel se simula como cubo. |
| **Cuerpos fijos / dinámicos / cinemáticos** | Fijo = piso y paredes; dinámico = lo que cae; cinemático = lo que mueve el guion (se anima su posición por paso y empuja a los dinámicos). |
| **CCD** (`ccd`) para objetos rápidos | `setCcdEnabled(true)` en lo chico o veloz: si no, atraviesa el piso. |
| **Eventos de colisión + sensores** | Es lo más valioso: `fisica.mjs` los exporta para el audio. Un sensor sirve para "se dispara algo cuando X cruza la zona". |
| **Joints** (fijo, bisagra/revolute, esférico, prismático, resorte, cuerda) | Bisagra = tapa de la notebook; resorte = paquete que rebota; cuerda = cable colgando; prismático = pistón/servidor que se desliza. Se usan solo si el guion lo pide. |
| **Parámetros del mundo** (`gravity`, `numSolverIterations`, `allowedLinearError`, `predictionDistance`) | Gravedad ajustable por escena (en escala de reel conviene −9,81 con objetos de 0,05–0,4 m, como los reales; si se ve "lento", subir la gravedad, no escalar los objetos). Los demás, por defecto. |
| **Snapshots** (`world.takeSnapshot()`) | Idea para reintentar: guardar el estado en un instante y re-simular desde ahí (ej. cambiar solo el final del reel). Hoy no hace falta. |
| **Debug** (`<Debug/>` dibuja los colliders) | Si un objeto "flota" o se hunde, dibujar los colliders como alambre para ver el desfase. |

## Lo que NO se toma
- **React/R3F, `<Physics>`, hooks, `InstancedRigidBodies`**: no tenemos React; instancing no hace falta (docs/THREEJS.md §5).
- **Bucle en vivo (`updateLoop`, `useFrame`, `FrameStepper`)**: rompe el render determinista. Todo se hornea.
- **Interacción del usuario / controles / `Attractor`**: es video, no interactivo; el "empujón" se programa en el spec (posición inicial, `applyImpulse` en un paso dado).
- Un detalle: `scaleColliderArgs` de `utils-collider.ts` tiene un error (multiplica `s.x` tres veces en vez de x/y/z); si alguna vez se escala un collider, calcularlo a mano.

## Reglas para usarlo
- **Física solo si explica algo** (como todo lo 3D: nada decorativo). Buenos usos: paquetes cayendo en una cola, pila apilándose (stack), datos que rebotan al chocar, cable colgante, caja que se vuelca, dominó (reacción en cadena), péndulo.
- **Determinismo**: nada de `Math.random()` en el spec; posiciones y empujes explícitos. Si algo se ve mal, se cambia un número y se vuelve a hornear (el resultado cambia por completo ante cualquier cambio: es caótico).
- **Dirigir en vez de dejar al azar**: si la simulación sale fea, ajustar la posición inicial o el impulso hasta que haga lo que pide el guion; el horneado es barato, probar 5–10 variantes.
- Los objetos físicos usan el mismo esquema de color/material que el resto (`marca.css` / tema).
- `fisica.json` va a `assets/` del video (va al repo: es chico, ≈ 340 KB por 20 cuerpos × 5 s; si pasa de 1 MB, bajar a 30 fps o menos cuerpos).
- Mirar `snapshot` en el instante del choque y en el reposo antes de renderizar.

## Pendiente (cuando aparezca el primer reel con física)
Probarlo en una escena real, medir el costo de render y, si hace falta, un `E.debugFisica` para ver los colliders.

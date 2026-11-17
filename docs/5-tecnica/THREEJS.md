# three.js en la fábrica: cómo se escribe un set
Referencia de la librería `assets/escena3d.js` (three.js r187, local) y del patrón "un set, muchos planos". Molde para copiar: `videos/_plantilla/assets/set.js`. Ejemplo completo: `videos/2026-11-tokens-1-v2/assets/fabrica.js`. Reglas de cámara: `docs/2-estilo/CAMARA.md`. Look: `docs/2-estilo/ESTILO.md`.
Ante una duda de API de three.js: leer el código local (`node_modules/three` no está; usar `videos/_plantilla/assets/three.module.js` / `three.core.js`), no adivinar.

## Cómo funciona el render
HyperFrames pide cuadros sueltos (puede pedir el segundo 3,2 antes que el 1,0, o repetirlo). Por eso **cada cuadro se dibuja como función del tiempo**: nada de reloj, `requestAnimationFrame`, azar ni estado que se acumule. Para física: se hornea antes (`FISICA.md`).

## El patrón
```js
// videos/X/assets/set.js  — lo único de 3D que se escribe en cada reel
import { plano } from './escena3d.js';
import { ESC, cuando, hasta } from './tiempos.js';          // generado desde video.json + la voz

export const montar = (root, tl, id) => plano(root, tl, id, async (E) => {
  // 1) ARMAR el set una vez: estaciones, objetos, rótulos, lista de poses de cámara
  const { THREE, V, P } = E, R = E.rotulos();
  const cubo = E.contornear(E.caja(0.5, 0.5, 0.5, E.std())); cubo.position.y = 0.25; E.scene.add(cubo);
  const CAM = [{ t: 0, p: [1.7, 1.6, 3], l: [0, 0.6, 0] }, { t: 3, p: [1.5, 1.4, 2.6], l: [0, 0.6, 0], e: 'lin' }];
  // 2) DEVOLVER la función que dibuja el cuadro del segundo T (tiempo GLOBAL del video)
  return (T) => { E.ruta(T, CAM); E.pop(cubo, T, cuando('l01', 'cubo')); R.dibujar(T); };
});
```
- Cada escena de `video.json` es un **plano**: su composición (`compositions/<id>.html`, generada) llama `montar(root, tl, '<id>')`, que arma **el mismo set** y lo dibuja durante esa escena. Como todos usan el tiempo global `T`, los límites no se ven: es un plano secuencia.
- `plano()` lee de `tiempos.js` cuándo empieza y cuánto dura la escena y registra el timeline. **No se escriben duraciones a mano.**
- `E.T0`, `E.dur`, `E.id`: inicio, duración e id del plano actual (casi nunca hacen falta).

## Tiempos (`assets/tiempos.js`, generado)
| | |
|---|---|
| `ESC.gancho.t0` / `.t1` / `.d` | segundo en que empieza / termina la escena, y su duración |
| `VOZ.l03.t0` / `.t1` | inicio y fin de la frase |
| `cuando('l03')` | segundo en que empieza la línea |
| `cuando('l03', 'router')` | segundo en que la voz **empieza a decir** esa palabra (`cuando('l03','de',1)` = la segunda vez) |
| `hasta('l03', 'router')` | segundo en que termina de decirla |
| `DUR` | duración total |
La palabra se escribe como en el texto de `video.json` (da igual mayúsculas, tildes y puntuación). `reel.py revisar` avisa si no está en la línea.

## Ayudantes de tiempo (todos devuelven 0→1)
| | |
|---|---|
| `E.st(a, b, T)` | rampa lineal entre los segundos a y b |
| `E.io(a, b, T)` | arranca y frena suave |
| `E.out(a, b, T)` | llega frenando |
| `E.ventana(T, a, b, f=0.25)` | 1 entre a y b, con entrada y salida de `f` segundos |
| `E.pop(obj, T, t0, d=0.35, s=1)` | el objeto entra por escala en `t0` (antes es invisible) |
| `E.EASE.io/out/in/expo/lin(x)` | curvas sueltas; `E.clamp(x)` |

## Cámara
`E.ruta(T, CAM, GOLPES)` — `CAM = [{ t, p: [x,y,z], l: [x,y,z], e }]`: en el segundo `t` la cámara está en `p` mirando a `l`; llega desde la pose anterior con la curva `e` (`'io'` por defecto, `'out'`, `'in'`, `'expo'`, `'lin'`).
- **Retención** = repetir la misma pose en dos tiempos (`e: 'lin'`).
- `GOLPES = [[tGolpe, 0.006, semilla], …]`: temblor de aterrizaje (metros; decae solo en ≈ 0,4 s).
- FOV vertical 40°. Unidades en metros, piso en y = 0, z negativo = al fondo.
- Ayuda para poses relativas a una estación: `const K = (T, s, p, l, e) => ({ t: T, p: [S[s].x + p[0], p[1], S[s].z + p[2]], l: [S[s].x + l[0], l[1], S[s].z + l[2]], e })`.
- Probar una pose sin renderizar: `python engine/reel.py encuadre "px,py,pz" "lx,ly,lz" "x,y,z"`.

## Materiales y trazos (tema línea)
| | |
|---|---|
| `E.std()` | relleno negro que tapa lo de atrás (marca el objeto para `contornear`) |
| `E.contornear(obj, color=P.edge, px=2.2)` | le dibuja las aristas a cada malla con `E.std()`; devuelve el objeto |
| `E.basic(color, opacidad=1)` | color plano exacto (para lo tan o blanco: puntos, paquetes) |
| `E.trazo([a0, a1, b0, b1, …], color, px)` | líneas sueltas por pares de puntos (`V`), con grosor en píxeles |
| `E.caja(w, h, d, material)` | caja (malla) |
| `E.sombra(w, d)` | mancha de contacto (solo en tema sólido; en línea casi no se ve) |
| `E.textoTex(w, h)` → `{ tex, texto(str, color, tamaño, alinear) }` | textura de texto para pantallas (Geist Mono; admite `\n`) |
Colores: `P.acc` (tan), `P.hi` (blanco), `P.edge` (gris de aristas), `P.mid` / `P.piso`, `P.plate` (negro), `P.ok`, `P.warn`. Vector: `new V(x, y, z)`. three completo: `E.THREE`.
Objeto propio: `const g = new THREE.Group(); g.add(malla con E.std()); E.contornear(g); E.scene.add(g);`. Geometrías con pocos segmentos. **No usar `obj.clone()`** en objetos con `userData` (falla): construirlos de nuevo.

## Objetos listos
| | Tamaño | `userData` |
|---|---|---|
| `E.laptop()` | 0,34 m, frente hacia +z, sin antena | `pantalla.texto('1011\n0110', color, tamaño)`, `emisor` (de dónde sale la onda), `lid` |
| `E.router()` | 0,42 m, dos antenas | `pantalla`, `puertoTrasero`, `puertoLado`, `puntaAntena` |
| `E.globo()` | esfera de 0,3 m con meridianos | — |
| `E.pared(w, h, d)` | apoyada en el piso | — |
| `E.paquete(color, lado)` | cubito relleno (solo sobre cables) | — |
| `E.cable(A, B, color=P.hi, radio, holgura)` | cable con caída; **se agrega solo a la escena** | `.set(p)` crece 0→1 · `.at(s)` punto sobre el cable (para mover paquetes) |
| `E.onda({ A, B, amp, lambda, up, color })` | senoide (solo para frecuencias); se agrega sola | `.set(p)`, `.at(s)`, `.opacity(o)` |
| `E.anillo(color, normal, grosor)` | onda de radio; se agrega solo | `.emitir(p, radioMax, centro)` con p 0→1 |
Puntos locales a mundo: `obj.updateMatrixWorld(true); obj.localToWorld(obj.userData.puertoLado.clone())`.
Objetos de otros reels que se pueden copiar a `assets/`: `videos/2026-11-tokens-1-v2/assets/token3d.js` (fichas de texto con número atrás, marcos, cubitos) y `tensor3d.js` (planillas de números, foto suave, bloques).

## Rótulos HTML sobre el 3D
```js
const R = E.rotulos();
R.anclado('6 <b>tokens</b>', 'rot', new V(0, 0.98, 0), tEntra, tSale, 'css extra', 'arriba');   // sigue a un punto 3D
R.fijo('Título de <span class="acc">cuatro</span> palabras', 'titular', 90, 350, -1, tSale, 'width: 900px; font-size: 140px; text-align: left;');   // en (x, y) px
// … y al FINAL de dibujar(T), después de E.ruta:
R.dibujar(T);
```
- `anclado(html, clase, punto, tEntra, tSale, css, pos)`: `pos` = `'centro'`, `'arriba'` (queda sobre el punto) o `'izq'` (empieza en el punto). Aparece y se va solo (fundido de 0,25 s).
- `fijo(html, clase, x, y, tEntra, tSale, css)`: no se mueve con la cámara (título, firma). `tEntra = -1` = visible desde el cuadro 0.
- Clases de `marca.css`: `rot` (58 px; `<b>` en tan), `rot mono` (46 px), `titular`, `firma`, `chip`. Devuelven `{ a, d }` (contenedor y contenido) para animarlos a mano.
- `E.label(elemento, punto3D)` ubica cualquier `.ancla` sobre un punto (lo usa `R`).

## Otras
- `E.fisica(datos, { nombre: objeto })` → `poner(t)`: reproduce una simulación horneada (`FISICA.md`).
- `E.animar(tl, dur, fn)`: dibujo por cuadro en tiempo local (lo usa `plano`; directo solo en composiciones especiales).
- `crear(root, { dy, fov, piso })`: bajo nivel; `plano(root, tl, id, armar, opciones)` acepta las mismas opciones.

## Costo de render (CPU, 4 workers)
| | s de render por s de video |
|---|---|
| Plantilla (set de 3 estaciones) | 2,0 |
| Tokens v2 (5 estaciones, ~60 fichas) | ≈ 2–2,5 |
| Con entorno, biseles y sombras (tema sólido viejo) | 3,7 |
**Regla: ≤ 3.** Cada plano arma el set entero, así que el set tiene que ser liviano: decenas de mallas, pocos segmentos, sin sombras reales, sin postproceso (bloom, grano), sin entorno HDRI, `setPixelRatio(1)`. No crear objetos dentro de `dibujar(T)` (se arma todo antes; adentro solo se mueven, muestran u ocultan). Textos en pantallas: `texto()` solo redibuja si cambió.

## Lo que no se usa
OrbitControls, React/R3F, WebGPU, instancing, postprocesado, sombras reales, CDN, `Math.random()`. Manim solo para matemática que se transforma (`MANIM.md`).

## Checklist del set antes de renderizar
- ☐ Todos los tiempos con `cuando()` / `ESC` (ningún segundo escrito a mano).
- ☐ Objetos con `E.std()` + `E.contornear()`; colores solo de `P`.
- ☐ Cables tocan; ondas = anillos; sin etiquetas obvias; un solo tan por plano.
- ☐ `R.dibujar(T)` al final de `dibujar`.
- ☐ Lo que se lee, entre y 200 y 1100 (`reel.py encuadre` + cuadros).
- ☐ `reel.py revisar` sin errores.

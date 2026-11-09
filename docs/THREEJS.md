# three.js en la fábrica de reels: cómo trabajamos y qué criterios usamos
Resume la investigación de Ayrton (`docs/material/2026-11-threejs-guia-profesional-r187.md`, guía "Three.js para videos y reels con calidad profesional", r187), el artículo "100 consejos de Three.js que mejoran el rendimiento" (Utsubo, 2026) y lo que **verificamos probando** acá (r187, CPU sin GPU). La documentación oficial (threejs.org) está bloqueada desde la nube; ante una duda de API se lee el código del paquete (`node_modules/three`, `examples/jsm`) o la wiki en `raw.githubusercontent.com`. **Todo tiene que encajar con la estética HackTheBox** (azul-negro + lima; `docs/ESTILO.md`).

## 1. Stack y flujo (ya montado)
- HyperFrames renderiza cada cuadro buscando el tiempo en el timeline (determinístico): nuestras escenas 3D dibujan **como función del tiempo local** `t` (`E.animar`), sin reloj, sin `requestAnimationFrame`, sin azar. Es lo que la guía llama "render offline determinista"; no hace falta Mediabunny/Remotion/CCapture.
- `assets/escena3d.js` (librería compartida) + `three.module.js`/`three.core.js` (r187) + `RoundedBoxGeometry.js` + `RoomEnvironment.js`, todo **local** (sin CDN). Una escena = `<canvas>` + HTML encima + `crear(root)`. Detalle de uso en `docs/CAMARA.md`.
- Texto siempre HTML sobre el 3D (nítido, con la tipografía de marca); se ubica sobre puntos 3D con `E.label`.

## 2. El "look" HackTheBox en 3D (lo que hace la librería)
| Decisión | Por qué (guía) |
|---|---|
| `NeutralToneMapping`, exposición 1 | "Neutral respeta el color real: ideal para material educativo con colores de marca": el lima y el celeste salen exactos. Costo ≈ 0. |
| Entorno procedural `RoomEnvironment` (PMREM), `environmentIntensity` 0,4 | Lo que más rinde: reflejos y relleno; sin él los metales quedan planos. **Cuesta ≈ +30 % de render** pero se nota (comparado lado a lado); se mantiene. Sin archivos HDRI. |
| Key cálida suave + **contraluz celeste** + hemisférica azul | "Cálida en el key y fría en el rim dan volumen gratis"; el rim recorta las siluetas sobre el fondo oscuro. |
| Aristas **biseladas** (`RoundedBoxGeometry`) | "Ninguna arista es perfectamente filosa": diferencia entre cubo de tutorial y objeto de producto. |
| **Sombra de contacto** falsa (plano con degradé radial) | Ancla los objetos al piso; casi gratis (las sombras reales cuestan una pasada por luz). |
| Neones (`MeshBasic`, `toneMapped: false`) + halo aditivo | El lima exacto, sin que el tone mapping lo apague. |
| Piso de **tiras** con ancho en metros + niebla | Líneas que convergen al horizonte (le gustan a Ayrton); las `GridHelper` de 1 px desaparecen. |
| Materiales: metalness 0,4–0,55 en carcasas, roughness 0,35–0,5 | Valores de partida de la guía; nunca roughness 0; nada de `metalness` intermedio sin entorno. |
| Escala real (notebook 0,34 m, router 0,42 m) | Luces y proporciones creíbles. |
| FOV vertical 40° | La guía pide 20–35° para un objeto protagonista y 35–50° para escena explicativa: acá son escenas explicativas. |

## 3. Reglas de objetos y composición (correcciones de Ayrton)
- **Los cables tocan los objetos**: salen de un puerto real (`router.userData.puertoTrasero/puertoLado`, lado de la notebook) y entran **hasta el centro** del globo. Las señales de radio no tienen que encajar justo con el objeto, los cables sí.
- **Las notebooks no tienen una antena a la vista**: la onda sale de la tapa (`laptop.userData.emisor`) y se expande por el piso en anillos. Los routers sí llevan antenas.
- **Los bits caben en la pantalla**: 3 líneas de 8 dígitos, chicas, tipeadas de a poco.
- **No poner etiquetas obvias** (una pared no necesita decir "pared"; "el espectador no es idiota"). Cada rótulo tiene que aportar algo.
- Lo que se conecta comparte plano/trazo; los rótulos HTML nunca pisan el título ni la franja de subtítulos.
- Escena y encuadre: la imagen no pasa de y ≈ 1100 (`dy` de la librería), con la cámara guionada (`E.ruta`, easings `io`/`expo`/`out`), sin OrbitControls.

## 4. Costo de render (CPU, 4 workers, medido el 2026-11-09)
| Versión del reel de WiFi (33 s) | Render |
|---|---|
| r160, sin entorno, objetos de cajas | 66 s (2,0 s por segundo) |
| r187 + entorno + biseles + sombras | 122 s (3,7 s por segundo) |
Escena "router" aislada (5,2 s): actual 25 s · **sin entorno 18 s** · sin entorno ni tone mapping 17 s · sin antialias 21 s. Conclusión: el entorno es lo más caro y lo que más se nota; el tone mapping no cuesta. Con GPU (`--browser-gpu`) baja mucho. Si un reel pasa de ~4 s por segundo: quitar el entorno en las escenas donde no se luce (`crear(root, …)`), reducir segmentos de las mallas o el halo de las ondas.

## 5. Lo que NO usamos (y por qué)
- **Postprocesado** (bloom, viñeta, grano, SMAA con pmndrs): la viñeta ya es CSS; el bloom real cuesta mucho en CPU y el halo aditivo de las ondas lo reemplaza. Si algún día se agrega: HalfFloat + grano 3–8 % para evitar el banding de los degradés oscuros que Instagram/TikTok empeoran.
- **WebGPU/TSL, compute, instancing/BatchedMesh, Draco/KTX2/LOD**: nuestras escenas tienen decenas de mallas; el cuello de botella es el relleno de píxeles en CPU, no las llamadas de dibujo.
- **HDRI externos** (Poly Haven, CC0): posibles si hace falta un look de estudio; bajar el `.hdr` 1k–2k a `assets/` y usar `HDRLoader` (antes `RGBELoader`). Hoy alcanza `RoomEnvironment`.
- **Supersampling 2×** (render a 2160×3840 y bajar con lanczos): da bordes más limpios, pero cuesta ~4×; reservar para un "modo final" si algún día se publica en mejor calidad.

## 6. Consejos de los 100 de Utsubo que aplican acá
- Medir antes de optimizar (`renderer.info`); compartir materiales; no crear objetos dentro del bucle de dibujo (`E.anillo` solo regenera geometría cuando cambia el radio); `dispose()` de geometrías/texturas que se reemplazan.
- Evitar transparencias apiladas (sobredibujo): los halos son pocos y finos.
- Escalas reales y origen cerca de 0 (sin z-fight); `NoToneMapping` si se usa postprocesado.
- `Timer` reemplaza a `Clock` (r183); `PCFSoftShadowMap` no existe desde r186 (si se usan sombras reales: `PCFShadowMap` + `shadow.radius`).
- `RoomEnvironment` + PMREM: generar **una vez** por renderer (ya lo hace `crear`).

## 7. Checklist antes de entregar un reel con 3D
1. ☐ Objetos con bisel, sombra de contacto y escala real. ☐ Cables tocan; ondas continuas; sin etiquetas obvias.
2. ☐ Neones con `toneMapped:false`; colores solo de las variables del tema.
3. ☐ `snapshot` de cada escena en 3–4 instantes (inicio, medio, fin, cortes) y de las partes con texto encima.
4. ☐ Tiempo de render razonable (≈ ≤ 4 s por segundo en CPU).
5. ☐ Revisar en el teléfono el texto y el banding de fondos oscuros.

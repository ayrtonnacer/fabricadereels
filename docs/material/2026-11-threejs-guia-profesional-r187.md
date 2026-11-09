# Three.js para videos y reels con calidad profesional: guía práctica (versión r187, noviembre 2026)

La mayor mejora para tus videos no está en agregar efectos. Está en cuatro cosas de base: iluminar con un HDRI vía `scene.environment`, cuidar el color (sRGB en las texturas de color y un tone mapping elegido a propósito, AgX o Neutral), usar materiales PBR con valores realistas y renderizar cuadro por cuadro con un reloj propio, sin grabar la pantalla en tiempo real. El post-procesado y la cámara pulen lo que ya funciona; no rescatan una escena mal iluminada.

## TL;DR

- **Lo que más rinde, en orden:** (1) un HDRI de Poly Haven como `scene.environment` más una luz principal, (2) `toneMapping = AgXToneMapping` o `NeutralToneMapping` con la exposición ajustada y las texturas en el espacio de color correcto, (3) bordes biselados con roughness/metalness creíbles y (4) sombras de contacto suaves. Con solo eso el resultado deja de parecer amateur.
- **Para el video final, no grabes la pantalla.** Renderizá de forma determinista: el tiempo de la animación sale de `frame / fps`, no de un reloj. Cada cuadro se codifica a MP4 con WebCodecs, y la librería recomendada es Mediabunny: el README de mp4-muxer en GitHub dice que quedó "deprecated in favor of Mediabunny, which entirely supersedes it" y que ya no recibe correcciones. La otra opción es exportar PNGs y unirlos con ffmpeg. Si trabajás en React, Remotion con `@remotion/three` resuelve todo esto.
- **Al día con r187:** `PCFSoftShadowMap` se eliminó (`PCFShadowMap` ya es suave), `RGBELoader` ahora se llama `HDRLoader` y `PostProcessing` pasó a llamarse `RenderPipeline` en WebGPU. Según el blog oficial de la release 3.13 de GSAP (30 de abril de 2025), GSAP es "100% FREE including ALL of the bonus plugins… even for commercial use", gracias a Webflow, que había comprado GreenSock en octubre de 2024. Para WebGL conviene pmndrs/postprocessing con buffers HalfFloat, que evitan el banding.

---

## Key Findings

1. **Versión actual.** La última release es r187 (`three@0.187.0`), publicada el 30 de octubre de 2026. En r187 se reconstruyeron los environment maps PMREM, se agregó el BRDF difuso EON en `MeshPhysicalMaterial` y se deprecó `iridescenceThicknessRange`, que ahora se reemplaza por `iridescenceThicknessMinimum` y `iridescenceThicknessMaximum`. La r186 había reforzado la conservación de energía en el sombreado PBR. Si actualizás un proyecto viejo, compará capturas de antes y después: los materiales pueden verse un poco distintos.\[1\]
2. **Luces físicamente correctas.** Desde r155 el modo legacy viene apagado y después se eliminó.\[2\] Las PointLight y SpotLight se miden en candelas y caen con el cuadrado de la distancia (decay 2). Por eso una intensidad de 1 casi no ilumina, y lo normal es usar valores de decenas a cientos.\[3\] Las luces ambient, hemisphere y directional que vengan de tutoriales viejos se corrigen multiplicando su intensidad por π.\[2\]
3. **Tone mapping.** Hay tres opciones modernas. ACES Filmic da un look "cinematográfico" pero altera los colores saturados. AgX conserva mejor el tono en las luces altas y da a propósito una base de poco contraste, buena para hacer gradación después. Neutral (Khronos PBR Neutral) respeta el color real del material, lo cual lo hace ideal para producto y para material educativo con colores de marca.\[4\]\[5\]
4. **Sombras.** `PCFSoftShadowMap` se deprecó en r182 y se eliminó en r186.\[1\] `PCFShadowMap` ya es suave, y la suavidad se controla con `shadow.radius`.\[6\]
5. **Post-procesado.** pmndrs/postprocessing junta varios efectos en un solo pase, lo que lo hace más eficiente que encadenar pases con el EffectComposer nativo.\[7\] Por defecto usa buffers sRGB de 8 bits; su propio manual advierte que con ellos "colors will be clamped to [0.0, 1.0] and information loss will shift to the darker spectrum which leads to noticable banding in dark scenes", y que los buffers `HalfFloatType` "don't have these issues". Se activan con `frameBufferType: HalfFloatType`. En WebGPU el camino nativo es `RenderPipeline` con nodos TSL.\[8\]\[9\]
6. **Exportar video.** MediaRecorder graba en tiempo real: si un cuadro tarda, el video pierde fluidez. La forma correcta es fijar cada timestamp a mano con WebCodecs, así la velocidad del render no afecta el resultado.\[10\] Hoy las herramientas son Mediabunny (sucesora oficial de mp4-muxer), canvas-record y la reescritura moderna de CCapture.js, que suma WebCodecs y motion blur.\[11\]\[12\]\[13\]
7. **Assets gratis.** Poly Haven y ambientCG publican todo bajo CC0: podés usarlo comercialmente sin dar crédito. La portada de ambientCG anuncia "2000+ PBR Materials, HDRIs and more for free under the CC0 Public Domain license", gratis "without attribution - even in commercial circumstances".

---

## Details

### 1. Iluminación

**Principio:** primero el entorno (IBL) y después las luces directas. Un HDRI aporta a la vez reflejos, luz de relleno y variación sutil. Sin él, los metales y los materiales brillantes se ven planos y "de plástico", aunque tengas diez luces.

#### 1.1 HDRI con `scene.environment` (actualizado a r187)

```js
import * as THREE from 'three';
import { HDRLoader } from 'three/addons/loaders/HDRLoader.js'; // antes RGBELoader (renombrado)

const hdr = await new HDRLoader().loadAsync('/hdri/studio_small_09_2k.hdr');
hdr.mapping = THREE.EquirectangularReflectionMapping;

scene.environment = hdr;            // ilumina y refleja
scene.environmentIntensity = 1.0;   // control global (r163+)
// Opcional: usarlo también de fondo, desenfocado y tenue
scene.background = hdr;
scene.backgroundBlurriness = 0.6;
scene.backgroundIntensity = 0.4;
// Si querés fondo de color liso (típico en reels educativos):
// scene.background = new THREE.Color('#0f1115');
```

- **Fuentes gratuitas CC0:** Poly Haven (HDRIs de estudio como "studio_small", "photo_studio" y otros) y ambientCG.\[14\] Para iluminar alcanza con 1k o 2k. Solo si el HDRI se ve nítido de fondo conviene subir a 4k.
- **Sin archivo externo:** `RoomEnvironment` (en `three/addons/environments/RoomEnvironment.js`) genera un estudio neutro procedural. Pasalo por `PMREMGenerator`, `scene.environment = pmrem.fromScene(new RoomEnvironment()).texture`. Sirve como base rápida para prototipar.

#### 1.2 Esquema de 3 puntos sobre el HDRI

El HDRI hace de relleno, y encima agregás una luz principal (key) y un contraluz (rim) que separa el objeto del fondo. En un fondo oscuro, el rim light es lo que más "producto premium" aporta.

```js
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap; // ya es suave desde r182; PCFSoftShadowMap fue eliminado en r186

// KEY: cálida, a 45° arriba y al costado, proyecta la sombra
const key = new THREE.DirectionalLight('#fff1e0', 2.5);
key.position.set(3, 5, 4);
key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
key.shadow.radius = 4;          // suavidad del borde
key.shadow.bias = -0.0001;
key.shadow.normalBias = 0.02;
// Ajustá la cámara de sombra al tamaño de tu escena (más chica = sombra más nítida)
Object.assign(key.shadow.camera, { left: -3, right: 3, top: 3, bottom: -3, near: 0.5, far: 20 });
scene.add(key);

// FILL: lo aporta el HDRI; si hace falta, una luz débil y fría del lado opuesto
const fill = new THREE.DirectionalLight('#dbe8ff', 0.4);
fill.position.set(-4, 2, 2);
scene.add(fill);

// RIM / contraluz: detrás y arriba, recorta la silueta
const rim = new THREE.SpotLight('#ffffff', 60, 0, Math.PI / 6, 0.5, 2); // candelas, decay 2
rim.position.set(-2, 3, -4);
rim.target.position.set(0, 0.5, 0);
scene.add(rim, rim.target);
```

**Intensidades:** para DirectionalLight, entre 1 y 4 suele andar bien con un HDRI a intensidad 1. Para Point y Spot hacen falta valores de decenas a cientos, porque se miden en candelas y caen con el cuadrado de la distancia\[3\] (la unidad de escena equivale a 1 metro). Trabajá en escala real: un objeto de 1 unidad mide 1 metro, y si modelás a escala 100, las luces físicas dejan de comportarse como esperás.\[15\]

#### 1.3 Luces de área (softbox)

`RectAreaLight` imita una ventana o un softbox y genera reflejos rectangulares preciosos sobre metal y vidrio. Tiene límites: solo funciona con `MeshStandardMaterial` y `MeshPhysicalMaterial`, no proyecta sombras, hay que llamar a `RectAreaLightUniformsLib.init()` y tampoco aplica `sheen`.\[16\]\[17\]

```js
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
RectAreaLightUniformsLib.init();
const softbox = new THREE.RectAreaLight('#ffffff', 8, 2, 1); // color, intensidad, ancho, alto
softbox.position.set(0, 3, 2);
softbox.lookAt(0, 0.5, 0);
scene.add(softbox);
```

Una alternativa más barata y vistosa en R3F es meter `<Lightformer>` dentro de `<Environment>` (drei).\[18\] Así "pintás" softboxes en el mapa de entorno y conseguís reflejos de estudio sin el costo de una luz dinámica.

### 2. Materiales PBR

#### 2.1 ¿Standard o Physical?

| Material | Cuándo usarlo | Costo |
|---|---|---|
| `MeshStandardMaterial` | El 80% de los objetos: plástico, madera, metal, piedra, piel estilizada | Bajo |
| `MeshPhysicalMaterial` | Cuando necesitás alguna de estas capas: **clearcoat** (pintura de auto, laca, plástico barnizado), **transmission** (vidrio, agua, gemas), **sheen** (tela, terciopelo), **iridescence** (pompas de jabón, películas aceitosas, escarabajos) | Medio-alto (transmission es lo más caro) |

#### 2.2 Valores de partida recomendados

| Material | `metalness` | `roughness` | Extra |
|---|---|---|---|
| Plástico mate | 0 | 0.5–0.7 | — |
| Plástico brillante | 0 | 0.15–0.3 | `clearcoat: 1, clearcoatRoughness: 0.1` |
| Metal pulido (cromo) | 1 | 0.05–0.15 | sin HDRI se ve negro |
| Metal cepillado/anodizado | 1 | 0.3–0.5 | normal map de rayado |
| Cerámica / esmalte | 0 | 0.1–0.2 | clearcoat leve |
| Vidrio | 0 | 0–0.05 | `transmission: 1, thickness: 0.5, ior: 1.5` |
| Tela | 0 | 0.8–1 | `sheen: 1, sheenRoughness: 0.5, sheenColor` |
| Goma | 0 | 0.8–0.9 | — |

**Regla de oro:** `metalness` va en 0 o en 1, casi nunca en un punto intermedio. Y nada en el mundo real tiene `roughness: 0` perfecto: un 0.05 se ve mucho más creíble que un espejo ideal.

```js
// Pintura de auto / plástico premium
const carPaint = new THREE.MeshPhysicalMaterial({
  color: '#c1121f', metalness: 0.0, roughness: 0.4,
  clearcoat: 1.0, clearcoatRoughness: 0.08,
});

// Vidrio
const glass = new THREE.MeshPhysicalMaterial({
  color: '#ffffff', metalness: 0, roughness: 0.02,
  transmission: 1, thickness: 0.6, ior: 1.5,
  attenuationColor: new THREE.Color('#bfe6ff'), attenuationDistance: 2,
});

// Pompa / película iridiscente (r187: usar Minimum/Maximum)
const bubble = new THREE.MeshPhysicalMaterial({
  color: '#ffffff', roughness: 0.05, transmission: 1, thickness: 0.05,
  iridescence: 1, iridescenceIOR: 1.3,
  iridescenceThicknessMinimum: 100, iridescenceThicknessMaximum: 400,
});

// Terciopelo
const velvet = new THREE.MeshPhysicalMaterial({
  color: '#3a0ca3', roughness: 0.9, sheen: 1, sheenRoughness: 0.4,
  sheenColor: new THREE.Color('#b8a1ff'),
});
```

#### 2.3 Texturas (Poly Haven / ambientCG) y espacio de color

El error más común es marcar como sRGB las texturas que son datos. Solo las texturas de color (albedo/baseColor y emissive) van en sRGB. Las de normal, roughness, metalness y AO son datos y quedan en `NoColorSpace`.\[5\]

```js
const tl = new THREE.TextureLoader();
const load = (url, srgb = false) => {
  const t = tl.load(url);
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = renderer.capabilities.getMaxAnisotropy(); // nitidez en ángulos rasantes
  return t;
};

const mat = new THREE.MeshStandardMaterial({
  map:          load('/tex/wood_diff_2k.jpg', true),  // color → sRGB
  normalMap:    load('/tex/wood_nor_gl_2k.jpg'),      // OJO: versión OpenGL (_gl), no DirectX
  roughnessMap: load('/tex/wood_rough_2k.jpg'),
  aoMap:        load('/tex/wood_ao_2k.jpg'),
  normalScale: new THREE.Vector2(1, 1),
});
// Si combinás AO+roughness+metalness en un solo archivo (ORM): aoMap=R, roughnessMap=G, metalnessMap=B
```

- Las texturas de ambientCG y Poly Haven traen normal maps en versión OpenGL y en versión DirectX. Three.js usa la convención OpenGL; si cargás la DirectX, el relieve se ve "invertido". Como arreglo de emergencia: `normalScale.y = -1`.
- Para relieve fino (rayado, poros, huella dactilar) un normal map sutil suma muchísimo realismo. Combinado con una `roughnessMap` que tenga variación, rompe el aspecto "CG perfecto".
- Los modelos glTF ya declaran bien sus espacios de color, y esa es una razón más para preferir ese formato.\[5\]

### 3. Configuración del renderer

```js
const W = 1080, H = 1920; // 9:16 para reels

const renderer = new THREE.WebGLRenderer({
  antialias: true,              // MSAA nativo (si NO usás composer)
  powerPreference: 'high-performance',
  preserveDrawingBuffer: true,  // solo necesario si capturás el canvas DESPUÉS de render() (ver §7)
});
renderer.setSize(W, H, false);  // false: no toca el CSS, así podés previsualizar escalado
renderer.setPixelRatio(1);      // en export usá tamaño exacto; en preview: Math.min(devicePixelRatio, 2)

renderer.outputColorSpace = THREE.SRGBColorSpace;   // ya es el default desde r152
renderer.toneMapping = THREE.AgXToneMapping;        // o NeutralToneMapping / ACESFilmicToneMapping
renderer.toneMappingExposure = 1.0;                 // ajustá con lil-gui: 0.8–1.6 típico

renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;
```

**Cuál tone mapping elegir:**
- **Neutral:** colores de marca exactos, diagramas educativos, producto.\[19\] Es la opción menos "sorprendente".
- **AgX:** escenas con luces muy intensas o emisivos (neón, bloom). No vira los colores saturados hacia el amarillo o el blanco. De entrada se ve más lavado, así que compensá con un poco más de exposición o con contraste en post.\[4\]\[5\]
- **ACES Filmic:** look de cine con más contraste y saturación, pero altera los tonos (los rojos y naranjas saturados se corren).\[4\]\[19\]
- Probá los tres con la misma escena y quedate con uno para toda la serie de videos. La coherencia visual entre episodios vale más que el operador "ideal".

**Antialiasing para video:** el método más limpio es el **supersampling**: renderizás a 2x (2160×3840) y reducís a 1080×1920 al codificar, con ffmpeg y `-vf scale=1080:1920:flags=lanczos`. Elimina el aliasing de bordes finos y el parpadeo de reflejos especulares que el MSAA no resuelve. Como no estás en tiempo real, el costo no importa.

### 4. Post-procesado

#### 4.1 ¿Qué librería?

| Opción | Cuándo |
|---|---|
| **pmndrs/postprocessing** (WebGL) | Recomendada. Junta los efectos en un solo pase, trae SMAA, bloom, DOF, viñeta, ruido, SSAO/N8AO, tone mapping y LUT. En R3F se usa con `@react-three/postprocessing`.\[20\]\[21\] |
| **EffectComposer nativo** (`three/addons/postprocessing`) | Cuando necesitás un pase concreto de los ejemplos oficiales (GTAOPass, UnrealBloomPass, SAOPass) o no querés dependencias. Siempre terminá con `OutputPass`. |
| **RenderPipeline + TSL** (WebGPURenderer) | Si migrás a WebGPU. El EffectComposer no funciona ahí. Los efectos (bloom, GTAO, DOF, SMAA, TRAA, FXAA) viven en `three/addons/tsl/display/`.\[8\]\[22\]\[23\] |

#### 4.2 Receta pmndrs para video (WebGL)

```js
import { HalfFloatType } from 'three';
import {
  EffectComposer, RenderPass, EffectPass,
  BloomEffect, VignetteEffect, NoiseEffect, SMAAEffect,
  ToneMappingEffect, ToneMappingMode, BlendFunction,
} from 'postprocessing';

// Con postprocessing, el tone mapping lo hace el composer, no el renderer:
renderer.toneMapping = THREE.NoToneMapping;

const composer = new EffectComposer(renderer, {
  frameBufferType: HalfFloatType, // evita banding en degradés oscuros
  multisampling: 4,               // MSAA en el render target
});
composer.addPass(new RenderPass(scene, camera));

const bloom = new BloomEffect({ intensity: 0.6, luminanceThreshold: 0.9, luminanceSmoothing: 0.2, mipmapBlur: true });
const vignette = new VignetteEffect({ offset: 0.3, darkness: 0.5 });
const grain = new NoiseEffect({ blendFunction: BlendFunction.OVERLAY, premultiply: true });
grain.blendMode.opacity.value = 0.06; // grano MUY sutil: dithering anti-banding
const tone = new ToneMappingEffect({ mode: ToneMappingMode.AGX });

composer.addPass(new EffectPass(camera, bloom, tone, vignette, grain, new SMAAEffect()));

// en el loop / por frame:
composer.render(deltaFijo);
```

**Notas:**
- Los nombres de opciones pueden variar un poco entre versiones de la librería (la v7 rediseña el pipeline con `RenderPipeline`/`GeometryPass`).\[24\] Revisá la versión que instalás.
- **Bloom selectivo:** dejá el umbral (`luminanceThreshold`) alto y subí `emissiveIntensity` (por ejemplo a 2–5) solo en los objetos que tienen que brillar.\[7\] Así no "florece" toda la escena.
- **AO:** SSAO/N8AO/GTAO agregan contacto y peso. Con un HDRI bueno y AO horneado en el modelo, muchas veces no hacen falta.

#### 4.3 Equivalente WebGPU (TSL)

```js
import * as THREE from 'three/webgpu';
import { pass } from 'three/tsl';
import { bloom } from 'three/addons/tsl/display/BloomNode.js';

const renderer = new THREE.WebGPURenderer({ antialias: true });
await renderer.init();
const renderPipeline = new THREE.RenderPipeline(renderer); // antes "PostProcessing" (renombrado en r183)
const scenePass = pass(scene, camera);
const color = scenePass.getTextureNode('output');
renderPipeline.outputNode = color.add(bloom(color, 0.6, 0.4, 0.9)); // strength, radius, threshold
// loop: renderPipeline.render();
```

En este pipeline el tone mapping y la conversión de color se aplican solos al final. Si querés FXAA o una LUT, desactivalos con `renderPipeline.outputColorTransform = false` y usá `renderOutput()`.\[22\]

#### 4.4 Cuándo NO pasarse

- **Bloom:** si se nota como "niebla" sobre todo el cuadro, está demasiado fuerte. Tiene que afectar solo a los emisivos y a los reflejos más intensos.
- **Aberración cromática y glitch:** casi nunca suman en contenido educativo; delatan un efecto de plantilla.
- **DOF:** sutil. Si el desenfoque come la información que querés enseñar, hiciste un mal trade-off.
- **Viñeta:** del orden de 0.3–0.5 de oscuridad. Que se perciba, pero que no se vea.
- **Grano:** entre 3% y 8% de opacidad. Su tarea real es **romper el banding** de los degradés, que la compresión de Instagram y TikTok empeora mucho.

### 5. Geometría y detalle

**Biseles:** en el mundo real ninguna arista es perfectamente filosa. Un bisel pequeño atrapa la luz y dibuja un brillo en el borde, y es la diferencia número uno entre un "cubo de tutorial" y un "objeto de producto".

```js
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
const box = new THREE.Mesh(new RoundedBoxGeometry(1, 1, 1, 6, 0.06), mat); // segmentos, radio

// Texto / formas extruidas con bisel
const geo = new THREE.ExtrudeGeometry(shape, {
  depth: 0.2, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.015, bevelSegments: 5,
});
```

- En R3F tenés `<RoundedBox args={[1,1,1]} radius={0.06} smoothness={6} />` de drei.
- **Normales:** `geometry.computeVertexNormals()` suaviza, pero en geometrías con vértices duplicados conviene soldarlos antes con `BufferGeometryUtils.mergeVertices`. Para objetos low-poly facetados a propósito, `flatShading: true`.
- **Esferas y cilindros:** usá suficientes segmentos (64×32 o más). En un primer plano vertical a 1080×1920 los polígonos se notan en la silueta.

**Flujo con Blender → glTF/GLB:**
1. En Blender: modificador **Bevel** (con 2–3 segmentos), **Weighted Normal** y Shade Auto Smooth. Aplicá la escala (Ctrl+A), con 1 unidad equivalente a 1 metro.
2. Materiales con Principled BSDF, que se exporta como PBR glTF (incluidos clearcoat, transmission, sheen e iridescence vía extensiones KHR).
3. Horneá el AO si la escena es estática.
4. Exportá GLB y optimizalo:

```bash
npm i -g @gltf-transform/cli
gltf-transform inspect modelo.glb                     # ¿pesa la geometría o las texturas?
gltf-transform optimize modelo.glb modelo-opt.glb \
  --compress meshopt --texture-compress webp --texture-size 2048
```

- `optimize` usa **Meshopt** por defecto. Su `--texture-compress` viene en `auto`, que re-codifica las texturas en su formato original, así que pasá `webp` o `ktx2` de forma explícita.\[25\]\[26\]
- Comprimí la geometría **al final**: gltf-transform decodifica Draco al leer, y si encadenás comandos se pierde la compresión o se cuantiza dos veces.\[27\]
- **Para video offline**, la compresión importa mucho menos que en web. Lo prioritario es que las texturas tengan resolución suficiente para el primer plano. No achiques a 1024 un objeto que va a ocupar media pantalla vertical.
- Para cargar un GLB con Meshopt: `loader.setMeshoptDecoder(MeshoptDecoder)`. Con Draco: `DRACOLoader`.

### 6. Composición y cámara para video vertical

**Lente / FOV.** En Three.js, el `fov` de `PerspectiveCamera` es **vertical**. En 9:16, un FOV vertical de 50° da un horizontal muy estrecho, y uno de 75° (el típico de los tutoriales) deforma los bordes como un gran angular. Recomendación:
- **Producto / objeto protagonista:** FOV vertical de 20–35° y cámara más lejos. Equivale a un teleobjetivo: menos distorsión y aspecto de "foto de estudio".
- **Escena amplia / explicativa:** 35–50°.

```js
const camera = new THREE.PerspectiveCamera(28, 1080 / 1920, 0.1, 100);
camera.position.set(0, 1.2, 7);
camera.lookAt(0, 0.8, 0);
// o usar mm reales:
camera.setFocalLength(85); // usa filmGauge (35mm por defecto)
```

**Encuadre vertical:**
- Dejá libres el **15–20% superior e inferior**, porque ahí van la UI de la app, los subtítulos y la descripción. El objeto va en el tercio central.
- Usá la vertical: apilá la información (el objeto arriba y la etiqueta o el texto abajo) y aprovechá los movimientos de cámara verticales (tilt y pedestal).
- Un piso con sombra de contacto "ancla" el objeto. Si flota sin sombra se ve falso, salvo que lo hagas a propósito con un `Float` lento.

**Movimiento suave:**
- Animá el **objetivo** de la cámara y su posición con curvas de ease-in-out (`power2.inOut` o `sine.inOut`). Nada de cortes lineales.
- Un **dolly lento** con algo de parallax (2–5% del encuadre por segundo) se ve cinematográfico. Los giros rápidos de OrbitControls se ven a "demo".
- Para trayectorias, `THREE.CatmullRomCurve3` más `curve.getPointAt(easedT)`.
- No uses OrbitControls con damping para grabar: depende del framerate y no es reproducible.

**GSAP en modo determinista** (según el blog oficial de la release 3.13, del 30 de abril de 2025, GSAP es "100% FREE including ALL of the bonus plugins like SplitText, MorphSVG… even for commercial use", gracias a Webflow, que compró GreenSock en octubre de 2024):

```js
import gsap from 'gsap';

const tl = gsap.timeline({ paused: true, defaults: { ease: 'power2.inOut' } });
tl.to(camera.position, { z: 4.5, y: 1.0, duration: 2.5 }, 0)
  .to(model.rotation, { y: Math.PI * 0.75, duration: 3 }, 0.5)
  .to(mat, { emissiveIntensity: 3, duration: 0.6 }, 2.2);

// Al exportar: NUNCA dejes correr el reloj de GSAP; posicioná la timeline por frame
function renderFrame(i, fps) {
  tl.seek(i / fps, false);     // tiempo exacto del frame i
  camera.lookAt(target);
  composer.render(1 / fps);
}
```

**Paleta y estética coherente:**
- Definí una paleta de 3–5 colores (fondo, objeto principal, acento y neutros) y usala en materiales, fondo y texto del video.
- Una temperatura cálida en el key y una fría en el fill o el rim generan volumen "gratis".
- Mantené el mismo HDRI, tone mapping, exposición, FOV y curva de easing en toda la serie. Eso es lo que hace que un canal se vea "producido".

### 7. Grabación y exportación de video de calidad

**El problema:** grabar la pantalla, o usar MediaRecorder con `canvas.captureStream()`, toma los cuadros en tiempo real. Si un cuadro tarda, el video tartamudea, y el resultado cambia en cada corrida.\[10\] El bitrate y el codec además quedan en manos del navegador.\[28\]

**La solución: render offline determinista.**
1. Detené el loop de `requestAnimationFrame` y no uses `Clock` ni `Timer` para la animación.
2. Para cada cuadro `i`: `t = i / fps`, posicionás todo (timeline de GSAP, mixers con `mixer.setTime(t)`, shaders con `uniforms.uTime.value = t`), renderizás y capturás.
3. Codificás con WebCodecs, dejando que cada cuadro lleve su timestamp exacto, o exportás PNGs y los unís con ffmpeg.

#### 7.1 Opción A: Mediabunny (WebCodecs → MP4 en el navegador)

El README de mp4-muxer en GitHub (de Vanilagy, su autor) dice que la librería "has been deprecated in favor of Mediabunny, which entirely supersedes it" y que "is no longer being maintained and will not receive any new features or bug fixes". La API actual usa `quality: new Quality(...)`; `QUALITY_HIGH` y el campo `bitrate` siguen funcionando, pero están deprecados desde la v1.52.\[29\]\[30\]

```js
import { Output, Mp4OutputFormat, BufferTarget, CanvasSource, Quality } from 'mediabunny';

const FPS = 60, DURATION = 8, TOTAL = FPS * DURATION;

const output = new Output({ format: new Mp4OutputFormat(), target: new BufferTarget() });
const source = new CanvasSource(renderer.domElement, {
  codec: 'avc',                       // H.264: máxima compatibilidad con Instagram/TikTok
  quality: new Quality('very-high'),  // o new Quality({ bitrate: 20e6 })
  keyFrameInterval: 1,
});
output.addVideoTrack(source, { frameRate: FPS });
await output.start();

for (let i = 0; i < TOTAL; i++) {
  renderFrame(i, FPS);                    // posiciona y renderiza el frame i
  await source.add(i / FPS, 1 / FPS);     // capturar en el mismo tick que el render
}
await output.finalize();

const blob = new Blob([output.target.buffer], { type: 'video/mp4' });
const a = Object.assign(document.createElement('a'), { href: URL.createObjectURL(blob), download: 'reel.mp4' });
a.click();
```

- Hacé `await` en cada `add()`, porque así se respeta el backpressure del encoder. Tampoco cambies el tamaño del canvas a mitad de la grabación: el default es `sizeChangeBehavior: 'deny'`.\[31\]
- **`preserveDrawingBuffer`:** el navegador borra el buffer de WebGL después de componer. Si capturás en el mismo bloque síncrono que `renderer.render()` no hace falta, pero si entre el render y la captura hay un `await`, activalo.\[32\]\[33\] En export offline el costo de rendimiento es irrelevante, así que activarlo es un default seguro.

#### 7.2 Opción B: PNG por cuadro + ffmpeg (máxima calidad y control)

Exportá cada cuadro con `canvas.toBlob(..., 'image/png')`, guardalo con la File System Access API o mandalo a un servidor local, y después:

```bash
# H.264 alta calidad, compatible con todo (yuv420p), 60 fps, supersampling 2x → 1080x1920
ffmpeg -framerate 60 -i frames/f_%05d.png \
  -vf "scale=1080:1920:flags=lanczos" \
  -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p \
  -movflags +faststart reel.mp4
```

- **CRF 14–18** es "visualmente sin pérdida" para un master. La plataforma va a recomprimir igual, así que conviene entregarle un master de alta calidad.
- **Banding:** las plataformas comprimen fuerte los degradés oscuros. Para mitigarlo combiná buffers HalfFloat en el composer, un grano sutil y fondos no completamente lisos (un degradé leve con ruido).
- **Motion blur:** una forma de conseguirlo es renderizar N sub-cuadros por cuadro y promediarlos (acumulación). La reescritura de CCapture.js lo trae integrado con la opción `motionBlurFrames`.\[11\] En movimientos rápidos de cámara elimina el efecto "stop-motion" de los 30 fps.

#### 7.3 Otras herramientas actuales

| Herramienta | Para qué |
|---|---|
| **Remotion + `@remotion/three`** | La mejor opción si usás React/R3F y armás videos con texto, subtítulos y audio. `<ThreeCanvas>` se sincroniza con `useCurrentFrame()`, y durante el render fuerza `frameloop` a `'never'`, así que cada cuadro es determinista. **Regla:** animá con `useCurrentFrame()`, nunca con `useFrame()` de R3F, porque si no aparecen saltos o parpadeos. Para WebGPU existe `<ThreeWebGPUCanvas>` (experimental).\[34\]\[35\]\[36\] Renderiza MP4 desde la CLI. |
| **CCapture.js (reescritura moderna)** | `capture(canvas)` en cada cuadro, framerate fijo, salida MP4 o WebM por WebCodecs, motion blur por GPU.\[11\] |
| **canvas-record** (dmnsgn) | Graba canvas 2D, WebGL o WebGPU a MP4, WebM, MOV o secuencia PNG con WebCodecs o WASM, avanzando cuadro a cuadro con `await canvasRecorder.step()`.\[12\] |
| **MediaRecorder** | Solo para previews rápidos o grabaciones informales. No sirve para el master. |

**Resolución y fps:** el master va a 1080×1920. Usá 60 fps si hay movimiento de cámara rápido o texto que se desplaza; 30 fps alcanzan para animaciones lentas y además pesan la mitad.

### 8. Ecosistema y herramientas

**React Three Fiber + drei**, los componentes que más "profesionalizan" una escena:

```jsx
import { Canvas } from '@react-three/fiber';
import { Environment, Lightformer, ContactShadows, AccumulativeShadows, RandomizedLight,
         MeshTransmissionMaterial, Float, RoundedBox } from '@react-three/drei';
import { EffectComposer, Bloom, Vignette, Noise, ToneMapping } from '@react-three/postprocessing';
import { ToneMappingMode } from 'postprocessing';

export default function Scene() {
  return (
    <Canvas shadows camera={{ fov: 28, position: [0, 1.2, 7] }}
            gl={{ preserveDrawingBuffer: true }} style={{ aspectRatio: '9 / 16' }}>
      <color attach="background" args={['#0f1115']} />

      {/* IBL con archivo local (los presets usan CDN: no recomendados para producción) */}
      <Environment files="/hdri/studio_small_09_2k.hdr" environmentIntensity={0.8}>
        <Lightformer form="rect" intensity={4} position={[0, 3, 2]} scale={[3, 1, 1]} />
        <Lightformer form="ring" intensity={2} position={[-3, 1, -2]} scale={2} />
      </Environment>

      <Float speed={1.2} rotationIntensity={0.3} floatIntensity={0.4}>
        <RoundedBox args={[1, 1, 1]} radius={0.08} smoothness={6} castShadow>
          <MeshTransmissionMaterial thickness={0.5} roughness={0.05} ior={1.5}
                                    chromaticAberration={0.03} backside samples={8} resolution={1024} />
        </RoundedBox>
      </Float>

      {/* Sombra de piso: ContactShadows (barata) o AccumulativeShadows (más realista, escena estática) */}
      <ContactShadows position={[0, -0.7, 0]} opacity={0.5} blur={2.5} scale={6} far={2} />

      <EffectComposer multisampling={4}>
        <Bloom intensity={0.5} luminanceThreshold={0.9} mipmapBlur />
        <ToneMapping mode={ToneMappingMode.AGX} />
        <Vignette offset={0.3} darkness={0.5} />
        <Noise opacity={0.05} premultiply />
      </EffectComposer>
    </Canvas>
  );
}
```

- **`<Environment>`:** los `preset` ("city", "studio", "sunset" y otros) dependen de un CDN, y la propia documentación de drei aclara que no están pensados para producción.\[37\] Descargá el HDRI y usá `files`.
- **`AccumulativeShadows` + `RandomizedLight`:** acumulan muchas pasadas de sombra con la luz "temblando" y dan sombras suaves con un AO de apariencia trazada. Asumen una escena estática; con objetos en movimiento dejan estela. Ojo: en versiones recientes de Three.js, `RandomizedLight` necesita más intensidad (del orden de 3) por las unidades físicas.\[18\]\[38\]\[39\]
- **`MeshTransmissionMaterial`:** vidrio más vistoso que `MeshPhysicalMaterial`, con aberración cromática, cara trasera y distorsión. Es caro, pero en un render offline no importa.
- **`Float`:** flotación sutil, ideal para el objeto protagonista. Para exportar en modo determinista, reemplazalo por una animación que dependa del número de cuadro, porque `Float` usa el reloj interno.

**Ajuste en vivo:**
- **lil-gui** (viene con three en `three/addons/libs/lil-gui.module.min.js`) o **Leva** (pmndrs, para R3F). Exponé `toneMappingExposure`, `environmentIntensity`, la intensidad y la posición de las luces, roughness, bloom y FOV. Ajustar a ojo con sliders es el 50% del "look".

**Secuenciación / timeline:**
- **GSAP:** lo más robusto y gratuito, con timelines exactas y `seek()` determinista.
- **Theatre.js:** editor visual de keyframes con integración para R3F (`@theatre/r3f`), muy cómodo para coreografías de cámara. Su README en GitHub dice: "Theatre.js 1.0 is around the corner. We have temporarily moved development to a private repo so we can iterate faster. We'll push our work back to this public repo soon", y promete que la licencia seguirá siendo open source. Úsalo sabiendo que su ritmo de mantenimiento público es incierto, y fijá la versión.
- **Remotion:** si el video entero (texto, audio, cortes) se arma en código.

**WebGPU / TSL hoy:** WebGPU viene activado por defecto en Chrome, Edge, Safari 26 y Firefox (Windows y Mac con Apple Silicon), y `WebGPURenderer` cae automáticamente a WebGL 2 si no hay soporte.\[1\] Para tus videos, **no es necesario migrar**: WebGL con pmndrs/postprocessing da la misma calidad final en un render offline. Conviene si querés shaders TSL (que compilan a WGSL y a GLSL), partículas con compute o el pipeline de post con MRT. El costo: el EffectComposer y pmndrs/postprocessing no funcionan sobre WebGPURenderer.\[23\]

### 9. Errores comunes que delatan una escena amateur

| Error | Síntoma | Arreglo |
|---|---|---|
| Sin `scene.environment` | Metales negros, plásticos planos | HDRI o RoomEnvironment |
| Texturas de color sin `SRGBColorSpace` (o normal/roughness marcadas como sRGB) | Colores lavados u oscuros, relieve raro | Color → sRGB; datos → `NoColorSpace` |
| Sin tone mapping (o el default `NoToneMapping`) | Luces quemadas con bordes duros, colores que "clipean" | AgX / Neutral + exposición |
| Aristas filosas perfectas | Aspecto de "primitiva de tutorial" | Bisel de 2–6% del tamaño |
| `metalness: 0.5`, `roughness: 0` | Material de "plástico metalizado" irreal | Metalness 0 o 1, roughness ≥ 0.05 con variación |
| `AmbientLight` fuerte como relleno | Todo plano, sin volumen | Quitarla o bajarla; relleno con HDRI |
| Objeto flotando sin sombra | No "pesa" ni pertenece a la escena | ContactShadows / AccumulativeShadows |
| FOV 75° en vertical | Distorsión en los bordes | 20–35° para objetos |
| Movimiento lineal y OrbitControls en el video | Aspecto de demo técnica | Easing y trayectorias guionadas |
| Grabación de pantalla / MediaRecorder | Saltos, cuadros perdidos, compresión fuerte | Export cuadro a cuadro determinista |
| Bloom y aberración cromática exagerados | "Efecto de plantilla" | Bloom solo sobre emisivos; sin aberración |
| Degradés oscuros con escalones | Banding (empeora en Instagram/TikTok) | HalfFloat + grano sutil + CRF bajo |
| Usar PointLight con intensidad 1 de tutoriales viejos | La luz "no hace nada" | Candelas: decenas a cientos\[40\] |
| `PCFSoftShadowMap` en código nuevo | Warning / sombras inesperadas desde r182–r186 | `PCFShadowMap` + `shadow.radius`\[3\] |
| Escala del modelo en cm (100×) | Luces y sombras raras, bias imposible | Escala real: 1 unidad = 1 m |

---

## Recommendations

### Checklist priorizado por impacto (hacelo en este orden)

**Nivel 1: impacto enorme, 1 hora de trabajo**
1. ☐ `scene.environment` con un HDRI de estudio de Poly Haven (2k).
2. ☐ `renderer.toneMapping = AgXToneMapping` (o Neutral) y `toneMappingExposure` ajustado con lil-gui.
3. ☐ `colorSpace = SRGBColorSpace` **solo** en `map` y `emissiveMap`.
4. ☐ Metalness 0 o 1; roughness realista (nunca 0 exacto).
5. ☐ Sombra de contacto bajo el objeto.

**Nivel 2: el salto a "producto"**
6. ☐ Biseles en todas las aristas (RoundedBox, ExtrudeGeometry con bevel o Bevel en Blender).
7. ☐ Key cálida + rim de contraluz sobre el HDRI.
8. ☐ FOV vertical de 20–35° y encuadre con márgenes seguros arriba y abajo.
9. ☐ Normal y roughness maps con variación (ambientCG / Poly Haven, versión OpenGL).
10. ☐ Paleta fija de 3–5 colores para toda la serie.

**Nivel 3: pulido cinematográfico**
11. ☐ pmndrs/postprocessing con `HalfFloatType`, bloom selectivo, viñeta suave, grano del 3–8% y SMAA.
12. ☐ Animación con timeline de GSAP y easing `power2.inOut`; cámara con dolly lento.
13. ☐ Materiales Physical donde aporten: clearcoat en plásticos premium, transmission en vidrio.

**Nivel 4: entrega final**
14. ☐ Export determinista (`t = i / fps`) con Mediabunny o PNG + ffmpeg (CRF 14–18, `yuv420p`, `+faststart`).
15. ☐ Supersampling 2x y downscale con lanczos.
16. ☐ Motion blur por acumulación en tomas rápidas.
17. ☐ Revisá el resultado **en el teléfono**, después de subirlo, para ver si hay banding y si se lee el texto.

### Stack recomendado según tu perfil

- **Si programás en JS "vanilla":** three r187 + pmndrs/postprocessing + GSAP + lil-gui + Mediabunny.
- **Si usás o querés usar React:** R3F + drei + @react-three/postprocessing + Leva + **Remotion** para el render final. Remotion resuelve de una sola vez el determinismo, el texto, el audio y la exportación.

### Recursos recomendados

- **Oficiales:** el manual de three.js (páginas de Color Management y de Post-Processing con WebGPURenderer), la Migration Guide en la wiki de GitHub (leela antes de cada actualización y avanzá de a 10 releases como máximo), los ejemplos oficiales (`webgl_lights_rectarealight`, `webgl_loader_gltf`, `webgpu_postprocessing_*`) y discourse.threejs.org (hilos "Updates to lighting in r155", "Updates to Color Management in r152" y "Tone Mapping Overview").
- **pmndrs:** documentación de drei (sección Staging: Environment, Lightformer, AccumulativeShadows, ContactShadows), react-postprocessing y el README de pmndrs/postprocessing (color space y HalfFloat).
- **Cursos:** Three.js Journey (Bruno Simon) es la referencia más completa e incluye lecciones de Environment and Staging con R3F.
- **Video/export:** documentación de Remotion (`@remotion/three`, `<ThreeCanvas>`), mediabunny.dev (guía de Media Sources y de Writing Media Files) y los repos de canvas-record y CCapture.js.
- **Assets:** polyhaven.com y ambientcg.com (CC0), gltf-transform.dev (CLI y `inspect`) y gltf.report para inspeccionar modelos en el navegador.
- **Al día:** el changelog de releases en GitHub (mrdoob/three.js/releases) y los resúmenes de Utsubo sobre cada release y la migración a WebGPU.

---

## Caveats

- **API en movimiento:** Three.js publica una release cada 7–11 semanas.\[1\] Los nombres que más cambiaron hace poco son `HDRLoader` (antes `RGBELoader`), `RenderPipeline` (antes `PostProcessing`), `Timer` (antes `Clock`), la eliminación de `PCFSoftShadowMap` y los parámetros de iridescence en r187.\[1\]\[6\]\[41\]\[42\] El código de esta guía apunta a r186–r187; en versiones anteriores pueden cambiar algunos nombres.
- **pmndrs/postprocessing v7** rediseña el pipeline (`RenderPipeline`, `GeometryPass`).\[24\] Los ejemplos de esta guía siguen la API v6, que es la estable más difundida; verificá la versión que instales.
- **Theatre.js:** su estado de mantenimiento público es incierto (el desarrollo de la 1.0 se movió a un repo privado).\[43\] Para proyectos a largo plazo, GSAP o Remotion son apuestas más seguras.
- **Valores numéricos** (intensidades, roughness, FOV, CRF, opacidad del grano): son **puntos de partida** a partir de la práctica habitual, no constantes físicas. Ajustalos a ojo con lil-gui o Leva sobre tu escena real y verificá en el teléfono.
- **Mediabunny y `preserveDrawingBuffer`:** que `CanvasSource.add()` tome el cuadro de forma síncrona antes de su primer `await` interno es una inferencia de la documentación, no algo verificado en el código fuente. Por eso la guía recomienda activar `preserveDrawingBuffer: true` en la exportación.
- **WebCodecs:** el soporte de H.264 por hardware depende del navegador y del sistema operativo; en algunos entornos (por ejemplo, Chromium en Linux sin códecs propietarios) puede fallar.\[44\] El camino PNG + ffmpeg funciona siempre.

## Fuentes

1. [Three.js Latest Version: r187 Changelog & 2026 Releases](https://www.utsubo.com/blog/threejs-2026-what-changed)
2. [Updates to lighting in three.js r155 - Discussion - three.js forum](https://discourse.threejs.org/t/updates-to-lighting-in-three-js-r155/53733)
3. [threejs-lighting Skill - cloudai-x](https://www.ui-skills.com/skills/cloudai-x/threejs-lighting)
4. [Tone Mapping Overview - Showcase - three.js forum](https://discourse.threejs.org/t/tone-mapping-overview/75204)
5. [Three.js Official Manual, Distilled: Three.js guide for coding agents](https://better-design.com/principles/three-js/threejs-official-manual)
6. [Migration Guide · mrdoob/three.js Wiki · GitHub](https://github.com/mrdoob/three.js/wiki/Migration-Guide)
7. [Pmndrs post-processing: How to get selective Bloom - Questions - three.js forum](https://discourse.threejs.org/t/pmndrs-post-processing-how-to-get-selective-bloom/58452)
8. [threejs-skills/skills/threejs-postprocessing/SKILL.md at main · CloudAI-X/threejs-skills · GitHub](https://github.com/CloudAI-X/threejs-skills/blob/main/skills/threejs-postprocessing/SKILL.md)
9. [100 Three.js Tips That Actually Improve Performance (2026)](https://www.utsubo.com/blog/threejs-best-practices-100-tips)
10. [CubeRoot — WebCodecs frame-accurate decoding](https://cuberoot.me/dev/algorithms/webcodecs)
11. [GitHub - spite/ccapture.js: A library to capture canvas-based animations at a fixed framerate · GitHub](https://github.com/spite/ccapture.js/)
12. [GitHub - dmnsgn/canvas-record: Record a video in the browser or directly on the File System from a canvas region (2D/WebGL/WebGPU) as MP4, WebM, MKV, MOV, GIF, PNG/JPG Sequence using WebCodecs and Wasm when available. · GitHub](https://github.com/dmnsgn/canvas-record)
13. [GitHub - Vanilagy/mp4-muxer: MP4 multiplexer in pure TypeScript with support for WebCodecs API, video & audio. · GitHub](https://github.com/Vanilagy/mp4-muxer)
14. [Free PBR Textures, Materials and HDRIs for Games (2026)](https://app.cinevva.com/guides/free-textures-hdris-materials)
15. [WebGLRenderer: \`.physicallyCorrectLights\` -\> \`.useLegacyLights\` by WestLangley · Pull Request #24975 · mrdoob/three.js · GitHub](https://github.com/mrdoob/three.js/pull/24975)
16. [RectAreaLight](https://cs.wellesley.edu/~cs307/threejs/r124/three.js-master/docs/api/en/lights/RectAreaLight.html)
17. [RectAreaLight does not apply sheen (MeshPhysicalMaterial, both WebGLRenderer and WebGPURenderer) · Issue #34438 · mrdoob/three.js · GitHub](https://github.com/mrdoob/three.js/issues/34438)
18. [Drei Catalog: Three.js guide for coding agents](https://better-design.com/principles/three-js/drei-catalog)
19. [threejs-game-studio/references/tone-mapping-color.md at main · chrislaupama/threejs-game-studio · GitHub](https://github.com/chrislaupama/threejs-game-studio/blob/main/references/tone-mapping-color.md)
20. [GitHub - pmndrs/react-postprocessing: 📬 Postprocessing for react-three-fiber · GitHub](https://github.com/pmndrs/react-postprocessing)
21. [pmndrs/postprocessing](https://deepwiki.com/pmndrs/postprocessing)
22. [Post-Processing with WebGPURenderer](https://threejs.org/manual/pages/webgpu-postprocessing.html)
23. [Migrate Three.js to WebGPU (2026) — The Complete Checklist](https://www.utsubo.com/blog/webgpu-threejs-migration-guide)
24. [Render Pipeline Redesign · Issue #419 · pmndrs/postprocessing · GitHub](https://github.com/pmndrs/postprocessing/issues/419)
25. [How to Optimize GLB Files for the Web: Draco, Meshopt, and KTX2 (2026)](https://app.cinevva.com/guides/optimize-glb-for-web)
26. [gltf-transform optimize: A Practical Guide to Shrinking glTF/GLB Files](https://compress-glb.com/blog/gltf-transform-optimize/)
27. [Reduce GLB File Size: 8 Techniques to Compress GLB Files](https://compress-glb.com/blog/reduce-glb-file-size/)
28. [Stop Piping Video Through Canvas: WebCodecs Has Real Codec Control](https://talkingtech.io/stop-piping-video-through-canvas-webcodecs-has-real-codec-control/)
29. [QUALITY\_HIGH](https://mediabunny.dev/api/QUALITY_HIGH)
30. [Quantizer support in Mediabunny v1.52.0](https://mediabunny.dev/blog/quantizer-support)
31. [Media sources | Mediabunny](https://mediabunny.dev/guide/media-sources)
32. [preserveDrawingBuffer in WebGLRenderer for toDataURL support by jeromeetienne · Pull Request #421 · mrdoob/three.js · GitHub](https://github.com/mrdoob/three.js/pull/421)
33. [Rendering the configured 3D product to an image for the quote - DEV Community](https://dev.to/gronskideveloper/rendering-the-configured-3d-product-to-an-image-for-the-quote-2gg2)
34. [ThreeCanvas component (@remotion/three)](https://www.remotion.dev/docs/three-canvas)
35. [ThreeWebGPUCanvas component (@remotion/three)](https://www.remotion.dev/docs/three-webgpu-canvas)
36. [remotion-best-practices: Guides creation of programmatic videos in React using Remotion APIs and patterns](https://skills.rest/skill/remotion-best-practices-haydenbleasel)
37. [@srinivasprabhu/drei - npm](https://www.npmjs.com/package/@srinivasprabhu/drei)
38. [AccumulativeShadows - React-Three-Drei - Poimandres](https://drei.docs.pmnd.rs/staging/accumulative-shadows)
39. [Environment and Staging with R3F — Three.js Journey](https://threejs-journey.com/lessons/environment-and-staging-with-r3f)
40. [Shadow and color problems going from v64 to v161 - Questions - three.js forum](https://discourse.threejs.org/t/shadow-and-color-problems-going-from-v64-to-v161/61640)
41. [webgpu-claude-skill/skills/webgpu-threejs-tsl/docs/post-processing.md at main · dgreenheck/webgpu-claude-skill · GitHub](https://github.com/dgreenheck/webgpu-claude-skill/blob/main/skills/webgpu-threejs-tsl/docs/post-processing.md)
42. [Releases · mrdoob/three.js · GitHub](https://github.com/mrdoob/three.js/releases)
43. [Theatre.js: Why Pro Animators Ditch CSS for This Secret Weapon](https://converter.brightcoding.dev/blog/theatrejs-why-pro-animators-ditch-css-for-this-secret-weapon)
44. [Export speed fixes, mediabunny migration, drag-and-drop waypoints by SurajFc · Pull Request #8 · SurajFc/RouteReel · GitHub](https://github.com/SurajFc/RouteReel/pull/8)

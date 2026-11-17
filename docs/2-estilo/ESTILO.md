# Estilo visual
Cómo se ve un reel de @ayrtonnacer. Todo esto ya está en la plantilla (`videos/_plantilla/`): al hacer un reel **no se rediseña**, se respeta. Sistema de diseño completo: `docs/media-kit/` (abrir `Media Kit.dc.html`). Cámara: `CAMARA.md`. Subtítulos: `SUBTITULOS.md`. Viudas y huérfanas: `TIPOGRAFIA.md`.

## Formato y zonas
- 1080×1920, 30 fps.
- **Lo que se lee**: x 60–1020, **y 200–1100**. Arriba de 200 y abajo de 1330 lo tapa la interfaz de las apps.
- **Subtítulos**: y 1120–1320. Nada del set debe leerse ahí (el piso sí puede pasar).
- Debajo de y 1330: solo piso.
- La librería 3D sube la imagen 170 px (`dy`) para que el centro del encuadre caiga en la zona de lectura. `python engine/reel.py encuadre` dice en qué píxel cae un punto 3D.

## Lenguaje
**Motion graphics en 3D**: objetos three.js de línea sobre negro, un solo set por reel, cámara de película que lo recorre. El texto es HTML nítido encima del 3D. Nada de modelos fotorrealistas, sombras, brillos ni postproceso.

## Paleta — un color = un significado
Siempre por variable (`var(--acc)` en HTML/CSS; `P.acc` en three.js). Nunca un color escrito a mano. Si hace falta uno nuevo: se agrega acá y en `assets/marca.css`.
| Variable (CSS / 3D) | Valor | Significa |
|---|---|---|
| `--acc` / `P.acc` | `#A8927C` Foundry Tan | **el único acento**: la palabra clave, la firma, la señal, "mirá acá". Uno por plano |
| `--text`, `--hi` / `P.hi` | `#FFFFFF` | texto, cables, lo que debe resaltar |
| `--edge` / `P.edge` | `#929292` | aristas de los objetos (trazo 2,2 px) |
| `--muted` | `#C7C7C7` | rótulos secundarios |
| `--mid`, `--piso` / `P.piso` | `#4D4D4D` | piso y detalles |
| `--bg`, `--plate` / `P.plate` | `#000000` | fondo y relleno de los objetos (negro puro, sin halos) |
| `--ok` / `P.ok` | `#2EE08C` | ✓ correcto (solo en estados) |
| `--warn` / `P.warn` | `#A8927C` + ⚠ | aviso (siempre con el símbolo, para distinguirlo del énfasis) |
| `--err` | `#DC2626` | ✕ error: **bloque relleno** con ✕ (`.chip.err`) |
| extra | Cloud Slate `#839CB2`, Archive Purple `#79648C` | solo si hay que distinguir varias categorías (canales de una foto). Agregarlos como variable antes de usarlos |

Reglas: nunca el mismo color para lo bueno y lo malo; verde y rojo solo en estados; los colores van de acento, **nunca de fondo**.

## Tipografía
- **Host Grotesk** (`--sans`): títulos y texto, peso 700, espaciado −0,02 a −0,03 em. **Geist Mono** (`--mono`): números, datos, código. Locales en `assets/fonts/`.
- Nunca mayúsculas con espaciado amplio. Nunca una palabra sola en la última línea (`text-wrap: balance`, `&nbsp;` entre las dos últimas, o reescribir).
- **Tamaños** (px a 1080 de ancho): título de portada y gancho 140 · CTA 118 · rótulo principal sobre un objeto 58 (`.rot`) · dato en mono 40–46 (`.rot.mono`) · número grande destacado 64 · subtítulos 70 · firma 60 (gancho) / 58 (cierre). **Mínimo 40 px**: menos no se lee en el celular.
- Clases listas en `marca.css`: `.titular`, `.bajada`, `.acc`, `.mono`, `.firma`, `.rot` (+ `<b>` = tan), `.chip` (`.ok`, `.warn`, `.err`), `.terminal`, `.pasos` ("Paso 1 de 3", en sans).

## Anatomía fija (media kit) — no se cambia entre reels
**Portada (cuadro 0, 0,1 s) y gancho**: son el mismo plano; la portada es su primer cuadro y sirve de miniatura.
- Firma `@ayrtonnacer` en tan, arriba a la izquierda (x 90, y 262), 60 px.
- Título de **3–5 palabras**, 140 px, alineado a la izquierda desde (x 90, y 350), ancho 900, máximo 3 líneas, **una sola palabra en tan**.
- Debajo, el **objeto protagonista** del reel, grande, de línea gris, con **un único punto o detalle tan**, apoyado en el piso. **Nada pasa por detrás del título** (las otras estaciones aparecen recién cuando la cámara viaja).
- El título y la firma se van al terminar el gancho.

**Cierre**: CTA centrado de 4 líneas a 118 px ("Dale like y / seguime para / aprender más / de <tema>", con "like" y el tema en tan), entra palabra por palabra con desenfoque; a los 1,3 s aparece la firma, 58 px, debajo. Cámara que aterriza y queda quieta.

En el medio, opcional: "Paso N de M" fijo arriba (`.pasos`) si es un tutorial.

## Objetos 3D
- Relleno negro que tapa lo de atrás + contorno gris de 2,2 px (`E.std()` + `E.contornear()`). Líneas continuas, sin cortes; nada de contornos de 4–5 px.
- Escala real en metros (notebook 0,34 m; router 0,42 m). Formas suaves; nada pixelado como protagonista.
- Blanco solo para cables y señal. Tan para lo que se nombra en ese momento.
- Lo que se conecta se toca. Ondas de radio = anillos. Paquetes solo sobre cables.
- Un objeto muestra **su forma real** (no todo es un cubo).
- Revisar cada objeto de cerca en los cuadros.

## Texto en pantalla
- Solo el término o el número que se enseña; no repetir la oración de la voz ni lo que dice el subtítulo.
- Los rótulos van **arriba** del objeto (abajo pisan los subtítulos), con aire entre sí y sin tapar otro objeto.
- Entradas: aparece con leve desplazamiento o desenfoque (0,18–0,25 s); escalonado de 60–120 ms entre ítems. Un texto que aterrizó **queda quieto**.
- Advertencias importantes van en pantalla, no en la voz.

## Fondo
Negro puro + piso de líneas grises en perspectiva (automático en `escena3d.js`) + viñeta suave. Sin puntitos, bits, partículas, degradés ni nada que no signifique algo.

## Prohibido
Scanlines · marcos HUD / esquinas en L · "// TUTORIAL", "[ GRATIS ]" · texto de la fuente al final · loops de "flotar" o "respirar" · rebote en interfaz · neón y brillos · colores de fondo · estética roja, Anduril o lima · todo entrando igual.

## Tema "noir" (en prueba desde 2026-11-17, pedido de Ayrton)
Inspirado en los reels de Instagram que le gustan (medidos en `docs/4-referencias/material/2026-11-17-refs-instagram-dinamismo/`). Se activa por reel con `plano(root, tl, id, armar, { estilo: 'noir' })` en `assets/set.js`; el tema "línea" sigue siendo el de los reels anteriores.
**Cómo es** (lo que se ve en las referencias):
- **Negro absoluto y monocromo**: todo es negro, gris y blanco. Nuestro único color sigue siendo el tan de la marca (palabra clave, firma, la etiqueta que se nombra).
- **Objetos con volumen**: no son dibujos de línea, son piezas de **metal oscuro** (casi negro, semibrillante) que reflejan un entorno suave. Lo que los separa del fondo es un **contraluz blanco** que les dibuja el borde.
- **Tarjetas de interfaz**: placas con **esquinas redondeadas** y **borde blanco fino**, texto blanco nítido (como las tarjetas de chat o perfil de las referencias). Nuestras fichas (valores, etiquetas) se dibujan así.
- **La luz es la señal**: los cables o hilos son **blancos y brillan** (halo suave alrededor) y tienen un **punto de luz** en cada extremo. Lo importante brilla; lo demás se apaga.
- **Piso de puntos**: grilla blanca muy tenue cada medio metro con un **punto brillante en cada cruce**; con la distancia se apaga en la niebla (da profundidad).
- **Niebla más cerrada** (5–20 m): lo lejano se funde con el negro, lo cercano queda nítido.
- **Cámara**: la del reel es de movimiento casi continuo (69–88 % de los cuadros en las referencias), ver `CAMARA.md`.
**Lo que NO tomamos de las referencias**: mayúsculas espaciadas en los rótulos (nuestra tipografía es mejor, dijo Ayrton), bloom de posproceso (caro: el brillo se hace con halos aditivos baratos, `E.brillo`), fondos blancos.
**Funciones nuevas** (`escena3d.js`): `E.NOIR`, `E.brillo(color, tamaño, opacidad)` (halo de luz), `E.marcoRedondo(w, h, r, z, color, px)` (borde de tarjeta), piso de puntos automático.
Esto reemplaza, solo en el tema noir, las reglas "objetos de línea gris" y "sin brillos detrás de los objetos" (Ayrton pidió esta estética el 2026-11-17).

## Temas viejos
`engine/themes/` (línea roja, cyber/HackTheBox) y los videos de `videos/_archivo/` quedaron como historia. No se usan ni se copian salvo que Ayrton lo pida.

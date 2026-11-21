# Referencia: instagram.com/reel/Df9LK09t9QB (Ayrton, 2026-11-21)
Tema: cómo funcionan los servidores de GTA VI / GTA Online. Ayrton lo pasó para entender **cómo maneja la cámara y los planos en un espacio 3D, la estética "noir" y los zoom in / zoom out**.
Medido con `engine/analisis/medir.py` (el video no se guarda). Acá: `INFORME.md`, `metricas.json`, `hoja_resumen.jpg` (0–59 s), `hoja_60-111s.jpg` y tiras de los momentos clave.

## Números
- 1080×1920, **60 fps**, **111 s**, **0 cortes** (un solo plano secuencia de punta a punta).
- Cámara en movimiento el **82,5 %** de los cuadros, **73 % con zoom**. 3,1 movimientos notorios cada 10 s; el 64 % del movimiento es deriva lenta (< 100 px/s).
- Ataque y liberación de los movimientos casi iguales (0,17 s / 0,17 s): ease simétrico, arranca y frena igual.
- Brillo medio **0,72**, saturación **0,0**: blanco y negro puro. Colores: blanco #FCFCFC 52 %, negro #282828 8 %, gris #D8D8D8 6 %.
- Audio −14,2 LUFS (igual que nosotros), voz activa 76 %, 3 golpes graves.

## Estética: "noir" = blanco y negro, no "fondo negro"
- **Estudio blanco infinito** (fondo sin horizonte, como un ciclorama de fotografía) el 85 % del video. Sobre él, objetos de **plástico/cerámica blanca mate** y piezas de **negro brillante** (bolitas, bases, racks, etiquetas). Contraste alto entre blanco y negro, sin color.
- **Sombras de contacto suaves** bajo cada objeto (manchas grises difusas en el piso): es lo que hace que los objetos "apoyen" sin dibujar el piso.
- **Vidrio** (cúpulas tipo globo de nieve) con reflejos suaves: la única transparencia.
- **Desenfoque de profundidad** (bokeh) fuerte en primer plano y fondo durante los viajes y en los planos de detalle; lo que se explica siempre está nítido.
- **Un solo tramo en clave baja** (38,8–46 s): fondo negro total con el rack iluminado de costado, para "lo que no se ve: el servidor por dentro". El paso a negro es parte del movimiento (la cámara cruza un objeto), no un corte.
- Texto: etiquetas chicas tipo píldora negra con texto blanco en mono ("TÚ", "AUTORIDAD", "ROCKSTAR"), rótulos mono en mayúsculas finos con una línea guía al objeto, y frases sueltas en **serif itálica** ("barato", "la última palabra", "son miles de máquinas") como voz interior. Fecha mono arriba ("HOY · 19 NOV 2026") en el gancho.

## Cámara y planos
- **El set es un mundo, no estaciones separadas**: campo de bolitas → cúpula con ciudad → red de cúpulas conectadas → servidor de Rockstar → rack → centro de datos → maqueta de ciudad → Vice City → campo de racks → vuelve al campo de bolitas (el final calca el principio: **loop**).
- **Escala como recurso** (el más usado): se arranca en un objeto y la cámara se aleja hasta que ese objeto es uno entre cientos (una cúpula → una red de cúpulas; un rack → un centro de datos infinito, alejamiento de −82 % en 4,7 s a los 61 s). Y al revés: de un campo de racks hasta meterse en la maqueta de una ciudad, y de ahí a un plano cenital de una esquina (+75 % en 7,9 s).
- **Zoom in = ir adentro, zoom out = mostrar cuántos hay.** Cada alejamiento grande responde a "y hay miles"; cada acercamiento grande a "así funciona uno por dentro".
- **Atravesar objetos** como transición: la cámara entra en la rejilla del rack (los agujeros hexagonales llenan el cuadro y se vuelven otra textura) y sale en el siguiente lugar. Reemplaza al corte.
- **Latigazos cortos** (0,3–0,4 s, picos de 7000–47000 px/s) con desenfoque de movimiento para cambiar de lugar (ej. 49,9 s: del anillo de emparejamiento a la cúpula, pasando por blanco).
- **Retenciones con deriva**: casi nunca está quieta del todo; en las explicaciones hay un acercamiento lento (push-in de +3 a +15 % en 1–3 s) o un paneo mínimo. Las retenciones verdaderas (0 px/s) son pocas y cortas (4 de ≥ 0,5 s).
- **Ángulos**: casi todo en **picado de tres cuartos** (desde arriba y de costado); el centro de datos y el campo de bolitas en **picado rasante con perspectiva** hasta el horizonte; un **cenital** sobre la maqueta; **contrapicado** leve sobre el rack en negro.
- **Los objetos se transforman mientras la cámara se mueve**: las bolitas se ordenan en letras GTA VI, la cúpula se rompe en triángulos, el rack se arma pieza por pieza, la ciudad crece.

## Qué podemos tomar (propuesta, sin aplicar)
1. "Zoom out = cuántos hay / zoom in = cómo es por dentro" como gramática fija de escala.
2. Transición atravesando un objeto en vez de travelling cuando se cambia de escala.
3. Versión clara del tema noir: fondo blanco infinito con objetos blancos mate y acentos negros brillantes, sombras de contacto, bokeh. Un tramo en negro para "lo oculto".
4. Final que vuelve al primer cuadro (loop) antes del CTA.

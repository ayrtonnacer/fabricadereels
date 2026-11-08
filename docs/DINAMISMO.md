# Dinamismo y subtítulos
> **Estado (2026-11-07): material de referencia, NO obligatorio.** Un intento de rediseñar el Parrot con todo esto junto (v3) fue rechazado: se perdió el 3D y quedó peor que el video original. Usarlo como capa, de a una pieza por vez, mostrando frames. Ayrton pidió no agregar subtítulos por ahora. Las animaciones 3D le gustan: conservarlas.

Referencia: 9 shorts de @aprendeiadecero que Ayrton pasó el 2026-11-07. Los analizamos cuadro a cuadro. De ellos se toma **el ritmo, las animaciones y los subtítulos**, no la estética: seguimos con nuestros temas (red team / HackTheBox).
Lo que Ayrton marcó: en esos videos las letras tienen **demasiado espacio entre sí**, y en eso nuestros videos están mejor. Hay que mantener el espaciado normal o apretado (`letter-spacing` ≤ 0, y −0.02 a −0.035em en titulares). Nada de mayúsculas con tracking amplio.

## Subtítulos (lo más importante)
- **Siempre hay subtítulos**, quemados en el video, en el tercio inferior (por encima de la zona segura de 380 px).
- Se muestran por **bloques de 2 a 4 palabras** (una línea, o dos como máximo). El bloque aparece entero, de golpe.
- **Cada palabra tiene su propia "pastilla"**: un rectángulo claro de esquinas apenas redondeadas, texto en negrita y una sombra corta.
- La **palabra que se está diciendo se invierte** (fondo oscuro o acento, texto claro). El cambio es un corte seco, sin transición, sincronizado con la voz. En nuestros temas oscuros se invierte al revés: pastilla oscura y la palabra activa en el acento del tema.
- Cuando entra una **palabra gigante** (ver abajo), el subtítulo se oculta y vuelve cuando la palabra gigante sale. Nunca compiten.
- El subtítulo **no reemplaza** a los titulares: el titular dice la idea y el subtítulo sigue la voz.
- Sincronizar palabra por palabra exige tiempos por palabra. Por ahora se estiman repartiendo la duración de cada línea de voz por sílabas. Si se nota desfasado, hay que pasar a una alineación real.

## Palabra gigante ("golpe")
- Cada 5–8 s aparece **una palabra o número clave en grande**, de 2 a 4 veces el tamaño del titular, en mayúsculas compactas (ej.: "GRATIS", "305 MIL", "DISTINTAS", "TE SIRVEN", "HOY").
- Entra con **desenfoque de movimiento** (blur que se limpia en 4–6 cuadros), a veces con escala desde 1.3 o deslizándose. Dura 0.8–1.5 s y sale rápido.
- Variante "sello": una banda o etiqueta rotada −6 a −10° atravesando la pantalla ("GRATIS", "CÓDIGO ABIERTO"), en el color de énfasis.
- Lleva un efecto de sonido de impacto (ver AUDIO.md), sin ser literal.

## Movimiento constante (que nunca quede quieto)
- **Algo se mueve en todo momento**: un zoom lento (Ken Burns, 1.00 a 1.06 en la escena), un cursor que se desplaza, un contador que sube o un elemento que entra.
- **Cursor de mouse** que viaja, hace clic y "presiona": confirma visualmente cada acción ("ahora tocás acá").
- **Capturas reales** (web, GitHub, terminal) dentro de tarjetas con sombra. La parte importante se **resalta con un recuadro de color que se dibuja** o con un subrayado que crece de izquierda a derecha.
- **Pop de íconos**: badges pequeños (✓, ✕, logo, estrella) que aparecen con rebote sobre las tarjetas.
- **Conectores**: líneas curvas o punteadas que se dibujan entre tarjetas, flechas A → B y tachados rojos sobre lo que "dejás de hacer o pagar".
- **Profundidad**: lo que no importa en ese momento se desenfoca o se achica al fondo, y lo importante pasa adelante.
- Partículas sueltas (`? # { } ≠ $`) flotando alrededor para la idea de "confusión" o "código".

## Estructura que se repite
1. **Cuadro 0 = portada**: titular de 2 o 3 líneas grande (la clave resaltada), una ilustración o tarjeta central y una fila de íconos de las herramientas. Sirve de miniatura.
2. **Índice persistente**: si el video es una lista ("4 trucos", "6 agentes", pasos), una mini tarjeta queda fija en una esquina superior y se va **tildando** (1 ✓, 2 ✓, …). Se combina con nuestro "Paso N de M".
3. **Rótulo de sección** arriba a la izquierda: corto, en el color de énfasis, subrayado ("SEGUNDO", "LO QUE DEJÁS DE PAGAR"). Sin tracking amplio.
4. **Número gigante** al empezar cada ítem ("2").
5. Cierre: tarjeta con firma y CTA, y la lista completa tildada.

## Ritmo
- **Un cambio visual cada 1.5–3 s** (entra un elemento, cambia el zoom o aparece un resalte). Las escenas siguen durando lo que dura la voz, pero por dentro pasan cosas.
- Hay que evitar más de 3 s con la pantalla igual salvo el subtítulo.

## Qué falta en el motor (para implementar)
- `subs`: generador de subtítulos por pastillas a partir de `voz.lineas` (bloques de 2 a 4 palabras, palabra activa invertida, se oculta cuando hay palabra gigante).
- `golpe`: componente de palabra gigante con blur de movimiento (`filter: blur()` que baja a 0) y la variante sello.
- `cursor`: cursor con trayectoria por puntos clave y clic.
- `resalte`: recuadro o subrayado que se dibuja sobre una captura.
- `kenburns`: zoom lento por escena.
- `indice`: mini lista fija que se va tildando.

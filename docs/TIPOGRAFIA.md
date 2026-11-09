# Tipografía: viudas, huérfanas y palabras sueltas
Fuente: artículo de Adobe que pasó Ayrton (`docs/material/2026-11-viudas-y-huerfanas-adobe.pdf`). Su definición: una **viuda** es una palabra suelta o línea corta al final de un párrafo; una **huérfana**, al principio de una página o columna, separada del resto del párrafo. En pantalla las dos nos molestan por lo mismo: **una palabra sola colgando** ("Por eso a veces no / **llega**" — caso real del reel de WiFi, marcado por Ayrton).

## Reglas para los videos
1. **Nunca una palabra sola en la última línea** de un bloque de 2 líneas o más (titulares, bajadas, subtítulos, tarjetas).
2. `text-wrap: balance` en `.titular`, `.bajada`, tarjetas y subtítulos (ya está en `assets/marca.css`).
3. **Espacio de no separación** (`&nbsp;`) entre las dos últimas palabras de un bloque (el generador de subtítulos ya lo hace). En HTML: `última&nbsp;palabra`.
4. Si igual queda una palabra suelta: **reformular el texto** (el artículo lo recomienda: cambiar una palabra por otra más corta) o ajustar el ancho del bloque. Priorizar la legibilidad a la perfección.
5. En titulares con salto manual (`<br>`) elegir los cortes a mano, balanceados, con frases completas por línea.
6. Cuando un texto en pantalla repite lo que dice el subtítulo, se saca (menos texto = menos huérfanas).
7. Revisar siempre con `snapshot` los bloques de varias líneas: el motor de texto parte distinto según el ancho.

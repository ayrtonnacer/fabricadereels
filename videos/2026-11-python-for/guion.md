---
tipo: concepto
tema: "Python"
concepto_unico: "Un for repite lo mismo para cada elemento de una lista"
duracion_objetivo_s: 49
palabras_max: 137
gancho_tipo: "dato sorprendente"
loop: "¿Cómo tres líneas hacen un millón de repeticiones?"
cierre_loop: "Así, tres líneas alcanzan para un millón. Cambia la lista, no el código."
detalle_profesional: "El for no cuenta: pide el próximo elemento (iter/next) hasta StopIteration; por eso range(10**9) ocupa 48 bytes"
titulo_portada: "El bucle for (for en tan)"
estetica: "prueba del tema claro: estudio blanco infinito, objetos blancos mate y negros brillantes, sombras de contacto, un tramo en negro"
fuentes:
  - "https://docs.python.org/3/reference/compound_stmts.html#the-for-statement (el for llama a iter() y a next() hasta StopIteration)"
  - "Medido en Python 3.13.18 (2026-11-21): sys.getsizeof(range(10**9)) = 48 bytes; sys.getsizeof(list(range(10**6))) = 8 000 056 bytes; next() sobre un iterador agotado lanza StopIteration"
verificado: true
---
### gancho · 0–3,4 s
- VOZ: "Tres líneas de código. Un millón de repeticiones."
- SE VE: firma + título "El bucle **for**". Debajo, un campo de esferas negras brillantes sobre blanco infinito que se pierde en el horizonte.
- CÁMARA: plano general en picado rasante, con perspectiva hasta el horizonte; push-in lento mientras se lee el título.

### lista · 3,5–12,5 s
- VOZ: "Tenés una lista con cinco nombres y querés saludar a cada uno." / "Podrías escribir cinco veces el saludo. Con mil nombres, ya no."
- SE VE: una fila de 5 esferas con una píldora negra cada una (Ana, Beto, Caro, Dani, Eli). Aparecen cinco tarjetas "Hola, Ana"… apiladas. En "mil", la fila se estira: entran cientos de esferas y la pila de tarjetas se vuelve torre.
- CÁMARA: grúa que baja desde el campo a plano medio de la fila en tres cuartos; en "mil", dolly out rápido (zoom out = "cuántos hay").
- TEXTO EN PANTALLA: los nombres; "×1000".

### recorre · 12,5–22,9 s
- VOZ: "El bucle for dice otra cosa. Para cada nombre de la lista, saludalo." / "Python toma el primero, hace lo que está adentro y pasa al siguiente."
- SE VE: la torre de tarjetas se desarma. Aparece una tarjeta blanca redondeada con el código de 3 líneas (`for nombre in nombres:` / `print("Hola", nombre)`). Un anillo blanco (el for) se apoya sobre la primera esfera: se ilumina y sale "Hola, Ana"; el anillo salta a la siguiente.
- CÁMARA: dolly in a la tarjeta de código (quieta mientras se nombra); travelling lateral acompañando al anillo de esfera en esfera.
- TEXTO EN PANTALLA: el código; `for` en tan.

### adentro · 22,9–31,5 s · el tramo en negro
- VOZ: "Pero el for no cuenta vueltas." / "Le pide a la lista el próximo elemento, una y otra vez. Cuando no queda ninguno, termina solo."
- SE VE: la cámara atraviesa el anillo y todo pasa a negro. Adentro, la lista es un tubo de vidrio que entrega una esfera por vez a la boca del for ("próximo"). La última sale, el tubo queda vacío y aparece la etiqueta "fin".
- CÁMARA: atravesar el anillo (transición sin corte); contrapicado del tubo, quieto mientras cae cada esfera; leve dolly in en "termina solo".
- TEXTO EN PANTALLA: "próximo" · "fin".

### rango · 31,5–38,9 s · detalle de profesional
- VOZ: "Por eso un rango de mil millones de números ocupa casi nada. Los números se crean de a uno."
- SE VE: se sale del negro al blanco. Una sola esfera negra con la píldora `range(1 000 000 000)` y "48 bytes"; de ella nacen números de a uno (0, 1, 2…) que se van y se apagan.
- CÁMARA: cenital que gira despacio sobre la esfera; quieta en "casi nada".
- TEXTO EN PANTALLA: `range(1 000 000 000)` · "48 bytes".

### payoff · 38,9–44,5 s
- VOZ: "Así, tres líneas alcanzan para un millón. Cambia la lista, no el código."
- SE VE: la tarjeta de código, chica, adelante; detrás, una onda de luz recorre un campo de un millón de esferas (el mismo del gancho: el video cierra el loop).
- CÁMARA: grúa hacia arriba + gran alejamiento hasta el plano general del gancho.

### cierre · CTA
- VOZ: "Dale me gusta y seguime para aprender más de Python."
- SE VE: "Dale like y seguime para aprender más de Python" + firma chica debajo.

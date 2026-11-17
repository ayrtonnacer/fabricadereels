---
tipo: concepto
tema: "Python"
concepto_unico: "En Python, una variable es un nombre que apunta a un valor, no una caja."
duracion_objetivo_s: 70
palabras_max: 185
gancho_tipo: "mito"
loop: "Si una variable no es una caja, ¿qué es?"
cierre_loop: "Una variable no guarda el valor. Lo nombra."
detalle_profesional: "pedido = compras no copia la lista: un cambio por un nombre se ve en el otro. Con enteros, x += 1 crea un número nuevo y mueve solo esa etiqueta (son inmutables; las listas son mutables)."
titulo_portada: "Una variable es una etiqueta"
fuentes: ["Variables in Python: Usage and Best Practices (Real Python)", "Referencia del lenguaje Python, 4.2 Naming and binding (docs.python.org)", "medido en Python 3.13: a=[1,2]; b=a; b.append(3) → a==[1,2,3]; x=19; y=x; x+=1 → y==19"]
verificado: true
---
### gancho · 0–3,6 s
- VOZ: "En Python, una variable no es una caja."
- SE VE: título (etiqueta en tan) + una caja de línea gris tachada y un valor con una etiqueta colgada
- CÁMARA: plano medio frontal, leve picado; push-in lento
### nombre · cuerpo A (qué es y cómo se crea)
- VOZ: l02–l04 (ver video.json)
- SE VE: un valor (19) flota en la memoria; baja la etiqueta "edad" y se le pega; la etiqueta se usa en una cuenta y el 19 reemplaza al nombre
- CÁMARA: travelling lateral hacia la memoria, quieta al nombrar; push-in suave a la cuenta
### tipo · cuerpo B (el tipo vive en el valor)
- VOZ: l05–l07
- SE VE: tres valores con su forma (número, texto, lista) y su tipo grabado en el bloque; la etiqueta se despega del número y se pega al texto
- CÁMARA: plano general de los tres valores; travelling corto lateral para el movimiento de la etiqueta
### compartida · giro + detalle de profesional (mutable / inmutable)
- VOZ: l08–l15 (ver video.json)
- SE VE: una lista con dos bloques (pan, leche) y la etiqueta "compras"; baja "pedido" y se pega a la MISMA lista (dos hilos, un objeto); la lista se rotula "mutable" (con un renglón que se escribe por dentro); entra "huevos" por el hilo de pedido y crece una sola lista. Al lado, el 19 rotulado "inmutable" con dos etiquetas; al sumarle uno aparece un 20 nuevo y solo una etiqueta salta a él, la otra queda en el 19
- CÁMARA: travelling lateral a la lista; grúa ascendente para ver los dos hilos; quieta cuando entra "huevos"; travelling lateral al número; quieta en el 20 y el 19
### payoff
- VOZ: l16
- SE VE: plano general: etiquetas, hilos y valores; la caja del gancho desaparece
- CÁMARA: dolly out, quieta
### cierre · CTA
- VOZ: "Dale me gusta y seguime para aprender más de Python."

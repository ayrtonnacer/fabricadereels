---
tipo: concepto
tema: "Python"
concepto_unico: "La barra invertida avisa a Python que lo que sigue es una orden, no una letra."
duracion_objetivo_s: 45
palabras_max: 125
gancho_tipo: "error común"
loop: "¿Por qué Python rompe esta ruta sin avisar?"
cierre_loop: "Porque \\n y \\t son órdenes; con una r delante Python respeta cada barra."
detalle_profesional: "La ruta tiene 22 caracteres escritos pero Python cuenta 20: cada barra+letra se funde en uno solo."
titulo_portada: "La barra que rompe rutas"
fuentes: ["Python Print New Line (K. Fessel)", "medido en Python 3.13: len('\\n')=1; len('C:\\new_folder\\text.txt')=20, con r delante 22"]
verificado: true
---
### gancho · 0–3 s
- VOZ: "Python rompe esta ruta de archivo sin avisarte."
- SE VE: título "La barra que rompe rutas" (rompe en tan) + la ruta C:\new_folder\text.txt (estación A)
- CÁMARA: plano medio frontal, leve picado; push-in lento
### orden · contexto
- VOZ: "La barra invertida no es una letra. Es una orden."
- SE VE: la barra se separa de la ruta y queda sola, grande, en tan
- CÁMARA: travelling lateral corto (0,8 s) y queda quieta
### salto · cuerpo A
- VOZ: l03 + l04 (ver video.json)
- SE VE: dos bloques "\" y "n" se funden en UN bloque; el renglón se dobla y baja a la línea siguiente (1 solo carácter); cada mensaje cae en su renglón
- CÁMARA: grúa descendente al renglón; contrapicado al bloque; retención quieta al nombrarlo
### ruta · giro + cuerpo B
- VOZ: l05–l08
- SE VE: la ruta se parte: "\n" salta de línea, "\t" abre un hueco; contador 22 → 20
- CÁMARA: dolly out al plano general, luego dos acercamientos laterales (uno por barra), quieta en el contador
### payoff
- VOZ: "La solución: una erre delante de las comillas. Así Python respeta cada barra."
- SE VE: una "r" aterriza delante de las comillas y la ruta vuelve entera (22)
- CÁMARA: plano general, quieto
### cierre · CTA
- VOZ: "Dale me gusta y seguime para aprender más de Python."

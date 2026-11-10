---
tipo: concepto
tema: "Conceptos básicos de redes: switch, router y punto de acceso (Cisco, Networking Basics)"
concepto_unico: "Switch, router y punto de acceso: tres equipos, tres funciones distintas en una red."
duracion_objetivo_s: 60
wps: 2.3
palabras_max: 138
cierre: cta
loop_principal: "¿Qué trabajo hace cada uno: switch, router y punto de acceso?"
cierre_loop: "El switch une adentro, el router conecta hacia afuera, el punto de acceso extiende."
verificado: sí   # todo sale del artículo, en su orden (switch → router → punto de acceso); ver tabla de fidelidad
fuente: https://www.cisco.com/site/us/en/learn/topics/small-business/networking-basics.html
serie: parte 1 de 2 (parte 2: tipos de switch y despliegues inalámbricos)
---
## Voz (137 palabras ≈ 60 s a 2,3 palabras/s)
| Bloque | Voz |
|---|---|
| HOOK · 0–4 s · 9 pal | Switch, router y punto de acceso: tres trabajos distintos. |
| CONTEXTO · 4–9 s · 11 pal | Con ellos tus equipos se hablan entre sí y con internet. |
| SWITCH · 9–22 s · 26 pal | El switch es la base de casi toda red de empresa. Actúa como controlador: conecta computadoras, impresoras y servidores dentro de un edificio o un campus. |
| ROUTER · 22–38 s · 33 pal | El router conecta varias redes entre sí, y a tus equipos con internet, para que todos compartan una sola conexión. Funciona como un despachador: analiza los datos, elige la mejor ruta y los envía. |
| PUNTO DE ACCESO · 38–51 s · 29 pal | El punto de acceso permite conectarse sin cables. Funciona como amplificador: el router da el ancho de banda y él lo extiende, para soportar más dispositivos y llegar más lejos. |
| PAYOFF · 51–55 s · 14 pal | El switch une adentro, el router conecta hacia afuera, el punto de acceso extiende. |
| CTA · 55–61 s · 15 pal | Si te gustó el video, dale me gusta, y seguime para aprender más de redes. |
(Total: 9+11+26+33+29+14+15 = 137. Sin micro-loop: en 60 s se permiten 0–2 y acá el contenido ya es denso.)

## Fidelidad al artículo
| Lo que dice el video | Lo que dice Cisco |
|---|---|
| tres equipos permiten que tus dispositivos se comuniquen entre sí y con internet | «Switches, routers y wireless access points son lo esencial… los dispositivos pueden comunicarse entre sí y con otras redes, como Internet» |
| switch: base de casi toda red de empresa; controlador; computadoras, impresoras y servidores en un edificio o campus | «Switches are the foundation of most business networks. A switch acts as a controller, connecting computers, printers, and servers to a network in a building or a campus» |
| router: conecta varias redes y las computadoras con internet; una sola conexión compartida | «Routers connect multiple networks together… enable all networked computers to share a single Internet connection» |
| router como despachador: analiza, elige la mejor ruta, envía | «A router acts a dispatcher. It analyzes data being sent across a network, chooses the best route… and sends it on its way» |
| punto de acceso: conecta sin cables; amplificador: el router da el ancho de banda y él lo extiende | «An access point allows devices to connect to the wireless network without cables… acts like an amplifier… While a router provides the bandwidth, an access point extends that bandwidth so that the network can support many devices… from farther away» |
| payoff: switch adentro / router afuera / punto de acceso extiende | resumen de las tres definiciones (no es una frase del artículo) |

**En pantalla (chips, sin voz) para no perder contenido del artículo:**
- Switch: «Administrado en sitio» (configurás y monitoreás tu LAN, más control del tráfico) · «Administrado en la nube» (gestión multisitio, actualizaciones automáticas).
- Router: «Firewall» · «VPN» · «Telefonía IP» (opciones según la seguridad que necesites); «prioridad por equipo».
- Punto de acceso: datos de los dispositivos y seguridad proactiva; «Estándares IEEE: cada uno con su frecuencia, ancho de banda y cantidad de canales».
**Parte 2 (otro reel):** tipos de switch, y los tres despliegues inalámbricos: centralizado (campus, controladores en sitio), convergente (sucursales: un access switch hace de switch y de controlador) y en la nube (Cisco Meraki).

## Estructura técnica (borrador; se confirma con los tiempos reales de la voz)
Mundo 3D: **sala técnica de una oficina** (no repite el pasillo de servidores de la demo ni el USB del Parrot): un rack con el switch (44 cm de ancho), un router (≈25 cm), un punto de acceso de techo (≈20 cm), computadoras, impresora y servidor a escala real; un cable que sale hacia «Internet». Referencias: Motion Templates (objeto → mundo, cursor que dispara), Instagram strategy (una frase por beat, un impacto por idea). Corriente del reel: izquierda; `zoom` (Z adelante) para entrar a cada equipo; grúa a cenital solo en el payoff.

| Esc | Tiempo (estim.) | Qué se ve | Cámara / transición de salida | Texto en pantalla | SFX |
|---|---|---|---|---|---|
| s1 Hook | 0–4 | Los tres equipos en fila, apagados, vista frontal; firma @ayrtonnacer | órbita corta + push-in → `curva-izq` | «Switch · Router · Punto de acceso» (nombres en acento al decirse) | boom corto |
| s2 Contexto | 4–9 | Se encienden y aparecen líneas entre dispositivos y una nube «Internet» | cenital con giro lento → `curva-izq` | «Comunicación: entre sí y con otras redes» | tono de enlace |
| s3 Switch | 9–22 | Cámara entra al rack; el switch enciende puertos: PC, impresora y servidor; marco «edificio / campus» | `mover` hacia el switch (push-in) → `zoom` | «Switch» · chips «en sitio / en la nube» | ticks de LEDs, impacto al encender |
| s4 Router | 22–38 | Dos redes (LAN y otra red) unidas por el router y salida a internet; al llegar datos, se iluminan varias rutas y se elige una | `fpv` por el cable hacia el router → `latigazo` hacia el globo | «Router» · chips «Firewall · VPN · Telefonía IP» | riser corto + whoosh en el latigazo |
| s5 Punto de acceso | 38–51 | Router → ancho de banda como barra; el punto de acceso de techo la extiende en ondas a más dispositivos y más lejos | órbita + `foco` | «Punto de acceso» · «Ancho de banda» · «Estándares IEEE» | tono ascendente al extender |
| s6 Payoff | 51–55 | Cenital: los tres, cada uno con su verbo iluminado | grúa que sube a cenital | «Une · Conecta · Extiende» (en acento) | un impacto limpio |
| s7 CTA | 55–61 | Cierre quieto: CTA y firma | corte seco, 3 s de quietud | «Dale like» · «Seguime para aprender más de redes» · @ayrtonnacer | ding suave |

Música: no hay ninguna en el repo (`assets/musica/` vacío); falta tu pista y su BPM. Pronunciación a agregar al diccionario (sin verificar): switch → «suich», router → «rúter».

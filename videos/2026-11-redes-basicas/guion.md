---
tipo: concepto
tema: "Conceptos básicos de redes (Cisco: Networking Basics, What You Need To Know)"
concepto_unico: "Una red son tres aparatos con tres trabajos: extender, unir y despachar."   # 12 palabras
duracion_objetivo_s: 45
wps: 2.3
palabras_max: 103
cierre: cta
loop_principal: "¿Por cuáles tres aparatos pasa tu mensaje antes de llegar a internet?"
cierre_loop: "Punto de acceso, switch y router: tres aparatos, tres trabajos."
verificado: parcial   # definiciones: sí (artículo de Cisco); orden punto de acceso → switch → router: configuración típica, no la dice el artículo
fuente: https://www.cisco.com/site/us/en/learn/topics/small-business/networking-basics.html
---
## Voz (101 palabras ≈ 44 s a 2,3 palabras/s)
| Bloque | Voz |
|---|---|
| HOOK · 0–3 s · 9 pal | Tu mensaje pasa por tres aparatos antes de internet. |
| CONTEXTO · 3–7 s · 9 pal | Seguilo conmigo. Sale de tu celular, por el aire. |
| CUERPO A · 7–19 s · 25 pal | Primero lo recibe el punto de acceso: conecta tus equipos sin cables. Después pasa por el switch, que une computadoras, impresoras y servidores del edificio. |
| MICRO-LOOP · 19–22 s · 7 pal | Pero todavía no salió de la red. |
| CUERPO B · 22–33 s · 26 pal | El router conecta tu red con otras, y con internet. Es como un despachador: mira adónde va cada dato, elige el mejor camino y lo manda. |
| PAYOFF · 33–37 s · 10 pal | Punto de acceso, switch y router: tres aparatos, tres trabajos. |
| CTA · 37–44 s · 15 pal | Si te gustó el video, dale me gusta, y seguime para aprender más de redes. |

## Estructura técnica (borrador; se confirma con los tiempos reales de la voz)
Mundo 3D: **maqueta de una oficina** vista desde arriba (piso con escritorios, techo con un disco, canaleta con cable, rack, salida a internet). Dispositivos a escala real: punto de acceso ≈20 cm, switch de rack 44 cm de ancho, router ≈25 cm, celular ≈15 cm. El «mensaje» es un punto de luz (`var(--acc)`) que viaja por la maqueta. Referencias elegidas: Motion Templates (silencio → clic → arranca todo; objeto → mundo), Instagram strategy (una frase por beat, un impacto por idea, una palabra en el acento).
Corriente del reel: izquierda. Vectores reservados: Z adelante (`zoom`) para entrar a cada aparato; arriba (grúa a cenital) solo en el payoff.

| Esc | Tiempo (estim.) | Qué se ve | Cámara / transición de salida | Texto en pantalla | SFX |
|---|---|---|---|---|---|
| s1 Hook | 0–4 | Cenital de la maqueta; el celular con un punto de luz; firma @ayrtonnacer arriba | cenital con giro lento → `curva-izq` | «Tres aparatos» (tres en acento) | boom corto al aparecer; silencio de 0,4 s antes del clic |
| s2 Celular | 4–8 | Primer plano del celular, clic en «enviar»; el punto de luz sale como ondas | cámara se pega al punto (toma `fpv` corta) → `zoom` hacia el techo | — | clic, whoosh suave |
| s3 Punto de acceso | 8–13 | El punto llega al disco del techo; el disco se enciende y reparte señal a laptops y celulares | órbita corta + push-in → `curva-izq` | «Extiende» | tono de enlace al encender |
| s4 Switch | 13–19 | El punto baja por la canaleta (FPV) hasta el rack; el switch enciende sus puertos: PC, impresora y servidor | `fpv` por la canaleta → `zoom` dentro del switch | «Une» | ticks de LEDs, un impacto al llegar |
| s5 Micro-loop | 19–22 | El punto frena en el borde de la maqueta: el límite de la red; grúa corta muestra que todo es «adentro» | pull-out en cenital, 0,4 s de quietud | — | silencio y un grave suave |
| s6 Router | 22–33 | El punto llega al router; se abren varios caminos hacia otras redes; elige uno y sale por el cable hacia un globo (internet) | `mover` con ease `entrada` hacia el router, bifurcaciones que se encienden, `latigazo` hacia el globo | «Despacha» | riser corto y whoosh en el latigazo |
| s7 Payoff | 33–37 | Cenital: los tres tramos recorridos quedan iluminados con sus tres nombres | grúa que sube a cenital (elevación = conclusión) | «Extender · Unir · Despachar» | un impacto limpio |
| s8 CTA | 37–44 | Cierre quieto: CTA y firma en acento | corte seco, 3 s de quietud | «Dale like» · «Seguime para aprender más de redes» · @ayrtonnacer | ding suave |

Música: no hay ninguna en el repo (`assets/musica/` vacío). Con voz el sonido es escaso (un impacto por idea); falta tu pista y su BPM para ubicar los cortes.

## Qué usa y qué deja el artículo
- **Usa (definiciones de Cisco):** el punto de acceso conecta sin cables y extiende el alcance; el switch conecta computadoras, impresoras y servidores de un edificio; el router conecta redes entre sí y con internet y actúa como despachador que elige el mejor camino.
- **Deja:** los tipos de switch (en sitio o en la nube), las funciones extra del router (firewall, VPN) y los tres tipos de despliegue inalámbrico (centralizado, convergente, en la nube): son del catálogo de Cisco Meraki y rompen la regla de una idea por reel. Podrían ser un segundo reel («qué es una VPN» o «cómo se conectan las redes de una empresa»).
- **Aclaración:** que el mensaje pase en ese orden (punto de acceso → switch → router) es la configuración típica de una red chica; el artículo no lo dice. Si querés ceñirte al artículo, se cambia el orden de las escenas.

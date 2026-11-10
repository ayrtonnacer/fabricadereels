# Movimiento y transiciones (doctrina)

Fuente: reglas de movimiento de **HyperFrames** (heygen-com/hyperframes, Apache-2.0: `motion-doctrine`, `cut-the-curve`, `references/motion.md`, `review.md`), medidas por ellos cuadro a cuadro en sus propios videos. Revisado el 2026-11-08 y adaptado a este motor; **no usamos HyperFrames** (ver "Qué se tomó y qué no" al final).
Implementación: `engine/costuras.js` (transiciones entre escenas), `engine/camara3d.js` (cámara 3D), `engine/revisar.py` (chequeos).

## 1. La ley del vector (lo más importante)
> Cómo SALE una escena decide cómo ENTRA la siguiente: mismo eje, misma dirección, misma velocidad, y el corte cae a mitad del movimiento de los dos lados.

- **Eje**: lo horizontal sigue horizontal, lo vertical sigue vertical, la profundidad (Z) sigue en Z.
- **Dirección**: nunca en espejo. En Z la dirección es el SIGNO del zoom: si la salida crece (empuje hacia adelante), la entrada también crece; si la salida se achica (retroceso), la entrada también se achica. El error más común: salir alejándose y entrar con un "pop" que crece desde chico.
- **Velocidad**: la salida acelera (`acelera` = power4.in) y la entrada frena (`frena` = power4.out), con el mismo recorrido y duración: son las dos mitades de un mismo movimiento.
- **Fase**: nada se detiene antes del corte ni arranca de cero después. **La escena que entra tiene que estar compuesta en el corte** (su elemento principal ya visible y en movimiento), no esperar a que sus `data-a` arranquen desde abajo.
- Nunca se ven las dos escenas a la vez: no hay fundidos encadenados entre "mundos".

## 2. La corriente y los vectores reservados
Cada reel elige UNA dirección dominante (la "corriente"; por defecto, izquierda) y la usa en las transiciones comunes. Las otras direcciones significan algo, se GASTAN con motivo:

| Vector | Significa |
|---|---|
| la corriente (izq.) | "lo que sigue", avance neutro |
| hacia arriba | elevación: una conclusión o revelación |
| Z adelante (`zoom`, zoom through) | ir más hondo en la misma idea |
| Z atrás (`zoom-inverso`) | LLEGADA: algo grande aterriza (el payoff) |

- Nunca dos transiciones seguidas en direcciones opuestas (ping-pong): se lee como error. Cambiar de dirección necesita una causa visible (un clic, un golpe) o un cambio de capítulo.
- **Presupuesto**: 2–4 tipos de transición por reel, repetidos. La transición por defecto es `curva` en la dirección de la corriente.
- Que la corriente de cada reel sea distinta es parte de la variedad (docs/CAMARA-3D.md): un reel puede ir hacia la izquierda y el siguiente hacia arriba.

## 3. Portadores y causa
- El ojo sigue objetos, no abstracciones. La mejor transición le pasa un **portador** al otro lado: el cursor a mitad de camino, una tarjeta que se achica y se acomoda en la escena siguiente, la pantalla de la notebook que se convierte en el mundo nuevo, el nodo que la cámara atraviesa.
- **Movimiento causal**: cada movimiento lo dispara el anterior (clic → se aplasta → sale disparado → impacta → rebota → aparece). El efecto empieza EN el cuadro de la causa, nunca "un ratito después". El sonido también (docs/AUDIO.md: el whoosh en el pico).
- **Quietud antes del clímax**: 0,3–0,75 s de pausa entre la acción y el resultado (la coma dramática). El payoff se ve a velocidad normal.

## 4. Catálogo de transiciones (`"salida"` en video.json)
| `salida` | Qué hace | Cuándo |
|---|---|---|
| `curva-izq/der/arriba/abajo` | sale acelerando ~230 px (12 % del cuadro, nunca afuera de pantalla), entra en la misma dirección frenando; se apaga al final de la salida y entra desde 35 % de opacidad; blur 8 px | por defecto, en la corriente |
| `zoom` | todo crece: sale 1→1,2 con blur 0→10 px; entra 0,75→1 con blur 10→0 | ir más hondo en la misma idea |
| `zoom-inverso` | todo se achica: sale 1→0,8; entra de 1,25→1 | el payoff / una llegada (no como variedad) |
| `foco` | rack focus: pico de desenfoque (10 px) que tapa un corte seco; leve escala 1,06 como respiración de lente | el ÚNICO corte que se quiere que se vea; como mucho cada ~8 s |
| `latigazo-izq/der` | barrido de 0,15 s con desenfoque direccional; lo que llega aterriza borroso y se aclara en ~0,13 s | cambio brusco de tema |
| `oscuro` | la escena se oscurece ~40 % tres cuadros antes del corte seco | que un corte se lea intencional |
| `corte` | corte seco | dentro de una misma escena (punch-in); como mucho un tercio de las transiciones |

Blur: 10 px máximo sobre texto (20 px lo vuelve un glitch); 18–20 px solo si lo que se mueve es un cuadro completo.
En 3D (`camara3d.js`) vale lo mismo: el latigazo entre tomas, el zoom through con `destello`, y si se corta entre dos escenas 3D el movimiento de cámara sigue en la misma dirección.

## 5. Tiempos y curvas por rol
- **Llegar lento, irse limpio**: las entradas aterrizan con cola larga (`llegada` = expo.out, `frena`); las salidas son 40–50 % más cortas que las entradas y aceleran (`acelera`). Un movimiento de cámara va suave a ambos lados (`suave`). Lineal solo para rotación, progreso o velocidad constante que sea el punto (el dron).
- **El mismo `ease-out` de 0,5 s en todo** es lo que hace que un video "se sienta generado". Variar por rol.
- **Movimientos rápidos**: 0,3–0,6 s, con desenfoque de movimiento en su cuadro más rápido.
- **Reacomodar un grupo** (correr una lista, hacer lugar): curva `empujon` (rampa lenta 20 % → ráfaga lineal → cola larga 62 %), no un ease-in-out que frena de golpe.
- **Escalonado**: letras a 1 cuadro, palabras 60–120 ms, ítems de lista 40–80 ms; el siguiente arranca cuando el anterior va 30–50 %. Todo a la vez = barato; todo en fila = robótico.
- **Lectura**: una línea que hay que leer queda ≈ 0,5 s + 0,3 s por palabra; la última del video, al menos 2 s.
- **Ritmo**: contrastar velocidades. Planos de 1,8–3 s con movimiento adentro; montajes rápidos cada 0,13–0,8 s; una demo puede sostener 7–10 s si adentro pasan cosas.

## 6. Señales de "video hecho por IA" (evitarlas)
- todas las escenas entran igual, o el mismo movimiento beat tras beat;
- todo aparece con fundido + deslizamiento hacia arriba;
- títulos que siguen moviéndose o escalando después de aterrizar (**un título que aterrizó queda quieto**; el movimiento pasa al siguiente elemento, a la cámara o al fondo);
- loops de "respiración", flotado o pulso que reemplazan al movimiento con intención;
- vacío oscuro con cositas flotando, brillo y partículas sin motivo; tres tarjetas en fila;
- rebote en interfaz, anillos de clic.
Ya aprendido con Ayrton (DECISIONES.md): mayúsculas espaciadas, HUD/esquinas, scanlines.

## 7. Revisión antes de renderizar
1. `./reel revisar videos/X` (estático) y `--quietud` (busca tramos de más de 3 s sin cambios y el primer cuadro vacío, que es la miniatura).
2. `preview` en el cuadro de cada costura (−0,1 / +0,05 s) y en el pico de cada movimiento.
3. Mirar los cuadros como un extraño: describir cada uno en una frase nombrando todo lo que hay; si algo hay que explicarlo, es un problema.
4. Anotar cada problema en una línea: `t=4,2 s · dónde · problema → cambio exacto · qué queda igual`, con prioridad **P0** (no se entiende / rompe una regla), **P1** (debilita: tramo muerto, payoff flojo, costura que salta), **P2** (detalle). Arreglar todos los P0 y los P1 que valgan la pena; texto primero, después tiempos, después detalles. Si se siente cargado: sacar un tercio del movimiento y quedarse con lo que guía la mirada.

## Conflictos con lo que ya teníamos (decide Ayrton)
- `docs/DINAMISMO.md` pide "que nunca quede quieto" con zoom lento (Ken Burns 1,00→1,06). HyperFrames considera el zoom lento sobre un título y los loops de respiración una señal de video generado, y propone en su lugar revelar contenido al ritmo de la voz, mover la cámara con intención o que la interfaz "haga cosas". No se cambió nada: Ayrton elige. Mientras tanto: un título que aterrizó queda quieto; el zoom lento, si se usa, va sobre el fondo o el 3D, no sobre el texto.
- El `temblor` de cámara de `camara3d.js` es cámara en mano o dron (actuación con intención), no un loop de respiración; usarlo solo cuando el plano lo pida.

## Qué se tomó de HyperFrames y qué no
- **Se tomó**: la ley del vector, la corriente, el catálogo de costuras con sus números, las curvas por rol y la `empujon`, el dolly zoom (`vertigo` en camara3d.js), la lista de señales de video generado, los chequeos de `check` que aplican (determinismo, transiciones CSS, tramos quietos, primer cuadro vacío), la revisión P0/P1/P2, y del flujo `reverse-any-video` la tira de cuadros alrededor de cada corte (`hoja-cortes` en analizar_video.py).
- **No se tomó**: el motor en sí (GSAP + su CLI). El nuestro ya hace lo mismo (render determinístico de HTML/three.js con Playwright + FFmpeg) y tiene la voz, el audio, el tema y el 3D a medida; migrar implicaría rehacer el Parrot que ya gusta. Tampoco sus servicios pagos (render en la nube, "reverse" Pro, modelos de HeyGen).

# Cómo escribir el guion
Base: `docs/INVESTIGACION-GUIONES.md` (investigación completa, con fuentes y plantillas por tipo de reel). Acá va lo que se aplica siempre. Donde la investigación choca con una decisión de Ayrton, gana Ayrton (ver "Conflictos").

## Público
**Mixto** (Ayrton, 2026-11-09): gente técnica, **principiantes que están aprendiendo** y **reclutadores** que buscan perfiles técnicos. Los reels son también el portfolio de Ayrton: tienen que **demostrar que sabe**. Entonces:
- Explicar bien y con precisión, sin tratar a nadie de tonto ni simplificar de más (un técnico nota lo incorrecto). Vocabulario del área sí, pero cada término nuevo se ancla con una imagen o una frase corta para que el principiante no se pierda.
- Cada reel lleva **un detalle de profesional**: algo preciso que no está en la explicación típica (por ejemplo, que en 2,4 GHz solo los canales 1, 6 y 11 no se pisan). Es lo que diferencia "lo copié" de "lo entiendo". Si no sale de la fuente, se marca como tal en el checkpoint y se verifica.
- Mostrar el mecanismo (el porqué), no solo el nombre de las cosas.

## Reglas de siempre
- Voz en español rioplatense (voseo): "Necesitás", "elegí", "seguime". Escribir como se habla ("ojo", "pensalo así", "posta").
- Frases cortas (≤ 12 palabras). Un paso = una o dos frases.
- NO leer: comandos, rutas, texto de carteles/tarjetas. La voz explica el porqué; la pantalla muestra el qué.
- Términos técnicos sí (público técnico), pero dichos como se hablan: siglas y palabras en inglés por el diccionario de pronunciación. Explicar solo lo que no es de uso común en el área.
- Cero palabras prohibidas (ver `pronunciacion.json`): pendrive→memoria, like→me gusta, dev, guardalo.
- Sin muletillas de IA: "¿Sabías que…?", "En el mundo de…", "Imaginá…", "Sumérgete", "Desbloqueá", "Aquí está la clave", "y lo mejor de todo". Ni hooks vacíos ("No vas a creer…", "Esto cambia todo", "El 99% no sabe esto").
- Advertencias importantes (p. ej. "se borra todo") van en pantalla, no en la voz.
- En el texto de pantalla se puede escribir "like"; en `voz.lineas[].texto` va "me gusta".
- Formato del guion para aprobar: tabla escena | pantalla | voz | duración (más los campos de abajo si hace falta).

## Estructura (45 s, ~100–110 palabras de voz)
Hook-promesa (0–3 s) → Contexto mínimo (3–7) → Cuerpo A (7–20) → Micro-loop/giro (20–23) → Cuerpo B (23–36) → **Payoff que cierra lo prometido en el hook** (36–41) → CTA (41–45).
- **30 s:** sin contexto ni micro-loop. **60 s:** agregar un segundo micro-loop. **Tutorial con más de 4 pasos → serie de 2–3 partes** (cada parte se entiende sola).
- Duración = la mínima que necesita UNA idea completa. Nunca más de 3 min.
- **Un solo loop principal**: se abre en el hook y se cierra en el payoff, antes del CTA. Nunca dos abiertos a la vez. **Jamás un loop abierto justo antes del CTA.**
- El cierre es *literal* respecto de lo prometido ("lo rompés en segundos" → se muestra cómo se rompe en segundos).
- **Hook:** 1–3 s, 6–9 palabras, promesa verificable que el video cumple; el primer cuadro ya muestra algo concreto (terminal, hash, mensaje cifrado), nunca logo ni "hola, hoy vamos a ver". Fórmulas: resultado primero, mito, error común, historia, pregunta, dato sorprendente, desafío, comparación, humor. Alternar el tipo entre videos.
- **Una idea por reel**, escrita en una frase de ≤ 12 palabras. Si hace falta "y además…", son dos reels.
- Proceso: elegir concepto → buscar el ángulo (error, historia, sorpresa) → **escribir primero el payoff y después el hook** → elegir la analogía visual antes del cuerpo (rueda, interruptores, embudo, resto) → recortar sin piedad.

## Calibración de la voz (medido en este repo)
- Piper Daniela con `length_scale 0.92` habla ≈ 3,4 palabras/s *mientras habla*; con pausas y escenas, el video completo da **≈ 2,3 palabras/s**. **Planificar con 2,3 wps** (ojo: el reel de WiFi, con 103 palabras en 33 s, midió **3,11 pal/s** en total y 3,9 hablando; la referencia citada es 2,77. Para público que aprende, apuntar a ~2,8 y recortar o bajar la velocidad de la voz; ver `docs/MEDICION.md`) (la investigación sugiere 2,5 genérico): 30 s ≈ 69 palabras, 45 s ≈ 103, 60 s ≈ 138.
- Contar palabras *como se pronuncian*: "777" = 3, "SHA-256" = 4–5, "@ayrtonnacer" = "arroba ayrton nacer".

## Lo visual del guion (Mayer + práctica)
- Cada indicación visual cae *mientras* la voz nombra la cosa (contigüidad). Nada queda igual más de 3 s: un cambio cada 2–3 s.
- Texto grande en pantalla solo para el término o número que se enseña, no para repetir la oración (redundancia). Resaltar la palabra clave con el acento del tema.
- Construcción progresiva (la fórmula o tabla se arma al ritmo de la voz); zoom al resultado cuando algo "da"; antes/después en rojo/verde.
- Sonido: música de colchón baja; 3–5 SFX con significado fijo (tecla = acción, ding = resultado, tono grave = problema).

## Cierre
- **El texto del cierre en pantalla coincide con la voz** (Ayrton, 2026-11-09): "Dale like y seguime para aprender más de <tema>" (en voz: "dale me gusta y seguime…").
- "aprender más **de** <tema>" para temas de una palabra (redes, Linux); "**sobre** <tema>" para temas largos o frases ("sobre cómo funciona internet").
- Fórmula multiplataforma: "Dale me gusta y seguime para aprender más de <área concreta>." (variar el área; nunca "guardalo"). En pantalla, la firma `@ayrtonnacer`.
- **Versión bucle** (shorts/reels): sin CTA hablado; la última frase desemboca en el hook y el último cuadro vuelve al primero (cámara en la misma pose al final y al principio; el corte se esconde en un movimiento; música en silencio en el empalme; ver el video Parrot en bucle en el historial de git, commit `ae9a888`). Para contenido educativo funciona mejor como *desafío* ("¿te animás a descifrar el mensaje del principio?") que como truco de edición.
- En humor: el CTA mata el remate; solo texto en pantalla o nada.

## Originalidad (riesgo de "contenido no auténtico" en YouTube)
La plantilla fija la **arquitectura** (bloques, tiempos, campos), no las frases, hooks ni animaciones. Variar tipo de hook, analogía visual y música entre videos. Poner marca personal en cada guion (primera persona, anécdota de la cursada, un error real, un callejón sin salida). Material propio en pantalla; nada de capturas ajenas sin transformar. Fuente primaria en la descripción para historias de hackeos; nunca flags de máquinas activas de HTB.

## Conflictos con la investigación (decide Ayrton)
- La investigación sugiere evitar el "verde Matrix". Ayrton eligió HackTheBox (lima sobre azul-negro) para Parrot: se mantiene.
- Sugiere subtítulos de 2–4 palabras. Ayrton pidió **no** agregarlos por ahora: se mantiene.
- Sugiere tutoriales de un solo Short ≤ 4 pasos. Parrot (7 pasos, 54–58 s) quedó como video único porque a Ayrton le gustó así; en temas nuevos, ofrecer serie.

## Checklist antes de aprobar el guion
- [ ] Concepto en ≤ 12 palabras. [ ] Hook ≤ 3 s, promesa que se cumple. [ ] Primer cuadro concreto.
- [ ] Un loop abierto en el hook y cerrado en el payoff, antes del CTA. [ ] Palabras pronunciadas ≤ duración × 2,3.
- [ ] Sin muletillas de IA ni términos sin explicar. [ ] Al menos una marca personal. [ ] Cifras y comandos verificados/ejecutados.
- [ ] Cada bloque con visual sincronizado a una palabra y su movimiento de cámara (`docs/CAMARA.md`); nada quieto > 3 s. [ ] Otro tipo de hook y de analogía que el video anterior.
Plantilla de guion: `videos/_plantilla/guion.md`.

# Cómo escribir el guion
Base: `docs/INVESTIGACION-GUIONES.md` (investigación completa, con fuentes y plantillas por tipo de reel). Acá va lo que se aplica siempre. Donde la investigación choca con una decisión de Ayrton, gana Ayrton (ver "Conflictos").

## Reglas de siempre
- Voz en español rioplatense (voseo): "Necesitás", "elegí", "seguime". Escribir como se habla ("ojo", "pensalo así", "posta").
- Frases cortas (≤ 12 palabras). Un paso = una o dos frases.
- NO leer: comandos, rutas, texto de carteles/tarjetas. La voz explica el porqué; la pantalla muestra el qué.
- Evitar tecnicismos; si es imprescindible, nombrarlo y explicar en una palabra ("herramienta", "memoria", "descomprimir").
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
- Piper Daniela con `length_scale 0.92` habla ≈ 3,4 palabras/s *mientras habla*; con pausas y escenas, el video completo da **≈ 2,3 palabras/s**. **Planificar con 2,3 wps** (la investigación sugiere 2,5 genérico): 30 s ≈ 69 palabras, 45 s ≈ 103, 60 s ≈ 138.
- Contar palabras *como se pronuncian*: "777" = 3, "SHA-256" = 4–5, "@ayrtonnacer" = "arroba ayrton nacer".

## Lo visual del guion (Mayer + práctica)
- Cada indicación visual cae *mientras* la voz nombra la cosa (contigüidad). Nada queda igual más de 3 s: un cambio cada 2–3 s.
- Texto grande en pantalla solo para el término o número que se enseña, no para repetir la oración (redundancia). Resaltar la palabra clave con el acento del tema.
- Construcción progresiva (la fórmula o tabla se arma al ritmo de la voz); zoom al resultado cuando algo "da"; antes/después en rojo/verde.
- Sonido: música de colchón baja; 3–5 SFX con significado fijo (tecla = acción, ding = resultado, tono grave = problema).

## Cierre
- Fórmula multiplataforma: "Dale me gusta y seguime para aprender más de <área concreta>." (variar el área; nunca "guardalo"). En pantalla, la firma `@ayrtonnacer`.
- **Versión bucle** (shorts/reels): sin CTA hablado; la última frase desemboca en el hook y el último cuadro vuelve al primero (ver `videos/2026-11-parrot-loop`). Para contenido educativo funciona mejor como *desafío* ("¿te animás a descifrar el mensaje del principio?") que como truco de edición.
- En humor: el CTA mata el remate; solo texto en pantalla o nada.

## Qué es fijo y qué varía entre reels
- **Fijo (identidad de @ayrtonnacer):** voz Piper Daniela, música de fondo, estética visual (tema `cyber.css`, IBM Plex, color = significado), firma al inicio y al final.
- **Varía en cada reel:** tipo de reel (concepto, mito, tutorial, historia, CTF, matemática visual…), tipo de hook, analogía visual, mundo 3D, plan de cámara y transiciones, ritmo, duración. Las reglas de este documento fijan la *arquitectura* del guion, no la apariencia ni la coreografía. Antes de planear un reel, revisar el anterior y elegir algo distinto en hook, analogía y cámara.

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
- [ ] Cada bloque con visual sincronizado a una palabra; nada quieto > 3 s. [ ] Otro tipo de hook y de analogía que el video anterior.
Plantilla de guion: `videos/_plantilla/guion.md`.

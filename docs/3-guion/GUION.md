# Cómo escribir el guion
Lo que se aplica siempre. La investigación completa, con fuentes y plantillas por tipo de reel, está en `INVESTIGACION-GUIONES.md` (consulta; donde choque con este documento o con Ayrton, gana este). Público: `docs/1-canal/PUBLICO.md`.

## Para quién
**La mayoría no es de IT**; también miran principiantes y reclutadores (los reels son el portfolio de Ayrton). Las dos cosas a la vez:
- **Se entiende sin saber nada de antemano.** Cada término nuevo llega con una imagen o un ejemplo cotidiano (una planilla, una foto, un video). Sin jerga de especialista en un reel introductorio.
- **No tiene errores que un experto pueda marcar**, y trae **un detalle de profesional**: algo preciso que no está en la explicación típica (p. ej. que en 2,4 GHz solo los canales 1, 6 y 11 no se pisan).
- Se muestra el **mecanismo** (el porqué), no solo el nombre de las cosas. No se trata a nadie de tonto.

## Proceso
1. **Una idea**, escrita en una frase de ≤ 12 palabras. Si hace falta "y además…", son dos reels (ofrecer serie).
2. Elegir el **ángulo**. Para un tema nuevo, ofrecer 2–3. El guion cubre el tema central de la fuente.
3. **Escribir primero el payoff y después el gancho** (el payoff cierra literalmente lo que el gancho promete).
4. Elegir **el ejemplo que crece**: un caso cotidiano que avanza de a un paso (píxel → fila → foto → video; un mensaje → pedazos → números). Cada paso es una estación del set.
5. Poner los **datos concretos y verificados** (2–4 números o mecanismos medidos). El "para qué sirve" se muestra funcionando dentro de la explicación, no como lista al final.
6. Recortar sin piedad hasta que entre en el ritmo.

## Estructura (45 s ≈ 110–125 palabras)
| Bloque | Segundos | Palabras | Qué hace |
|---|---|---|---|
| **Gancho** | 0–3 | 6–10 | promesa verificable que el video cumple; el cuadro 0 ya muestra algo concreto (título + objeto) |
| Contexto | 3–7 | 8–12 | lo mínimo para entender la pregunta |
| Cuerpo A | 7–20 | ~32 | el primer paso del ejemplo |
| Giro | 20–23 | 6–8 | "pero…": mantiene la atención (solo en 45–60 s) |
| Cuerpo B | 23–36 | ~32 | el segundo paso; el detalle de profesional |
| **Payoff** | 36–41 | 10–14 | cierra lo prometido en el gancho; se ve funcionando |
| **CTA** | 41–45 | 10–12 | "Dale me gusta y seguime para aprender más de <tema>." |
- 30 s: sin contexto ni giro. 60 s: un segundo giro. Tutorial con más de 4 pasos → serie de 2–3 partes que se entienden solas.
- Duración = la mínima que necesita una idea completa (lo habitual: 30–60 s).
- **Un solo loop**: se abre en el gancho y se cierra en el payoff, antes del CTA. Nunca un loop abierto justo antes del CTA.
- **Tipos de gancho** (alternar entre reels): resultado primero · mito · error común · pregunta · dato sorprendente · comparación · desafío. Nunca "hola, hoy vamos a ver".

## Reglas de la voz
- **Rioplatense, voseo**: "necesitás", "elegí", "seguime". Como se habla.
- **Frases cortas**: ideal ≤ 12 palabras; más de 16, partirla.
- **Ritmo: 2,4–2,8 palabras por segundo del video completo** (máximo 2,9). Medido en los reels que funcionaron (tokens 2,42; tensores 2,67; WiFi 2,90, que quedó rápido). Con Daniela a `length_scale` 1,05: 30 s ≈ 75–85 palabras · 45 s ≈ 110–125 · 60 s ≈ 145–165.
- Contar las palabras como se pronuncian: "777" = 3, "SHA-256" = 4–5.
- **No leer** comandos, rutas ni lo que dice un cartel: la voz explica el porqué, la pantalla muestra el qué. Las advertencias ("se borra todo") van en pantalla.
- **Palabras que no van en la voz**: "pendrive" (→ memoria), "like" (→ me gusta), "dev", "guardalo", "IA" (Piper lo lee "ya" → "inteligencia artificial"). Lista completa en `engine/audio/pronunciacion.json` → `prohibidas`.
- **Sin muletillas de IA**: "¿Sabías que…?", "En el mundo de…", "Imaginá…", "Sumergite", "Desbloqueá", "Aquí está la clave", "y lo mejor de todo", "No vas a creer…", "Esto cambia todo", "El 99 % no sabe…".
- Evitar frases con la misma palabra repetida ("con mayúscula, sin mayúscula"): la voz sintética las enreda.
- **Palabras en inglés o siglas**: fijarse si están en `pronunciacion.json`; si no, agregarlas y ofrecerle a Ayrton variantes de audio en el checkpoint.
- Marca personal: primera persona cuando suma (una anécdota, un error real).

## Lo visual del guion
- Cada cosa aparece **mientras** la voz la nombra. Un cambio visual por idea; la cámara quieta mientras se nombra (`docs/2-estilo/CAMARA.md`).
- Texto en pantalla solo para el término o el número que se enseña; nunca la oración entera (ya está el subtítulo).
- Construcción progresiva: la tabla o la fórmula se arma al ritmo de la voz.
- **Título de portada**: 3–5 palabras, una en tan; que se entienda en miniatura.

## Cierre
- Voz: **"Dale me gusta y seguime para aprender más de <tema>."** Pantalla: "Dale like y seguime para aprender más de <tema>". El tema es el mismo en los dos. "de" para una palabra (redes, Linux); "sobre" para una frase ("sobre inteligencia artificial").
- **Versión bucle** (opcional, sin CTA hablado): la última frase desemboca en el gancho y el último cuadro vuelve al primero. Funciona mejor como desafío que como truco. Avisarle a Ayrton si se propone.
- En humor: el CTA mata el remate; solo en pantalla.

## Originalidad
La plantilla fija la arquitectura, no las frases. Variar tipo de gancho, ejemplo y recorrido de cámara entre reels. **Las referencias que pasa Ayrton son para ver cómo se explica, no para copiar** su gancho, su orden ni sus objetos. Fuente primaria en la descripción; nunca flags de máquinas activas de HackTheBox.

## Formato para el checkpoint
Una tabla **escena | lo que se ve (plano y movimiento) | voz | duración**, más: la idea en una frase, el título de portada, los datos con su fuente y las pronunciaciones dudosas. Corto: Ayrton tiene que poder aprobarlo de una leída.

## Checklist antes de mostrarlo
- [ ] `python engine/reel.py guion videos/X` sin errores (ritmo, gancho, CTA, palabras prohibidas, muletillas).
- [ ] Idea en ≤ 12 palabras. [ ] Gancho con promesa que el payoff cumple. [ ] Un solo loop, cerrado antes del CTA.
- [ ] Alguien que no sabe nada lo entiende; un experto no encuentra errores. [ ] Un detalle de profesional.
- [ ] Cada dato verificado contra la fuente primaria o medido. [ ] Otro tipo de gancho y de ejemplo que el reel anterior.
Plantilla: `videos/_plantilla/guion.md`.

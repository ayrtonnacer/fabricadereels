# Preferencias de Ayrton — lo vigente, por tema
**Leer entero al empezar un reel y antes de entregarlo.** Es el destilado de todo lo que dijo (`BITACORA.md`, cronológico) y de cada corrección (`DECISIONES.md`). Acá está **solo lo que vale hoy**: cuando cambia de opinión, se reemplaza el renglón en su sección (no se agrega al final). Entre paréntesis, la fecha de la decisión.

## 1. Qué busca
- Canal **sin cara** que se reconozca en un cuadro (como Kurzgesagt, Fireship, 3Blue1Brown): **lo que se repite es la marca**. Inicio, cierre, paleta, tipografía, voz, música y sonidos fijos no varían entre reels (11-14).
- Cada reel es su **portfolio**: tiene que demostrar que sabe (un detalle de profesional) y a la vez lo obliga a aprender el tema.
- **Reels rápidos de producir** y **gastar pocos tokens**: ir directo, pocas iteraciones, no releer documentos ni regenerar de más (11-10).
- **Medir en vez de opinar**: parámetros que se puedan repetir, no "se siente" (11-10). Pero **los números son una alarma, no un objetivo**: si el ojo dice que confunde, gana el ojo (11-15).
- **Una mejora por vez, mostrada antes de sumar la siguiente** (11-07, 11-15). Ante "cambiar la estética": 3–4 cuadros antes de renderizar todo.
- **Borrar lo que no se usa.** Todo lo importante en `main`, para que otra persona pueda hacer los videos como él quiere (11-14).

## 2. Público y contenido
- **La mayoría no es de IT** (feedback del reel de tensores, 11-14). Se entiende sin saber nada de antemano y no tiene errores que un experto pueda marcar. Sin jerga de especialista en un reel introductorio (nada de "lote", "pérdida", "NCHW").
- En un reel conceptual, primero **que quede claro QUÉ ES la cosa**, con un ejemplo cotidiano que crece de a un paso (píxel → fila → foto → video). El "para qué sirve" se muestra **funcionando dentro de la explicación**, no como lista al final (11-12).
- **No quedarse en la definición**: datos técnicos concretos y verificados (números, mecanismos). Si no entra, serie (11-16).
- **Validar los datos aunque la fuente sea una empresa grande**: medir con la herramienta real (11-16). Revisión técnica antes de publicar: "no quiero cometer un papelón" (11-13).
- Un dato se muestra con **su forma real** (una foto es un bloque 3D, un sonido una fila; "bloque", no "cubo", si no es cúbico) (11-13).
- **Las referencias que pasa son para aprender CÓMO se explica o la técnica de cámara, no para copiarlas**: nunca repetir su hook, su orden ni sus objetos (11-12).
- Ante una fuente, el guion cubre **su tema central**; los ángulos laterales se ofrecen como otros reels (11-09).
- No rotular lo obvio ("pared"): "el espectador no es tonto" (11-09).

## 3. Cámara y puesta en escena
- **Un solo set 3D recorrido en plano secuencia** (le gustó la v2 de tokens, "la fábrica"): estaciones en profundidad, dolly in/out, grúa, travelling y **ángulos distintos** (picado, contrapicado, lateral) (11-16).
- **Viajes rápidos (~0,8 s) y retenciones quietas** cuando se nombra algo. Pausas para que se lea (11-15, 11-16).
- **No**: cámara que se mueve todo el tiempo, zoom de más, desenfocar o recortar lo que se explica (banco de prueba, 11-15).
- **Plano general** para mostrar las ideas juntas (escalar, vector y matriz vistos de lejos).
- **Cada reel con su propia puesta en escena**: se mantienen inicio y cierre; el medio no copia el reel anterior (orden de planos, objetos de frente, título arriba) (11-16).
- **Nada que estorbe al texto**: un decorado que pasa detrás de lo que se lee se saca (la cinta de la fábrica) (11-16).
- **Profundidad real**: objetos 3D con perspectiva, **piso de líneas en perspectiva**. No reemplazar el 3D por dibujos planos (11-07).
- Quiere que se le explique lo hecho con **vocabulario de cine** y segundos (`docs/2-estilo/GLOSARIO-EDICION.md`) (11-16).

## 4. Estética
- **Tema Scale** (por defecto desde 11-14): negro puro, objetos de **línea gris fina y continua**, **un solo acento Foundry Tan**, blanco solo para texto, cables y señal; Host Grotesk + Geist Mono.
- **El negro no se ensucia**: sin halos, degradés grises ni brillos detrás de los objetos (11-15). Los colores de Scale van de acento, **nunca de fondo** (el verde Evergreen de fondo no le gustó) (11-13).
- **No**: estética roja o Anduril, lima/HackTheBox (temas viejos), scanlines, HUD/esquinas, mayúsculas espaciadas, "// TUTORIAL", texto de la fuente al final (11-04 a 11-14).
- **Nada pixelado o "cuadrado" como protagonista** (la cara de 8×8): formas suaves, objetos con riqueza (11-12).
- **Objetos**: contornos finos (≈ 2 px; a 4–5 px se tapan), líneas que no se cortan, antenas con cuerpo, escala real, revisar cada objeto de cerca (11-11). Las notebooks no llevan antena a la vista; los routers sí (11-09).
- **Lo que se conecta se toca**: los cables salen de un puerto real y llegan al cuerpo del objeto. Lo que viaja sigue la forma del medio: cuadraditos solo sobre cables (`cable.at(s)`), en el aire solo ondas (11-11).
- **Ondas de radio = anillos** que se expanden; la senoide solo para explicar frecuencias. Ondas continuas, nunca cortadas (11-10).
- **Sin decorado sin sentido**: ni puntitos, ni bits flotando, ni un "1" suelto (11-09).
- **Tipografía**: le hacen ruido los textos muy juntos o con mucho vacío; texto centrado en su placa; chips con aire; **nunca una palabra sola en la última línea** (11-09, 11-13).
- **Media kit** (`docs/media-kit/`, 11-16): manda en portada, gancho, tamaños y reglas de uso.

## 5. Inicio y cierre (fijos)
- **Portada**: cuadro fijo de 0,1 s que sirve de miniatura: firma + título de 3–5 palabras (una en tan) + objeto protagonista con un punto tan. Después el **gancho con el mismo título** (11-13, 11-16).
- **Firma `@ayrtonnacer`** al inicio y al final, en tan, **sola** (sin punto ni adorno). Lo resaltado es lo que hay que recordar (11-04).
- **Cierre**: el foco es el **CTA**; la firma chica debajo; **nunca zoom a su usuario**. El texto coincide con la voz: "Dale like y seguime para aprender más de <tema>" ("de" para una palabra, "sobre" para una frase). **Nunca "guardalo"** (11-09).

## 6. Voz y pronunciación
- **Daniela (Piper) limpia**, sin efectos. El efecto de radio y el Adjutant se probaron y no le gustaron: no proponerlos (11-09, 11-11).
- El público marcó la voz como lo más flojo ("se nota lo robótico"); pendiente **clonar su voz** (`docs/2-estilo/AUDIO.md` → Voz propia) (11-14).
- **Ritmo**: `length_scale` 1,05 y 2,4–2,8 palabras por segundo en total; más de 2,9 es demasiado rápido para quien aprende (11-11).
- **Cuidar la pronunciación**: ante una palabra en inglés, ofrecer variantes de audio antes de usarla. Cada pronunciación que confirma o corrige va a `pronunciacion.json` en el momento (11-11, 11-12).
- Confirmadas: "uaifai" (WiFi), "ráuter", "ísernet", "gigaérts", "dos coma cuatro". No le gustó "mashín lérnin": decir "inteligencia artificial". La voz lee "IA" como "ya": escribir "inteligencia artificial".
- **Tono**: educativo de alta calidad, serio y riguroso, entretenido pero no denso. **Nada de frases canchereras** que buscan hacerse el simpático ("Python no protesta"): suenan naif. **Sin dos puntos** en la voz: la narración es oral, se escribe con puntos y comas (11-17).
- No decir "pendrive" (memoria), "like" (me gusta). No leer la terminal ni los carteles. Frases con palabras repetidas se entienden mal: simplificar.

## 7. Sonido y música
- **Sonido limpio**: sin ruido de fondo, sin glitch ni estática; efectos puntuales con significado (11-09).
- **Fijos de marca**: boom grave (`boom-cinematico`) al inicio y al final; **chinn** cuando aterriza el CTA (11-09).
- **Efectos variados**: no repetir siempre el mismo whoosh o golpe; usar los sonidos reales del banco y los propios que encajan con el tema (11-16). Tipeo real de teclado para código; sonido digital para los 0 y 1; módem para "conexión"; hit metálico mejor que un whoosh suave antes del cierre.
- **Música firma**: *Can You Hear The Music*, en todos los reels, **desde el segundo 0 (los violines)**, nivelada para que se oiga desde el principio sin tapar la voz. **No recortar una canción que él pasa sin avisar** (11-16).

## 8. Subtítulos
- **Siempre** (mucha gente mira sin sonido), en zona segura (y 1120–1320), con **barra negra** detrás, palabra dicha en tan (11-09, 11-13).
- No repetir en pantalla lo que ya dice el subtítulo.

## 9. Cómo trabajar con él
- **Checkpoint del guion antes de animar**, salvo que pida "hacelo directo".
- **Guardar todo en el repo sin que lo pida** (indicaciones, archivos, pronunciaciones, reels terminados en `docs/4-referencias/propios/`).
- **Una sola rama (`main`)**, sin pull requests; GitHub explicado en simple.
- **No instalar ni ejecutar repos de terceros** que pasa para estudiar: leerlos y tomar ideas; respetar licencias (onetake es no comercial) (11-15).
- **No publicar en redes** sin que lo pida.
- No cambiar tema, estructura y animaciones a la vez: una cosa por vez (11-07).

## 10. Pendientes abiertos (decide Ayrton)
- Voz clonada propia. Música propia con licencia (la firma actual tiene copyright: puede ser silenciada; lo más seguro es agregarla desde la biblioteca de la app).
- Los materiales de sonido de `engine/onetake/` son de **uso no comercial**: confirmar si se siguen usando en reels publicados o se reemplazan por el banco CC0.
- Confirmar de oído las pronunciaciones `sin_verificar` de `pronunciacion.json` ("token", "tokenizador", entre otras).
- Publicación programada en redes (ver `docs/5-tecnica/PUBLICACION.md`).

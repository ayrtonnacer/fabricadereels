# Audio
Referencias: video "15 efectos de sonido que debes usar" (Mirko Vigna, 2026-11) y la experiencia de los videos anteriores.

## Las 4 capas
1. **Voz** (esqueleto del video): Piper `es_AR-daniela-high` (CC BY-SA 4.0; acreditar). Parámetros en `video.json`: length_scale 0.92, noise_scale 0.6, noise_w_scale 0.7.
2. **Música**: define el tono y el ritmo. Siempre debajo de la voz.
3. **Efectos**: ambiente (base), foley (acciones en pantalla), creativos (whoosh, impact, hit, riser, bass drop, braam, silencio) y de UI/texto (click, pop, bell, electric, mechanic, glitch, keyboard).
4. Los efectos son "actores secundarios": **un buen SFX no se nota, se siente**. Nunca al mismo nivel que la voz ni que la música.

## Niveles (referencia)
- Voz −1 a −6 dB (en la mezcla final queda a −14 LUFS integrado; pico real ≤ −1,5 dBTP).
- Efectos 12–18 dB por debajo de la voz; música 22–24 dB por debajo de la voz mientras habla. `mezcla.py` lo logra con ganancias + sidechain: efectos ×1,25 bajan cuando habla la voz; música −8 dB con compresión sidechain más fuerte.
- Ayrton prefiere efectos informáticos/de radio bien audibles: subirlos sin pisar la voz (usar `sfx_gain` en `video.json`).
- **Voz estilo Adjutant (StarCraft)** — *probada el 2026-11-11 y descartada por Ayrton: la voz va SIN efecto*. Queda como opción apagada — `voz.efecto: "adjutant"` (+ `adjutant_fuerza` 0–1; `adjutant_reverb` 0 por defecto); guiño para el público nerd (Ayrton, 2026-11-11). **Afinada midiendo con earshot** (CLAP + AudioSet) contra el audio de referencia: el Adjutant es **seco** (cae en ≈ 170 ms, silencio digital entre frases; cualquier reverb lo aleja: con 5 % de sala el parecido baja de 0,65 a 0,54), **brillante** (2,1 kHz contra 1,0 kHz de Daniela, +5 a +8 dB entre 1,6 y 12 kHz) y **tonal/metálico** (AudioSet: teléfono, timbre; no ruidoso). Cadena en `radio.adjutant()`: EQ al espectro de la referencia (`adjutant_perfil.json`, solo números) → armónicos de agudos → peine de 3 ms (metálico) → remuestreo a 11 kHz (alias "de juego") → puerta de silencio. Con fuerza 0,7: brillo 2,2 kHz (ref 2,2), AudioSet pasa a "Speech synthesizer 0,84", piso de ruido −76 dBFS (antes −55). Muestras en `docs/material/voz-adjutant/`. Para rehacer solo efecto y mezcla sin volver a sintetizar (no cambia tiempos ni subtítulos): `VOZ_REUSAR=1 python engine/audio/voz.py videos/X`.
- Música: fade in 1,5 s, fade out 3,5 s, recortada al largo del video; **música por defecto: `assets/musica/palladio.mp3` (Palladio, Karl Jenkins; decisión de Ayrton 2026-11-11)** con `musica_desde: 0.6` (la pista abre con 0,56 s de silencio); si se cambia el tramo, evitar silencios. La anterior `fondo.mp3` tenía un hueco en 22,6–24,1 s.

## Reglas de colocación
- **Whoosh**: en el momento de máximo movimiento (la entrada de un elemento/transición), no antes ni después. Transiciones: 0,12 s antes de cada escena.
- **Impact/hit**: remarcan una acción importante o un momento de tensión; el hit es más corto y suave. A veces van juntos.
- **Riser**: genera tensión antes de algo importante. Variar: usar `reverse(riser)` como "succión" antes de un impact. Patrón fuerte: **riser → impact → un instante de silencio → frase clave → whoosh**.
- **Bass drop**: pocas veces por video (cámaras lentas, revelación). **Braam**: entrada dramática, con mesura.
- **Silencio**: parar en seco después de una secuencia frenética hace que la frase siguiente pese más. No silencio absoluto: dejar el ambiente.
- **Ambiente** (`T.ambient`): base baja en todo el video para que nunca suene vacío cuando se corta la música o la voz.
- **UI/texto**: click/tick al escribir, pop cuando aparece algo, bell/ding de éxito, glitch (sin abusar: está quemado), keyboard para terminal.
- **No ser literal**: el sonido no tiene que describir exactamente lo que se ve (una luz que parpadea puede llevar un trueno, no una bombilla).
- **Efectos de filtro**: pasa-bajos = sensación de "bajo el agua"/abstracción; pasa-altos = énfasis, como oído por auriculares; reverb = profundidad (impact/riser/ambiente).
- Errores a evitar: volumen demasiado alto, sonidos fuera de tiempo, ser demasiado literal, no organizar la biblioteca (una subcarpeta por tipo, ver `assets/sfx/LEEME.md`).

## Significado fijo de los sonidos (usar siempre igual)
whoosh=transición · pop=aparece algo · ding/chime=éxito · alert=aviso · buzz/powerdown=error o pérdida · powerup=algo se activa · thunk=Enter/enchufar · tick=tecla/dato · glitch=texto que tiembla · riser=progreso · boom/impact=golpe de apertura o remarque · **chinn** (`propio("chinn")`, de Ayrton) = cierre/CTA (preferido sobre el sparkle sintético) · zoom-click = zoom de cámara sobre código.

## Efecto de radio en la voz (militar / walkie-talkie)
En `video.json`: `"voz": {"efecto": "radio", "radio_fuerza": 0.6, ...}`. Lo aplica `voz.py` línea por línea (`engine/audio/radio.py`): banda telefónica 380–3100 Hz, saturación, estática de fondo solo mientras habla, clic de apertura y "squelch" (golpe de ruido) al soltar el botón. Fuerza 0.3 = radio limpia · 0.6 = walkie · 0.9 = radio rota. Uso pensado para videos de CTF/red team; en tutoriales largos cansa: usar fuerza baja o solo en el gancho. Probar suelto: `python engine/audio/radio.py in.wav out.wav 0.6`. Ojo: la voz queda más angosta, así que revisar inteligibilidad con palabras técnicas.

## Sonidos reales (preferirlos cuando suenen mejor que los sintéticos)
- **Tipeo**: los ticks sintéticos sonaban artificiales (feedback de Ayrton, 2026-11-04). Ahora `Track.typing()` usa teclas **reales** cortadas de `assets/sfx/propios/typing-keyboard.mp3` (de su repo code-reel-studio, `public/sounds/`) con `engine/audio/cortar_teclas.py` → `assets/sfx/propios/teclas/kNN.wav` (104 teclas). Reglas: nunca la misma tecla dos veces seguidas, variación de nivel (±2 dB) y de tiempo (±8 ms); Enter usa la tecla más pesada del lote. Sin esas teclas, cae a los ticks sintéticos.
- **Sonido grave de apertura y cierre** (Ayrton, 2026-11-09): `assets/sfx/propios/boom-cinematico.mp3` ("cinematic impact boom 05", archivo de Universfield, ~2 s). Va **al inicio** (`propio('boom-cinematico')` en t = 0, nivel ~0,6) y **al final** (justo antes del CTA, ~0,55, junto con el chinn). El ducking lo baja cuando habla la voz. Si falta el archivo cae al `boom()` sintético.
- **Otros propios** (`sfxlib.propio('intro-whoosh' | 'mouse-click' | 'zoom-click')`): disponibles para whoosh de apertura y clics de interfaz.
- **Banco opcional** de Adobe Audition en `assets/sfx/<tipo>/` (ver LEEME) y `sfxlib.sample(tipo)`.

## Principios tomados de earshot (Leonxlnx/earshot, MIT; solo lectura de sus notas, no se ejecuta su código)
- Un buen efecto tiene 2–4 capas (transitorio, cuerpo, grave, cola) y cada capa ocupa su banda; una sola capa suena amateur.
- Todo efecto tiene movimiento (filtro, tono y nivel cambian); un whoosh de espectro fijo suena barato.
- Efectos sincronizados al cuadro (un cuadro corrido rompe la ilusión) y usados con mesura: la música ya mueve la imagen, los acentos grandes son pocos.
- Una "paleta": los sonidos de interfaz de un video comparten timbre y registro; variar solo tono y envolvente.
- Variación (round robin): varias versiones elegidas al azar; jitter de nivel ±1–2 dB y tiempo ±10 %.
- Tipeo de motion graphics: toques cortos (50–80 ms) y agudos, ~11 teclas por segundo (separación mediana ≈ 87 ms).
- Reverb solo en cuerpo y cola, el grave seco; pasa-altos a 20–25 Hz y limitador a −1 dBTP al final.

## Herramientas
`sfxlib.py` (sintéticos + tipeo real + `sample()`/`propio()` para sonidos reales de `assets/sfx/`), `cortar_teclas.py`, `sfx.py` (ejecuta `sfx_events.py`), `mezcla.py` (cadena de voz, ducking, música, loudnorm −14 LUFS). Referencia lograda en el video de Parrot: −14,2 LUFS.

## Pronunciación
Piper lee mal siglas y palabras en inglés. Se corrige con `engine/audio/pronunciacion.json`:
- `reemplazos`: palabra → escritura fonética ("Parrot" → "Párrot"); `estado: sin_verificar` hasta que Ayrton la escuche y confirme (→ `ok`).
- `prohibidas`: palabras que no van en la voz; `voz.py` avisa y propone alternativa.
Se escribe el texto natural en `video.json`; `voz.py` aplica el diccionario. Si algo suena mal, se agrega al diccionario en el mismo commit. Tips: acento escrito para marcar la sílaba tónica; siglas separadas por letras ("u ese be").

## Voz propia (pendiente, 2026-11-14)
El público marcó la voz como lo más flojo ("se nota un poco lo robótico"; "si es para tu marca personal debería tener tu voz", `PUBLICO.md`). Opciones evaluadas (costos aproximados de 2026-11; confirmarlos antes de pagar):
| Opción | Costo | Notas |
|---|---|---|
| **ElevenLabs** (clonación instantánea) | Starter ≈ USD 5/mes (≈ 30.000 caracteres ≈ 40–50 reels de 40 s) · Creator ≈ USD 22/mes (≈ 100.000) | Mejor calidad y el acento queda fiel; uso comercial desde Starter. Sin GPU. No usa `pronunciacion.json`: escribir fonético o usar sus diccionarios. Si se cancela, se pierde la voz. Clave por credencial del entorno (nunca en el chat) y permitir `api.elevenlabs.io`. |
| **Chatterbox multilingüe** (Resemble, MIT) | Gratis, local | Clona con 10–30 s de audio. Lento en CPU: conviene GPU (Colab). El acento puede irse a neutro. |
| **XTTS-v2** (Coqui) | Gratis, local | Mantiene bien el acento, pero la licencia es **no comercial**. |
| **Piper entrenado con su voz** | Gratis | Rápido en CPU y con diccionario, pero pide 1–3 h de grabaciones y GPU para entrenar. |
Plan: Ayrton graba 1–2 min (sin eco, WAV mono ≥ 24 kHz, hablando como en un reel) → `docs/material/voz-ayrton/` → prueba lado a lado con Daniela, mismo guion → si convence, `voz.py --voz piper|clon` (la voz sale por línea; `video.json` sigue mandando en los tiempos). Daniela queda de respaldo.

## Audio y HyperFrames
HyperFrames renderiza el video **mudo** (`out/mudo.mp4`); la voz, los efectos y la música los hace y mezcla este repo (`voz.py` → `sfx.py` → `mezcla.py`), que ya cumple −14 LUFS con ducking. No poner `<audio>` en las composiciones (se mezclaría dos veces). La skill `/media-use` de HyperFrames ofrece voces y música propias; Ayrton eligió Daniela (Piper): no cambiarla sin que lo pida.

## Cómo verificar el audio sin escucharlo
Dibujar la onda de `voz.wav` y `sfx.wav` con los inicios de palabra de `audio/palabras.json` (ver `docs/SUBTITULOS.md`): la voz debe quedar sobre el efecto cuando habla, el grave de apertura/cierre no tapa las primeras/últimas palabras y cada whoosh cae en el pico de su movimiento de cámara. Medir también `mezcla.py` (−14 LUFS, pico ≤ −1,5 dB).

## Sonidos propios y dónde se usan (assets/sfx/propios/)
| Archivo | Uso |
|---|---|
| `chinn.mp3` | aterriza el CTA |
| `boom-cinematico.mp3` | grave al inicio y antes del CTA |
| `hit-metal.mp3` | acento metálico justo antes del grave final (reemplaza el whoosh suave de succión; Ayrton, 2026-11-09) |
| `interface-texto-digital.mp3` | tipeo de **0 y 1** / texto digital en pantallas (1,5 s: se recorta con `tramo()` en `sfx_events.py`) |
| `typing-keyboard.mp3` (+ `teclas/`) | tipeo de **código** (terminal), no de bits |
| `modem-conexion.mp3` | guiño de "conectándose a internet"; el tramo 3,3–5,1 s es el handshake reconocible (0–3,4 s marcado, 5–17 s ruido) |
| `zoom-click`, `mouse-click`, `intro-whoosh` | zoom sobre código, clics, whoosh de apertura |
`tramo(nombre, a, b, fade_in, fade_out, gain)` (en `sfx_events.py` del reel de WiFi) recorta y hace fundidos; moverlo a `sfxlib.py` si se repite.

## Sonido limpio (2026-11-09)
- La voz **no** lleva efecto de radio (`voz.efecto: "ninguno"`). Si suena "de radio": revisar (1) ambiente/zumbido, (2) efectos de estática (`glitch()`: evitarlo), (3) procesamiento dinámico. `mezcla.py` ya no usa `loudnorm` (comprimía y bombeaba): voz con `highpass 70 Hz` + compresión leve (2:1) y ganancia lineal a −16 LUFS; la mezcla se lleva a −14 LUFS con **ganancia lineal + limitador** (pico −1,5 dBTP).
- Piper entrega 22 kHz: no hay contenido sobre ~11 kHz; es propio del modelo y no es un efecto.
- Pronunciación: ver `engine/audio/pronunciacion.json`; "gui" se lee /gi/ ("guifi" suena "gifi"): para "WiFi" se usa "uaifai".

## Principios tomados de onetake (feitangyuan/onetake, 2026-11-15; solo ideas, `docs/material/2026-11-onetake.md`)
- **Un seno puro por evento suena a chiptune/tragamonedas**: un objeto real tiene parciales inarmónicos y un transitorio de ruido (cristal: fundamental + 2,76× y 5,4× con decaimientos más rápidos + soplido de ~2 kHz; madera: golpe grave con caída de tono + chasquido a ~3 kHz; sub: seno con caída de tono, saturado, para golpes y aterrizajes; burbuja: resonancia que sube, para un pop redondo).
- **Un solo "cuarto"** para todos los efectos: una respuesta al impulso sintética (≈ 1,1 s de cola, 12 ms de pre-retardo, 3 primeras reflexiones) con envío del 15 % (tecla) al 60–70 % (soplido largo de aire). Así los sonidos quedan *dentro* de la imagen.
- **Menos eventos que escenas/movimientos**; si dos sonidos caen a < 40 ms, dejar uno. Los golpes son lo más fuerte del film; **el aterrizaje tiene que sonar más fuerte que el movimiento que lo precede** (medir por loudness K de cada beat, no por RMS).
- **Cámara como instrumento**: el "aire" de un movimiento de cámara = ruido filtrado cuyo volumen sigue |d log zoom / dt|^1,3 (en zoom a fondo, bandas cada vez más agudas). Es el whoosh *en el pico*, derivado de la curva real y no puesto a ojo.
- **Barro**: medir bandas por ventana de 0,5 s (`python engine/analisis/barro.py final.mp4`); alarma si la mezcla entera pasa de ~35 % en 100–300 Hz (palladio sola: 32 %) o una ventana de 60 %. Notas del acompañamiento de F4 para arriba y colas cortas.
- **Muchos golpes parecidos alineados forman un tono** (efecto "rana"): variar el timbre en cada golpe y romper la alineación temporal; no repetir un ping tonal.
- **Final**: no cerrar con un acorde de vibráfono/shimmer genérico (se oye "efecto de stock"); cerrar con la cadencia de la música o con un golpe propio del film.
- Volumen de ellos: −16 LUFS / −3,5 dBTP; **el nuestro sigue siendo −14 LUFS** (Instagram/Reels) con pico real ≤ −1,5 dBTP.

## Escuchar con Whisper (2026-11-15)
`python engine/audio/escuchar.py final.mp4 --video videos/X [--modelo small|medium]` transcribe con faster-whisper (local; la 1.ª vez baja el modelo de Hugging Face) y compara con `voz.lineas`: % de palabras entendidas por línea y qué palabra se oyó distinta. **Antes de entregar un reel**, correrlo y mirar las palabras que fallan: si fallan en varias líneas (o con `medium`), suenan mal → `pronunciacion.json`.
- Whisper solo entiende **voz**: no describe la música (para eso: `barro.py`, `medir.py` y el oído de Ayrton).
- Primera lectura del reel de tensores (small): 90 % de palabras. Sospechosas: **"texto" → "tecto"** (2 líneas), **"álgebra" → "alfeora"**, "seguime" → "sílame", "larga"→"lara", "convertidas"→"cometidas". Revisarlas en el diccionario antes del próximo reel.



## Banco de efectos y materiales (2026-11-16)
Pedido de Ayrton: "todos los recursos necesarios para hacer videos profesionales". Antes solo había 10 sonidos propios + sintéticos simples; el banco real de Adobe nunca se cargó. Ahora hay tres capas, de más a menos propia:
1. **Propios de Ayrton** (`assets/sfx/propios/`): boom-cinematico (inicio y final), chinn (CTA), tipeo, interface-texto-digital, módem, hit-metal. Siempre tienen prioridad.
2. **Banco CC0** (`bash engine/audio/bajar_sfx.sh`, ~450 archivos; `sfxlib.banco(tipo, filtro, i)`): licencia CC0 verificada en cada página de OpenGameArt el 2026-11-16 (no exige atribución; se listan igual): Swishes (artisticdude), Air Whoosh (pyranostudios), UI SFX Set (51 sonidos), Kenney Interface Sounds, 10 Clicks and Switches (StarNinjas), 75 CC0 Breaking/Falling/Hit SFX (rubberduck), 4 Metal Dings (StarNinjas), Kenney Sci-Fi Sounds, 7 Space Sounds (Joth). **No se usó** "Weird Whooshes" (licencia CC-BY: pide atribución). Kenney.nl y Freesound están bloqueados desde la nube.
3. **Materiales sintetizados de onetake** (`engine/onetake/`, **solo uso no comercial**, ver su LEEME): `air` (whoosh de aire filtrado), `glass` (tono golpeado con parciales inarmónicos), `wood` (golpe seco), `sub` (golpe grave), `bubble` (pop redondo), `wobble` (gelatina). Suenan a objeto real, no a chiptune.
**Sala compartida**: `T.put(t, sonido, gain, send=0.3)` manda parte del sonido a UNA reverb (T60 1,1 s) para todo el video: es lo que hace que sonidos distintos suenen en el mismo cuarto (idea de onetake). Referencia: click/tick `send` 0,15; pop/ding 0,3–0,6; whoosh 0,4–0,5.
**Reglas que sumamos de onetake**: menos eventos que beats (si dos sonidos caen a < 40 ms, dejar uno); un whoosh = aire sintético + swish real superpuestos; acordes suaves de dos notas (no la cadencia de vibráfono de siempre); revisar graves-medios por ventana de 0,5 s (`barro.py`).
**Pendiente**: grabaciones foley propias (papel, tela, objetos) y una pista de ambiente muy baja; ver si Ayrton consigue el banco de Adobe.

## Música propia (Suno) — recomendación 2026-11-16 (medida, no escuchada)
Palladio (medido): 31 % de la energía en 20–100 Hz, 35 % en 100–300 Hz, 27 % en 300–1000 Hz, solo 7 % arriba de 1 kHz → ocupa la misma franja que la voz (200–3000 Hz) y es la causa de las ventanas de barro. Para una pista propia: instrumental, 90–100 BPM (o 120 con sensación de mitad de tempo), electrónica mínima y oscura; graves solo en sub (< 80 Hz) y brillo arriba de 4 kHz, **medios vacíos** para la voz; un pulso de plucks/ticks que acompañe los clicks de datos; partes que se puedan cortar (intro 4 compases, cuerpo en loop, final con cadencia propia, sin vibráfono de stock); 60–90 s. Una sola pista firma para todos los reels (marca reconocible). Licencia: con el plan gratis de Suno las canciones no se pueden usar comercialmente; con plan pago sí.


## Música firma desde 2026-11-16: *Can You Hear The Music*
Ayrton la pasó (webm → `assets/musica/can-you-hear-the-music.mp3`) para todos los reels. Medida: 110 s; crescendo de −28 dB (inicio) a −10 dB (≈ 95 s) y corte a los 100 s. Bandas: 33 % 20–100 Hz, 23 % 100–300 Hz, 30 % 300–1000 Hz (pisa menos la voz que Palladio: la mezcla del reel de tokens bajó de 34 % a 29 % en 100–300 Hz).
- **Tramo**: `musica_desde = 100 − duración del reel` (para 47,5 s → 52) → el crescendo llega al máximo en el CTA y termina antes del corte de la pista.
- **Nivel**: el tramo 52–99,5 s mide −11,5 LUFS; `musica_db: −8`, sin `musica_nivelar` (el nivelado aplastaría el crescendo). Revisar de oído en cada reel.
- **Derechos**: es una obra con copyright (banda sonora). Instagram/TikTok/YouTube pueden silenciar el video o reclamarlo; lo más seguro es agregarla desde la biblioteca de música de la app al publicar (y subir el video sin música) o confirmar la licencia. Lo mismo valía para Palladio.

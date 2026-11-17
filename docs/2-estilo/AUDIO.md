# Audio
Primero lo que se usa en cada reel; al final, el detalle y los pendientes. HyperFrames renderiza **mudo**: la voz, los efectos y la música los hace este repo (`voz.py` → `sfx.py` → `mezcla.py`; todo junto con `python engine/reel.py render`). No poner `<audio>` en las composiciones.

## Las 4 capas y sus niveles
| Capa | Qué | Nivel |
|---|---|---|
| **Voz** | Piper `es_AR-daniela-high`, **limpia** (`efecto: "ninguno"`), `length_scale` 1,05 | la referencia; mezcla final a **−14 LUFS**, pico ≤ −1,5 dBTP |
| **Música** | la firma: `assets/musica/can-you-hear-the-music.mp3` | 9–13 dB bajo la voz mientras habla (ducking) |
| **Efectos** | `sfx_events.py` | audibles pero bajo la voz (ducking); `sfx_gain` 1,25 |
| **Silencio** | recurso: frenar en seco antes de una frase clave la hace pesar | — |
Sonido **limpio**: sin ambiente de fondo, sin estática ni glitch. Los valores de `audio` en el `video.json` de la plantilla ya están calibrados: no tocarlos salvo motivo.

## Fijos de marca (iguales en todos los reels)
- **`P.apertura()`**: boom grave (`boom-cinematico`) en el segundo 0.
- **`P.cierre(S['cierre'])`**: **hit metálico real + boom** → **chinn** cuando aterriza el CTA.
- **Música firma** desde el segundo 0 (los violines): `musica_desde: 0`, `musica_fade_in: 0.4`, `musica_nivelar: [-32, 4]`, `musica_db: 10`, `musica_duck: 2`. La pista crece de −28 a −10 dB; sin nivelar, el inicio no se oye y el final tapa la voz. **No recortar otro tramo sin avisarle a Ayrton.**

## Cómo se escribe `sfx_events.py`
```python
from sfxlib import *
def build(T, S, lib=None):
    P = Paleta(T)
    P.apertura()
    P.viaje(S['explica'])                         # viaje de cámara: t = el PICO de velocidad (la mitad del viaje)
    P.aterriza(S['explica'] + 0.45)               # la cámara llega (donde está el temblor)
    P.tipeo(cuando('l02', 'concepto'), 24, bits=True)
    P.aparece(cuando('l03', 'segundo'))
    P.resultado(cuando('l04', 'funcionando'))
    P.cierre(S['cierre'])
```
`S['escena']` = segundo en que empieza la escena · `cuando('l03', 'palabra')` = segundo en que la voz dice esa palabra (los mismos tiempos que `assets/set.js`).
| Paleta | Significa | Cuándo |
|---|---|---|
| `P.viaje(t, d=0.6, g=0.4)` | movimiento de cámara (aire + una "curva" real distinta cada vez) | en el pico de cada viaje; `d=0.9` para grúas largas |
| `P.aterriza(t)` | golpe grave corto | al llegar a una estación |
| `P.aparece(t)` | algo entra | objetos y rótulos importantes (no todos) |
| `P.dato(t)` | tic | un número o dato que se muestra |
| `P.resultado(t)` | acorde de "dio" | el payoff, un resultado correcto |
| `P.error(t)` | zumbido | algo falla o se pierde |
| `P.tipeo(t, n, bits=False)` | teclado real (código) o sonido digital (`bits=True`: 0 y 1 en una pantalla) | texto que se escribe |
Cada llamada elige un sonido real del banco **sin repetir dentro del reel y en otro orden en cada reel** (queda la lista en `audio/sfx_usados.txt`). Para un sonido puntual: `T.put(segundo, sonido, volumen, send=reverb)` con `propio('hit-metal')`, `tramo('modem-conexion', 3.3, 5.1)`, `banco('ui', 'click')`, `elegir(rol, max_dur=…)`.

## Reglas de colocación
- **Menos sonidos que movimientos.** Si dos caen a menos de 40 ms, dejar uno. Los acentos grandes son pocos.
- El sonido del viaje va en el **pico de velocidad**, no al empezar. El aterrizaje suena más fuerte que el viaje que lo precede.
- El efecto empieza **en el cuadro** de lo que lo causa (un cuadro corrido rompe la ilusión).
- Patrón para un momento fuerte: riser → golpe → un instante de silencio → frase clave.
- No ser literal en todo; no repetir el mismo golpe (muchos iguales seguidos forman un tono).
- Todos los efectos comparten una sala (`send`): tic 0,15 · pop/ding 0,3–0,6 · viaje 0,4–0,5.
- No cerrar con un acorde de vibráfono genérico: el cierre es el boom + chinn de marca.

## Sonidos propios (`assets/sfx/propios/`, siempre tienen prioridad)
| Archivo | Uso |
|---|---|
| `boom-cinematico` | inicio y antes del CTA (marca) |
| `chinn` | aterriza el CTA (marca) |
| `hit-metal` | acento metálico antes del boom final |
| `interface-texto-digital` | 0 y 1 / texto digital en pantallas |
| `typing-keyboard` + `teclas/` | tipeo de código (104 teclas reales, nunca la misma dos veces) |
| `modem-conexion` | guiño de "conectándose" (tramo 3,3–5,1 s) |
| `zoom-click`, `mouse-click`, `intro-whoosh` | acercamiento sobre código, clics |

## Banco de efectos
- **CC0** (~450 archivos; `bash engine/audio/bajar_sfx.sh`; se baja solo al iniciar la sesión; no se sube a git): swishes, UI, clicks, golpes, dings, sci-fi de OpenGameArt/Kenney. Catálogo medido con su rol: `engine/audio/catalogo_sfx.json`.
- **Sintéticos** (`sfxlib.py`: whoosh, tick, pop, ding, boom, riser…): respaldo si falta el banco.
- **Materiales de onetake** (`engine/onetake/`: aire, vidrio, madera, sub, burbuja): suenan a objeto real, pero su licencia es de **uso no comercial**. ⚠ Pendiente que Ayrton decida si siguen (`PREFERENCIAS.md` §10); la paleta funciona igual sin ellos.
- Elegir de oído: `python engine/audio/muestras_sfx.py` arma muestras numeradas por rol en `docs/4-referencias/material/sfx-muestras/`.

## Pronunciación
Piper lee mal siglas y palabras en inglés. Se escribe el texto natural en `video.json` y `voz.py` aplica `engine/audio/pronunciacion.json`:
- `reemplazos`: palabra → escritura fonética ("WiFi" → "uaifai"); `estado: "sin_verificar"` hasta que Ayrton la confirma de oído (→ `"ok"` + nota con fecha).
- `prohibidas`: palabras que no van en la voz; `reel.py guion` las marca.
- Trucos: tilde para marcar la sílaba fuerte; siglas letra por letra ("u ese be"); "gui" se lee /gi/; la r inicial o doble sale muy corta ("arranca" → "arr ranca").
- Ante una palabra nueva en inglés: generar 2–3 variantes y ofrecérselas antes de usarla.
- `python engine/reel.py medir videos/X --escuchar`: Whisper transcribe el final y lo compara con el guion; las palabras que no entiende van al diccionario. (Whisper solo juzga la voz, no la música ni los efectos.)
- Rehacer solo la mezcla sin volver a sintetizar: `VOZ_REUSAR=1 python engine/audio/voz.py videos/X`.

## Cómo verificar sin escuchar
`reel.py medir` informa: LUFS y pico (−14 / ≤ −1,5), **barro** (energía en 100–300 Hz: alarma si pasa de 35 % en total o 60 % en una ventana de 0,5 s) y ataques por segundo (2,2–4,5). El gusto de un efecto lo decide Ayrton escuchando.

## Pendientes y opciones
- **Derechos de la música**: *Can You Hear The Music* tiene copyright; las plataformas pueden silenciar o reclamar el video. Lo más seguro: subir el video sin música (`--db -60`) y agregarla desde la biblioteca de la app, o usar una pista propia con licencia.
- **Música propia** (idea medida): instrumental, 90–100 BPM, electrónica mínima y oscura, graves solo bajo 80 Hz y brillo sobre 4 kHz, **medios vacíos** para la voz, 60–90 s, con partes cortables.
- **Voz propia** (el público marcó la voz como lo más flojo):
  | Opción | Costo aprox. (2026-11; confirmar) | Notas |
  |---|---|---|
  | ElevenLabs (clonación instantánea) | USD 5–22 / mes | la mejor calidad; uso comercial; no usa `pronunciacion.json`; clave por credencial del entorno, nunca en el chat |
  | Chatterbox multilingüe (MIT) | gratis, local | clona con 10–30 s; lento sin GPU; el acento puede irse a neutro |
  | XTTS-v2 | gratis | licencia no comercial |
  | Piper entrenado con su voz | gratis | pide 1–3 h de grabación y GPU |
  Plan: Ayrton graba 1–2 min (WAV mono, sin eco) → `docs/4-referencias/material/voz-ayrton/` → prueba lado a lado con Daniela.
- **Efectos de voz** (radio, Adjutant): existen en `engine/audio/radio.py`, probados y **descartados por Ayrton**. No proponerlos.
- Foley propio y banco de Adobe: pendientes.

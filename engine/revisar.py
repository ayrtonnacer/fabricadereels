#!/usr/bin/env python3
"""Revisor de un video ANTES de renderizar (idea tomada del `check` de HyperFrames, adaptada a las reglas de este repo).

  python engine/revisar.py videos/X              # chequeos estáticos (rápido)
  python engine/revisar.py videos/X --quietud    # + renderiza un cuadro cada 0,5 s y busca tramos > 3 s sin cambios y el primer cuadro vacío

Niveles: ERROR rompe el render o una regla firme · AVISO es una pregunta (se arregla o se deja a propósito y se dice por qué).
Sale con código 1 si hay errores."""
import json, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
V = Path(sys.argv[1]).resolve(); QUIETUD = '--quietud' in sys.argv
cfg = json.loads((V / 'video.json').read_text()); html = (V / 'index.html').read_text()
dic = json.loads((ROOT / 'engine/audio/pronunciacion.json').read_text())
R = []
def err(c, m): R.append(('ERROR', c, m))
def av(c, m): R.append(('AVISO', c, m))
def linea(i): return html[:i].count('\n') + 1

SC = cfg['scenes']; dur = sum(s['d'] for s in SC); t0 = {}; acc = 0
for s in SC: t0[s['id']] = acc; acc += s['d']
ids = set(re.findall(r'<section[^>]*\bid="([^"]+)"', html))

# --- estructura
for s in SC:
    if s['id'] not in ids: err('escena_sin_html', f"la escena {s['id']} de video.json no tiene <section id=\"{s['id']}\"> en index.html")
for i in ids - set(t0): av('html_sin_escena', f'<section id="{i}"> no está en video.json (no se va a ver)')
if any(s.get('gl') for s in SC) and 'three' not in html: err('falta_three', 'hay escenas con "gl": true pero index.html no importa three.js')

# --- determinismo: el cuadro tiene que ser función pura de t (render.mjs llama __render(t))
for pat, nom in [(r'Math\.random\s*\(', 'Math.random'), (r'Date\.now\s*\(', 'Date.now'), (r'performance\.now\s*\(', 'performance.now'),
                 (r'requestAnimationFrame\s*\(', 'requestAnimationFrame'), (r'set(Timeout|Interval)\s*\(', 'setTimeout/setInterval'), (r'new Date\s*\(', 'new Date')]:
    for m in re.finditer(pat, html): err('no_deterministico', f'línea {linea(m.start())}: {nom} hace que cada render salga distinto; usar hash(n) o el tiempo t')
for m in re.finditer(r'transition\s*:\s*(?!none)[^;"]+', html):
    av('css_transition', f'línea {linea(m.start())}: una transición CSS no se puede "saltar" a un tiempo t; animar con data-a o en custom(id, lt)')
for m in re.finditer(r'(animation\s*:|@keyframes)', html): av('css_animation', f'línea {linea(m.start())}: animación CSS: corre con el reloj, no con t')

# --- errores ya cometidos (docs/DECISIONES.md)
for m in re.finditer(r'id="gl"', html): err('id_gl', f'línea {linea(m.start())}: id="gl" está reservado para el canvas 3D del tema')
for m in re.finditer(r'class="[^"]*\bln\b', html):
    if 'data-show' not in html[m.start():m.start() + 200]: av('clase_ln', f'línea {linea(m.start())}: .ln es visibility:hidden en el tema (solo para líneas de terminal con data-show)')

# --- estética (CLAUDE.md regla 1): colores por variables del tema
hexes = [(m.group(0), linea(m.start())) for m in re.finditer(r'#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b(?![0-9A-Fa-f])', html)]
hexes = [(h, l) for h, l in hexes if not re.match(r'#(s\d+|gl|bg)\b', h)]
if hexes:
    av('color_fijo', f'{len(hexes)} colores fijos (regla: var(--acc) / colorTema()); primeros: ' + ', '.join(f'{h} (l.{l})' for h, l in hexes[:6]))
for m in re.finditer(r'font-family\s*:\s*([^;"]+)', html):
    fam = m.group(1)
    if not re.search(r'\b(SG|JB|inherit)\b', fam): av('fuente', f'línea {linea(m.start())}: fuente "{fam.strip()}" fuera de IBM Plex (SG/JB)')
for m in re.finditer(r'letter-spacing\s*:\s*([0-9.]+)(em|px)', html):
    if float(m.group(1)) > 0.01: av('espaciado', f'línea {linea(m.start())}: letter-spacing positivo ({m.group(0)}); Ayrton quiere espaciado normal o apretado')
for m in re.finditer(r'text-transform\s*:\s*uppercase', html): av('mayusculas', f'línea {linea(m.start())}: mayúsculas; evitar etiquetas en mayúsculas espaciadas')

# --- firma (regla 2): al inicio y al final, salvo videos en bucle
def html_escena(i):
    m = re.search(rf'<section[^>]*\bid="{re.escape(i)}"[^>]*>(.*?)</section>', html, re.S); return m.group(1) if m else ''
bucle = bool(cfg.get('audio', {}).get('musica_ventana')) or cfg.get('bucle')
if '@ayrtonnacer' not in html_escena(SC[0]['id']): err('firma_inicio', f"la primera escena ({SC[0]['id']}) no tiene la firma @ayrtonnacer")
if not bucle and '@ayrtonnacer' not in html_escena(SC[-1]['id']) and '@ayrtonnacer' not in html[html.find('<script'):]:
    av('firma_final', f"la última escena ({SC[-1]['id']}) no muestra @ayrtonnacer (si es un bucle, poner \"bucle\": true en video.json)")
for m in re.finditer(r'@ayrtonnacer\s*[.·•|]', html): err('firma_adorno', f'línea {linea(m.start())}: la firma va sin punto ni adornos al lado')

# --- voz (regla 4, 7): palabras prohibidas, ritmo de palabras, tiempos
L = cfg.get('voz', {}).get('lineas', [])
pal = sum(len(re.findall(r"[\wáéíóúñü@']+", l['texto'])) for l in L)
if L and pal > dur * 2.3 + 2: av('demasiadas_palabras', f'{pal} palabras de voz para {dur:.1f} s (máximo ≈ {dur * 2.3:.0f} a 2,3 palabras/s)')
for l in L:
    for p in dic.get('prohibidas', []):
        w = p.get('palabra') or p.get('de') or ''
        if w and re.search(rf'\b{re.escape(w)}\b', l['texto'], re.I): err('palabra_prohibida', f"{l['id']}: \"{w}\" → {p.get('usar') or p.get('a') or p.get('alternativa', '')}")
    e = l.get('escena')
    if e and e in t0 and not (t0[e] <= l['t'] < t0[e] + next(s['d'] for s in SC if s['id'] == e)):
        err('voz_fuera_de_escena', f"{l['id']} empieza en {l['t']} s, fuera de su escena {e} ({t0[e]:.1f}–{t0[e] + next(s['d'] for s in SC if s['id'] == e):.1f} s)")
    if re.search(r'\b(sabías que|en el mundo de|sumérgete|desbloqueá|aquí está la clave|lo mejor de todo|no vas a creer|esto cambia todo)\b', l['texto'], re.I):
        av('muletilla_ia', f"{l['id']}: muletilla de IA en la voz (docs/GUION.md)")
if L and L[0]['t'] > 0.6: av('hook_tarde', f"la voz arranca a los {L[0]['t']} s; el hook va en los primeros 3 s")

# --- costuras (docs/MOVIMIENTO.md): dirección y presupuesto de transiciones
sal = [(s['id'], s.get('salida')) for s in SC[:-1] if s.get('salida')]
def dir_de(x):
    if isinstance(x, dict): return x.get('tipo'), x.get('dir')
    t, *r = x.split('-'); return ('zoom-inverso', None) if x == 'zoom-inverso' else (t, '-'.join(r) or None)
tipos = {dir_de(x)[0] for _, x in sal}
if len(tipos) > 4: av('muchas_transiciones', f'{len(tipos)} tipos de transición ({", ".join(sorted(tipos))}); usar 2–4 y repetirlos')
opuesto = {'izq': 'der', 'der': 'izq', 'arriba': 'abajo', 'abajo': 'arriba'}
for (a, x), (b, y) in zip(sal, sal[1:]):
    da, db = dir_de(x)[1], dir_de(y)[1]
    if da and db and opuesto.get(da) == db: av('ping_pong', f'{a} sale hacia {da} y {b} hacia {db}: direcciones opuestas seguidas se leen como error (cambiar solo con una causa en pantalla)')
    if dir_de(x)[0] == 'zoom-inverso' and dir_de(y)[0] == 'zoom-inverso': av('reservado_gastado', f'{a} y {b}: dos "zoom-inverso" seguidos; es la llegada/payoff, no un recurso de variedad')

# --- quietud: renderiza un cuadro cada 0,5 s y mide cuánto cambia
if QUIETUD:
    import numpy as np
    from PIL import Image
    ts = [round(x * 0.5, 2) for x in range(int(dur / 0.5) + 1)]
    fr = V / 'frames'
    subprocess.run(['node', str(ROOT / 'engine/render.mjs'), str(V), 'preview', *[f'{t:g}' for t in ts]], check=True, capture_output=True)
    img = [np.asarray(Image.open(fr / f'preview_{t:g}.jpg').convert('L').resize((108, 192)), float) for t in ts]
    if img[0].std() < 6: av('primer_cuadro_vacio', 'el primer cuadro está casi vacío: es la miniatura en las redes')
    quieto = None
    for i in range(1, len(img)):
        cambia = np.abs(img[i] - img[i - 1]).mean() > 0.6
        if not cambia and quieto is None: quieto = ts[i - 1]
        if (cambia or i == len(img) - 1) and quieto is not None:
            fin = ts[i] if not cambia else ts[i - 1]
            if fin - quieto >= 3: av('tramo_quieto', f'{quieto}–{fin} s: {fin - quieto:.1f} s sin cambios en pantalla (docs/DINAMISMO.md: un cambio cada 1,5–3 s)')
            quieto = None
    for t in ts: (fr / f'preview_{t:g}.jpg').unlink(missing_ok=True)

E = [r for r in R if r[0] == 'ERROR']
for n, c, m in R: print(f'{n:5} {c:22} {m}')
print(f"\n{V.name}: {len(E)} error(es), {len(R) - len(E)} aviso(s). " + ('Listo para renderizar.' if not E else 'Corregir los errores antes de renderizar.'))
sys.exit(1 if E else 0)

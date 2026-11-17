#!/usr/bin/env python3
"""Genera <video>/audio/sfx.wav ejecutando <video>/sfx_events.py → build(T, S, lib):
  T = pista (T.put(segundo, sonido, volumen, send=reverb)),  S = {id_escena: segundo en que empieza},
  cuando('l03', 'palabra') = segundo en que la voz dice esa palabra (los mismos tiempos que usa assets/set.js; viene de assets/tiempos.js).
Uso: python engine/audio/sfx.py videos/<video>"""
import importlib.util, json, re, sys, unicodedata
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import sfxlib
V = Path(sys.argv[1]); cfg = json.loads((V / 'video.json').read_text())
S, acc = {}, 0.0
for s in cfg['scenes']: S[s['id']] = acc; acc += s['d']
PAL = []; js = V / 'assets/tiempos.js'
if js.exists():
    m = re.search(r'^export const PAL = (\[.*\]);$', js.read_text(), re.M); PAL = json.loads(m.group(1)) if m else []
LIN = {l['id']: l['t'] for l in cfg.get('voz', {}).get('lineas', [])}
_n = lambda x: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', x.lower()).encode('ascii', 'ignore').decode())
def cuando(linea, palabra=None, k=0):
    if linea not in LIN: sys.exit(f'sfx_events.py: cuando(): no existe la línea {linea}')
    if not palabra: return LIN[linea]
    h = [p for p in PAL if p[0] == linea and _n(p[1]) == _n(palabra)]
    if len(h) <= k: sys.exit(f'sfx_events.py: cuando(): "{palabra}" no está en {linea} (o falta correr voz.py)')
    return h[k][2]
sfxlib.cuando = cuando; sfxlib.SEMILLA = V.resolve().name
spec = importlib.util.spec_from_file_location('ev', V / 'sfx_events.py'); ev = importlib.util.module_from_spec(spec); spec.loader.exec_module(ev)
T = sfxlib.Track(acc)
try: ev.build(T, S, sfxlib)
except KeyError as e: sys.exit(f'sfx_events.py usa la escena {e}, que no está en video.json (escenas: {", ".join(S)})')
(V / 'audio').mkdir(exist_ok=True); T.save(V / 'audio/sfx.wav'); (V / 'audio/sfx_usados.txt').write_text('\n'.join(f'{r}\t{a}' for r, a in sfxlib.USADOS)); print(f'sfx.wav listo ({acc:.1f}s, {len(sfxlib.USADOS)} sonidos del banco)')

#!/usr/bin/env python3
"""Genera <video>/audio/sfx.wav ejecutando <video>/sfx_events.py (función build(T, S): T=Track, S={id_escena: t0}).
Uso: python engine/audio/sfx.py videos/<video>"""
import importlib.util, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import sfxlib
V = Path(sys.argv[1]); cfg = json.loads((V / 'video.json').read_text())
S, acc = {}, 0.0
for s in cfg['scenes']: S[s['id']] = acc; acc += s['d']
spec = importlib.util.spec_from_file_location('ev', V / 'sfx_events.py'); ev = importlib.util.module_from_spec(spec); spec.loader.exec_module(ev)
T = sfxlib.Track(acc); ev.build(T, S, sfxlib)
(V / 'audio').mkdir(exist_ok=True); T.save(V / 'audio/sfx.wav'); print(f'sfx.wav listo ({acc:.1f}s)')

#!/usr/bin/env python3
"""Copia las duraciones de video.json (única fuente de verdad) a index.html: data-start / data-duration de cada
escena (el host con id = id de la escena) y la duración total del root.
Uso: python engine/tiempos.py videos/<video>
Correrlo cada vez que cambian las duraciones (después de ajustar la voz con voz.py)."""
import json, re, sys
from pathlib import Path

V = Path(sys.argv[1]); cfg = json.loads((V / 'video.json').read_text()); html_p = V / 'index.html'; html = html_p.read_text()


def fmt(x): return f'{round(x, 3):g}'


def set_attr(tag, attr, val):
    return re.sub(rf'{attr}="[^"]*"', f'{attr}="{val}"', tag) if attr + '=' in tag else tag.replace('<div', f'<div {attr}="{val}"', 1)


t = 0.0
for s in cfg['scenes']:
    m = re.search(rf'<div\b[^>]*\bid="{re.escape(s["id"])}"[^>]*>', html)
    if not m: sys.exit(f'index.html no tiene un host con id="{s["id"]}" (escena de video.json)')
    tag = set_attr(set_attr(m.group(0), 'data-start', fmt(t)), 'data-duration', fmt(s['d']))
    html = html[:m.start()] + tag + html[m.end():]
    print(f'{s["id"]:10} {t:6.2f} → {t + s["d"]:6.2f}')
    t += s['d']
m = re.search(r'<div\b[^>]*data-composition-id="main"[^>]*>', html)
html = html[:m.start()] + set_attr(m.group(0), 'data-duration', fmt(t)) + html[m.end():]
html_p.write_text(html); print(f'total      {t:.2f} s  → index.html actualizado')

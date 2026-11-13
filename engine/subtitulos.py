#!/usr/bin/env python3
"""Genera los subtítulos quemados del video a partir de los tiempos exactos por palabra (voz.py → audio/palabras.json).
Uso: python engine/subtitulos.py videos/<video>      (correr después de voz.py y tiempos.py)
Salida: <video>/compositions/subtitulos.html (+ el host en index.html si falta).
Reglas (docs/SUBTITULOS.md): bloques de 2–4 palabras, 1–2 líneas, nunca una palabra sola en la última línea; la palabra que se dice
va en el acento; zona segura: franja y 1120–1320 (arriba de la interfaz de las apps y debajo de la imagen, que el set deja libre)."""
import json, re, sys
from pathlib import Path

V = Path(sys.argv[1]); cfg = json.loads((V / 'video.json').read_text()); P = json.loads((V / 'audio/palabras.json').read_text())
total = round(sum(s['d'] for s in cfg['scenes']), 3)
FIN = re.compile(r'[.?!…]$'); PAUSA = re.compile(r'[,;:]$')
MAXP, MAXC = 4, 30
# fondo del subtítulo (opcional, video.json → "subtitulos": {"fondo": "rgba(0,0,0,.86)"}): barra detrás del texto para que no se pierda sobre imágenes
_fondo = cfg.get('subtitulos', {}).get('fondo')
FONDO = f" background: {_fondo}; padding: 12px 30px 16px; border-radius: 14px;" if _fondo else ''

# 1) agrupar palabras en bloques
grupos, cur = [], []
def largo(ws): return len(' '.join(w['w'] for w in ws))
for w in P:
    cur.append(w)
    corte = FIN.search(w['w']) or len(cur) >= MAXP or largo(cur) >= MAXC or (PAUSA.search(w['w']) and len(cur) >= 2)
    if corte: grupos.append(cur); cur = []
if cur: grupos.append(cur)
# un bloque de una sola palabra se une al anterior si entra (evita palabras sueltas), salvo que haya pausa larga
i = 1
while i < len(grupos):
    g = grupos[i]
    if len(g) == 1 and not FIN.search(grupos[i - 1][-1]['w']) and len(grupos[i - 1]) + 1 <= 5 and largo(grupos[i - 1] + g) <= 34:
        grupos[i - 1] += g; del grupos[i]
    else: i += 1
if len(grupos) > 1 and len(grupos[-1]) == 1 and len(grupos[-2]) <= 3 and not FIN.search(grupos[-2][-1]['w']): grupos[-2] += grupos[-1]; grupos.pop()

# un bloque no termina en artículo, preposición o conjunción: esa palabra pasa al bloque siguiente (se lee mejor)
DEBIL = {'y','o','de','del','la','las','el','los','lo','un','una','a','al','en','por','para','que','su','sus','con','se','no','tu','mi','le','me'}
norm = lambda x: x['w'].lower().strip('.,;:¿?¡!')
for k in range(len(grupos) - 1):
    g, nx = grupos[k], grupos[k + 1]
    while len(g) > 1 and norm(g[-1]) in DEBIL and not (FIN.search(g[-1]['w']) or PAUSA.search(g[-1]['w'])) and len(nx) < 6 and largo(nx) + len(g[-1]['w']) < 36:
        nx.insert(0, g.pop())

# 2) tiempos de aparición: desde un pelo antes de la primera palabra hasta la siguiente, o 0,3 s después de la última
dat = []
for k, g in enumerate(grupos):
    a = max(0.0, g[0]['t0'] - 0.05)
    nxt = grupos[k + 1][0]['t0'] - 0.05 if k + 1 < len(grupos) else total
    b = min(nxt, g[-1]['t1'] + 0.3) if nxt - g[-1]['t1'] > 0.3 else nxt
    dat.append({'a': round(a, 3), 'b': round(b, 3), 'w': [{'w': w['w'], 't0': w['t0'], 't1': w['t1']} for w in g]})

def html_grupo(k, g):
    ws = g['w']; partes = []
    for j, w in enumerate(ws):
        sp = f'<span class="s" id="s{k}_{j}">{w["w"]}</span>'
        partes.append(sp)
    if len(partes) >= 2: partes[-2:] = [partes[-2] + '&nbsp;' + partes[-1]]   # las dos últimas palabras nunca se separan
    return f'<div class="g" id="g{k}"><span class="t">' + ' '.join(partes) + '</span></div>'

body = '\n    '.join(html_grupo(k, g) for k, g in enumerate(dat))
js = json.dumps(dat, ensure_ascii=False)
comp = f'''<!-- SUBTÍTULOS (generado por engine/subtitulos.py: no editar a mano; se rehace desde audio/palabras.json).
     Franja segura y 1120–1320. Los bloques aparecen de golpe; la palabra que se dice se pinta con el acento. -->
<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .g {{ position: absolute; left: 70px; right: 70px; top: 1120px; height: 200px; display: none; align-items: center; justify-content: center;
      text-align: center; text-wrap: balance; font: 700 70px/1.08 var(--sans); letter-spacing: -0.01em; color: var(--text);
      text-shadow: 0 3px 0 rgba(0, 0, 0, .6), 0 0 28px rgba(0, 0, 0, .85); }}
    .g .t {{ display: block; width: fit-content; max-width: 940px; text-align: center; text-wrap: balance;{FONDO} }}
    .g .s {{ display: inline; }}
  </style>
  <div id="root" data-composition-id="subtitulos" data-width="1080" data-height="1920">
    {body}
  </div>
  <script>
    const root = document.querySelector('[data-composition-id="subtitulos"]');
    const tl = gsap.timeline({{ paused: true }});
    const ACC = getComputedStyle(document.documentElement).getPropertyValue('--acc').trim() || '#9FEF00';
    const TXT = getComputedStyle(document.documentElement).getPropertyValue('--text').trim() || '#E8EEF7';
    const D = {js};
    D.forEach((g, k) => {{
      const el = root.querySelector('#g' + k);
      tl.fromTo(el, {{ display: 'none' }}, {{ display: 'flex', duration: 0.001 }}, g.a);
      tl.to(el, {{ display: 'none', duration: 0.001 }}, g.b);
      g.w.forEach((w, j) => {{
        const s = root.querySelector('#s' + k + '_' + j);
        tl.fromTo(s, {{ color: TXT }}, {{ color: ACC, duration: 0.001 }}, w.t0);
        tl.to(s, {{ color: TXT, duration: 0.001 }}, Math.min(g.b - 0.01, w.t1 + 0.015));
      }});
    }});
    window.__timelines["subtitulos"] = tl;
  </script>
</template>
'''
(V / 'compositions/subtitulos.html').write_text(comp)
idx = (V / 'index.html').read_text()
host = f'''      <div id="subtitulos" data-composition-id="subtitulos" data-composition-src="compositions/subtitulos.html"
        data-start="0" data-duration="{total}" data-track-index="9" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 50"></div>
'''
if 'id="subtitulos"' in idx: idx = re.sub(r'      <div id="subtitulos".*?</div>\n', host, idx, flags=re.S)
else: idx = idx.replace('    </div>\n    <script>', host + '    </div>\n    <script>', 1)
(V / 'index.html').write_text(idx)
print(f'{len(dat)} bloques de subtítulos (máx. {max(len(g["w"]) for g in dat)} palabras); franja y 1120–1320')
for g in dat: print(f'  {g["a"]:6.2f}–{g["b"]:6.2f}  ' + ' '.join(w['w'] for w in g['w']))

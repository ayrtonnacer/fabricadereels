#!/usr/bin/env python3
"""video.json es la ÚNICA fuente de verdad de los tiempos. Este script los copia a todo lo que los necesita:

  1. index.html            → un host por escena (inicio y duración) + el de subtítulos, y la duración total.
  2. assets/tiempos.js     → ESC (inicio y duración de cada escena), VOZ (cada línea de voz), PAL (cada palabra con su segundo exacto)
                             y cuando('l03', 'palabra'): lo usa assets/set.js para que cada cosa aparezca cuando la voz la nombra.
  3. compositions/<id>.html → si una escena de video.json no tiene composición, crea el "plano" estándar del set único (assets/set.js).

Uso: python engine/tiempos.py videos/<video>      (lo corre solo `python engine/reel.py voz videos/<video>`)
Correrlo cada vez que cambian escenas, duraciones o la voz. Nunca escribir tiempos a mano en index.html ni en una composición."""
import json, re, sys
from pathlib import Path

INI, FIN = '<!-- ESCENAS:INICIO (generado por engine/tiempos.py; no editar) -->', '<!-- ESCENAS:FIN -->'

PLANO = '''<!-- {id}: un plano del set único (assets/set.js). Generado por engine/tiempos.py; no hace falta editarlo:
     qué se ve y cómo se mueve la cámara se escribe en assets/set.js, en tiempo global del video. -->
<template>
  <style>#root {{ position: absolute; inset: 0; }}</style>
  <div id="root" data-composition-id="{id}" data-width="1080" data-height="1920">
    <div class="fondo" data-layout-ignore></div>
    <canvas class="canvas3d" width="1080" height="1920" data-layout-ignore></canvas>
    <div class="hud" data-layout-ignore></div>
    <div class="vineta" data-layout-ignore></div>
  </div>
  <script>
    const root = document.querySelector('[data-composition-id="{id}"]');
    const tl = gsap.timeline({{ paused: true }});
    import('./assets/set.js').then((S) => S.montar(root, tl, '{id}'));
  </script>
</template>
'''

JS_CUANDO = r'''const norm = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, '');
/* Segundo (tiempo global del video) en que la voz EMPIEZA a decir `palabra` dentro de la línea `linea` (k = 0 la primera vez, 1 la segunda…).
   Sin palabra: el inicio de la línea. Ej.: cuando('l03', 'router'). `python engine/reel.py revisar` avisa si la palabra no está en la línea. */
export function cuando(linea, palabra, k = 0) {
  const v = VOZ[linea]; if (!v) { console.error('cuando(): no existe la línea ' + linea); return 0; }
  if (!palabra) return v.t0;
  const hits = PAL.filter((p) => p[0] === linea && norm(p[1]) === norm(palabra));
  if (!hits[k]) { console.error(`cuando(): "${palabra}" no está en ${linea}`); return v.t0; }
  return hits[k][2];
}
/* Segundo en que la voz TERMINA de decir la palabra (o la línea). */
export function hasta(linea, palabra, k = 0) {
  const v = VOZ[linea]; if (!v) return 0; if (!palabra) return v.t1;
  const hits = PAL.filter((p) => p[0] === linea && norm(p[1]) === norm(palabra)); return hits[k] ? hits[k][3] : v.t1;
}
'''


def fmt(x): return f'{round(x, 3):g}'


def escenas(cfg):
    """[(id, inicio, duración)] y duración total."""
    out, t = [], 0.0
    for s in cfg['scenes']: out.append((s['id'], round(t, 3), s['d'])); t += s['d']
    return out, round(t, 3)


def palabras(V):
    """Tiempos por palabra: de audio/palabras.json (los escribe voz.py) o, si no está (repo recién clonado), los que ya había en assets/tiempos.js."""
    p = V / 'audio/palabras.json'
    if p.exists(): return [[w['l'], w['w'], w['t0'], w['t1']] for w in json.loads(p.read_text())], True
    js = V / 'assets/tiempos.js'
    if js.exists():
        m = re.search(r'^export const PAL = (\[.*\]);$', js.read_text(), re.M)
        if m: return json.loads(m.group(1)), False
    return [], False


def set_attr(tag, attr, val):
    return re.sub(rf'{attr}="[^"]*"', f'{attr}="{val}"', tag) if attr + '=' in tag else tag.replace('<div', f'<div {attr}="{val}"', 1)


def sincronizar(V, silencio=False):
    V = Path(V); cfg = json.loads((V / 'video.json').read_text()); esc, total = escenas(cfg)
    say = (lambda *a: None) if silencio else print
    # 3) planos que faltan
    for i, _, _ in esc:
        c = V / f'compositions/{i}.html'
        if not c.exists(): c.write_text(PLANO.format(id=i)); say(f'  + compositions/{i}.html (plano del set único)')
    # 1) index.html
    html_p = V / 'index.html'; html = html_p.read_text()
    host = lambda i, t0, d, pista=1, tipo='graphics', extra='': (
        f'      <div id="{i}" data-composition-id="{i}" data-composition-src="compositions/{i}.html"\n'
        f'        data-start="{fmt(t0)}" data-duration="{fmt(d)}" data-track-index="{pista}" data-track-kind="{tipo}" data-width="1080" data-height="1920"{extra}></div>\n')
    if INI in html and FIN in html:
        bloque = ''.join(host(i, t0, d) for i, t0, d in esc)
        if (V / 'compositions/subtitulos.html').exists(): bloque += host('subtitulos', 0, total, 9, 'captions', ' style="z-index: 50"')
        html = html[:html.index(INI) + len(INI)] + '\n' + bloque + '      ' + html[html.index(FIN):]
    else:   # videos anteriores al 2026-11-17 (sin marcas): solo se actualizan inicio y duración de cada host
        for i, t0, d in esc:
            m = re.search(rf'<div\b[^>]*\bid="{re.escape(i)}"[^>]*>', html)
            if not m: sys.exit(f'index.html no tiene un host con id="{i}" (escena de video.json)')
            html = html[:m.start()] + set_attr(set_attr(m.group(0), 'data-start', fmt(t0)), 'data-duration', fmt(d)) + html[m.end():]
        m = re.search(r'<div\b[^>]*\bid="subtitulos"[^>]*>', html)
        if m: html = html[:m.start()] + set_attr(m.group(0), 'data-duration', fmt(total)) + html[m.end():]
    m = re.search(r'<div\b[^>]*data-composition-id="main"[^>]*>', html)
    html = html[:m.start()] + set_attr(m.group(0), 'data-duration', fmt(total)) + html[m.end():]
    html_p.write_text(html)
    # 2) assets/tiempos.js
    pal, frescas = palabras(V); fin_linea = {}
    for l, _, _, t1 in pal: fin_linea[l] = max(fin_linea.get(l, 0), t1)
    ids_esc = {i: (t0, d) for i, t0, d in esc}; voz = {}
    for l in cfg.get('voz', {}).get('lineas', []):
        voz[l['id']] = {'t0': l['t'], 't1': fin_linea.get(l['id'], round(l['t'] + len(l['texto'].split()) / 2.9, 2)), 'escena': l['escena'], 'texto': l['texto']}
    if pal and not {p[0] for p in pal} <= set(voz): say('  ~ aviso: los tiempos por palabra tienen líneas que ya no están en video.json → correr voz.py')
    js = ('// GENERADO por engine/tiempos.py desde video.json y audio/palabras.json. NO EDITAR: cambiar video.json y correr `python engine/reel.py voz videos/X`.\n'
          f'export const DUR = {fmt(total)};\n'
          '// ESC.<escena> = { t0: segundo en que empieza, d: duración, t1: segundo en que termina }\n'
          'export const ESC = ' + json.dumps({i: {'t0': t0, 'd': d, 't1': round(t0 + d, 3)} for i, (t0, d) in ids_esc.items()}, ensure_ascii=False) + ';\n'
          '// VOZ.<línea> = { t0, t1 (inicio y fin de la frase, en segundos del video), escena, texto }\n'
          'export const VOZ = ' + json.dumps(voz, ensure_ascii=False) + ';\n'
          '// PAL = [línea, palabra, inicio, fin] de cada palabra dicha (tiempos exactos de Piper)\n'
          'export const PAL = ' + json.dumps(pal, ensure_ascii=False) + ';\n' + JS_CUANDO)
    (V / 'assets/tiempos.js').write_text(js)
    for i, t0, d in esc: say(f'{i:12} {t0:6.2f} → {t0 + d:6.2f}')
    say(f'total        {total:.2f} s  → index.html y assets/tiempos.js ({len(pal)} palabras{"" if frescas or not pal else ", de la corrida anterior"}{"" if pal else ": falta correr voz.py"})')
    return total


if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    sincronizar(sys.argv[1])

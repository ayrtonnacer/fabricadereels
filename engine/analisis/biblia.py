#!/usr/bin/env python3
"""Arma las tablas numéricas de docs/referencias/BIBLIA-DE-ESTILO.md a partir de todos los metricas.json.
Uso: python engine/analisis/biblia.py            (reescribe las tablas entre <!-- TABLAS:inicio --> y <!-- TABLAS:fin -->)
Fuentes: docs/referencias/externos/*/metricas.json (referencias), propios/*/metricas.json (nuestros reels), metas.json (rangos objetivo).
Los grupos son: TODAS (todas las referencias) y AFINES (las oscuras y contemplativas, parecidas a nuestro estilo)."""
import glob, json, os, statistics as st, sys
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', 'referencias')
AFINES = ['motion-ref-2', 'motion-ref-3', 'motion-ref-4']          # lente explosionada, anuncio de vidrio, miedo y codicia
CLAVES = [  # (ruta, etiqueta, unidad, decimales)
    ('segundos', 'Duración', 's', 0),
    ('cortes.por_minuto', 'Cortes por minuto', '', 1), ('cortes.plano_mediano_s', 'Plano mediano', 's', 2),
    ('cortes.pct_con_movimiento_previo', 'Cortes con movimiento fuerte antes (transición)', '%', 0), ('cortes.pct_sobre_golpe_100ms', 'Cortes a ±0,1 s de un golpe de sonido', '%', 0),
    ('camara.pct_cuadros_en_movimiento', 'Cámara en movimiento', '% cuadros', 0), ('camara.velocidad_mediana_px_s', 'Velocidad mediana', 'px/s', 0), ('camara.velocidad_p95_px_s', 'Velocidad p95', 'px/s', 0),
    ('camara.pct_movimiento_lento', 'Movimiento lento (< 100 px/s)', '%', 0), ('camara.zoom_neto_pct_por_s', 'Zoom neto (+ acerca)', '%/s', 2), ('camara.jerk_mediano_px_s3', 'Tirón mediano (menos = más suave)', 'px/s³', 0),
    ('camara.movimientos_notorios_por_10s', 'Movimientos notorios (pico ≥ 100 px/s) cada 10 s', '', 1), ('camara.pico_notorio_mediano_px_s', 'Pico mediano de un movimiento notorio', 'px/s', 0),
    ('camara.duracion_notorio_mediana_s', 'Duración de un movimiento notorio', 's', 2), ('camara.retencion_mediana_s', 'Retención entre movimientos (≥ 0,5 s)', 's', 2), ('camara.ataque_mediano_s', 'Ataque de un movimiento (10 % → pico)', 's', 2), ('camara.liberacion_mediana_s', 'Liberación (pico → 10 %)', 's', 2),
    ('imagen.brillo_medio', 'Brillo medio', '0–1', 2), ('imagen.saturacion_media', 'Saturación media', '0–1', 2),
    ('audio.lufs_integrado', 'Volumen integrado', 'LUFS', 1), ('audio.pico_real_dbtp', 'Pico real', 'dBTP', 1), ('audio.silencio_pct', 'Silencio', '%', 1), ('audio.voz_activa_pct', 'Voz activa', '%', 0),
    ('audio.onsets_por_s', 'Ataques de sonido por segundo', '', 1), ('audio.golpes_graves', 'Golpes graves', 'n', 0),
    ('audio.palabras_por_s_total', 'Palabras por segundo (total)', 'pal/s', 2),
]
def get(d, ruta):
    for k in ruta.split('.'):
        if not isinstance(d, dict) or k not in d: return None
        d = d[k]
    return d if isinstance(d, (int, float)) else None
def cargar(sub):
    return {os.path.basename(os.path.dirname(f)): json.load(open(f)) for f in sorted(glob.glob(os.path.join(RAIZ, sub, '*', 'metricas.json')))}
def metas():
    p = os.path.join(RAIZ, 'metas.json'); return {k: v for k, v in json.load(open(p)).items() if not k.startswith('_')} if os.path.exists(p) else {}
def vals(grupo, ruta): return [v for v in (get(m, ruta) for m in grupo.values()) if v is not None]
def resumen(grupo, ruta):
    v = sorted(vals(grupo, ruta))
    if not v: return None
    q = lambda p: v[min(len(v) - 1, int(round(p * (len(v) - 1))))]
    return dict(med=st.median(v), p25=q(.25), p75=q(.75), mn=v[0], mx=v[-1], n=len(v))
def f(x, d): return '—' if x is None else (f'{x:.{d}f}'.replace('.', ',') if d else f'{x:.0f}')
def veredicto(x, meta):
    if x is None or not meta: return ''
    lo, hi = meta; return '✓' if lo <= x <= hi else ('▲ sobre la meta' if x > hi else '▼ bajo la meta')

def tablas():
    ext, prop = cargar('externos'), cargar('propios'); afin = {k: v for k, v in ext.items() if k in AFINES}; M = metas()
    L = ['### Cada video, número por número', '', '| Parámetro | ' + ' | '.join(f'`{k}`' for k in list(ext) + list(prop)) + ' |', '|---|' + '---|' * (len(ext) + len(prop))]
    for ruta, et, un, d in CLAVES:
        L.append(f'| {et}{" (" + un + ")" if un else ""} | ' + ' | '.join(f(get(m, ruta), d) for m in list(ext.values()) + list(prop.values())) + ' |')
    L += ['', f'### Resumen: {len(ext)} referencias · afines = {", ".join(AFINES)} · propio = último reel medido', '',
          '| Parámetro | Todas: mediana (p25–p75) | Afines: mediana (mín–máx) | Meta nuestra | ' + ' | '.join(f'**{k}**' for k in prop) + ' | Veredicto |', '|---|---|---|---|' + '---|' * (len(prop) + 1)]
    for ruta, et, un, d in CLAVES:
        a, b = resumen(ext, ruta), resumen(afin, ruta); meta = M.get(ruta)
        if not a: continue
        ult = list(prop.values())[-1] if prop else {}
        L.append(f'| {et}{" (" + un + ")" if un else ""} | {f(a["med"], d)} ({f(a["p25"], d)}–{f(a["p75"], d)}) | ' + (f'{f(b["med"], d)} ({f(b["mn"], d)}–{f(b["mx"], d)})' if b else '—') +
                 f' | {(f(meta[0], d) + "–" + f(meta[1], d)) if meta else "—"} | ' + ' | '.join(f(get(m, ruta), d) for m in prop.values()) + f' | {veredicto(get(ult, ruta), meta)} |')
    return '\n'.join(L)

def main():
    ruta = os.path.join(RAIZ, 'BIBLIA-DE-ESTILO.md'); s = open(ruta).read(); a, b = '<!-- TABLAS:inicio -->', '<!-- TABLAS:fin -->'
    if a not in s or b not in s: sys.exit('faltan los marcadores en BIBLIA-DE-ESTILO.md')
    open(ruta, 'w').write(s[:s.index(a) + len(a)] + '\n' + tablas() + '\n' + s[s.index(b):]); print('tablas actualizadas')
if __name__ == '__main__': main()

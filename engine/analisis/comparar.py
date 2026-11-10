#!/usr/bin/env python3
"""Compara un video propio contra la biblia de estilo (o contra una referencia puntual) y dice qué número se aleja (docs/MEDICION.md).
Uso:
  python engine/analisis/comparar.py propio/metricas.json                      # contra metas.json + referencias afines (lo normal)
  python engine/analisis/comparar.py referencia/metricas.json propio/metricas.json [--tolerancia 25]   # contra un video puntual
No juzga el gusto: marca qué número está fuera de rango."""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import biblia as B

def contra_biblia(P):
    ext = B.cargar('externos'); afin = {k: v for k, v in ext.items() if k in B.AFINES}; M = B.metas()
    L = [f"# `{P['archivo']}` ({P['segundos']} s) contra la biblia de estilo", '', '| Parámetro | Propio | Meta | Afines (mediana) | Todas (mediana) | |', '|---|---|---|---|---|---|']; fuera = []
    for ruta, et, un, d in B.CLAVES:
        p = B.get(P, ruta)
        if p is None: continue
        meta, a, t = M.get(ruta), B.resumen(afin, ruta), B.resumen(ext, ruta); v = B.veredicto(p, meta)
        if v and v != '✓': fuera.append((et, p, meta, v, d, un))
        L.append(f"| {et}{' (' + un + ')' if un else ''} | **{B.f(p, d)}** | {(B.f(meta[0], d) + '–' + B.f(meta[1], d)) if meta else '—'} | {B.f(a['med'], d) if a else '—'} | {B.f(t['med'], d) if t else '—'} | {v} |")
    L += ['', '## Fuera de la meta'] + ([f"- **{et}**: {B.f(p, d)} {un}, meta {B.f(m[0], d)}–{B.f(m[1], d)} → {v}" for et, p, m, v, d, un in fuera] or ['- Nada: todo dentro de las metas.'])
    return '\n'.join(L)

def contra_video(R, P, tol):
    L = [f"# Comparación: referencia `{R['archivo']}` ({R['segundos']} s) vs propio `{P['archivo']}` ({P['segundos']} s)", '', '| Parámetro | Referencia | Propio | Diferencia | |', '|---|---|---|---|---|']; lejos = []
    for ruta, et, un, d in B.CLAVES:
        r, p = B.get(R, ruta), B.get(P, ruta)
        if r is None or p is None: continue
        dif = (p - r) / abs(r) * 100 if r else (0 if p == 0 else 100); marca = '≈' if abs(dif) <= tol else ('▲' if dif > 0 else '▼')
        if marca != '≈': lejos.append((et, r, p, dif))
        L.append(f"| {et}{' (' + un + ')' if un else ''} | {r} | {p} | {dif:+.0f} % | {marca} |")
    L += ['', f'## Lo que se aleja más de ±{tol:.0f} %'] + ([f"- **{et}**: referencia {r}, propio {p} ({dif:+.0f} %)" for et, r, p, dif in sorted(lejos, key=lambda z: -abs(z[3]))] or ['- Nada: todo dentro de la tolerancia.'])
    return '\n'.join(L)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('archivos', nargs='+'); ap.add_argument('--tolerancia', type=float, default=25); a = ap.parse_args()
    J = [json.load(open(x)) for x in a.archivos]
    print(contra_biblia(J[0]) if len(J) == 1 else contra_video(J[0], J[1], a.tolerancia))
if __name__ == '__main__': main()

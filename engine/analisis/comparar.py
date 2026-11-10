#!/usr/bin/env python3
"""Compara las métricas de un video propio contra las de una referencia y dice qué se aleja (docs/MEDICION.md).
Uso: python engine/analisis/comparar.py referencia/metricas.json propio/metricas.json [--tolerancia 25]
Lee ambos metricas.json (salida de medir.py) y arma una tabla: referencia | propio | diferencia | veredicto. No juzga el gusto: marca qué número cambió."""
import argparse, json

CLAVES = [  # (ruta, etiqueta, unidad, "mayor es": para explicar la diferencia)
    ('cortes.por_minuto', 'Cortes por minuto', '', 'más cortes = más ritmo'),
    ('cortes.plano_mediano_s', 'Plano mediano', 's', 'más largo = más calma'),
    ('camara.pct_cuadros_en_movimiento', 'Cámara en movimiento', '% cuadros', 'más = nunca queda quieta'),
    ('camara.velocidad_mediana_px_s', 'Velocidad mediana de cámara', 'px/s', 'más = movimientos más notorios'),
    ('camara.pct_movimiento_lento', 'Movimiento lento (<100 px/s)', '%', 'más = deriva sutil'),
    ('camara.zoom_neto_pct_por_s', 'Zoom neto', '%/s', '+ acerca, − aleja'),
    ('camara.jerk_mediano_px_s3', 'Tirón (jerk) mediano', 'px/s³', 'menos = más suave'),
    ('imagen.brillo_medio', 'Brillo medio', '0–1', ''), ('imagen.contraste_medio', 'Contraste medio', '0–1', ''), ('imagen.saturacion_media', 'Saturación media', '0–1', ''),
    ('audio.lufs_integrado', 'Volumen integrado', 'LUFS', ''), ('audio.rango_dinamico_lu', 'Rango dinámico', 'LU', ''), ('audio.silencio_pct', 'Silencio', '%', ''),
    ('audio.onsets_por_s', 'Ataques de sonido por segundo', '', 'más = más efectos/golpes'), ('audio.golpes_graves', 'Golpes graves', 'n', ''),
    ('audio.palabras_por_s_total', 'Palabras por segundo (total)', 'pal/s', 'más = habla más rápido'), ('audio.palabras_por_s_hablando', 'Palabras por segundo (hablando)', 'pal/s', ''),
]
def get(d, ruta):
    for k in ruta.split('.'):
        if not isinstance(d, dict) or k not in d: return None
        d = d[k]
    return d if isinstance(d, (int, float)) else None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('ref'); ap.add_argument('propio'); ap.add_argument('--tolerancia', type=float, default=25); a = ap.parse_args()
    R, P = json.load(open(a.ref)), json.load(open(a.propio))
    L = [f"# Comparación: referencia `{R['archivo']}` ({R['segundos']} s) vs propio `{P['archivo']}` ({P['segundos']} s)", '', '| Parámetro | Referencia | Propio | Diferencia | |', '|---|---|---|---|---|']
    lejos = []
    for ruta, et, un, nota in CLAVES:
        r, p = get(R, ruta), get(P, ruta)
        if r is None or p is None: continue
        dif = (p - r) / abs(r) * 100 if r else (0 if p == 0 else 100)
        marca = '≈' if abs(dif) <= a.tolerancia else ('▲' if dif > 0 else '▼')
        if marca != '≈': lejos.append((et, r, p, dif, nota, un))
        L.append(f"| {et}{' (' + un + ')' if un else ''} | {r} | {p} | {dif:+.0f} % | {marca} |")
    L += ['', f"## Lo que se aleja más de ±{a.tolerancia:.0f} %"] + ([f"- **{et}**: referencia {r}, propio {p} ({dif:+.0f} %). {nota}" for et, r, p, dif, nota, un in sorted(lejos, key=lambda z: -abs(z[3]))] or ['- Nada: todo dentro de la tolerancia.'])
    print('\n'.join(L))
if __name__ == '__main__': main()

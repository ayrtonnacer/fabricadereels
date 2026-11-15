#!/usr/bin/env python3
"""Mide el ENCUADRE de un video (lo que medir.py no mide): cuánto del cuadro ocupa el contenido y qué tan ancho es.
Uso:  python engine/analisis/encuadre.py video.mp4 [video2.mp4 ...] [--zona 0,1920] [--cada 0.5] [--json salida.json]
Por cada video, sobre cuadros cada `--cada` segundos:
  • ocupacion_pct   % de píxeles con contenido (luma > 10 % por encima del negro de fondo, después de un desenfoque leve que borra las líneas finas del piso)
  • ancho_pct       ancho del contenido (percentiles 3–97 de las columnas con contenido) / ancho del cuadro
  • alto_pct        lo mismo en vertical, dentro de la zona
  • nitidez_rel     varianza del laplaciano en el 10 % más nítido / en la mediana: > 1 = hay planos nítidos y planos desenfocados (profundidad de campo)
`--zona y0,y1` limita la medición a una franja (para nuestros reels: 200,1100 = la zona de imagen, sin subtítulos ni piso de abajo).
Las referencias se miden en el cuadro completo. Devuelve la mediana de cada número."""
import argparse, json, subprocess, sys
import numpy as np, cv2


def cuadros(ruta, cada):
    cap = cv2.VideoCapture(ruta); fps = cap.get(cv2.CAP_PROP_FPS) or 30; n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); paso = max(1, int(round(fps * cada)))
    for i in range(0, n, paso):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i); ok, f = cap.read()
        if ok: yield i / fps, f


def medir_cuadro(f, zona):
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    g = cv2.resize(g, (540, int(540 * g.shape[0] / g.shape[1])), interpolation=cv2.INTER_AREA)
    if zona: s = g.shape[0] / 1920; g = g[int(zona[0] * s):int(zona[1] * s)]
    fondo = np.percentile(g, 5); b = cv2.GaussianBlur(g, (0, 0), 2.0); m = b > fondo + 0.10
    ocup = 100 * m.mean()
    cols, filas = np.where(m.any(0))[0], np.where(m.any(1))[0]
    def extension(idx, total):
        if len(idx) < 2: return 0.0
        peso = m.sum(0) if total == m.shape[1] else m.sum(1); c = np.cumsum(peso) / max(1, peso.sum())
        return 100 * (np.searchsorted(c, 0.97) - np.searchsorted(c, 0.03)) / total
    lap = np.abs(cv2.Laplacian(g, cv2.CV_32F)); tiles = [lap[y:y + 40, x:x + 40].var() for y in range(0, lap.shape[0] - 40, 40) for x in range(0, lap.shape[1] - 40, 40)]
    tiles = np.array([t for t in tiles if t > 1e-5]) if tiles else np.array([0])
    nit = float(np.percentile(tiles, 90) / max(1e-6, np.median(tiles))) if len(tiles) > 4 else 0.0
    return ocup, extension(cols, m.shape[1]), extension(filas, m.shape[0]), nit


def medir(ruta, zona, cada):
    R = [medir_cuadro(f, zona) for _, f in cuadros(ruta, cada)]
    A = np.array(R) if R else np.zeros((1, 4))
    med = np.median(A, 0)
    return dict(archivo=ruta, cuadros=len(R), ocupacion_pct=round(float(med[0]), 1), ancho_pct=round(float(med[1]), 1), alto_pct=round(float(med[2]), 1), nitidez_rel=round(float(med[3]), 1))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('videos', nargs='+'); ap.add_argument('--zona'); ap.add_argument('--cada', type=float, default=0.5); ap.add_argument('--json')
    a = ap.parse_args(); zona = tuple(int(x) for x in a.zona.split(',')) if a.zona else None
    out = [medir(v, zona, a.cada) for v in a.videos]
    print('| Video | Ocupación (%) | Ancho del contenido (%) | Alto (%) | Nitidez relativa |\n|---|---|---|---|---|')
    for r in out: print(f"| `{r['archivo'].split('/')[-1]}` | {r['ocupacion_pct']} | {r['ancho_pct']} | {r['alto_pct']} | {r['nitidez_rel']} |")
    if a.json: json.dump(out, open(a.json, 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__': main()

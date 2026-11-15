#!/usr/bin/env python3
"""Puntaje de continuidad ("arrastre"): ¿qué sobrevive a cada corte de escena? (idea de `probe.py` de feitangyuan/onetake, PolyForm NC: solo la idea, código propio).
Uso:  python engine/analisis/arrastre.py video.mp4 --escenas videos/X/video.json   (o --cortes 7.2,15.0,...)  [--json salida.json]
Solo numpy + PIL + ffmpeg (sin OpenCV ni scipy).

Método
  • Cortes: los límites de escena de video.json (--escenas: suma de las `d`), o los que pasás con --cortes. Sin ninguno, se detectan picos de diferencia
      entre cuadros, pero en motion graphics eso confunde cortes con animación: usar --escenas siempre que se pueda.
  • En cada corte se comparan el cuadro justo ANTES y el justo DESPUÉS: se marca "lo que hay" (píxeles claramente distintos del fondo) y se mide
    cuánto de lo de antes sigue en el después, dejando que se desplace (correlación cruzada por FFT, tolerancia de 2 px a 108 px de ancho).
    arrastre = área común / área del más chico, de 0 a 1.  < 0,2 = diapositiva (se reemplazó todo); 0,2–0,5 = parcial; ≥ 0,5 = algo continúa.
  • Reposo: % de cuadros quietos (diferencia ≈ 0) y tramo quieto más largo. Variación de los planos: coeficiente de variación de su duración.
Umbrales de onetake (referencia, no meta): puntaje medio ≥ 0,5 aceptado; planos con CV ≥ 0,25; ≥ 25 % de cuadros quietos y un tramo ≥ 1 s.
OJO: en nuestro estilo (negro puro, objetos de línea) el fondo casi no cambia entre escenas; por eso se mide sobre los objetos y no sobre el cuadro entero."""
import argparse, json, subprocess, sys
import numpy as np

W, H = 108, 192
FG = 0.10            # brillo (0–1) por encima del cual un píxel cuenta como "objeto" sobre fondo oscuro


def info(ruta):
    j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', ruta], capture_output=True, text=True).stdout)
    v = next(s for s in j['streams'] if s['codec_type'] == 'video'); n, d = v['r_frame_rate'].split('/'); return float(n) / float(d)


def cuadros(ruta):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', ruta, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
    out = []
    while True:
        b = p.stdout.read(W * H)
        if len(b) < W * H: break
        out.append(np.frombuffer(b, np.uint8).reshape(H, W).astype(np.float32) / 255)
    return np.array(out)


def mascara(g):
    """Objetos sobre el fondo: más claros que el fondo (mediana) + FG, engordados 1 px para que una línea fina no se pierda por medio píxel."""
    m = g > (np.median(g) + FG)
    mm = m.copy(); mm[1:] |= m[:-1]; mm[:-1] |= m[1:]; mm[:, 1:] |= m[:, :-1]; mm[:, :-1] |= m[:, 1:]
    return mm


def superposicion(a, b, tol=2):
    """Máxima área común de a y b dejando mover b hasta ±tol px (en x e y), sobre el área del más chico. Correlación cruzada por FFT."""
    sa, sb = a.sum(), b.sum()
    if min(sa, sb) < 12: return 0.0, 0, 0                      # casi vacío: no hay qué arrastrar
    A, B = np.fft.rfft2(a.astype(np.float32)), np.fft.rfft2(b.astype(np.float32))
    c = np.fft.irfft2(A * np.conj(B), s=a.shape)               # c[dy,dx] = Σ a(y,x)·b(y−dy,x−dx)
    mejor, by, bx = 0.0, 0, 0
    for dy in range(-tol, tol + 1):
        for dx in range(-tol, tol + 1):
            if c[dy % H, dx % W] > mejor: mejor, by, bx = float(c[dy % H, dx % W]), dy, dx
    return min(1.0, mejor / min(sa, sb)), bx, by


def detectar(dif, fps):
    umbral = max(np.median(dif) * 8, 0.02); cand = np.where(dif > umbral)[0]; cortes = []
    for i in cand:
        if cortes and i - cortes[-1] <= int(fps * 0.4): continue
        cortes.append(int(i))
    return cortes


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--cortes', default=''); ap.add_argument('--escenas', default=''); ap.add_argument('--json', default='')
    a = ap.parse_args(); fps = info(a.video); F = cuadros(a.video); n = len(F)
    dif = np.r_[0, np.abs(np.diff(F, axis=0)).mean(axis=(1, 2))]
    ts = [float(t) for t in a.cortes.split(',') if t.strip()]
    if a.escenas:
        acc = 0.0
        for e in json.load(open(a.escenas))['scenes'][:-1]: acc += e['d']; ts.append(round(acc, 3))
    cortes = [int(round(t * fps)) for t in ts] or detectar(dif, fps)
    cortes = [c for c in cortes if 3 <= c < n - 3]; res = []
    for c in cortes:
        s, dx, dy = superposicion(mascara(F[c - 2]), mascara(F[c + 2]))
        res.append(dict(seg=round(c / fps, 2), arrastre=round(s, 2), desplazamiento_px=[dx, dy], veredicto='diapositiva' if s < 0.2 else 'parcial' if s < 0.5 else 'continuo'))
    quietos = dif < 0.0015; run = best = 0
    for q in quietos:
        run = run + 1 if q else 0; best = max(best, run)
    lim = [0] + cortes + [n]; planos = np.array([(lim[k + 1] - lim[k]) / fps for k in range(len(lim) - 1)])
    cv = float(planos.std() / planos.mean()) if len(planos) > 1 else 0.0
    # mapa de energía (1 carácter ≈ 1/12 s, filas de 4 s; ' .:-=+*#%@' de quieto a corte duro), como el de onetake: se ve dónde hay pausas y ráfagas
    paso = max(1, int(round(fps / 12))); e = [dif[i:i + paso].mean() for i in range(0, n, paso)]; fila = int(round(4 * fps / paso)); esc = ' .:-=+*#%@'; lv = np.array([0, .0015, .004, .008, .015, .03, .06, .1, .16])
    mapa = [''.join(esc[int(np.searchsorted(lv, x, side='right'))] for x in e[r:r + fila]) for r in range(0, len(e), fila)]; m_mapa = mapa
    m = dict(archivo=a.video, cortes=res, arrastre_medio=round(float(np.mean([r['arrastre'] for r in res])), 2) if res else None,
             pct_cuadros_quietos=round(100 * float(quietos.mean()), 1), tramo_quieto_max_s=round(best / fps, 2),
             planos_s=[round(float(p), 1) for p in planos], planos_cv=round(cv, 2), mapa_energia=m_mapa, plano_min_max_ratio=round(float(planos.max() / max(planos.min(), 1e-6)), 1))
    print(f"{a.video}: {len(res)} cortes · arrastre medio {m['arrastre_medio']} · quietos {m['pct_cuadros_quietos']} % (tramo máx. {m['tramo_quieto_max_s']} s) · CV de planos {m['planos_cv']} (máx/mín ×{m['plano_min_max_ratio']})")
    for r in res: print(f"  t={r['seg']:>6} s  arrastre {r['arrastre']:.2f}  {r['veredicto']}")
    print('mapa de energía (cada fila = 4 s; espacio = quieto, @ = corte duro):'); [print(f'  {k * 4:>3}s |{r}|') for k, r in enumerate(m_mapa)]
    if a.json: open(a.json, 'w').write(json.dumps(m, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    sys.exit(main())

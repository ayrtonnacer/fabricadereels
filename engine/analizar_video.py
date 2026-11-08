#!/usr/bin/env python3
"""Analiza un VIDEO DE REFERENCIA y deja un documento por video en referencias/<nombre>/ (ver docs/ANALISIS-REFERENCIAS.md).

  python engine/analizar_video.py assets/referencias/ejemplo.mp4 [--nombre slug] [--fuente URL] [--objetivo "qué quiero aprender"]
                                  [--desde 12] [--hasta 27] [--forzar]

Mide (todo automático, a ~200 px de ancho):
  · cortes y planos (guion técnico: inicio, duración, transición de entrada)
  · movimiento de cámara por plano (flujo óptico → desplazamiento, zoom, giro, velocidad, perfil de easing, latigazos)
  · ritmo (cortes por minuto, duración media de plano)
  · sonido (volumen LUFS, golpes/whooshes con su momento y brillo, silencios)
y genera hojas de cuadros para MIRAR. La parte cualitativa (qué se ve, qué técnica, cómo copiarla) la completa Claude mirando las hojas.
Salida: analisis.md (no pisa uno existente: escribe analisis.auto.md salvo --forzar), planos.json, audio.json, meta.json, hoja-*.jpg (los jpg no van a git).
Limitación: el movimiento es 2D (no distingue dolly de zoom ni mide profundidad real); sirve para tiempos, dirección, velocidad y easing."""
import argparse, json, math, re, subprocess, sys, datetime
from pathlib import Path
import cv2, numpy as np

ROOT = Path(__file__).resolve().parent.parent
AW = 200                                    # ancho de análisis


def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:48] or 'video'
def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


# ---------------------------------------------------------------- lectura y cortes
def leer(path, t0, t1):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened(): sys.exit(f'No pude abrir {path}')
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); dur = n / fps if n > 0 else 0
    step = max(1, round(fps / 30)); efps = fps / step
    t1 = min(t1 or dur, dur) if dur else (t1 or 1e9)
    i0 = int(t0 * fps); cap.set(cv2.CAP_PROP_POS_FRAMES, i0)
    gray, hist, idx = [], [], []
    i = i0
    while True:
        ok, fr = cap.read()
        if not ok or i / fps > t1: break
        if (i - i0) % step == 0:
            h = int(AW * H / W); sm = cv2.resize(fr, (AW, h), interpolation=cv2.INTER_AREA)
            g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY); gray.append(g); idx.append(i)
            hs = cv2.calcHist([cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)], [0, 1], None, [12, 8], [0, 180, 0, 256])
            hist.append(cv2.normalize(hs, hs).flatten())
        i += 1
    cap.release()
    return dict(fps=fps, efps=efps, W=W, H=H, dur=dur, t0=t0, t1=t0 + len(gray) / efps, gray=gray, hist=hist, idx=idx)


def cortes(V):
    g, hs = V['gray'], V['hist']
    d = np.array([0.0] + [cv2.compareHist(hs[i - 1], hs[i], cv2.HISTCMP_BHATTACHARYYA) for i in range(1, len(hs))])
    a = np.array([0.0] + [float(np.mean(cv2.absdiff(g[i - 1], g[i]))) for i in range(1, len(g))])
    br = np.array([float(x.mean()) for x in g])
    cut = (d > 0.38) | (a > 38)
    ini = [0]
    for i in np.nonzero(cut)[0]:
        if i - ini[-1] >= max(3, int(0.25 * V['efps'])): ini.append(int(i))
    ini.append(len(g))
    planos = []
    for k in range(len(ini) - 1):
        s, e = ini[k], ini[k + 1]
        ent = 'inicio' if k == 0 else 'corte'
        if k > 0 and br[max(0, s - 2):s + 1].min() < 18 or (k > 0 and br[s:s + 3].min() < 18): ent = 'fundido por negro'
        planos.append(dict(n=k + 1, i0=s, i1=e, t0=V['t0'] + s / V['efps'], t1=V['t0'] + e / V['efps'], entrada=ent))
    return planos, d


# ---------------------------------------------------------------- movimiento de cámara
def mov(a, b):
    p = cv2.goodFeaturesToTrack(a, 150, 0.01, 7)
    if p is None or len(p) < 12: return None
    q, st, _ = cv2.calcOpticalFlowPyrLK(a, b, p, None, winSize=(21, 21), maxLevel=3)
    ok = st.ravel() == 1
    if ok.sum() < 12: return None
    M, inl = cv2.estimateAffinePartial2D(p[ok], q[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0)
    if M is None or inl is None or inl.sum() < 8: return None
    s = math.hypot(M[0, 0], M[1, 0]); rot = math.degrees(math.atan2(M[1, 0], M[0, 0]))
    h, w = a.shape; c = np.array([w / 2, h / 2]); t = (M[:, :2] @ c + M[:, 2]) - c
    return float(t[0] / w), float(t[1] / w), math.log(max(s, 1e-3)), rot


def suavizar(x, k=5):
    x = np.array(x, float)
    if len(x) < k: return x
    return np.convolve(np.pad(x, (k // 2, k // 2), mode='edge'), np.ones(k) / k, mode='valid')


def analizar_plano(V, P):
    f = V['efps']; g = V['gray']; s, e = P['i0'], P['i1']
    dx, dy, dz, dr, fallo = [], [], [], [], 0
    lap = [cv2.Laplacian(g[i], cv2.CV_64F).var() for i in range(s, e)]
    for i in range(s + 1, e):
        m = mov(g[i - 1], g[i])
        if m is None: fallo += 1; dx.append(0.0); dy.append(0.0); dz.append(0.0); dr.append(0.0); continue
        dx.append(m[0]); dy.append(m[1]); dz.append(m[2]); dr.append(m[3])
    P['dur'] = P['t1'] - P['t0']
    if len(dx) < 3: P.update(mov='plano muy corto', vel='-', perfil='-', totales={}, pico=None, latigazo=False, estatico=True); return P
    dx, dy, dz, dr = [suavizar(v, 3) for v in (dx, dy, dz, dr)]
    inten = np.sqrt((dx * f) ** 2 + (dy * f) ** 2 + (dz * f) ** 2 + (np.radians(dr) * f) ** 2)   # "anchos de cuadro por segundo"
    sm = suavizar(inten, 5)
    tot = dict(x=float(dx.sum()), y=float(dy.sum()), zoom=float(dz.sum()), giro=float(dr.sum()))
    comp = {'x': abs(tot['x']), 'y': abs(tot['y']), 'zoom': abs(tot['zoom']), 'giro': abs(tot['giro']) / 30}
    orden = sorted(comp, key=lambda k: -comp[k])
    nombres = dict(
        zoom=lambda: 'acercamiento (push-in / zoom in)' if tot['zoom'] > 0 else 'alejamiento (pull-out / zoom out)',
        x=lambda: 'paneo o travelling hacia la izquierda' if tot['x'] > 0 else 'paneo o travelling hacia la derecha',
        y=lambda: 'inclinación hacia arriba o grúa que sube' if tot['y'] > 0 else 'inclinación hacia abajo o grúa que baja',
        giro=lambda: 'giro de la imagen en sentido horario' if tot['giro'] > 0 else 'giro de la imagen en sentido antihorario')
    med = float(np.median(sm)); pico = float(sm.max()); n = len(sm)
    estatico = pico < 0.06
    if estatico: desc = 'cámara casi quieta'
    else:
        desc = nombres[orden[0]]()
        if comp[orden[1]] > 0.6 * comp[orden[0]] and comp[orden[1]] > 0.02: desc += ' + ' + nombres[orden[1]]()
    vel = 'quieta' if estatico else 'lenta' if pico < 0.3 else 'media' if pico < 0.9 else 'rápida' if pico < 2.2 else 'muy rápida'
    t3 = [sm[:max(1, n // 3)].mean(), sm[n // 3:max(n // 3 + 1, 2 * n // 3)].mean(), sm[2 * n // 3:].mean()]
    if estatico: perfil = '-'
    elif t3[1] > 1.3 * max(t3[0], t3[2]): perfil = 'suave (arranca y frena: ease-in-out)'
    elif t3[0] > 1.5 * t3[2]: perfil = 'arranca rápido y frena (ease-out)'
    elif t3[2] > 1.5 * t3[0]: perfil = 'arranca lento y acelera (ease-in)'
    else: perfil = 'velocidad constante (lineal)'
    blur = float(np.median(lap[1:]) / (max(lap[1:]) + 1e-9)) if len(lap) > 3 else 1.0
    lat = bool(pico > 3.5 or (fallo >= 2 and pico > 0.9) or (blur < 0.35 and pico > 0.9))
    P['tramos'] = tramos_plano(V, P, dx, dy, dz, dr, sm) if P['dur'] > 1.5 else []
    P.update(mov=desc, vel=vel, perfil=perfil, totales={k: round(v, 3) for k, v in tot.items()}, pico_intensidad=round(pico, 2),
             pico_en=round(float(sm.argmax()) / max(1, n - 1), 2), cuadros_sin_traza=fallo, latigazo=bool(lat and P['dur'] <= 1.5), estatico=bool(estatico),
             serie=[round(float(x), 3) for x in sm[::max(1, n // 40)]])
    return P


def etiqueta_mov(dx, dy, dz, dr, f, umbral=0.08):
    c = {'x': abs(dx) * f, 'y': abs(dy) * f, 'zoom': abs(dz) * f, 'giro': abs(math.radians(dr)) * f}
    k = max(c, key=c.get)
    if c[k] < umbral: return 'quieta'
    if k == 'x': return 'paneo/travelling a la izquierda' if dx > 0 else 'paneo/travelling a la derecha'        # la escena corre a la derecha = cámara a la izquierda
    if k == 'y': return 'inclinación o grúa hacia arriba' if dy > 0 else 'inclinación o grúa hacia abajo'
    if k == 'zoom': return 'acercamiento' if dz > 0 else 'alejamiento'
    return 'giro horario' if dr > 0 else 'giro antihorario'


def tramos_plano(V, P, dx, dy, dz, dr, sm):
    f = V['efps']; lab = [etiqueta_mov(dx[i], dy[i], dz[i], dr[i], f) for i in range(len(dx))]
    k = int(max(3, 0.25 * f)) | 1; mod = []
    for i in range(len(lab)):                                   # moda en ventana: evita parpadeos entre etiquetas
        w = lab[max(0, i - k // 2):i + k // 2 + 1]; mod.append(max(set(w), key=w.count))
    runs = []
    for i, l in enumerate(mod):
        if runs and runs[-1][0] == l: runs[-1][2] = i + 1
        else: runs.append([l, i, i + 1])
    minlen = int(0.4 * f); ch = True
    while ch and len(runs) > 1:                                 # absorber tramos muy cortos en el vecino más largo
        ch = False
        for j, r in enumerate(runs):
            if r[2] - r[1] < minlen:
                nb = j - 1 if j > 0 and (j == len(runs) - 1 or runs[j - 1][2] - runs[j - 1][1] >= runs[j + 1][2] - runs[j + 1][1]) else j + 1
                a, b = runs[nb], r; a[1], a[2] = min(a[1], b[1]), max(a[2], b[2]); runs.pop(j); ch = True; break
        merged = []
        for r in runs:
            if merged and merged[-1][0] == r[0]: merged[-1][2] = r[2]
            else: merged.append(r)
        runs = merged
    out = []
    for l, a, b in runs:
        pk = float(sm[a:b].max()) if b > a else 0.0
        out.append(dict(t0=round(P['t0'] + (a + 1) / f, 2), t1=round(P['t0'] + (b + 1) / f, 2), mov=l, pico=round(pk, 2),
                        vel='quieta' if l == 'quieta' else 'lenta' if pk < 0.3 else 'media' if pk < 0.9 else 'rápida' if pk < 2.2 else 'muy rápida'))
    return out


def sugerencia(P):
    if len(P.get('tramos', [])) > 1: return f"plano continuo de {P['dur']:.1f} s con {len(P['tramos'])} tramos de movimiento: una `rig.toma` por tramo (ver tabla de tramos); un tramo muy rápido y corto con desenfoque = latigazo."
    if P.get('estatico'): return 'cámara quieta: el movimiento lo hacen los objetos (no hace falta `rig.toma`).'
    ease = {'suave': "'suave'", 'ease-out': "'salida'", 'ease-in': "'entrada'", 'lineal': "'lineal'"}
    e = next((v for k, v in ease.items() if k in P['perfil']), "'suave'")
    m = P['mov']; d = f"{P['dur']:.1f} s"
    if P.get('latigazo'): return f"latigazo: hueco de {max(0.3, P['dur']):.1f} s entre dos tomas + `rig.transicion(i, 'latigazo')` + `MotionBlur`."
    if 'acerc' in m: return f"`tipo:'mover'` acercando (push-in), ease {e}, {d}; fov 50→35 si hay zoom."
    if 'alej' in m: return f"`tipo:'mover'` alejando (pull-out), ease {e}, {d}."
    if 'paneo' in m: return f"travelling lateral (`tipo:'mover'`) u `'orbita'` si el objeto queda centrado; ease {e}, {d}."
    if 'grúa' in m: return f"grúa (`tipo:'mover'` cambiando la altura) o `'cenital'` si termina mirando abajo; ease {e}, {d}."
    return f"giro/roll: `roll` en `tipo:'mover'`, ease {e}, {d}."


# ---------------------------------------------------------------- audio
def audio(path, t0, t1):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(t0)] + (['-t', str(t1 - t0)] if t1 else []) + ['-i', str(path), '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-']
    x = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32)
    if len(x) < 16000: return None
    r = subprocess.run(['ffmpeg', '-nostats', '-ss', str(t0)] + (['-t', str(t1 - t0)] if t1 else []) + ['-i', str(path), '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    last = r[r.rfind('Summary:'):] if 'Summary:' in r else ''
    g = lambda k: (re.search(k + r':\s+(-?[\d.]+)', last) or [None, None])[1]
    out = dict(LUFS=float(g('I')) if g('I') else None, LRA=float(g('LRA')) if g('LRA') else None, pico_dBFS=float(g('Peak')) if g('Peak') else None)
    hop = 160; n = len(x) // hop
    env = 20 * np.log10(np.sqrt(np.maximum(1e-12, (x[:n * hop].reshape(n, hop) ** 2).mean(1))))
    piso = float(np.percentile(env, 20)); out['rango_dB'] = round(float(np.percentile(env, 95) - np.percentile(env, 10)), 1)
    gol, ult = [], -9
    for i in range(5, n - 12):
        t = i * hop / 16000
        if env[i] - env[i - 4] > 9 and env[i] > piso + 12 and t - ult > 0.25:
            seg = x[i * hop:i * hop + 1600 * 2] * np.hanning(min(3200, len(x) - i * hop))
            sp = np.abs(np.fft.rfft(seg)); fr = np.fft.rfftfreq(len(seg), 1 / 16000)
            cen = float((sp * fr).sum() / (sp.sum() + 1e-9))
            tipo = 'brillante (whoosh / chasquido)' if cen > 2500 else 'grave (golpe / boom)' if cen < 900 else 'medio (impacto / pop)'
            gol.append(dict(t=round(t + t0, 2), tipo=tipo, nivel_dB=round(float(env[i:i + 8].max()), 1), centroide_Hz=int(cen))); ult = t
    sil, ini = [], None
    for i in range(n):
        if env[i] < piso - 6:
            ini = i if ini is None else ini
        elif ini is not None:
            if (i - ini) * hop / 16000 > 0.4: sil.append([round(ini * hop / 16000 + t0, 2), round(i * hop / 16000 + t0, 2)])
            ini = None
    out.update(golpes=gol, silencios=sil); return out


# ---------------------------------------------------------------- hojas de cuadros
def frame_en(cap, fps, t, H_t):
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, int(t * fps))); ok, fr = cap.read()
    if not ok: return None
    w = int(H_t * fr.shape[1] / fr.shape[0]); return cv2.resize(fr, (w, H_t), interpolation=cv2.INTER_AREA)


def etiqueta(img, txt):
    cv2.rectangle(img, (0, 0), (img.shape[1], 26), (0, 0, 0), -1)
    cv2.putText(img, txt, (6, 19), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA); return img


def hojas(path, V, planos, out):
    cap = cv2.VideoCapture(str(path)); TH = 320; res = []
    filas = []
    for P in planos:
        d = P['t1'] - P['t0']; ts = [P['t0'] + d * k for k in ((0.12, 0.5, 0.88) if d > 0.6 else (0.5,))]
        fr = [frame_en(cap, V['fps'], t, TH) for t in ts]; fr = [f for f in fr if f is not None]
        if not fr: continue
        etiqueta(fr[0], f"P{P['n']}  {P['t0']:.1f}-{P['t1']:.1f}s")
        filas.append(np.hstack(fr))
    wmax = max(f.shape[1] for f in filas) if filas else 0
    for k in range(0, len(filas), 8):
        blk = [np.pad(f, ((0, 0), (0, wmax - f.shape[1]), (0, 0))) for f in filas[k:k + 8]]
        nom = f'hoja-planos-{k // 8 + 1}.jpg'; cv2.imwrite(str(out / nom), np.vstack(blk), [cv2.IMWRITE_JPEG_QUALITY, 85]); res.append(nom)
    # tira alrededor de cada corte (−0,2 s … +0,2 s, cuadros casi consecutivos): cómo está hecha la transición
    filas = []
    for P in planos[1:]:
        tc = P['t0']; fr = []
        for o in (-0.2, -0.1, -1.5 / V['fps'], 0.5 / V['fps'], 0.1, 0.2):
            f = frame_en(cap, V['fps'], tc + o, 240)
            if f is not None: fr.append(etiqueta(f, f'{o:+.2f}'))
        if fr: etiqueta(fr[0], f'corte {tc:.2f}s'); filas.append(np.hstack(fr))
    if filas:
        wm = max(f.shape[1] for f in filas)
        for k in range(0, len(filas), 10):
            blk = [np.pad(f, ((0, 0), (0, wm - f.shape[1]), (0, 0))) for f in filas[k:k + 10]]
            nom = f'hoja-cortes-{k // 10 + 1}.jpg'; cv2.imwrite(str(out / nom), np.vstack(blk), [cv2.IMWRITE_JPEG_QUALITY, 85]); res.append(nom)
    dur = V['t1'] - V['t0']; nc = min(60, max(12, int(dur))); cel = []
    for k in range(nc):
        t = V['t0'] + dur * (k + 0.5) / nc; f = frame_en(cap, V['fps'], t, 240)
        if f is not None: cel.append(etiqueta(f, f'{t:.1f}s'))
    if cel:
        cw = max(c.shape[1] for c in cel); cols = 8 if cw < 200 else 6
        cel = [np.pad(c, ((0, 0), (0, cw - c.shape[1]), (0, 0))) for c in cel]
        while len(cel) % cols: cel.append(np.zeros_like(cel[0]))
        cv2.imwrite(str(out / 'hoja-tiempo.jpg'), np.vstack([np.hstack(cel[i:i + cols]) for i in range(0, len(cel), cols)]), [cv2.IMWRITE_JPEG_QUALITY, 85]); res.append('hoja-tiempo.jpg')
    cap.release(); return res


# ---------------------------------------------------------------- documento
def ritmo(planos, dur):
    L = [p['dur'] for p in planos]; m = float(np.mean(L)); med = float(np.median(L))
    et = 'vertiginoso' if m < 1.2 else 'dinámico' if m < 2.5 else 'pausado' if m < 4.5 else 'contemplativo'
    mov_pct = 100 * sum(p['dur'] for p in planos if not p.get('estatico')) / max(dur, 1e-9)
    return dict(planos=len(planos), cortes_por_min=round(60 * (len(planos) - 1) / max(dur, 1e-9), 1), duracion_media=round(m, 2), mediana=round(med, 2),
                mas_corto=round(min(L), 2), mas_largo=round(max(L), 2), etiqueta=et, pct_camara_en_movimiento=round(mov_pct))


def md(meta, planos, R, A, hjs, nombre):
    f = lambda v: '-' if v is None else v
    s = [f"# Análisis de referencia — {meta['titulo']}", '',
         '> Documento generado por `engine/analizar_video.py`. Las columnas y secciones marcadas **(completar)** las llena Claude mirando las hojas de cuadros; los números son medidos. Para qué sirve y cómo se usa: `docs/ANALISIS-REFERENCIAS.md`.', '',
         '## Ficha', f"- **Fuente:** {meta['fuente'] or '(sin link)'}", f"- **Archivo:** `{meta['archivo']}` · {meta['resolucion']} · {meta['fps']:.0f} fps · tramo analizado {mmss(meta['t0'])}–{mmss(meta['t1'])} ({meta['t1'] - meta['t0']:.1f} s)",
         f"- **Analizado:** {meta['fecha']}", f"- **Qué queremos aprender:** {meta['objetivo'] or '(completar)'}",
         f"- **Hojas de cuadros (locales, no van a git):** " + ', '.join(f'`referencias/{nombre}/{h}`' for h in hjs), '',
         '## 1. En una frase (completar)', '', '## 2. Estructura narrativa (completar)',
         '| Bloque | Tiempo | Qué pasa |', '|---|---|---|', '| Hook | | |', '| Desarrollo | | |', '| Giro / micro-loop | | |', '| Payoff | | |', '| Cierre | | |', '',
         '## 3. Guion técnico (planos)', 'Movimiento medido por flujo óptico (2D). "Entrada" = cómo se llega a ese plano.', '',
         '| # | Tiempo | Dur. | Entrada | Movimiento de cámara | Velocidad | Perfil | Qué se ve (completar) | Texto / gráficos (completar) |', '|---|---|---|---|---|---|---|---|---|']
    for p in planos:
        s.append(f"| P{p['n']} | {p['t0']:.1f}–{p['t1']:.1f} | {p['dur']:.1f} s | {p['entrada']} | {p['mov']}{' · **latigazo**' if p.get('latigazo') else ''} | {p['vel']} | {p['perfil']} |  |  |")
    largos = [p for p in planos if len(p.get('tramos', [])) > 1]
    if largos:
        s += ['', '### Tramos de movimiento dentro de los planos continuos', 'Un plano largo puede mezclar varios movimientos (dron → latigazo → órbita…): acá se separan.', '',
              '| Plano | Tiempo | Movimiento | Velocidad | Pico |', '|---|---|---|---|---|']
        for p in largos:
            for t in p['tramos']: s.append(f"| P{p['n']} | {t['t0']}–{t['t1']} | {t['mov']} | {t['vel']} | {t['pico']} |")
    s += ['', '### Traducción sugerida a `engine/camara3d.js` (a confirmar mirando los cuadros)'] + [f"- **P{p['n']}** ({p['t0']:.1f} s): {sugerencia(p)}" for p in planos]
    s += ['', '## 4. Ritmo', f"- {R['planos']} planos · **{R['cortes_por_min']} cortes/min** · plano medio {R['duracion_media']} s (mediana {R['mediana']} s; más corto {R['mas_corto']} s, más largo {R['mas_largo']} s) → ritmo **{R['etiqueta']}**.",
          f"- La cámara se mueve en el {R['pct_camara_en_movimiento']}% del tiempo.", '- Qué cambia en pantalla cada cuántos segundos (completar):', '']
    s += ['## 5. Sonido']
    if A:
        s += [f"- Volumen integrado **{f(A['LUFS'])} LUFS** · rango {f(A['LRA'])} LU · pico {f(A['pico_dBFS'])} dBFS · rango dinámico ≈ {A['rango_dB']} dB"]
        if A['golpes']:
            s += ['', '| Momento | Tipo | Nivel | Qué es (completar) |', '|---|---|---|---|'] + [f"| {g['t']} s | {g['tipo']} | {g['nivel_dB']} dB | |" for g in A['golpes'][:40]]
        s += ['', f"- Silencios (> 0,4 s): " + (', '.join(f'{a}–{b} s' for a, b in A['silencios']) or 'ninguno')]
    else: s += ['- Sin pista de audio.']
    s += ['- Voz / música / efectos / ambiente: qué capas hay y cómo se mezclan (completar):', '',
          '## 6. Técnicas para tomar (completar)', '| Técnica | Cómo se hace | Cómo la hacemos nosotros |', '|---|---|---|', '|  |  |  |', '',
          '## 7. Qué NO copiar (completar)', 'La voz (Daniela), la música de fondo y la estética (cyber/HackTheBox) son nuestras; de la referencia se toma la técnica, no el look. Anotar acá lo que se descarta y por qué.', '',
          '## 8. Ideas para nuestros reels (completar)', '', '## Datos crudos', f"- `referencias/{nombre}/planos.json` (series de velocidad por plano) y `audio.json`.", '',
          '## Límites de este análisis', '- El movimiento es una estimación 2D: no distingue un dolly de un zoom ni mide profundidad. Funciona bien en push-in, travelling lateral y zoom through; **falla o se equivoca** en latigazos (desenfoque), órbitas alrededor de un objeto centrado, grúas combinadas con inclinación y escenas con poca textura. Por eso cada movimiento se confirma mirando las hojas de cuadros.',
          '- No separa voz de música: los golpes del audio son candidatos; confirmar escuchando.', '- Las transiciones suaves (disolvencias) pueden no detectarse como corte.']
    return '\n'.join(s) + '\n'


def indice():
    filas = []
    for m in sorted((ROOT / 'referencias').glob('*/meta.json')):
        d = json.loads(m.read_text()); filas.append(f"| [{d['titulo']}]({m.parent.name}/analisis.md) | {d['fecha']} | {d['t1'] - d['t0']:.0f} s | {d['ritmo']} | {d['objetivo'] or ''} |")
    (ROOT / 'referencias' / 'INDICE.md').write_text('# Videos de referencia analizados\nUn documento por video (`referencias/<nombre>/analisis.md`). Se regenera solo al analizar.\n\n| Video | Fecha | Duración | Ritmo | Qué queríamos aprender |\n|---|---|---|---|---|\n' + '\n'.join(filas) + '\n')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--nombre'); ap.add_argument('--fuente', default=''); ap.add_argument('--objetivo', default='')
    ap.add_argument('--desde', type=float, default=0); ap.add_argument('--hasta', type=float, default=0); ap.add_argument('--forzar', action='store_true'); a = ap.parse_args()
    path = Path(a.video).resolve(); nombre = slug(a.nombre or path.stem)
    out = ROOT / 'referencias' / nombre; out.mkdir(parents=True, exist_ok=True)
    V = leer(path, a.desde, a.hasta or 120)
    if len(V['gray']) < 10: sys.exit('Muy pocos cuadros leídos.')
    planos, _ = cortes(V)
    for P in planos: analizar_plano(V, P)
    dur = V['t1'] - V['t0']; R = ritmo(planos, dur); A = audio(path, V['t0'], V['t1'])
    hj = hojas(path, V, planos, out)
    meta = dict(titulo=path.stem, archivo=str(path.relative_to(ROOT)) if str(path).startswith(str(ROOT)) else path.name, fuente=a.fuente, objetivo=a.objetivo,
                resolucion=f"{V['W']}x{V['H']}", fps=V['fps'], t0=V['t0'], t1=V['t1'], fecha=datetime.date.today().isoformat(), ritmo=R['etiqueta'])
    (out / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    (out / 'planos.json').write_text(json.dumps(dict(ritmo=R, planos=planos), ensure_ascii=False, indent=1))
    if A: (out / 'audio.json').write_text(json.dumps(A, ensure_ascii=False, indent=1))
    dest = out / ('analisis.md' if (a.forzar or not (out / 'analisis.md').exists()) else 'analisis.auto.md')
    dest.write_text(md(meta, planos, R, A, hj, nombre)); indice()
    print(f'{len(planos)} planos · {R["cortes_por_min"]} cortes/min · ritmo {R["etiqueta"]}' + (f' · {A["LUFS"]} LUFS · {len(A["golpes"])} golpes' if A else ' · sin audio'))
    print('→', dest.relative_to(ROOT)); print('hojas:', ', '.join(hj))


if __name__ == '__main__': main()

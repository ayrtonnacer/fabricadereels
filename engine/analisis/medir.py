#!/usr/bin/env python3
"""Mide un video como un instrumento: pasa la percepción ("se siente suave", "va rápido") a NÚMEROS repetibles (docs/MEDICION.md).
Uso:  python engine/analisis/medir.py video.mp4 carpeta_salida [--transcripcion texto.txt] [--hojas]
Salida en carpeta_salida/:
  metricas.json   resumen: imagen, cortes, cámara (movimiento, zoom, velocidad, tirón/jerk), audio
  medidas.csv     por cuadro: dx, dy (px a 1080 de ancho), zoom %, diferencia, brillo, contraste, saturación
  INFORME.md      lectura en español de lo anterior
  hoja_resumen.jpg  1 cuadro por segundo (hasta 60); con --hojas también hojas de 60 cuadros (2 s) con número de cuadro
Método (inspirado en medir_30fps.py de luispablovillasenor-afk/shorts-animados-claude, MIT; código propio):
  • Cámara: correlación de fase entre cuadros consecutivos. Traslación = pico de la correlación de las FFT; zoom = lo mismo sobre el espectro en
    coordenadas log-polares (Fourier–Mellin). Calibrado con movimientos sintéticos (autotest: --autotest).
  • Tirón (jerk): tercera derivada de la posición de la cámara (Savitzky–Golay): qué tan bruscamente cambia la aceleración. Menos = más suave.
  • Cortes: diferencia de cuadros + distancia de histograma de color; se clasifican seco / transición."""
import argparse, csv, json, os, re, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw
from scipy.signal import savgol_filter, find_peaks, butter, sosfilt

W, H = 270, 480                 # tamaño de medición (0,25 de 1080×1920)
ESCALA = 1080 / W
ZOOM_CORR = 1.10                # corrección medida con zooms sintéticos (el método subestima ~10 %)
TW, TH = 108, 192


def info(ruta):
    j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', ruta], capture_output=True, text=True).stdout)
    v = next(s for s in j['streams'] if s['codec_type'] == 'video'); a = next((s for s in j['streams'] if s['codec_type'] == 'audio'), None)
    num, den = (v.get('avg_frame_rate') or v['r_frame_rate']).split('/'); fps = float(num) / float(den)
    return dict(fps=round(fps, 3), ancho=int(v['width']), alto=int(v['height']), dur=float(j['format']['duration']), audio=a is not None, codec=v.get('codec_name'))


def cuadros(ruta):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', ruta, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)


WIN = cv2.createHanningWindow((W, H), cv2.CV_32F)
MAXR = min(W, H) / 2; MLOG = W / np.log(MAXR)
def espectro_logpolar(g):
    F = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(g * WIN)))).astype(np.float32)
    return cv2.warpPolar(F, (W, H), (W / 2, H / 2), MAXR, cv2.WARP_POLAR_LOG | cv2.INTER_LINEAR)
def mover(prev, g, lp_prev, lp):
    (dx, dy), r = cv2.phaseCorrelate(prev, g, WIN)                      # traslación (px a 270 px de ancho)
    (sx, _), _ = cv2.phaseCorrelate(lp_prev, lp)                        # escala: desplazamiento en log-radio del espectro
    zoom = float(np.clip((np.exp(-sx / MLOG * ZOOM_CORR) - 1) * 100, -8, 8))   # % por cuadro (+ = acerca); un zoom de cámara real nunca pasa de unos %/cuadro
    if r < 0.1: return 0.0, 0.0, 0.0, r                                  # sin correlación confiable (corte, escena nueva, imagen sin estructura): no se mide
    return dx * ESCALA, dy * ESCALA, zoom, r


def nombre_color(rgb): return '#%02X%02X%02X' % tuple(int(x) for x in rgb)


def analizar_video(ruta, out, hojas):
    inf = info(ruta); fps = inf['fps']; os.makedirs(out, exist_ok=True)
    if hojas: os.makedirs(os.path.join(out, 'hojas'), exist_ok=True)
    filas, prev, lp_prev, hist_prev, thumbs, hoja = [], None, None, None, [], []
    colores = []
    for i, rgb in enumerate(cuadros(ruta)):
        g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV); lp = espectro_logpolar(g)
        hist = cv2.calcHist([hsv], [0, 1], None, [16, 8], [0, 180, 0, 256]); hist = cv2.normalize(hist, hist, 1, 0, cv2.NORM_L1).flatten().astype(np.float32)
        f = dict(cuadro=i, seg=round(i / fps, 3), dx=0.0, dy=0.0, zoom=0.0, resp=0.0, dif=0.0, hist=0.0, brillo=round(float(g.mean()), 4), contraste=round(float(g.std()), 4), sat=round(float(hsv[..., 1].mean() / 255), 4))
        if prev is not None:
            f['dif'] = round(float(np.abs(g - prev).mean() * 255), 2); f['hist'] = round(float(cv2.compareHist(hist_prev, hist, cv2.HISTCMP_BHATTACHARYYA)), 3)
            dx, dy, zm, r = mover(prev, g, lp_prev, lp); f['dx'], f['dy'], f['zoom'], f['resp'] = round(dx, 3), round(dy, 3), round(zm, 4), round(float(r), 3)
        filas.append(f); prev, lp_prev, hist_prev = g, lp, hist
        if i % max(1, round(fps)) == 0 and len(thumbs) < 60: thumbs.append((i, Image.fromarray(rgb).resize((TW, TH))))
        if i % 15 == 0: colores.append(rgb[::6, ::6].reshape(-1, 3))
        if hojas:
            hoja.append((i, Image.fromarray(rgb).resize((TW, TH))))
            if len(hoja) == 60: guardar_hoja(hoja, out, fps); hoja = []
    if hojas and hoja: guardar_hoja(hoja, out, fps)
    guardar_resumen_hoja(thumbs, out, fps)
    with open(os.path.join(out, 'medidas.csv'), 'w', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=list(filas[0].keys())); wr.writeheader(); wr.writerows(filas)
    return inf, filas, np.concatenate(colores)


def guardar_hoja(hoja, out, fps):
    img = Image.new('RGB', (10 * TW, 6 * (TH + 14)), (20, 20, 20)); d = ImageDraw.Draw(img)
    for k, (i, im) in enumerate(hoja):
        x, y = (k % 10) * TW, (k // 10) * (TH + 14); img.paste(im, (x, y + 14)); d.text((x + 3, y + 1), f'{i}  {i / fps:.2f}s', fill=(255, 220, 0))
    img.save(os.path.join(out, 'hojas', f'hoja_{hoja[0][0] // 60:03d}.jpg'), quality=82)
def guardar_resumen_hoja(thumbs, out, fps):
    cols = 10; rows = (len(thumbs) + cols - 1) // cols; img = Image.new('RGB', (cols * TW, rows * (TH + 14)), (20, 20, 20)); d = ImageDraw.Draw(img)
    for k, (i, im) in enumerate(thumbs): x, y = (k % cols) * TW, (k // cols) * (TH + 14); img.paste(im, (x, y + 14)); d.text((x + 3, y + 1), f'{i / fps:.0f}s', fill=(255, 220, 0))
    img.save(os.path.join(out, 'hoja_resumen.jpg'), quality=85)


def cortes_y_planos(filas, fps):
    n = len(filas); dif = np.array([f['dif'] for f in filas]); hist = np.array([f['hist'] for f in filas]); resp = np.array([f['resp'] for f in filas])
    # En motion graphics el fondo no cambia entre escenas, así que la diferencia de cuadros NO sirve sola. Lo que delata un corte es que la correlación
    # de fase pierde el pico (resp ~0,9 → <0,2: ya no hay un desplazamiento que explique el cuadro) junto con un salto del histograma de color.
    es_corte = ((resp < 0.2) & (hist > 0.08)) | (hist > 0.45); es_corte[0] = False
    cortes = []
    for i in np.where(es_corte)[0]:
        if cortes and i - cortes[-1]['cuadro'] <= 12: continue                   # una transición (p. ej. zoom a través del título) deja varios cuadros sin correlación: es UN corte
        a, b = max(0, i - 4), min(n, i + 5); previos = (resp[a:i] < 0.5).sum()
        tipo = 'transición + corte (movimiento fuerte antes)' if previos >= 2 else 'corte seco'
        cortes.append(dict(cuadro=int(i), seg=round(i / fps, 2), tipo=tipo, dif=float(dif[i])))
    # transiciones graduales (fundidos/barridos): diferencia alta sostenida sin un pico único
    lim = [0] + [c['cuadro'] for c in cortes] + [n]
    planos = [(lim[k + 1] - lim[k]) / fps for k in range(len(lim) - 1)]
    return cortes, planos


def camara(filas, cortes, fps):
    n = len(filas); vx = np.array([f['dx'] for f in filas]); vy = np.array([f['dy'] for f in filas]); vz = np.array([f['zoom'] for f in filas])
    for c in cortes:
        for k in range(c['cuadro'] - 1, c['cuadro'] + 2):
            if 0 <= k < n: vx[k] = vy[k] = vz[k] = 0
    vel = np.hypot(vx, vy)                                                         # px/cuadro (a 1080 de ancho)
    mov = (vel > 0.3) | (np.abs(vz) > 0.03)
    tramos, ini, hueco = [], None, 0
    for i, m in enumerate(mov):
        if m: ini = i if ini is None else ini; hueco = 0
        elif ini is not None:
            hueco += 1
            if hueco > 2: tramos.append((ini, i - hueco)); ini, hueco = None, 0
    if ini is not None: tramos.append((ini, n - 1))
    movs = []
    for a, b in tramos:
        if b - a < 4: continue
        z = vz[a:b + 1]; sx = vx[a:b + 1].sum(); sy = vy[a:b + 1].sum()
        tipo = 'acercamiento' if z.sum() > 0.5 and abs(z.sum()) * 10 > np.hypot(sx, sy) * 0.3 else 'alejamiento' if z.sum() < -0.5 else 'paneo/deriva'
        fuerza = np.maximum(vel[a:b + 1], np.abs(z) * 10); pico = int(np.argmax(fuerza))
        movs.append(dict(desde_s=round(a / fps, 2), hasta_s=round(b / fps, 2), seg=round((b - a + 1) / fps, 2), tipo=tipo, desplazamiento_px=[round(float(sx)), round(float(sy))], zoom_total_pct=round(float(z.sum()), 1),
                         vel_max_px_s=round(float(vel[a:b + 1].max() * fps)), pico_en_pct_del_tramo=round(100 * pico / max(1, b - a)), **ataque_liberacion(fuerza, pico, fps)))
    # tirón (jerk): tercera derivada de la posición acumulada, solo dentro de tramos de movimiento, con suavizado Savitzky–Golay
    jerks = []
    for a, b in tramos:
        if b - a < 12: continue
        for s in (vx[a:b + 1], vy[a:b + 1], vz[a:b + 1]):
            L = len(s) if len(s) % 2 == 1 else len(s) - 1; L = min(L, 9)
            if L < 5: continue
            pos = np.cumsum(s); jerks.append(np.abs(savgol_filter(pos, L, 3, deriv=3, delta=1 / fps)))
    jr = np.concatenate(jerks) if jerks else np.array([0.0])
    return dict(pct_cuadros_en_movimiento=round(100 * mov.mean(), 1), pct_cuadros_con_zoom=round(100 * (np.abs(vz) > 0.03).mean(), 1),
                zoom_neto_pct_por_s=round(float(vz[mov].sum() / max(1, mov.sum()) * fps), 2) if mov.any() else 0.0,
                velocidad_media_px_s=round(float(vel[mov].mean() * fps)) if mov.any() else 0, velocidad_mediana_px_s=round(float(np.median(vel[mov] * fps))) if mov.any() else 0, pct_movimiento_lento=round(100 * float((vel[mov] * fps < 100).mean()), 1) if mov.any() else 0.0, velocidad_p95_px_s=round(float(np.percentile(vel[mov] * fps, 95))) if mov.any() else 0,
                n_movimientos=len(movs), duracion_mediana_movimiento_s=round(float(np.median([m['seg'] for m in movs])), 2) if movs else 0.0,
                jerk_mediano_px_s3=round(float(np.median(jr))), jerk_p95_px_s3=round(float(np.percentile(jr, 95))),
                **ritmo_camara(movs, n, fps)), movs


def ataque_liberacion(fuerza, pico, fps):
    """Segundos que tarda la velocidad en subir del 10 % al pico (ataque) y en bajar del pico al 10 % (liberación), con la velocidad suavizada."""
    v = np.convolve(fuerza, np.ones(3) / 3, 'same'); pk = int(np.argmax(v)); u = 0.1 * v[pk]
    i = pk
    while i > 0 and v[i - 1] > u: i -= 1
    j = pk
    while j < len(v) - 1 and v[j + 1] > u: j += 1
    return dict(ataque_s=round((pk - i) / fps, 2), liberacion_s=round((j - pk) / fps, 2))


def ritmo_camara(movs, n, fps):
    """Gramática 'mover–retener–mover' y forma del movimiento, en números (docs/MEDICION.md)."""
    dur = n / fps; fuertes = [m for m in movs if m['vel_max_px_s'] >= 100]                       # los que se notan (no deriva)
    huecos = [movs[i + 1]['desde_s'] - movs[i]['hasta_s'] for i in range(len(movs) - 1)]
    ret = [h for h in huecos if h >= 0.5]
    lar = [m for m in fuertes if m['seg'] >= 0.5]
    return dict(movimientos_notorios=len(fuertes), movimientos_notorios_por_10s=round(len(fuertes) / dur * 10, 1),
                pico_notorio_mediano_px_s=round(float(np.median([m['vel_max_px_s'] for m in fuertes]))) if fuertes else 0,
                duracion_notorio_mediana_s=round(float(np.median([m['seg'] for m in fuertes])), 2) if fuertes else 0.0,
                retenciones=len(ret), retencion_mediana_s=round(float(np.median(ret)), 2) if ret else 0.0,
                ataque_mediano_s=round(float(np.median([m['ataque_s'] for m in lar])), 2) if lar else None,
                liberacion_mediana_s=round(float(np.median([m['liberacion_s'] for m in lar])), 2) if lar else None)


def enriquecer_cortes(cortes, filas, fps, ons, m):
    """Por cada corte: velocidad de cámara en los 0,3 s previos, duración del plano que sigue y distancia al golpe de sonido más cercano."""
    lim = [c['cuadro'] for c in cortes] + [len(filas)]; t_on = np.array([t for t, _ in ons])
    for k, c in enumerate(cortes):
        a = max(0, c['cuadro'] - 9); v = [np.hypot(f['dx'], f['dy']) * fps for f in filas[a:c['cuadro'] - 1]]
        c['vel_previa_px_s'] = round(float(np.median(v))) if v else 0
        c['plano_siguiente_s'] = round((lim[k + 1] - c['cuadro']) / fps, 2)
        c['golpe_cercano_s'] = round(float(np.min(np.abs(t_on - c['seg']))), 2) if len(t_on) else None
    if cortes and len(t_on):
        m['cortes']['pct_sobre_golpe_100ms'] = round(100 * float(np.mean([c['golpe_cercano_s'] <= 0.1 for c in cortes])), 1)
    if cortes:
        m['cortes']['pct_con_movimiento_previo'] = round(100 * float(np.mean([c['tipo'].startswith('transición') for c in cortes])), 1)


def audio(ruta, inf, transcripcion):
    if not inf['audio']: return None
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', ruta, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    g = lambda k: float(re.findall(rf'\n\s*{k}:\s+(-?[\d.]+)', r)[-1]) if re.findall(rf'\n\s*{k}:\s+(-?[\d.]+)', r) else None
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', ruta, '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, '<f4'); sr = 16000
    if len(x) < sr: return None
    hop = 160; n = (len(x) - 400) // hop
    rms = np.array([np.sqrt(np.mean(x[i * hop:i * hop + 400] ** 2)) for i in range(n)]); db = 20 * np.log10(rms + 1e-9)
    silencio = db < -50
    # silencios largos (> 0,25 s)
    runs, c = 0, 0
    for s in silencio:
        c = c + 1 if s else 0
        if c == 25: runs += 1
    # onsets por flujo espectral y golpes graves
    S = np.abs(np.array([np.fft.rfft(x[i * hop:i * hop + 512] * np.hanning(512)) for i in range(0, n - 3)])); fr = np.fft.rfftfreq(512, 1 / sr)
    flux = np.maximum(0, np.diff(np.log1p(S * 20), axis=0)).sum(1); thr = np.median(flux) + 4 * np.median(np.abs(flux - np.median(flux)))
    pk, _ = find_peaks(flux, height=thr, distance=8); graves = [p for p in pk if S[p + 1][fr < 200].sum() > 0.5 * S[p + 1].sum()]
    # ritmo de voz aproximado: núcleos silábicos = picos de la envolvente 300–3000 Hz
    sos = butter(4, [300, 3000], 'bandpass', fs=sr, output='sos'); env = np.abs(sosfilt(sos, x)); k = int(0.04 * sr); env = np.convolve(env, np.ones(k) / k, 'same')[::hop]
    activa = env > 0.06 * np.percentile(env, 95)                                   # umbral calibrado: reproduce el 79,5 % de voz de una pista conocida
    seg_activos = activa.sum() * hop / sr
    ons = [(round(float(p * hop / sr), 2), bool(p in set(graves))) for p in pk]
    out = dict(_onsets=ons, lufs_integrado=g('I'), rango_dinamico_lu=g('LRA'), pico_real_dbtp=g('Peak'), silencio_pct=round(100 * silencio.mean(), 1), silencios_largos=runs,
               onsets_por_s=round(len(pk) / (len(x) / sr), 2), golpes_graves=len(graves), voz_activa_pct=round(100 * activa.mean(), 1))
    if transcripcion:
        pal = len(re.findall(r"\w+", transcripcion)); out.update(palabras=pal, palabras_por_s_total=round(pal / (len(x) / sr), 2), palabras_por_s_hablando=round(pal / max(0.5, seg_activos), 2))
    return out


def color_fondo(px):
    q = (px // 16).astype(np.int32); clave = q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2]; vals, cuentas = np.unique(clave, return_counts=True)
    top = np.argsort(-cuentas)[:3]; res = []
    for t in top:
        sel = px[clave == vals[t]]; res.append(dict(hex=nombre_color(sel.mean(0)), pct=round(100 * cuentas[t] / len(px), 1)))
    return res


def _tabla_cortes(m, cortes):
    c = m['cortes']
    L = []
    if 'pct_con_movimiento_previo' in c: L.append(f"- {c['pct_con_movimiento_previo']} % de los cortes llegan después de un movimiento fuerte de cámara (transición); el resto son cortes secos.")
    if 'pct_sobre_golpe_100ms' in c: L.append(f"- {c['pct_sobre_golpe_100ms']} % de los cortes caen a ±0,1 s de un golpe de sonido.")
    if cortes:
        L += ['', '| # | seg | tipo | vel. cámara antes | plano que sigue | golpe más cercano |', '|---|---|---|---|---|---|']
        L += [f"| {i + 1} | {x['seg']} | {x['tipo']} | {x.get('vel_previa_px_s', '—')} px/s | {x.get('plano_siguiente_s', '—')} s | {x.get('golpe_cercano_s', '—')} s |" for i, x in enumerate(cortes)]
    return L


def informe(m, cortes, movs):
    c, cam, a, im = m['cortes'], m['camara'], m.get('audio'), m['imagen']
    L = [f"# Informe de medición: {m['archivo']}", '', f"{m['resolucion']} · {m['fps']} fps · {m['segundos']} s · {m['cuadros']} cuadros", '',
         '## Imagen', f"- Brillo medio {im['brillo_medio']} · contraste {im['contraste_medio']} · saturación {im['saturacion_media']}", '- Colores dominantes: ' + ', '.join(f"{x['hex']} ({x['pct']} %)" for x in im['colores_dominantes']), '',
         '## Cortes y planos', f"- {c['n']} cortes ({c['por_minuto']} por minuto); plano medio {c['plano_medio_s']} s, mediano {c['plano_mediano_s']} s, más largo {c['plano_max_s']} s.",
         '- Tipos: ' + (', '.join(f"{k}: {v}" for k, v in c['tipos'].items()) or 'ninguno'), '', *_tabla_cortes(m, cortes), '',
         '## Cámara', f"- Se mueve en el **{cam['pct_cuadros_en_movimiento']} %** de los cuadros ({cam['pct_cuadros_con_zoom']} % con zoom); zoom neto {cam['zoom_neto_pct_por_s']} % por segundo (+ acerca).",
         f"- Velocidad mediana {cam['velocidad_mediana_px_s']} px/s (media {cam['velocidad_media_px_s']}, p95 {cam['velocidad_p95_px_s']}); {cam['pct_movimiento_lento']} % del movimiento es lento (< 100 px/s: deriva casi imperceptible). A 1080 de ancho. {cam['n_movimientos']} movimientos, mediana {cam['duracion_mediana_movimiento_s']} s.",
         f"- **Tirón (jerk)**: mediano {cam['jerk_mediano_px_s3']} px/s³, p95 {cam['jerk_p95_px_s3']} px/s³ (menos = más suave).",
         f"- **Mover–retener–mover**: {cam['movimientos_notorios']} movimientos notorios (pico ≥ 100 px/s; {cam['movimientos_notorios_por_10s']} cada 10 s), pico mediano {cam['pico_notorio_mediano_px_s']} px/s, duran {cam['duracion_notorio_mediana_s']} s; {cam['retenciones']} retenciones ≥ 0,5 s (mediana {cam['retencion_mediana_s']} s); ataque (10 % → pico) mediano {cam['ataque_mediano_s']} s, liberación (pico → 10 %) {cam['liberacion_mediana_s']} s (parecidos = ease simétrico).", '', '| desde | hasta | seg | tipo | desplaz. px | zoom % | vel. máx px/s | ataque s | liberación s |', '|---|---|---|---|---|---|---|---|---|']
    L += [f"| {x['desde_s']} | {x['hasta_s']} | {x['seg']} | {x['tipo']} | {x['desplazamiento_px']} | {x['zoom_total_pct']} | {x['vel_max_px_s']} | {x['ataque_s']} | {x['liberacion_s']} |" for x in movs[:40]]
    if a:
        L += ['', '## Audio', f"- {a['lufs_integrado']} LUFS, rango {a['rango_dinamico_lu']} LU, pico {a['pico_real_dbtp']} dBTP", f"- Silencio {a['silencio_pct']} % ({a['silencios_largos']} silencios > 0,25 s), voz activa {a['voz_activa_pct']} %",
              f"- {a['onsets_por_s']} ataques por segundo; {a['golpes_graves']} golpes graves; voz activa = tiempo en que se oye hablar"]
        if 'palabras_por_s_total' in a: L.append(f"- Con transcripción: {a['palabras']} palabras → **{a['palabras_por_s_total']} palabras/s** en total, {a['palabras_por_s_hablando']} mientras se habla (sin transcripción no se puede medir: el ritmo de voz no se estima)")
    return '\n'.join(L) + '\n'


def autotest():
    """Verifica el método con movimientos sintéticos conocidos."""
    rng = np.random.default_rng(1); b = np.zeros((H, W), np.float32)
    for i in range(0, W, 18): b[:, i:i + 1] = 1
    for j in range(0, H, 18): b[j:j + 1, :] = 1
    b = cv2.GaussianBlur(b + 0.3 * rng.random((H, W)).astype(np.float32), (0, 0), 1.2)
    def mv(dx=0, dy=0, s=1.0):
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, s); M[0, 2] += dx; M[1, 2] += dy; return cv2.warpAffine(b, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    ok = True
    for dx, dy, s in [(3, 2, 1.0), (-2, 0, 1.0), (0, 0, 1.02), (0, 0, 0.98), (4, -3, 1.01)]:
        r = mover(b, mv(dx, dy, s), espectro_logpolar(b), espectro_logpolar(mv(dx, dy, s))); real = (dx * ESCALA, dy * ESCALA, (s - 1) * 100)
        bien = abs(r[0] - real[0]) < 0.5 * ESCALA and abs(r[1] - real[1]) < 0.5 * ESCALA and abs(r[2] - real[2]) < 0.5 + 0.2 * abs(real[2]); ok &= bien
        print(f"real dx={real[0]:+.1f} dy={real[1]:+.1f} zoom={real[2]:+.2f}%  →  medido dx={r[0]:+.1f} dy={r[1]:+.1f} zoom={r[2]:+.2f}%  {'OK' if bien else 'REVISAR'}")
    print('autotest', 'OK' if ok else 'FALLÓ'); return ok


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('video', nargs='?'); ap.add_argument('salida', nargs='?'); ap.add_argument('--transcripcion'); ap.add_argument('--hojas', action='store_true'); ap.add_argument('--autotest', action='store_true')
    a = ap.parse_args()
    if a.autotest: sys.exit(0 if autotest() else 1)
    if not a.video or not a.salida: ap.error('falta video y carpeta de salida')
    trans = open(a.transcripcion).read() if a.transcripcion else None
    inf, filas, px = analizar_video(a.video, a.salida, a.hojas); fps = inf['fps']
    cortes, planos = cortes_y_planos(filas, fps); cam, movs = camara(filas, cortes, fps)
    tipos = {}
    for c in cortes: tipos[c['tipo']] = tipos.get(c['tipo'], 0) + 1
    m = dict(archivo=os.path.basename(a.video), fps=fps, segundos=round(len(filas) / fps, 2), cuadros=len(filas), resolucion=f"{inf['ancho']}×{inf['alto']}",
             imagen=dict(brillo_medio=round(float(np.mean([f['brillo'] for f in filas])), 3), contraste_medio=round(float(np.mean([f['contraste'] for f in filas])), 3), saturacion_media=round(float(np.mean([f['sat'] for f in filas])), 3), colores_dominantes=color_fondo(px)),
             cortes=dict(n=len(cortes), por_minuto=round(len(cortes) / (len(filas) / fps / 60), 1), plano_medio_s=round(float(np.mean(planos)), 2), plano_mediano_s=round(float(np.median(planos)), 2), plano_max_s=round(float(np.max(planos)), 2), tipos=tipos),
             camara=cam, audio=audio(a.video, inf, trans))
    ons = (m['audio'] or {}).pop('_onsets', []) if m['audio'] else []
    enriquecer_cortes(cortes, filas, fps, ons, m)
    json.dump(dict(**m, cortes_detalle=cortes, movimientos=movs), open(os.path.join(a.salida, 'metricas.json'), 'w'), ensure_ascii=False, indent=1)
    open(os.path.join(a.salida, 'INFORME.md'), 'w').write(informe(m, cortes, movs))
    print(open(os.path.join(a.salida, 'INFORME.md')).read())


if __name__ == '__main__': main()

#!/usr/bin/env python3
"""LIBRO DE MOVIMIENTOS DE CÁMARA de un video de referencia: cada movimiento notorio con su nombre de cine, su receta numérica y 3 cuadros
(inicio · pico · fin). Sirve para APRENDER LA TÉCNICA DE CÁMARA de los reels virales sin importar el tema (Ayrton, 2026-11-16).
Parte de `medidas.csv` (lo escribe medir.py: desplazamiento dx, dy y zoom por cuadro, normalizados a 1080 px de ancho).

Uso:
  python engine/analisis/movimientos.py docs/4-referencias/externos/<slug> [--video ruta.mp4]   # un video → MOVIMIENTOS.md + movimientos.json + movimientos/*.jpg
  python engine/analisis/movimientos.py --catalogo                                              # junta todos los videos → docs/4-referencias/CATALOGO-MOVIMIENTOS.md
Convención: dx > 0 = la imagen se corre a la derecha = la cámara hace paneo a la IZQUIERDA; dy > 0 = la imagen baja = la cámara sube (grúa/tilt arriba);
zoom > 0 = la imagen crece = la cámara se acerca (dolly in / zoom in)."""
import csv, json, subprocess, sys
from pathlib import Path
import numpy as np

R = Path(__file__).resolve().parents[2]; EXT = R / 'docs/4-referencias/externos'; W = 1080

def segmentos(rows, fps, cortes):
    n = len(rows); vx = np.array([r['dx'] for r in rows]); vy = np.array([r['dy'] for r in rows]); vz = np.array([r['zoom'] for r in rows])
    for c in cortes:
        for k in range(int(c) - 1, int(c) + 2):
            if 0 <= k < n: vx[k] = vy[k] = vz[k] = 0
    vel = np.hypot(vx, vy); mov = (vel > 0.3) | (np.abs(vz) > 0.03)
    tr, ini, hueco = [], None, 0
    for i, m in enumerate(mov):
        if m: ini = i if ini is None else ini; hueco = 0
        elif ini is not None:
            hueco += 1
            if hueco > 2: tr.append((ini, i - hueco)); ini, hueco = None, 0
    if ini is not None: tr.append((ini, n - 1))
    out = []
    for a, b in tr:
        if b - a < 4: continue
        sx, sy, sz = vx[a:b + 1].sum(), vy[a:b + 1].sum(), vz[a:b + 1].sum(); fuerza = np.maximum(vel[a:b + 1], np.abs(vz[a:b + 1]) * 10)
        pico = int(np.argmax(fuerza)); v_pico = float(vel[a:b + 1].max() * fps); dur = (b - a + 1) / fps
        pan = float(np.hypot(sx, sy)) / W * 100; zoom = abs(float(sz))
        if pan < 3 and zoom < 3 and v_pico < 300: continue                     # deriva: no es un movimiento "de autor"
        if zoom > 0.5 * pan and zoom >= 3: tipo = 'dolly / zoom in (se acerca)' if sz > 0 else 'dolly / zoom out (se aleja)'
        else:
            h, v = abs(sx) >= abs(sy) * 1.5, abs(sy) >= abs(sx) * 1.5
            tipo = ('paneo / travelling a la izquierda' if sx > 0 else 'paneo / travelling a la derecha') if h else ('grúa / tilt hacia arriba' if sy > 0 else 'grúa / tilt hacia abajo') if v else 'diagonal'
            if dur <= 0.35 and v_pico > 2000: tipo = 'latigazo (whip pan)'
        p = 100 * pico / max(1, b - a)
        ease = 'arranca fuerte y frena largo (ease-out)' if p < 35 else 'arranca lento y termina fuerte (ease-in)' if p > 65 else 'simétrico (ease in-out)'
        out.append(dict(desde_s=round(a / fps, 2), hasta_s=round((b + 1) / fps, 2), dur_s=round(dur, 2), tipo=tipo, distancia_pct_ancho=round(pan, 1), zoom_pct=round(float(sz), 1),
                        pico_px_s=round(v_pico), pico_en_pct=round(p), curva=ease, cuadro_ini=a, cuadro_pico=a + pico, cuadro_fin=b))
    return out

def cuadro(video, seg, out):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{seg:.3f}', '-i', str(video), '-frames:v', '1', '-vf', 'scale=-2:480', str(out)], check=True)

def libro(carpeta, video):
    from PIL import Image
    carpeta = Path(carpeta); met = json.loads((carpeta / 'metricas.json').read_text()); fps = met['fps']
    rows = [{k: float(v) for k, v in r.items()} for r in csv.DictReader(open(carpeta / 'medidas.csv'))]
    esc = W / int(str(met['resolucion']).split('×')[0])   # medidas.csv ya viene normalizado a 1080; esc solo por si cambia
    movs = segmentos(rows, fps, [c['cuadro'] for c in met.get('cortes_detalle', [])])
    video = Path(video) if video else next((p for p in (R / 'assets/referencias').glob('*.mp4') if p.stem == carpeta.name), None)
    dst = carpeta / 'movimientos'; dst.mkdir(exist_ok=True)
    for i, m in enumerate(movs, 1):
        if video and video.exists():
            tiras = []
            for k, nom in ((m['cuadro_ini'], 'ini'), (m['cuadro_pico'], 'pico'), (m['cuadro_fin'], 'fin')):
                f = dst / f'_{nom}.jpg'; cuadro(video, k / fps, f); tiras.append(Image.open(f))
            ho = Image.new('RGB', (sum(t.width for t in tiras) + 8 * (len(tiras) - 1), tiras[0].height), 'black'); x = 0
            for t in tiras: ho.paste(t, (x, 0)); x += t.width + 8
            ho.save(dst / f'{i:02d}.jpg', quality=80)
            for nom in ('ini', 'pico', 'fin'): (dst / f'_{nom}.jpg').unlink(missing_ok=True)
    (carpeta / 'movimientos.json').write_text(json.dumps(movs, ensure_ascii=False, indent=1))
    L = [f'# Libro de movimientos: {carpeta.name}', f'{met["resolucion"]} · {fps:g} fps · {met["segundos"]} s · {len(movs)} movimientos notorios (deriva lenta excluida)', '',
         '| # | seg | movimiento | dur | distancia | zoom | pico | curva | cuadros |', '|---|---|---|---|---|---|---|---|---|']
    for i, m in enumerate(movs, 1):
        L.append(f"| {i} | {m['desde_s']}–{m['hasta_s']} | {m['tipo']} | {m['dur_s']} s | {m['distancia_pct_ancho']} % | {m['zoom_pct']:+} % | {m['pico_px_s']} px/s | {m['curva']} | `movimientos/{i:02d}.jpg` |")
    (carpeta / 'MOVIMIENTOS.md').write_text('\n'.join(L) + '\n'); print(f'{carpeta.name}: {len(movs)} movimientos → MOVIMIENTOS.md')

def catalogo():
    por, tot = {}, 0
    for j in sorted(EXT.glob('*/movimientos.json')):
        for m in json.loads(j.read_text()): por.setdefault(m['tipo'], []).append((j.parent.name, m)); tot += 1
    L = ['# Catálogo de movimientos de cámara (medido en las referencias)', 'Qué hace la cámara en los videos que le gustan a Ayrton, por tipo de movimiento y con su receta numérica; el tema no importa, importa la técnica. Se regenera con `python engine/analisis/movimientos.py --catalogo`. Vocabulario: `docs/2-estilo/GLOSARIO-EDICION.md`.', f'{tot} movimientos en {len(list(EXT.glob("*/movimientos.json")))} videos.', '']
    med = lambda a: float(np.median(a))
    L += ['| Movimiento | n | duración (s) | distancia (% ancho) | pico (px/s) | curva más común |', '|---|---|---|---|---|---|']
    for t, ms in sorted(por.items(), key=lambda kv: -len(kv[1])):
        cur = max({m['curva'] for _, m in ms}, key=lambda c: sum(1 for _, m in ms if m['curva'] == c))
        L.append(f"| {t} | {len(ms)} | {med([m['dur_s'] for _, m in ms]):.2f} | {med([m['distancia_pct_ancho'] for _, m in ms]):.0f} | {med([m['pico_px_s'] for _, m in ms]):.0f} | {cur} |")
    L += ['', '## Ejemplos para mirar (los 3 más rápidos de cada tipo)']
    for t, ms in sorted(por.items(), key=lambda kv: -len(kv[1])):
        L.append(f'### {t}')
        for slug, m in sorted(ms, key=lambda x: -x[1]['pico_px_s'])[:3]:
            L.append(f"- `{slug}` {m['desde_s']}–{m['hasta_s']} s · {m['dur_s']} s · {m['pico_px_s']} px/s · {m['curva']} → `externos/{slug}/movimientos/` ")
    (R / 'docs/4-referencias/CATALOGO-MOVIMIENTOS.md').write_text('\n'.join(L) + '\n'); print(f'catálogo: {tot} movimientos')

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--catalogo' in a: catalogo()
    elif a:
        libro(a[0], a[a.index('--video') + 1] if '--video' in a else None)
    else: print(__doc__)

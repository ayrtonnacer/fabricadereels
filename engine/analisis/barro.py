#!/usr/bin/env python3
"""Control de "barro" en la mezcla: reparte la energía de cada ventana de 0,5 s en 3 bandas y avisa si los graves-medios (100–300 Hz) se acumulan.
Uso:  python engine/analisis/barro.py final.mp4|audio.wav [--json salida.json]
Idea de onetake (references/sound.md): una mezcla con 41,6 % de energía en 100–300 Hz sonaba turbia; subir las notas una octava y acortar las colas bajó la ventana peor de 95 % a 6 %.
Alarmas (provisorias, no metas): una ventana con > 60 % en 100–300 Hz = barro; la mezcla entera > 35 % = revisar música/efectos graves. El oído decide.
Solo numpy + ffmpeg."""
import argparse, json, subprocess, numpy as np
SR = 22050
ap = argparse.ArgumentParser(); ap.add_argument('audio'); ap.add_argument('--json', default=''); a = ap.parse_args()
x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', a.audio, '-vn', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
N = int(SR * 0.5); BANDAS = {'grave <100': (20, 100), 'barro 100-300': (100, 300), 'medio y agudo >300': (300, SR / 2)}
f = np.fft.rfftfreq(N, 1 / SR); filas = []
for i in range(0, len(x) - N, N):
    P = np.abs(np.fft.rfft(x[i:i + N] * np.hanning(N))) ** 2; tot = P[(f >= 20)].sum() + 1e-12
    filas.append([float(P[(f >= lo) & (f < hi)].sum() / tot) for lo, hi in BANDAS.values()] + [float(np.sqrt((x[i:i + N] ** 2).mean()))])
F = np.array(filas); sil = F[:, 3] > 0.003                      # ignora ventanas en silencio
barro = F[sil, 1]; mal = [(round(i * 0.5, 1), round(float(F[i, 1]) * 100)) for i in range(len(F)) if sil[i] and F[i, 1] > 0.6]
res = dict(pct_barro_total=round(100 * float(barro.mean()), 1), pct_barro_ventana_max=round(100 * float(barro.max()), 1), ventanas_con_barro=mal)
print(f"{a.audio}: 100–300 Hz = {res['pct_barro_total']} % de la energía (peor ventana {res['pct_barro_ventana_max']} %)" + (f"; ventanas > 60 %: {mal}" if mal else '; sin ventanas con barro'))
if a.json: open(a.json, 'w').write(json.dumps(res, ensure_ascii=False, indent=1))

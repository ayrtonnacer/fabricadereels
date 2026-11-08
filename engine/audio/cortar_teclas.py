#!/usr/bin/env python3
"""Corta una grabación real de tipeo en teclas sueltas -> assets/sfx/propios/teclas/kNN.wav (48 kHz mono).
Uso: python engine/audio/cortar_teclas.py [assets/sfx/propios/typing-keyboard.mp3]
Fuente actual: typing-keyboard.mp3 de ayrtonnacer/code-reel-studio (public/sounds)."""
import subprocess, sys, wave
from pathlib import Path
import numpy as np
SR = 48000
root = Path(__file__).resolve().parents[2] / 'assets/sfx/propios'
src = Path(sys.argv[1]) if len(sys.argv) > 1 else root / 'typing-keyboard.mp3'
x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(src), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout, '<f4').astype(float)
h = int(.002 * SR); e = np.array([np.sqrt(np.mean(x[i:i + h] ** 2)) for i in range(0, len(x) - h, h)])
thr = max(np.percentile(e, 60) * 3, e.max() * .12); on, last = [], -1e9
for i in range(1, len(e) - 1):
    if e[i] > thr and e[i] >= e[i - 1] and e[i] >= e[i + 1] and (i - last) * .002 > .06: on.append(i); last = i
out = root / 'teclas'; out.mkdir(exist_ok=True)
for f in out.glob('k*.wav'): f.unlink()
n = 0
for j, i in enumerate(on):
    a = max(0, i * h - int(.004 * SR)); nxt = on[j + 1] * h - int(.004 * SR) if j + 1 < len(on) else len(x)
    b = min(nxt, a + int(.11 * SR))
    if b - a < int(.04 * SR): continue
    s = x[a:b].copy(); k = int(.012 * SR); s[-k:] *= np.linspace(1, 0, k); s /= np.max(np.abs(s)) + 1e-9
    with wave.open(str(out / f'k{n:02d}.wav'), 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((s * .9 * 32767).astype('<i2').tobytes())
    n += 1
print(n, 'teclas en', out)

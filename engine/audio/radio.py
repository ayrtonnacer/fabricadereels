#!/usr/bin/env python3
"""Efecto de radio (militar / walkie-talkie) para la voz. Uso desde voz.py (video.json: voz.efecto = "radio", voz.radio_fuerza = 0..1)
o suelto:  python engine/audio/radio.py entrada.wav salida.wav [fuerza]
Cadena: banda telefónica 380-3100 Hz -> saturación suave -> estática de fondo mientras habla -> "squelch" (golpe de ruido al soltar el botón)
+ clic de apertura. fuerza 0.3 = radio limpia, 0.6 = walkie, 0.9 = radio rota."""
import sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, resample_poly
SR = 48000
_rng = np.random.default_rng(11)

def _bp(x, lo, hi, order=4):
    return sosfilt(butter(order, [lo, hi], btype='band', fs=SR, output='sos'), x)

def radio(x, fuerza=0.6, squelch=True):
    """x: voz mono float 48 kHz. Devuelve la voz con efecto + cola de squelch (más larga que x en ~0.12 s)."""
    f = float(np.clip(fuerza, 0, 1))
    lo, hi = 380 + 120 * f, 3300 - 700 * f                       # más fuerza = banda más angosta
    y = _bp(x, lo, hi)
    drive = 1.2 + 3.0 * f; y = np.tanh(y * drive) / np.tanh(drive)  # saturación (aplasta picos como un micrófono de radio)
    if f > 0.5:                                                      # radio "rota": recorte de resolución leve
        q = 2 ** (9 - 4 * (f - 0.5) / 0.5 * 0.5); y = np.round(y * q) / q
    y = y / (np.max(np.abs(y)) + 1e-9) * 0.9 * (np.max(np.abs(x)) if np.max(np.abs(x)) > 0 else 1)
    # estática: ruido en banda, solo mientras hay voz (puerta suave), nivel crece con fuerza
    env = np.convolve(np.abs(y), np.ones(int(.03 * SR)) / int(.03 * SR), mode='same'); gate = np.clip(env / (env.max() + 1e-9) * 6, 0, 1)
    hiss = _bp(_rng.standard_normal(len(y)), 600, 4500) ; hiss /= np.max(np.abs(hiss))
    y = y + hiss * gate * (0.012 + 0.07 * f) * (np.max(np.abs(y)) + 1e-9)
    tail = int(.14 * SR); out = np.concatenate([y, np.zeros(tail)])
    if squelch:
        n = int(.075 * SR); t = np.arange(n) / SR
        burst = _bp(_rng.standard_normal(n), 900, 3600) * np.exp(-t / .022) * (0.35 + 0.35 * f)
        out[len(y) + int(.02 * SR): len(y) + int(.02 * SR) + n] += burst * (np.max(np.abs(y)) + 1e-9)
        k = int(.012 * SR); click = _bp(_rng.standard_normal(k), 700, 3000) * np.exp(-np.arange(k) / (SR * .003)) * 0.5
        out[:k] += click * (np.max(np.abs(y)) + 1e-9)
    return out

def _read(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(float) / 32768; sr = w.getframerate()
    return resample_poly(x, SR // 50, sr // 50) if sr != SR else x
def _write(p, x):
    with wave.open(p, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]; f = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
    _write(dst, radio(_read(src), f))

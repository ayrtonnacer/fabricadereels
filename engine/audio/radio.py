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


# ---------- Adjutant (Terran Advisor, StarCraft): voz brillante y "digital" con cola de sala ----------
# Medido del audio de referencia (engine/audio/adjutant_perfil.json): comparada con Daniela tiene +5 dB a 1,6–3,2 kHz, +7 a 3,2–6,4 y +8 a 6,4–12 kHz,
# menos graves bajos, y una cola de ≈ 340 ms (mediana) tras cada frase. Se hace en 3 pasos: EQ que lleva el espectro de la voz al de la referencia,
# excitación de agudos (armónicos por saturación) y reverb corta de sala. fuerza 0 = voz limpia, 1 = el espectro completo de la referencia.
import json as _json
from pathlib import Path as _P
from scipy.signal import fftconvolve as _conv

def _tercios(x):
    from scipy.signal import welch
    fr = int(.02 * SR); e = np.array([np.sqrt(np.mean(x[i:i + fr] ** 2)) for i in range(0, len(x) - fr, fr)])
    act = e > 0.3 * np.median(e[e > 0.01]); m = np.repeat(act, fr)[:len(x)]; v = x[:len(m)][m]
    f, P = welch(v, SR, nperseg=4096); P = P / P.sum(); return f, P

def adjutant(x, fuerza=0.7, reverb=0.22):
    """x: voz mono float 48 kHz. Devuelve la voz con timbre de Adjutant + cola de sala (≈ 0,5 s más larga)."""
    f_ = float(np.clip(fuerza, 0, 1)); ref = _json.loads((_P(__file__).parent / 'adjutant_perfil.json').read_text())
    cen = np.array(ref['centros_hz'], float); objetivo = np.array(ref['db'], float)
    f, P = _tercios(x)
    actual = np.array([10 * np.log10(P[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].sum() + 1e-12) for c in cen])
    sm = lambda a: np.convolve(np.pad(a, 3, mode='edge'), np.ones(7) / 7, mode='valid')   # ≈ 2 octavas: sin copiar los armónicos de OTRA voz
    g = np.clip((sm(objetivo) - sm(actual)) * f_, -9, 9)                      # dB de corrección por tercio (limitada para no romper la voz)
    g -= np.median(g)                                                  # que el nivel general no cambie, solo la forma
    N = len(x); X = np.fft.rfft(x); fr_ = np.fft.rfftfreq(N, 1 / SR)
    gain = 10 ** (np.interp(np.log2(np.maximum(fr_, 1)), np.log2(cen), g) / 20); gain[fr_ < 80] = 0   # sin graves por debajo de 80 Hz
    y = np.fft.irfft(X * gain, N)
    # excitación de agudos: armónicos de lo que hay sobre 2,5 kHz (da el brillo "digital" que la EQ sola no inventa)
    hi = sosfilt(butter(4, 2500, btype='high', fs=SR, output='sos'), y); y = y + 0.35 * f_ * np.tanh(hi * 4) / 4
    y = sosfilt(butter(4, 12500, btype='low', fs=SR, output='sos'), y)     # la referencia corta cerca de 12 kHz
    # reverb de sala: respuesta de ruido que decae (RT60 ≈ 0,55 s), 12 ms de pre-retardo, sin graves ni agudos extremos
    rng = np.random.default_rng(5); n = int(.7 * SR); t = np.arange(n) / SR
    ir = _bp(rng.standard_normal(n), 300, 7000) * np.exp(-6.9 * t / .55); ir[:int(.012 * SR)] = 0
    wet = _conv(y, ir)[:N + n]; wet *= (np.max(np.abs(y)) / (np.max(np.abs(wet)) + 1e-9)) * reverb * f_ * 2.2
    out = np.concatenate([y, np.zeros(n)]); out[:len(wet)] += wet
    return out / (np.max(np.abs(out)) + 1e-9) * (np.max(np.abs(x)) if np.max(np.abs(x)) > 0 else 1)

def _read(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(float) / 32768; sr = w.getframerate()
    return resample_poly(x, SR // 50, sr // 50) if sr != SR else x
def _write(p, x):
    with wave.open(p, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]; f = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
    modo = sys.argv[4] if len(sys.argv) > 4 else 'radio'   # radio | adjutant
    _write(dst, (adjutant if modo == 'adjutant' else radio)(_read(src), f))

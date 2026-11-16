#!/usr/bin/env python3
"""Catálogo MEDIDO del banco de efectos (assets/sfx/**): para cada archivo, su rol (qué significa en el video) y sus números
(duración, ataque, brillo = centroide espectral, cuánto pisa la voz = energía en 300–3000 Hz, cola). Sale engine/audio/catalogo_sfx.json,
que usa sfxlib.elegir() para VARIAR los sonidos entre reels y dentro de un mismo reel sin repetir.
Uso: python engine/audio/catalogo_sfx.py          (correr después de engine/audio/bajar_sfx.sh)
Claude no escucha: estos números describen el sonido; la elección final de oído es de Ayrton (engine/audio/muestras_sfx.py)."""
import json, re, subprocess
from pathlib import Path
import numpy as np

RAIZ = Path(__file__).resolve().parents[2]; SFX = RAIZ / 'assets' / 'sfx'; SR = 48000
ROLES = [   # (rol, carpeta, patrón en el nombre) — el primer patrón que coincide gana
    ('curva', 'whoosh', r'.'),
    ('dato', 'ui', r'^(click|tick|select|mouseclick)'), ('dato', 'click', r'click'),
    ('aparece', 'ui', r'^(pluck|drop|open|maximize|bong|toggle|rollover)'),
    ('se-va', 'ui', r'^(close|minimize|back)'),
    ('resultado', 'ui', r'^(confirmation|glass)'), ('resultado', 'bell', r'.'),
    ('error', 'ui', r'^error'),
    ('golpe', 'hit', r'(metal_hit|_hit_|wood_hit|glass_hit)'), ('golpe', 'scifi', r'^impactMetal'),
    ('digital', 'scifi', r'^computerNoise'), ('digital', 'ui', r'^(glitch|scratch|scroll)'),
    ('ambiente', 'scifi', r'^(spaceEngineLow|engineCircular|forceField)'),
]

def leer(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, '<f4').astype(float)

def medir(x):
    if len(x) < 64 or np.max(np.abs(x)) < 1e-5: return None
    x = x / np.max(np.abs(x)); env = np.convolve(np.abs(x), np.ones(240) / 240, 'same'); pk = int(np.argmax(env))
    dB = 20 * np.log10(env / env[pk] + 1e-9); fin = pk + int(np.argmax(dB[pk:] < -30)) if np.any(dB[pk:] < -30) else len(x)
    X = np.abs(np.fft.rfft(x)) ** 2; f = np.fft.rfftfreq(len(x), 1 / SR); E = X.sum() + 1e-12
    banda = lambda a, b: float(X[(f >= a) & (f < b)].sum() / E)
    return {'dur': round(len(x) / SR, 3), 'ataque': round(pk / SR, 3), 'cola': round((fin - pk) / SR, 3),
            'brillo_hz': int((f * X).sum() / E), 'graves': round(banda(20, 300), 3), 'voz': round(banda(300, 3000), 3), 'agudos': round(banda(3000, 16000), 3)}

def main():
    out = []
    for f in sorted(SFX.rglob('*')):
        if f.suffix.lower() not in ('.wav', '.ogg', '.mp3', '.flac') or f.name.startswith('._') or 'preview' in f.name: continue
        rel = f.relative_to(SFX); cat = rel.parts[0]
        rol = next((r for r, c, p in ROLES if c == cat and re.search(p, f.name, re.I)), None)
        if cat == 'propios': rol = 'propio'
        if rol is None: continue
        m = medir(leer(f))
        if m: out.append({'archivo': str(rel), 'rol': rol, **m})
    dst = Path(__file__).with_name('catalogo_sfx.json'); dst.write_text(json.dumps(out, ensure_ascii=False, indent=0))
    cuenta = {}; [cuenta.__setitem__(o['rol'], cuenta.get(o['rol'], 0) + 1) for o in out]
    print(f'{len(out)} sonidos → {dst.name}:', ', '.join(f'{k} {v}' for k, v in sorted(cuenta.items())))

if __name__ == '__main__': main()

#!/usr/bin/env python3
"""Arma un mp3 para que Ayrton ELIJA SONIDOS DE OÍDO: Daniela anuncia "curva 1", suena la opción, y así con cada rol.
Claude no escucha; mide (catalogo_sfx.json). La elección de oído de Ayrton se anota en docs/2-estilo/AUDIO.md y se usa con elegir(..., filtro=archivo).
Uso: python engine/audio/muestras_sfx.py [rol ...]      (por defecto: curva golpe resultado aparece dato digital)
Salida: docs/4-referencias/material/sfx-muestras/<rol>.mp3 + <rol>.txt (número → archivo)."""
import io, json, sys, wave, subprocess
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent)); import sfxlib
from scipy.signal import resample_poly

RAIZ = Path(__file__).resolve().parents[2]; SR = 48000
DST = RAIZ / 'docs/4-referencias/material/sfx-muestras'; DST.mkdir(parents=True, exist_ok=True)
roles = sys.argv[1:] or ['curva', 'golpe', 'resultado', 'aparece', 'dato', 'digital']
modelo = RAIZ / 'assets/voces/es_AR-daniela-high.onnx'
from piper import PiperVoice, SynthesisConfig
voz = PiperVoice.load(str(modelo)); cfg = SynthesisConfig(length_scale=1.0)
def decir(txt):
    b = io.BytesIO()
    with wave.open(b, 'wb') as w: voz.synthesize_wav(txt, w, syn_config=cfg)
    b.seek(0)
    with wave.open(b) as r: sr = r.getframerate(); x = np.frombuffer(r.readframes(r.getnframes()), '<i2').astype(float) / 32768
    return resample_poly(x, SR, sr) * 0.8
NOMBRE = {'curva': 'transición', 'golpe': 'golpe', 'resultado': 'resultado', 'aparece': 'aparece', 'dato': 'dato', 'digital': 'digital', 'se-va': 'se va', 'error': 'error'}
cat = json.loads((Path(__file__).with_name('catalogo_sfx.json')).read_text())
for rol in roles:
    ops = [o for o in cat if o['rol'] == rol and o['dur'] <= 2.5][:16]
    partes, lista = [], []
    for i, o in enumerate(ops, 1):
        x = sfxlib._leer(sfxlib.SFX_DIR / o['archivo'], 0.7)
        partes += [decir(f'{NOMBRE.get(rol, rol)} {i}'), np.zeros(int(SR * 0.25)), x, np.zeros(int(SR * 0.7))]
        lista.append(f"{i}\t{o['archivo']}\t{o['dur']} s\tbrillo {o['brillo_hz']} Hz\tpisa la voz {int(o['voz'] * 100)} %")
    y = np.concatenate(partes); y = y / (np.max(np.abs(y)) + 1e-9) * 0.9
    wav = DST / f'{rol}.wav'
    with wave.open(str(wav), 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-b:a', '128k', str(DST / f'{rol}.mp3')], check=True); wav.unlink()
    (DST / f'{rol}.txt').write_text('\n'.join(lista) + '\n'); print(f'{rol}: {len(ops)} opciones → {DST / (rol + ".mp3")}')

#!/usr/bin/env python3
"""Mezcla final: voz + efectos + música -> <video>/audio/mezcla.wav, y si existe out/mudo.mp4 lo une en <video>/final.mp4.
Uso: python engine/audio/mezcla.py videos/<video> [--musica ruta.mp3] [--desde seg] [--db -8] [--sfx 1.25]
Reglas (docs/AUDIO.md): voz a -14 LUFS (referencia); efectos y música bajan solos cuando habla la voz (sidechain);
música con fade in 1.5 s y fade out 3.5 s; arrancar la música en un tramo SIN silencios (ver docs/AUDIO.md)."""
import argparse, json, subprocess
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--musica'); ap.add_argument('--desde', type=float)
ap.add_argument('--db', type=float); ap.add_argument('--sfx', type=float); a = ap.parse_args()
V = Path(a.video); cfg = json.loads((V / 'video.json').read_text()); au = cfg.get('audio', {})
dur = sum(s['d'] for s in cfg['scenes'])
music = a.musica or au.get('musica', ''); ofs = a.desde if a.desde is not None else au.get('musica_desde', 0)
mdb = a.db if a.db is not None else au.get('musica_db', -8); sg = a.sfx if a.sfx is not None else au.get('sfx_gain', 1.25)
LUFS = au.get('loudness', -14); A = V / 'audio'
def ff(*x): subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *x], check=True)
# Capas: voz, efectos y música son opcionales (un video sin voz, o sin música en el repo, se mezcla igual con lo que haya).
hay_voz, hay_sfx, hay_mus = (A / 'voz.wav').exists(), (A / 'sfx.wav').exists(), bool(music) and Path(music).exists()
if not (hay_voz or hay_sfx or hay_mus): raise SystemExit('No hay ninguna capa de audio (voz.wav, sfx.wav o música).')
for n, ok in (('voz (audio/voz.wav)', hay_voz), ('efectos (audio/sfx.wav)', hay_sfx), (f'música ({music})', hay_mus)):
    if not ok: print(f'· sin {n}: se mezcla sin esa capa')
# 1) cadena de voz: pasa-altos, compresión suave, normalización
if hay_voz: ff('-i', A / 'voz.wav', '-af', f'aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I={LUFS}:TP=-1.5:LRA=9,aresample=48000', A / 'voz_norm.wav')
# música: completa (fade in 1.5 / out 3.5) o, en videos en bucle, solo en la ventana musica_ventana=[ini,fin] (silencio en el empalme)
if au.get('musica_ventana'):
    mi, mf = au['musica_ventana']; ml = mf - mi
    MCHAIN = f"atrim={ofs}:{ofs + ml},asetpts=PTS-STARTPTS,volume={mdb}dB,afade=t=in:st=0:d=1.2,afade=t=out:st={ml - 1.4}:d=1.4,adelay={int(mi*1000)}|{int(mi*1000)},apad=whole_dur={dur}"
else:
    MCHAIN = f"atrim={ofs}:{ofs + dur},asetpts=PTS-STARTPTS,volume={mdb}dB,afade=t=in:st=0:d=1.5,afade=t=out:st={max(0, dur - 3.5)}:d=3.5"
# 2) mezcla con ducking (efectos y música bajan cuando habla la voz)
F = 'aformat=sample_rates=48000:channel_layouts=stereo'
ins, g, capas, k = [], [], [], 0
if hay_voz: ins += ['-i', A / 'voz_norm.wav']; g.append(f'[{k}]{F},asplit=3[v][vk1][vk2]'); capas.append('[v]'); k += 1
if hay_sfx:
    ins += ['-i', A / 'sfx.wav']; g.append(f'[{k}]{F},volume={sg},apad=whole_dur={dur}[s]'); k += 1
    if hay_voz: g.append('[s][vk1]sidechaincompress=threshold=0.05:ratio=2.5:attack=5:release=200[sd]'); capas.append('[sd]')
    else: capas.append('[s]')
if hay_mus:
    ins += ['-i', music]; g.append(f'[{k}]{F},{MCHAIN}[m]'); k += 1
    if hay_voz: g.append('[m][vk2]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md]'); capas.append('[md]')
    else: capas.append('[m]')
if hay_voz and not hay_sfx: g.append('[vk1]anullsink')
if hay_voz and not hay_mus: g.append('[vk2]anullsink')
g.append(f"{''.join(capas)}amix=inputs={len(capas)}:normalize=0:duration=longest,atrim=0:{dur},loudnorm=I={LUFS}:TP=-1.5:LRA=11,aresample=48000[o]")
ff(*ins, '-filter_complex', ';'.join(g), '-map', '[o]', '-ac', '2', '-c:a', 'pcm_s16le', A / 'mezcla.wav')
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', A / 'mezcla.wav', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print('\n'.join(l.strip() for l in r.splitlines() if l.strip().startswith(('I:','Peak:'))))
mudo = V / 'out/mudo.mp4'
if mudo.exists():
    ff('-i', mudo, '-i', A / 'mezcla.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', V / 'final.mp4'); print('->', V / 'final.mp4')
else: print('(falta out/mudo.mp4: renderizar con engine/render.mjs … scenes y … join)')

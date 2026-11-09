#!/usr/bin/env python3
"""Mezcla final: voz + efectos + música -> <video>/audio/mezcla.wav, y si existe out/mudo.mp4 lo une en <video>/final.mp4.
Uso: python engine/audio/mezcla.py videos/<video> [--musica ruta.mp3] [--desde seg] [--db -8] [--sfx 1.25]
Reglas (docs/AUDIO.md): voz a -14 LUFS (referencia); efectos y música bajan solos cuando habla la voz (sidechain);
música con fade in 1.5 s y fade out 3.5 s; arrancar la música en un tramo SIN silencios (ver docs/AUDIO.md)."""
import argparse, json, subprocess
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--musica'); ap.add_argument('--desde', type=float)
ap.add_argument('--db', type=float); ap.add_argument('--sfx', type=float); a = ap.parse_args()
V = Path(a.video); cfg = json.loads((V / 'video.json').read_text()); au = cfg['audio']
dur = sum(s['d'] for s in cfg['scenes'])
music = a.musica or au['musica']; ofs = a.desde if a.desde is not None else au.get('musica_desde', 0)
mdb = a.db if a.db is not None else au.get('musica_db', -8); sg = a.sfx if a.sfx is not None else au.get('sfx_gain', 1.25)
LUFS = au.get('loudness', -14); A = V / 'audio'
def ff(*x): subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *x], check=True)
def lufs(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float([l for l in r.splitlines() if l.strip().startswith('I:')][-1].split()[1])
# 1) cadena de voz LIMPIA (Ayrton, 2026-11-09: "quiero un sonido limpio"): pasa-altos suave + compresión leve y una ganancia lineal.
#    Sin loudnorm dinámico (comprimía y "bombeaba": sonaba a radio). La voz queda en -16 LUFS; el nivel final se ajusta abajo con ganancia lineal.
ff('-i', A / 'voz.wav', '-af', 'aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=70,acompressor=threshold=-24dB:ratio=2:attack=10:release=120', A / 'voz_pre.wav')
ff('-i', A / 'voz_pre.wav', '-af', f'volume={-16 - lufs(str(A / "voz_pre.wav"))}dB,aresample=48000', A / 'voz_norm.wav')
# música: completa (fade in 1.5 / out 3.5) o, en videos en bucle, solo en la ventana musica_ventana=[ini,fin] (silencio en el empalme)
if au.get('musica_ventana'):
    mi, mf = au['musica_ventana']; ml = mf - mi
    MCHAIN = f"atrim={ofs}:{ofs + ml},asetpts=PTS-STARTPTS,volume={mdb}dB,afade=t=in:st=0:d=1.2,afade=t=out:st={ml - 1.4}:d=1.4,adelay={int(mi*1000)}|{int(mi*1000)},apad=whole_dur={dur}"
else:
    MCHAIN = f"atrim={ofs}:{ofs + dur},asetpts=PTS-STARTPTS,volume={mdb}dB,afade=t=in:st=0:d=1.5,afade=t=out:st={dur - 3.5}:d=3.5"
# 2) mezcla con ducking
g = f"""[0]aformat=sample_rates=48000:channel_layouts=stereo,asplit=3[v][vk1][vk2];
[1]aformat=sample_rates=48000:channel_layouts=stereo,volume={sg}[s];
[2]aformat=sample_rates=48000:channel_layouts=stereo,{MCHAIN}[m];
[s][vk1]sidechaincompress=threshold=0.05:ratio=2.5:attack=5:release=200[sd];
[m][vk2]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];
[v][sd][md]amix=inputs=3:normalize=0:duration=first,aresample=48000[o]"""
ff('-i', A / 'voz_norm.wav', '-i', A / 'sfx.wav', '-i', music, '-filter_complex', g, '-map', '[o]', '-ac', '2', '-c:a', 'pcm_s16le', A / 'premezcla.wav')
# 3) nivel final: ganancia lineal a -14 LUFS y limitador de picos (-1,5 dBTP); sin compresión dinámica
ff('-i', A / 'premezcla.wav', '-af', f'volume={LUFS - lufs(str(A / "premezcla.wav"))}dB,alimiter=limit=0.84:attack=3:release=60:level=0,aresample=48000', '-ac', '2', '-c:a', 'pcm_s16le', A / 'mezcla.wav')
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', A / 'mezcla.wav', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print('\n'.join(l.strip() for l in r.splitlines() if l.strip().startswith(('I:','Peak:'))))
mudo = V / 'out/mudo.mp4'
if mudo.exists():
    ff('-i', mudo, '-i', A / 'mezcla.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', V / 'final.mp4'); print('->', V / 'final.mp4')
else: print('(falta out/mudo.mp4: en la carpeta del video, npx hyperframes render -o out/mudo.mp4)')

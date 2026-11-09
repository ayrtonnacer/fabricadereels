#!/usr/bin/env python3
"""Genera la voz en off de un video desde video.json (voz.lineas) con Piper.
Uso:  python engine/audio/voz.py videos/<video> [--modelo assets/voces/es_AR-daniela-high.onnx]
Salida: <video>/audio/voz/<id>.wav y <video>/audio/voz.wav (líneas ubicadas en su tiempo, 48 kHz mono).
Chequea: palabras prohibidas, líneas que se pasan de su escena y líneas que se pisan entre sí."""
import argparse, json, re, sys, wave
from pathlib import Path
import numpy as np
from scipy.signal import resample_poly
sys.path.insert(0, str(Path(__file__).parent)); import radio as _radio

HERE = Path(__file__).parent
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--modelo', default=str(HERE.parent.parent / 'assets/voces/es_AR-daniela-high.onnx'))
a = ap.parse_args()
V = Path(a.video); cfg = json.loads((V / 'video.json').read_text())
dic = json.loads((HERE / 'pronunciacion.json').read_text())
_mp = Path(a.modelo)
if not _mp.exists():  # el .onnx va partido en el repo (GitHub limita a 100 MB)
    _partes = sorted(_mp.parent.glob(_mp.name + '.parte*'))
    if _partes:
        with open(_mp, 'wb') as _o:
            for _p in _partes: _o.write(_p.read_bytes())
if not _mp.exists(): sys.exit(f'Falta el modelo de voz: {a.modelo}\nVer assets/voces/LEEME.md')
from piper import PiperVoice, SynthesisConfig
try: voice = PiperVoice.load(a.modelo, include_alignments=True)   # tiempos por fonema (requiere el paquete onnx)
except Exception: voice = PiperVoice.load(a.modelo)
vc = cfg['voz']
syn = SynthesisConfig(length_scale=vc.get('length_scale', .92), noise_scale=vc.get('noise_scale', .6), noise_w_scale=vc.get('noise_w_scale', .7))

def respell(t):
    for r in dic['reemplazos']: t = re.sub(rf"(?<!\w){re.escape(r['de'])}(?!\w)", r['a'], t, flags=re.I)
    return t
PUNT = set('.,;:!?¿¡…—-–"\'()«»')
def palabras(texto, als, sr):
    """Tiempos (s, relativos al inicio de la línea) de cada palabra del TEXTO original a partir de los fonemas de Piper.
    Piper da la duración exacta de cada fonema; los ' ' separan palabras y la puntuación es una pausa que se pega a la palabra anterior."""
    ws, cur, t = [], None, 0.0
    for al in als:
        d = float(al.num_samples) / sr; ph = al.phoneme
        if ph in ('^', '$', ' '):
            if ph != '^' and cur: ws.append(cur); cur = None
            t += d; continue
        if ph in PUNT:
            if cur: cur['p'] += d
            t += d; continue
        if cur is None: cur = {'t0': t, 't1': t + d, 'p': 0.0}
        else: cur['t1'] = t + d
        t += d
    if cur: ws.append(cur)
    toks = texto.split(); ks = [max(1, len(respell(x).split())) for x in toks]
    out = []
    if sum(ks) == len(ws):
        i = 0
        for tk, k in zip(toks, ks): out.append({'w': tk, 't0': ws[i]['t0'], 't1': ws[i + k - 1]['t1']}); i += k
    else:   # el diccionario o los números cambian la cantidad de palabras: se reparte por largo (y se avisa)
        print(f"  ~ aviso: {len(toks)} palabras de texto vs {len(ws)} de voz en «{texto[:40]}…»: reparto proporcional")
        t0, t1 = ws[0]['t0'], ws[-1]['t1']; tot = sum(len(x) for x in toks); c = 0
        for tk in toks: out.append({'w': tk, 't0': t0 + (t1 - t0) * c / tot, 't1': t0 + (t1 - t0) * (c + len(tk)) / tot}); c += len(tk)
    return out
PAL = []
scenes, acc = {}, 0.0
for s in cfg['scenes']: scenes[s['id']] = (acc, acc + s['d']); acc += s['d']
total = acc; (V / 'audio/voz').mkdir(parents=True, exist_ok=True)
SR = 48000; out = np.zeros(int(total * SR) + SR); problemas = 0; prev_end = 0; prev_id = None
print(f"{'id':4} {'t':>6} {'dur':>5} {'fin':>6}  escena(fin)  texto")
for l in sorted(vc['lineas'], key=lambda x: x['t']):
    for p in dic['prohibidas']:
        if re.search(rf"(?<!\w){re.escape(p['palabra'])}(?!\w)", l['texto'], re.I):
            print(f"  !! {l['id']}: usa '{p['palabra']}' → mejor '{p['usar']}' ({p['motivo']})"); problemas += 1
    wav = V / f"audio/voz/{l['id']}.wav"
    with wave.open(str(wav), 'wb') as w: als = voice.synthesize_wav(respell(l['texto']), w, syn_config=syn, include_alignments=True)
    with wave.open(str(wav)) as w: x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768; sr = w.getframerate()
    x = resample_poly(x, SR // 50, sr // 50) if sr != SR else x
    if vc.get('efecto') == 'radio': x = _radio.radio(x, vc.get('radio_fuerza', 0.6))   # incluye squelch final
    if l.get('al_final'):   # video en bucle: sin silencio final y termina justo en el último cuadro
        nz = np.where(np.abs(x) > 0.012)[0]; x = x[:nz[-1] + int(0.03 * SR)] if len(nz) else x
        l = dict(l, t=total - len(x) / SR)
    dur = len(x) / SR; fin = l['t'] + dur; s0, s1 = scenes[l['escena']]
    if als: PAL += [{'l': l['id'], 'w': q['w'], 't0': round(l['t'] + q['t0'], 3), 't1': round(l['t'] + q['t1'], 3)} for q in palabras(l['texto'], als, sr)]
    flag = ''
    if l['t'] < s0 - 0.05: flag += ' EMPIEZA ANTES DE SU ESCENA'
    if fin > s1 - 0.1: flag += ' SE PASA DE SU ESCENA'
    if l['t'] < prev_end + 0.15 and prev_id: flag += f' PISA A {prev_id}'
    if flag: problemas += 1
    print(f"{l['id']:4} {l['t']:6.2f} {dur:5.2f} {fin:6.2f}  {l['escena']}({s1:5.1f}){flag}  {l['texto'][:60]}")
    i = int(l['t'] * SR); out[i:i + len(x)] += x[:len(out) - i]; prev_end, prev_id = fin, l['id']
out = out[:int(total * SR)]
if PAL: (V / 'audio/palabras.json').write_text(json.dumps(PAL, ensure_ascii=False, indent=0)); print(f'palabras.json: {len(PAL)} palabras con tiempo exacto (para subtítulos)')
with wave.open(str(V / 'audio/voz.wav'), 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
print(f"\nvoz.wav listo ({total:.1f}s). {'⚠ ' + str(problemas) + ' problema(s) a revisar' if problemas else 'Sin problemas de tiempo ni palabras prohibidas.'}")

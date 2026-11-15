#!/usr/bin/env python3
"""Escucha un audio/video con Whisper (faster-whisper, local) y lo compara con el guion: sirve para ENTERARSE de qué se entiende y qué suena mal.
Uso:  python engine/audio/escuchar.py final.mp4 [--video videos/X] [--modelo small] [--idioma es] [--json salida.json]
  • Sin --video: solo imprime la transcripción con tiempos.
  • Con --video: compara palabra por palabra con `voz.lineas[].texto` de video.json → % de palabras entendidas por línea y las que se leyeron distinto
    (candidatas a diccionario de pronunciación: engine/audio/pronunciacion.json). OJO: Whisper también se equivoca; si una palabra falla en varias líneas
    o en varios modelos, probablemente suena mal; si falla una vez, escucharla.
  • Música: Whisper solo oye voz. Si la música "entra" en la transcripción (palabras inventadas sobre un tramo sin voz), se ve como línea sin guion.
Primer uso: baja el modelo de Hugging Face (small ≈ 480 MB, se guarda en ~/.cache). Requiere `pip install faster-whisper`. No usa av para decodificar (ffmpeg → numpy)."""
import argparse, json, re, subprocess, sys, unicodedata
import numpy as np


def norm(s):
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.findall(r"[a-z0-9ñ]+", s)


def audio(ruta):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', ruta, '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.int16).astype(np.float32) / 32768


def lcs_diff(ref, hyp):
    """Alineación de palabras (programación dinámica): devuelve (coinciden, [(esperada, oída)] de las que difieren)."""
    n, m = len(ref), len(hyp); T = np.zeros((n + 1, m + 1), int)
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1): T[i, j] = T[i + 1, j + 1] + 1 if ref[i] == hyp[j] else max(T[i + 1, j], T[i, j + 1])
    i = j = ok = 0; dif = []
    while i < n and j < m:
        if ref[i] == hyp[j]: ok += 1; i += 1; j += 1
        elif T[i + 1, j] >= T[i, j + 1]:
            # si la siguiente esperada coincide con lo oído, la actual se leyó distinto (sustitución): se anota con la palabra que se oyó en su lugar
            dif.append((ref[i], hyp[j] if i + 1 < n and ref[i + 1] != hyp[j] and (j + 1 >= m or ref[i + 1] == hyp[j + 1]) else '')); i += 1
        else: j += 1
    dif += [(r, '') for r in ref[i:]]
    return ok, dif


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('audio'); ap.add_argument('--video', default=''); ap.add_argument('--modelo', default='small')
    ap.add_argument('--idioma', default='es'); ap.add_argument('--json', default=''); a = ap.parse_args()
    from faster_whisper import WhisperModel
    seg, info = WhisperModel(a.modelo, device='cpu', compute_type='int8').transcribe(audio(a.audio), language=a.idioma, beam_size=5)
    S = [dict(ini=round(s.start, 1), fin=round(s.end, 1), texto=s.text.strip()) for s in seg]
    for s in S: print(f"[{s['ini']:6.1f}-{s['fin']:6.1f}] {s['texto']}")
    if not a.video: return
    L = json.load(open(f'{a.video}/video.json'))['voz']['lineas']; res = []; print('\nComparación con el guion (por línea):')
    for l in L:
        ref = norm(l['texto']); fin = l['t'] + 0.4 + len(ref) / 2.7 + 1.5
        hyp = norm(' '.join(s['texto'] for s in S if s['fin'] > l['t'] and s['ini'] < fin)); ok, dif = lcs_diff(ref, hyp)
        res.append(dict(id=l['id'], t=l['t'], pct=round(100 * ok / max(1, len(ref))), distintas=dif))
        print(f"  {l['id']} t={l['t']:>5}  {res[-1]['pct']:>3} %  " + (', '.join(f'{r}→{h or "∅"}' for r, h in dif) or 'ok'))
    tot = np.mean([r['pct'] for r in res]); print(f"\nPromedio {tot:.0f} % de palabras entendidas por Whisper ({a.modelo}).")
    if a.json: open(a.json, 'w').write(json.dumps(dict(segmentos=S, lineas=res, promedio=round(float(tot))), ensure_ascii=False, indent=1))


if __name__ == '__main__':
    sys.exit(main())

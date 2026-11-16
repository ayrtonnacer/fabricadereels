#!/usr/bin/env python3
"""Mide en lote los mp4 de assets/referencias/_nuevas/: para cada uno corre medir.py → docs/4-referencias/externos/<slug>/,
lo mueve a assets/referencias/ (junto con su .txt) y al final regenera las tablas de la biblia (biblia.py).
Uso: python engine/analisis/analizar_lote.py [--sin-mover]"""
import shutil, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]; IN = R / 'assets/referencias/_nuevas'; OUT = R / 'docs/4-referencias/externos'
mover = '--sin-mover' not in sys.argv
vids = sorted(IN.glob('*.mp4'))
if not vids: sys.exit('No hay mp4 nuevos en assets/referencias/_nuevas/')
for v in vids:
    slug = v.stem.lower().replace(' ', '-'); dst = OUT / slug; dst.mkdir(parents=True, exist_ok=True)
    print(f'== {slug}'); subprocess.run([sys.executable, str(R / 'engine/analisis/medir.py'), str(v), str(dst)], check=True)
    subprocess.run([sys.executable, str(R / 'engine/analisis/movimientos.py'), str(dst), '--video', str(v)], check=True)   # libro de movimientos de cámara
    txt = v.with_suffix('.txt')
    if txt.exists(): shutil.copy(txt, dst / 'NOTAS-DE-AYRTON.txt')
    if mover:
        shutil.move(str(v), R / 'assets/referencias' / v.name)
        if txt.exists(): shutil.move(str(txt), R / 'assets/referencias' / txt.name)
subprocess.run([sys.executable, str(R / 'engine/analisis/biblia.py')], check=True)
subprocess.run([sys.executable, str(R / 'engine/analisis/movimientos.py'), '--catalogo'], check=True)
print(f'listo: {len(vids)} referencia(s) medida(s). Revisar docs/4-referencias/BIBLIA-DE-ESTILO.md y los INFORME.md nuevos.')

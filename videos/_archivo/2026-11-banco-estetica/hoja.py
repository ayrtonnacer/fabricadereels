#!/usr/bin/env python3
"""Hoja comparativa del banco: una fila por versión (v0…v4) y una fila de la referencia motion-ref-2, en los mismos momentos de cada plano.
Uso (desde la raíz del repo):  python videos/2026-11-banco-estetica/hoja.py  → analisis/hoja-comparativa.jpg"""
import os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(AQUI, '../../assets/referencias/motion-ref-2.mp4')
# momentos: (etiqueta, segundo en el banco, segundo en la referencia con un momento equivalente)
MOM = [('Gancho · 3 objetos', 2.0, 1.0), ('Gancho · salida', 4.55, 3.0), ('Planilla', 8.5, 5.0), ('Viaje a 3/4', 10.75, 9.0), ('Bloque 3D', 14.5, 12.0), ('Cierre', 19.5, 19.0)]
VERS = [('v0 original', 'out/v0.mp4'), ('v1 encuadre', 'out/v1.mp4'), ('v2 + luz', 'out/v2.mp4'), ('v3 + desenfoque', 'out/v3.mp4'), ('v4 + cámara', 'out/v4.mp4')]
W, H, PAD, LAB = 216, 384, 6, 150


def cuadro(video, t):
    with tempfile.NamedTemporaryFile(suffix='.png') as f:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', video, '-frames:v', '1', f.name], check=True)
        return Image.open(f.name).convert('RGB').resize((W, H), Image.LANCZOS)


def main():
    filas = [(n, os.path.join(AQUI, p)) for n, p in VERS if os.path.exists(os.path.join(AQUI, p))] + [('motion-ref-2', REF)]
    hoja = Image.new('RGB', (LAB + len(MOM) * (W + PAD), 40 + len(filas) * (H + PAD)), (24, 24, 24)); d = ImageDraw.Draw(hoja)
    try: fuente = ImageFont.truetype('DejaVuSans.ttf', 18)
    except OSError: fuente = ImageFont.load_default()
    for j, (et, _, _) in enumerate(MOM): d.text((LAB + j * (W + PAD) + 4, 10), et, fill=(230, 230, 230), font=fuente)
    for i, (nom, vid) in enumerate(filas):
        y = 40 + i * (H + PAD); d.text((8, y + H // 2 - 10), nom, fill=(230, 230, 230), font=fuente)
        for j, (_, tb, tr) in enumerate(MOM): hoja.paste(cuadro(vid, tr if vid == REF else tb), (LAB + j * (W + PAD), y))
    salida = os.path.join(AQUI, 'analisis/hoja-comparativa.jpg'); hoja.save(salida, quality=88); print(salida)


if __name__ == '__main__': main()

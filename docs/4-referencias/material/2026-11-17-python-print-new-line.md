# Python Print New Line (artículo pegado por Ayrton, 2026-11-17)
Autora: Kimberly Fessel. Tema: saltos de línea en Python: `\n`, `\r`, `\r\n`, `print()` (final automático), `end=`, `sep=`, cadenas de triple comilla, y el error de las rutas de Windows (`'C:\new_folder\text.txt'` → `\n` salto, `\t` tabulador) con 3 arreglos: cadena cruda `r'...'`, barras dobles `\\`, barras comunes `/`.
Pedido: "un reel explicando sintaxis en python, con este material".

## Datos medidos en Python 3.13 (2026-11-17)
- `len('\n') == 1`, `ord('\n') == 10`, `ord('\t') == 9`, `ord('\r') == 13`.
- `'C:\new_folder\text.txt'` tiene **20** caracteres (escritos son 22); `print` lo muestra partido: `C:` / salto / `ew_folder` + tabulador + `ext.txt`.
- `r'C:\new_folder\text.txt'` tiene **22** caracteres y se imprime tal cual.
- `print('a','b','c',sep='\n')` imprime una letra por renglón; `print('Hi',end='')` no salta.

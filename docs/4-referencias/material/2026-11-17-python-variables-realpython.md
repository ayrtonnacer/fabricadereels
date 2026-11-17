# Variables in Python: Usage and Best Practices (Real Python, L. Pozo Ramos, act. 15-abr-2026)
Pasado por Ayrton el 2026-11-17 (texto truncado en el mensaje; llega hasta "Best Practices for Naming"). Pedido: "un reel que explique las variables en Python".
Ideas del artículo: variable = nombre simbólico que apunta a un objeto en memoria (`nombre = valor`); tipado dinámico (reasignar cambia el tipo); usos: contadores, acumuladores, temporales (swap), banderas booleanas (`is_`/`has_`), variables de bucle, almacenamiento; nombres: letras/dígitos/guion bajo, no empiezan con dígito (SyntaxError), distinguen mayúsculas, snake_case (PEP 8), evitar una letra y abreviaturas; secciones finales (sin leer): referencias, type hints, desempaquetado, scopes.
## Medido en Python 3.13 (2026-11-17)
- `a=[1,2]; b=a; b.append(3)` → `a == [1,2,3]` y `a is b` es True: un solo objeto, dos nombres.
- `x=19; y=x; x="diecinueve"` → `type(x)` pasa a str, `y` sigue en 19.
- `age` y `Age` son variables distintas; `2age=1` da SyntaxError.

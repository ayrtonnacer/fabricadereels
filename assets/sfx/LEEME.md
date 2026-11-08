# Banco de efectos reales (opcional, no se sube a git)
Si ponés sonidos reales acá, `sfxlib.sample('<categoria>')` los usa en lugar de los sintéticos. Subcarpetas (una por tipo, como recomienda el video de diseño sonoro):
`whoosh/ impact/ hit/ riser/ bassdrop/ braam/ ui/ click/ pop/ bell/ glitch/ keyboard/ ambiente/ foley/`
Fuente sugerida: efectos gratuitos de Adobe Audition (https://www.adobe.com/products/audition/offers/adobeauditiondlcsfx.html). Descargarlos con tu cuenta de Adobe, descomprimir y copiar los archivos a la subcarpeta que corresponda. Revisá la licencia de Adobe antes de publicar videos con ellos y NO subas los archivos a un repo público (por eso `assets/sfx/*` está en .gitignore).
En `sfx_events.py`: `x = sample('whoosh') ; T.put(t, x if x is not None else whoosh(0.4), 0.55)`.

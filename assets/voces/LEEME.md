Modelo de voz Piper es_AR Daniela (alta calidad). El .onnx pesa 114 MB y GitHub no deja subir archivos de más de 100 MB sin LFS,
así que está partido en `.onnx.parte00/01/02`. Para armarlo (lo hace solo `python engine/audio/voz.py` si falta):
  cat assets/voces/es_AR-daniela-high.onnx.parte* > assets/voces/es_AR-daniela-high.onnx
El .onnx armado está ignorado por git.

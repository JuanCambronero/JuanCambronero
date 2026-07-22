"""Descarga el avatar de GitHub y lo convierte en una rejilla ASCII.

    avatar de GitHub  ->  data/ascii.json

Se guarda la rejilla ya calculada para que make_about.py no dependa de
Pillow ni de la red: el workflow diario solo necesita la libreria estandar.
Vuelve a ejecutar esto a mano si cambias la foto de perfil.

Requiere:  pip install pillow numpy
"""
import json
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
USER = "JuanCambronero"

# Una celda de texto monoespaciado mide ~0.6em de ancho por ~1.15em de alto:
# casi el doble de alta que ancha. Para que el retrato salga CUADRADO hay que
# muestrear la mitad de filas que de columnas.
# Menos columnas de las que uno esperaria, y es a proposito: la tarjeta mide
# 290px de ancho. Con 68 columnas cada glifo queda a 4.3px, los caracteres se
# funden en una textura gris y se pierde la cara. Con ~44 el glifo mide ~11px
# y su FORMA aporta informacion. En ASCII la resolucion util la marca el
# tamaño al que se pinta, no cuanto muestreas.
COLS = 56                    # las filas se calculan desde el recorte
CELDA_W, CELDA_H = 0.6, 1.15  # ancho y alto de una celda, en em

# Por encima de este brillo (0-255) se considera fondo y se deja en blanco.
# El fondo del avatar es casi uniforme y muy claro; la piel queda por debajo.
UMBRAL_FONDO = 228

# Rampa CORTA y ordenada por cobertura real de tinta.
# Probada tambien la rampa "estandar" de 70 caracteres: a este tamaño da peor
# resultado, porque mezcla glifos finos y altos (l, I, j, 1) con otros macizos
# ($, &, %) y el ojo lee ruido en vez de un degradado. Con 15 niveles bien
# ordenados la piel queda lisa y la silueta limpia.
RAMPA = " .,:;i1tfLCG08@"


def descargar() -> bytes:
    api = json.load(urllib.request.urlopen(
        urllib.request.Request(f"https://api.github.com/users/{USER}",
                               headers={"User-Agent": "profile-art"}), timeout=20))
    url = api["avatar_url"] + "&s=900" if "?" in api["avatar_url"] else api["avatar_url"] + "?s=900"
    print(f"  avatar: {url}")
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "profile-art"}), timeout=30).read()


def a_ascii(data: bytes) -> list[str]:
    import io

    import numpy as np
    from PIL import Image, ImageOps

    img = Image.open(io.BytesIO(data)).convert("L")

    # Encuadre explicito a la cabeza, en fracciones del avatar (izq, arr, der, aba).
    # Se ajusta mirando la foto, no a ojo: en este avatar la cara ocupa la
    # franja media, con el pelo oscuro arriba y la chaqueta negra abajo. Si se
    # deja entrar mucha chaqueta, esta se lleva todos los caracteres densos y
    # a la cara le quedan pocas celdas para los rasgos.
    CAJA = (0.27, 0.19, 0.73, 0.70)
    w, h = img.size
    img = img.crop((int(CAJA[0] * w), int(CAJA[1] * h),
                    int(CAJA[2] * w), int(CAJA[3] * h)))

    a = np.asarray(img, dtype=np.uint8)
    original = a.copy()          # brillos ORIGINALES, para separar el fondo

    # 1. Contraste LOCAL (CLAHE). Es el paso que mas se nota: un autocontraste
    #    global aplana la cara porque el pelo oscuro y el fondo claro se comen
    #    todo el rango. CLAHE ecualiza por zonas y saca ojos, nariz y boca.
    #    Se MEZCLA con el original al 50%: CLAHE a full iguala el pelo oscuro
    #    y la piel clara (ecualiza dentro de cada zona), y un retrato necesita
    #    justo lo contrario, que la silueta global se distinga.
    try:
        import cv2
        clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8)).apply(a)
        a = cv2.addWeighted(clahe, 0.5, a, 0.5, 0)
    except ImportError:
        print("  aviso: sin opencv uso autocontraste global (peor resultado)",
              file=sys.stderr)
        a = np.asarray(ImageOps.autocontrast(Image.fromarray(a), cutoff=2))

    # 2. Enfoque (mascara de desenfoque). Al reducir a ~90 columnas se pierden
    #    los bordes; realzarlos antes hace que sobrevivan al remuestreo.
    try:
        import cv2
    #    Radio pequeño (sigma 1.6) a proposito: interesa realzar ojos, cejas y
    #    boca, no el contorno general, que ya se ve solo.
        blur = cv2.GaussianBlur(a, (0, 0), sigmaX=1.6)
        a = cv2.addWeighted(a, 1.95, blur, -0.95, 0)
    except ImportError:
        pass

    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

    # Filas derivadas del recorte para no deformar la cara: una celda de texto
    # es ~2x mas alta que ancha, asi que hacen falta menos filas que columnas.
    cw, chh = img.size
    rows = max(1, round(COLS * (chh / cw) * (CELDA_W / CELDA_H)))
    g = np.asarray(img.resize((COLS, rows), Image.LANCZOS), dtype=float)

    # Mascara de fondo sobre los brillos ORIGINALES. Es imprescindible hacerlo
    # aqui y no despues: la piel de la cara es casi tan clara como el fondo, y
    # un umbral aplicado tras normalizar se lleva por delante mejillas y frente
    # dejando el rostro hueco. CLAHE ademas destruye los brillos absolutos.
    fondo = np.asarray(
        Image.fromarray(original).resize((COLS, rows), Image.LANCZOS), dtype=float
    ) > UMBRAL_FONDO

    # 3. Normalizar y levantar los medios tonos con una gamma. Sin esto la cara
    #    (que es tono medio) se va hacia los caracteres densos y se emborrona.
    lo, hi = np.percentile(g, 1), np.percentile(g, 99)
    g = np.clip((g - lo) / max(hi - lo, 1e-6), 0, 1)
    g = g ** 0.68

    # Invertido: pixel oscuro -> caracter denso
    d = 1 - g

    # 4. Silenciar el fondo con la mascara calculada arriba. CLAHE realza el
    #    ruido de las zonas planas y el fondo claro se llena de puntitos que
    #    ensucian la silueta.
    d[fondo] = 0

    idx = (d * (len(RAMPA) - 1)).round().astype(int)
    filas = ["".join(RAMPA[i] for i in fila) for fila in idx]

    # Recortar el marco vacio: sin esto el retrato queda flotando en medio
    # de su caja y se ve mas pequeño de lo que podria.
    while filas and not filas[0].strip():
        filas.pop(0)
    while filas and not filas[-1].strip():
        filas.pop()

    izq = min((len(f) - len(f.lstrip()) for f in filas if f.strip()), default=0)
    der = min((len(f) - len(f.rstrip()) for f in filas if f.strip()), default=0)
    if izq or der:
        filas = [f[izq:len(f) - der] for f in filas]

    return filas


if __name__ == "__main__":
    filas = a_ascii(descargar())

    cols = max(len(f) for f in filas)
    filas = [f.ljust(cols) for f in filas]

    out = ROOT / "data" / "ascii.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"cols": cols, "rows": len(filas), "rampa": RAMPA,
                               "filas": filas}, indent=1), encoding="utf-8")

    print(f"  {COLS} columnas muestreadas -> {cols}x{len(filas)} tras recortar")
    print(f"escrito {out}")
    print()
    for f in filas[::2]:                 # vista previa rapida en consola
        print("  " + f)

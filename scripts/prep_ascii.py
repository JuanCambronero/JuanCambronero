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
COLS, ROWS = 62, 32
RAMPA = " .·:-=+*#%@"        # de vacio a denso


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

    # Encuadre a la cara. Sin acercar, la ropa oscura ocupa la mitad de la
    # rejilla y sale un bloque solido de '@' que no se lee como un retrato.
    # ZOOM recorta un cuadrado mas pequeño; SUBIR lo desplaza hacia arriba
    # (la cara esta por encima del centro geometrico del avatar).
    ZOOM, SUBIR = 0.62, 0.10
    w, h = img.size
    lado = int(min(w, h) * ZOOM)
    cx, cy = w // 2, int(h // 2 - min(w, h) * SUBIR)
    izq = max(0, min(cx - lado // 2, w - lado))
    arr = max(0, min(cy - lado // 2, h - lado))
    img = img.crop((izq, arr, izq + lado, arr + lado))

    img = ImageOps.autocontrast(img, cutoff=2)

    # Muestreo: al ser el caracter ~2x mas alto que ancho, se pide el doble
    # de columnas y luego se promedian por pares. Da mas detalle horizontal.
    g = np.asarray(img.resize((COLS, ROWS), Image.LANCZOS), dtype=float)

    lo, hi = np.percentile(g, 3), np.percentile(g, 97)
    g = np.clip((g - lo) / max(hi - lo, 1e-6), 0, 1)

    # Invertido: pixel oscuro -> caracter denso
    idx = ((1 - g) * (len(RAMPA) - 1)).round().astype(int)
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

    print(f"  {COLS}x{ROWS} muestreado -> {cols}x{len(filas)} tras recortar")
    print(f"escrito {out}")
    print()
    for f in filas[::2]:                 # vista previa rapida en consola
        print("  " + f)

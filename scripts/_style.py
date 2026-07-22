"""Paleta y utilidades compartidas por todos los generadores.

Para cambiar la identidad de todo el perfil, toca solo ACCENT y ACCENT_2.
"""

# ── Identidad ────────────────────────────────────────────────────────────
# Naranja: el mismo acento del CV, la landing y LinkedIn.
# Si prefieres el azul, cambia estas dos lineas y regenera:
#     ACCENT, ACCENT_2 = "#0a66c2", "#00c6fb"
ACCENT   = "#ff5a1f"
ACCENT_2 = "#ffa13f"

BG      = "#0f0d0c"
PANEL   = "#141110"
LINE    = "#2a2523"
INK     = "#edeae5"
INK_MID = "#a49e97"
INK_LOW = "#8a847c"
GREEN   = "#3fb950"

# Sin fuentes externas: dentro de un <img> el SVG no puede cargarlas.
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"


def esc(s: str) -> str:
    """XML-escape. Los SVG se parsean como XML estricto."""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def panel(w: int, h: int, title: str = "", right: str = "") -> str:
    """Marco con barra de titulo, comun a todas las tarjetas."""
    out = (
        f'<rect width="{w}" height="{h}" rx="10" fill="{BG}"/>'
        f'<rect width="{w}" height="{h}" rx="10" fill="none" stroke="{LINE}"/>'
    )
    if title:
        out += (
            f'<rect x="1" y="1" width="{w - 2}" height="34" rx="10" fill="{PANEL}"/>'
            f'<rect x="1" y="26" width="{w - 2}" height="9" fill="{PANEL}"/>'
            f'<line x1="0" y1="35" x2="{w}" y2="35" stroke="{LINE}"/>'
            f'<text x="26" y="23" fill="{INK}" font-family="{MONO}" font-size="12.5" '
            f'font-weight="500">{esc(title)}</text>'
        )
        if right:
            out += (
                f'<text x="{w - 26}" y="23" text-anchor="end" fill="{ACCENT}" '
                f'font-family="{MONO}" font-size="11">{esc(right)}</text>'
            )
    return out


def wrap(texto: str, max_chars: int) -> list[str]:
    """Parte un texto en lineas de como mucho max_chars.

    Respeta los tramos marcados con |resaltado|: si una linea termina
    dentro de un tramo, lo cierra y lo vuelve a abrir en la siguiente.
    Las barras no cuentan para el ancho porque no se pintan.
    """
    lineas, actual, dentro = [], [], False
    largo = 0

    for palabra in texto.split():
        visible = len(palabra.replace("|", ""))
        if actual and largo + 1 + visible > max_chars:
            linea = " ".join(actual)
            if dentro:                      # cerrar el resaltado al cortar
                linea += "|"
            lineas.append(linea)
            actual, largo = (["|"] if dentro else []), 0

        actual.append(palabra)
        largo += visible + (1 if largo else 0)
        dentro ^= (palabra.count("|") % 2 == 1)

    if actual:
        lineas.append(" ".join(actual))
    return lineas


def write(path, svg: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    print(f"escrito {path}  ({path.stat().st_size / 1024:.1f} KB)")

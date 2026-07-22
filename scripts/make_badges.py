"""art/badge-*.svg — un badge por archivo.

Equivale a shields.io, servido desde tu repo.

Un archivo por badge y no una tira unica: GitHub sirve los SVG del README
dentro de un <img>, y ahi los <a> internos NO son clicables. Para que
LinkedIn/GitHub se puedan pulsar hay que envolver cada imagen en un
enlace desde el propio README.
"""
from pathlib import Path

from _style import GREEN, INK, MONO, esc, write

H = 30
PAD = 11
CHAR = 6.9                       # ancho por caracter a 11.5px

# (id, icono, etiqueta, color)
BADGES = [
    ("linkedin",  "in",   "LinkedIn",                     "#0a66c2"),
    ("email",     "mail", "Email",                        "#ea4335"),
    ("github",    "git",  "GitHub",                       "#2a2523"),
    ("madrid",    "pin",  "Madrid, España",               "#3a3330"),
    ("disponible","dot",  "Disponible · jornada completa", GREEN),
]


def icono(kind: str, x: float, y: float) -> str:
    """Iconos minimos en trazados: nada de fuentes de iconos externas."""
    c = INK
    if kind == "in":
        return (f'<rect x="{x}" y="{y - 6}" width="3" height="9" fill="{c}"/>'
                f'<circle cx="{x + 1.5}" cy="{y - 8.5}" r="1.7" fill="{c}"/>'
                f'<path d="M{x + 5} {y + 3} v-9 h3 v1.2 a3.4 3.4 0 0 1 5.6 2.6 V{y + 3} h-3 '
                f'v-4.6 a1.5 1.5 0 0 0 -3 0 V{y + 3} Z" fill="{c}"/>')
    if kind == "mail":
        return (f'<rect x="{x}" y="{y - 7}" width="14" height="10" rx="1.6" '
                f'fill="none" stroke="{c}" stroke-width="1.5"/>'
                f'<path d="M{x + 0.8} {y - 6.2} L{x + 7} {y - 1.6} L{x + 13.2} {y - 6.2}" '
                f'fill="none" stroke="{c}" stroke-width="1.5"/>')
    if kind == "git":
        return (f'<circle cx="{x + 6.5}" cy="{y - 2}" r="6.5" fill="{c}"/>'
                f'<path d="M{x + 3.4} {y + 3.4} v-2.4 a2 2 0 0 1 2-2 h2.2 a2 2 0 0 1 2 2 v2.4" '
                f'fill="none" stroke="#0f0d0c" stroke-width="1.4"/>')
    if kind == "pin":
        return (f'<path d="M{x + 5.5} {y + 3} C{x + 5.5} {y + 3} {x + 11} {y - 3} {x + 11} {y - 6.4} '
                f'a5.5 5.5 0 0 0 -11 0 C{x} {y - 3} {x + 5.5} {y + 3} {x + 5.5} {y + 3} Z" '
                f'fill="none" stroke="{c}" stroke-width="1.5"/>'
                f'<circle cx="{x + 5.5}" cy="{y - 6.4}" r="1.9" fill="{c}"/>')
    # punto que late
    return (f'<circle cx="{x + 5}" cy="{y - 2}" r="4" fill="{c}">'
            f'<animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/>'
            f'</circle>')


def build(ic: str, label: str, color: str) -> str:
    icon_w = 16 if ic != "dot" else 12
    w = int(PAD + icon_w + 6 + len(label) * CHAR + PAD)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" role="img" aria-label="{esc(label)}">
<g opacity="0">
  <animate attributeName="opacity" from="0" to="1" begin="0.2s" dur="0.5s" fill="freeze"/>
  <rect width="{w}" height="{H}" rx="4" fill="{color}"/>
  {icono(ic, PAD, H / 2 + 3)}
  <text x="{PAD + icon_w + 6}" y="{H / 2 + 4:.0f}" fill="{INK}"
        font-family="{MONO}" font-size="11.5" font-weight="500">{esc(label)}</text>
</g>
</svg>
"""


if __name__ == "__main__":
    art = Path(__file__).resolve().parent.parent / "art"
    for bid, ic, label, color in BADGES:
        write(art / f"badge-{bid}.svg", build(ic, label, color))

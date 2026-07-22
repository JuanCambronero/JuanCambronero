"""art/header.svg — cabecera con onda animada.

Equivale a capsule-render (?type=waving), pero servido desde tu repo.
La onda son dos trazados senoidales de doble ancho que se desplazan en
bucle: al moverse justo un periodo completo, la costura no se ve.
"""
import math
import random
from pathlib import Path

from _style import ACCENT, ACCENT_2, BG, INK, MONO, SANS, esc, write

W, H = 860, 190

NOMBRE = "Juan Cambronero"
SUB = "Full Stack Developer · Java + Spring Boot + Angular"


def onda(amp: float, largo: float, base: float, paso: int = 6) -> str:
    """Trazado senoidal de ancho 2W, cerrado por abajo para poder rellenarlo."""
    pts = []
    x = 0
    while x <= W * 2:
        y = base + amp * math.sin(2 * math.pi * x / largo)
        pts.append(f"{x},{y:.1f}")
        x += paso
    return f"M {' L '.join(pts)} L {W * 2},{H} L 0,{H} Z"


def particulas(n: int = 22) -> str:
    """Puntos que ascienden lentamente. Semilla fija: el SVG debe ser
    identico en cada ejecucion, o el workflow commitearia cambios cada dia."""
    rnd = random.Random(7)
    out = []
    for _ in range(n):
        x = rnd.uniform(20, W - 20)
        r = rnd.uniform(1.1, 2.6)
        dur = rnd.uniform(7, 15)
        desfase = rnd.uniform(0, dur)
        op = rnd.uniform(0.18, 0.5)
        out.append(
            f'<circle cx="{x:.0f}" cy="{H}" r="{r:.1f}" fill="#ffffff" opacity="0">'
            f'<animate attributeName="cy" from="{H + 10}" to="-10" dur="{dur:.1f}s" '
            f'begin="-{desfase:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;{op:.2f};{op:.2f};0" '
            f'keyTimes="0;0.15;0.75;1" dur="{dur:.1f}s" begin="-{desfase:.1f}s" '
            f'repeatCount="indefinite"/>'
            f'</circle>'
        )
    return "".join(out)


def build() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(NOMBRE)} — {esc(SUB)}">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0"   stop-color="{ACCENT}"/>
    <stop offset="0.55" stop-color="{ACCENT_2}"/>
    <stop offset="1"   stop-color="{ACCENT}"/>
  </linearGradient>
  <clipPath id="marco"><rect width="{W}" height="{H}" rx="12"/></clipPath>
</defs>

<g clip-path="url(#marco)">
  <rect width="{W}" height="{H}" fill="url(#g)"/>

  <!-- Particulas ascendentes, por detras de las ondas -->
  {particulas()}

  <!-- Dos ondas a distinta velocidad: da sensacion de profundidad -->
  <path d="{onda(13, 430, 132)}" fill="{BG}" opacity="0.28">
    <animateTransform attributeName="transform" type="translate"
                      from="0 0" to="-{W} 0" dur="11s" repeatCount="indefinite"/>
  </path>
  <path d="{onda(17, 620, 148)}" fill="{BG}" opacity="0.6">
    <animateTransform attributeName="transform" type="translate"
                      from="-{W} 0" to="0 0" dur="16s" repeatCount="indefinite"/>
  </path>
  <path d="{onda(11, 350, 163)}" fill="{BG}">
    <animateTransform attributeName="transform" type="translate"
                      from="0 0" to="-{W} 0" dur="8s" repeatCount="indefinite"/>
  </path>

  <!-- Texto: fade-in escalonado -->
  <text x="{W // 2}" y="82" text-anchor="middle" fill="{INK}"
        font-family="{SANS}" font-size="46" font-weight="700" opacity="0">
    {esc(NOMBRE)}
    <animate attributeName="opacity" from="0" to="1" begin="0.2s" dur="0.9s" fill="freeze"/>
  </text>
  <text x="{W // 2}" y="112" text-anchor="middle" fill="{INK}"
        font-family="{MONO}" font-size="14" opacity="0">
    {esc(SUB)}
    <animate attributeName="opacity" from="0" to="0.92" begin="0.7s" dur="0.9s" fill="freeze"/>
  </text>
</g>
</svg>
"""


if __name__ == "__main__":
    write(Path(__file__).resolve().parent.parent / "art" / "header.svg", build())

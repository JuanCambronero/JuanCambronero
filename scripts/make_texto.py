"""art/txt-*.svg — los fragmentos de texto sueltos del README, animados.

Cada uno lleva la animacion que le corresponde por lo que dice, no una
generica:

  stack   la lista de "lo que uso primero" se subraya de izquierda a
          derecha, como quien recorre una lista.
  otros   los proyectos menores aparecen de golpe pero atenuados: son
          secundarios y la animacion lo dice.
  pie     una sola linea que se desvanece hacia dentro. Es un cierre.
"""
from pathlib import Path

from _style import ACCENT, INK, INK_LOW, INK_MID, LINE, MONO, SANS, esc, write

W = 860


def stack_line() -> str:
    H = 46
    etiqueta = "Lo que uso primero"
    items = ["Java 17", "Spring Boot", "Spring Data JPA", "Spring Security",
             "Angular", "TypeScript", "PostgreSQL", "APIs REST"]

    partes, x, delay = [], 0, 0.3
    piezas = []
    for i, it in enumerate(items):
        piezas.append((it, x))
        x += len(it) * 7.1 + 22
    ancho_total = x - 22
    x0 = (W - ancho_total) / 2

    for i, (it, dx) in enumerate(piezas):
        px = x0 + dx
        w = len(it) * 7.1
        partes.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.35s" fill="freeze"/>'
            f'<text x="{px:.0f}" y="24" fill="{INK}" font-family="{MONO}" font-size="12">{esc(it)}</text>'
            f'<rect x="{px:.0f}" y="30" width="0" height="1.5" fill="{ACCENT}">'
            f'<animate attributeName="width" from="0" to="{w:.0f}" begin="{delay + 0.1:.2f}s" '
            f'dur="0.35s" fill="freeze"/></rect>'
            f'</g>'
        )
        if i < len(piezas) - 1:
            partes.append(
                f'<text x="{px + w + 8:.0f}" y="24" fill="{LINE}" font-family="{MONO}" '
                f'font-size="12">·</text>'
            )
        delay += 0.1

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(etiqueta)}: {esc(' · '.join(items))}">
{"".join(partes)}
</svg>
"""


def otros_line() -> str:
    H = 34
    intro = "También:"
    items = ["Impostor", "Hundir la flota", "Tic-Tac-Toe"]
    cola = "— ejercicios de lógica en Python."

    texto = f"{intro}  {'  ·  '.join(items)}  {cola}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(texto)}">
<g opacity="0">
  <animate attributeName="opacity" from="0" to="0.9" begin="0.3s" dur="0.7s" fill="freeze"/>
  <text x="{W // 2}" y="21" text-anchor="middle" fill="{INK_LOW}" font-family="{MONO}" font-size="11.5">
    <tspan>{esc(intro)}</tspan>
    <tspan fill="{INK_MID}">  {esc('  ·  '.join(items))}  </tspan>
    <tspan>{esc(cola)}</tspan>
  </text>
</g>
</svg>
"""


def pie() -> str:
    H = 62
    l1 = "Madrid  ·  juancambronerofresco@gmail.com  ·  Respondo a todo."
    l2 = "Animaciones en SVG generados con Python desde scripts/, sin servicios de terceros."

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(l1)} {esc(l2)}">
<line x1="{W // 2}" y1="8" x2="{W // 2}" y2="8" stroke="{LINE}">
  <animate attributeName="x1" from="{W // 2}" to="180" begin="0.2s" dur="0.9s" fill="freeze"/>
  <animate attributeName="x2" from="{W // 2}" to="{W - 180}" begin="0.2s" dur="0.9s" fill="freeze"/>
</line>
<g opacity="0">
  <animate attributeName="opacity" from="0" to="1" begin="0.7s" dur="0.6s" fill="freeze"/>
  <text x="{W // 2}" y="34" text-anchor="middle" fill="{INK_MID}" font-family="{SANS}" font-size="12.5">{esc(l1)}</text>
</g>
<g opacity="0">
  <animate attributeName="opacity" from="0" to="0.75" begin="1.0s" dur="0.6s" fill="freeze"/>
  <text x="{W // 2}" y="52" text-anchor="middle" fill="{INK_LOW}" font-family="{MONO}" font-size="10.5">{esc(l2)}</text>
</g>
</svg>
"""


if __name__ == "__main__":
    art = Path(__file__).resolve().parent.parent / "art"
    write(art / "txt-stack.svg", stack_line())
    write(art / "txt-otros.svg", otros_line())
    write(art / "txt-pie.svg", pie())

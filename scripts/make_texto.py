"""art/txt-*.svg — los fragmentos de texto sueltos del README, animados.

Cada uno lleva la animacion que le corresponde por lo que dice, no una
generica:

  stack   la lista de "lo que uso primero" se subraya de izquierda a
          derecha, como quien recorre una lista.
  otros   los proyectos menores aparecen atenuados: son secundarios y la
          animacion lo dice.
  pie     una regla que se abre desde el centro y el texto detras. Cierra.

De cada uno se genera version ancha y estrecha. En movil el SVG de 860 se
sirve a ~308px y el texto se queda ilegible; la estrecha reordena los
elementos en menos columnas.
"""
from pathlib import Path

from _style import (ACCENT, INK, INK_LOW, INK_MID, LINE, MONO, SANS,
                    esc, wrap, write)

STACK = ["Java 17", "Spring Boot", "Spring Data JPA", "Spring Security",
         "Angular", "TypeScript", "PostgreSQL", "APIs REST"]

OTROS_INTRO = "También:"
OTROS = ["Impostor", "Hundir la flota", "Tic-Tac-Toe"]
OTROS_COLA = "— ejercicios de lógica en Python."

PIE_1 = "Madrid  ·  juancambronerofresco@gmail.com  ·  Respondo a todo."
PIE_2 = "Animaciones en SVG generados con Python desde scripts/, sin servicios de terceros."


def stack_line(W: int, size: float, por_fila: int) -> str:
    """Reparte las tecnologias en filas centradas."""
    filas = [STACK[i:i + por_fila] for i in range(0, len(STACK), por_fila)]
    lh = int(size * 2.3)
    H = 14 + len(filas) * lh

    partes, delay = [], 0.3
    ch = size * 0.62                      # avance por caracter en monoespaciada

    for f, fila in enumerate(filas):
        anchos = [len(t) * ch for t in fila]
        total = sum(anchos) + (len(fila) - 1) * (ch * 3)
        x = (W - total) / 2
        y = 20 + f * lh

        for i, t in enumerate(fila):
            w = anchos[i]
            partes.append(
                f'<g opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" '
                f'dur="0.35s" fill="freeze"/>'
                f'<text x="{x:.0f}" y="{y}" fill="{INK}" font-family="{MONO}" '
                f'font-size="{size}">{esc(t)}</text>'
                f'<rect x="{x:.0f}" y="{y + 6}" width="0" height="1.5" fill="{ACCENT}">'
                f'<animate attributeName="width" from="0" to="{w:.0f}" '
                f'begin="{delay + 0.1:.2f}s" dur="0.35s" fill="freeze"/></rect>'
                f'</g>'
            )
            if i < len(fila) - 1:
                partes.append(
                    f'<text x="{x + w + ch * 1.2:.0f}" y="{y}" fill="{LINE}" '
                    f'font-family="{MONO}" font-size="{size}">·</text>'
                )
            x += w + ch * 3
            delay += 0.1

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Lo que uso primero: {esc(' · '.join(STACK))}">
{"".join(partes)}
</svg>
"""


def otros_line(W: int, size: float, cpl: int) -> str:
    texto = f"{OTROS_INTRO}  {'  ·  '.join(OTROS)}  {OTROS_COLA}"
    lineas = wrap(texto, cpl)
    lh = int(size * 1.7)
    H = 10 + len(lineas) * lh

    textos = "".join(
        f'<text x="{W // 2}" y="{16 + i * lh}" text-anchor="middle" fill="{INK_LOW}" '
        f'font-family="{MONO}" font-size="{size}">{esc(ln)}</text>'
        for i, ln in enumerate(lineas)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(texto)}">
<g opacity="0">
  <animate attributeName="opacity" from="0" to="0.9" begin="0.3s" dur="0.7s" fill="freeze"/>
  {textos}
</g>
</svg>
"""


def pie(W: int, s1: float, s2: float, cpl1: int, cpl2: int) -> str:
    l1 = wrap(PIE_1, cpl1)
    l2 = wrap(PIE_2, cpl2)
    lh1, lh2 = int(s1 * 1.55), int(s2 * 1.6)
    y1 = 30
    y2 = y1 + len(l1) * lh1 + 6
    H = y2 + len(l2) * lh2 + 10
    margen = max(60, W // 5)

    t1 = "".join(
        f'<text x="{W // 2}" y="{y1 + i * lh1}" text-anchor="middle" fill="{INK_MID}" '
        f'font-family="{SANS}" font-size="{s1}">{esc(ln)}</text>' for i, ln in enumerate(l1)
    )
    t2 = "".join(
        f'<text x="{W // 2}" y="{y2 + i * lh2}" text-anchor="middle" fill="{INK_LOW}" '
        f'font-family="{MONO}" font-size="{s2}">{esc(ln)}</text>' for i, ln in enumerate(l2)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(PIE_1)} {esc(PIE_2)}">
<line x1="{W // 2}" y1="8" x2="{W // 2}" y2="8" stroke="{LINE}">
  <animate attributeName="x1" from="{W // 2}" to="{margen}" begin="0.2s" dur="0.9s" fill="freeze"/>
  <animate attributeName="x2" from="{W // 2}" to="{W - margen}" begin="0.2s" dur="0.9s" fill="freeze"/>
</line>
<g opacity="0">
  <animate attributeName="opacity" from="0" to="1" begin="0.7s" dur="0.6s" fill="freeze"/>
  {t1}
</g>
<g opacity="0">
  <animate attributeName="opacity" from="0" to="0.75" begin="1.0s" dur="0.6s" fill="freeze"/>
  {t2}
</g>
</svg>
"""


if __name__ == "__main__":
    art = Path(__file__).resolve().parent.parent / "art"

    write(art / "txt-stack.svg",        stack_line(860, 12, por_fila=8))
    write(art / "txt-stack-movil.svg",  stack_line(380, 11, por_fila=2))

    write(art / "txt-otros.svg",        otros_line(860, 11.5, cpl=110))
    write(art / "txt-otros-movil.svg",  otros_line(380, 10.5, cpl=46))

    write(art / "txt-pie.svg",          pie(860, 12.5, 10.5, cpl1=80, cpl2=110))
    write(art / "txt-pie-movil.svg",    pie(380, 11.5, 9.5,  cpl1=38, cpl2=46))

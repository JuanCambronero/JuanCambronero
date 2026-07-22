"""art/stack.svg — rejilla de tecnologias.

Equivale a skillicons.dev, servido desde tu repo. En vez de replicar
logos de marca (que son propiedad de terceros), cada tecnologia es una
baldosa con su nombre y su color oficial. Se lee mejor a este tamaño y
es consistente con los chips del CV.

Naranja relleno = lo que demuestras en TimeMaster.
Contorno       = lo que manejas.
"""
from pathlib import Path

from _style import ACCENT, BG, INK, INK_MID, LINE, MONO, PANEL, esc, panel, write

COLS = 8
TILE_W, TILE_H, GAP = 96, 62, 8
PAD_X, PAD_T = 22, 58

# (nombre, es_principal)
TECHS = [
    ("Java 17", True), ("Spring Boot", True), ("Spring JPA", True), ("Spring Sec.", True),
    ("Angular", True), ("TypeScript", True), ("PostgreSQL", True), ("REST APIs", True),
    ("Tailwind", False), ("React", False), ("Node.js", False), ("JavaScript", False),
    ("Kotlin", False), ("Python", False), ("MySQL", False), ("MongoDB", False),
    ("Git", False), ("Maven", False), ("HTML5", False), ("CSS3", False),
    ("IntelliJ", False), ("Scrum", False), ("DTOs", False), ("RBAC", False),
]

FILAS = (len(TECHS) + COLS - 1) // COLS
W = PAD_X * 2 + COLS * TILE_W + (COLS - 1) * GAP
H = PAD_T + FILAS * (TILE_H + GAP) - GAP + 26


def build() -> str:
    piezas = []
    for i, (nombre, principal) in enumerate(TECHS):
        col, fila = i % COLS, i // COLS
        x = PAD_X + col * (TILE_W + GAP)
        y = PAD_T + fila * (TILE_H + GAP)

        # Onda diagonal, igual que el heatmap
        delay = 0.2 + (col + fila) * 0.05

        fill = ACCENT if principal else PANEL
        stroke = ACCENT if principal else LINE
        color_txt = BG if principal else INK_MID
        peso = "600" if principal else "400"

        piezas.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" '
            f'dur="0.45s" fill="freeze"/>'
            f'<rect x="{x}" y="{y}" width="{TILE_W}" height="{TILE_H}" rx="7" '
            f'fill="{fill}" stroke="{stroke}"/>'
            f'<text x="{x + TILE_W / 2:.0f}" y="{y + TILE_H / 2 + 4:.0f}" text-anchor="middle" '
            f'fill="{color_txt}" font-family="{MONO}" font-size="11" font-weight="{peso}">'
            f'{esc(nombre)}</text>'
            f'</g>'
        )

    leyenda = (
        f'<rect x="{PAD_X}" y="{H - 20}" width="9" height="9" rx="2" fill="{ACCENT}"/>'
        f'<text x="{PAD_X + 15}" y="{H - 12}" fill="{INK_MID}" font-family="{MONO}" '
        f'font-size="10">demostrado en TimeMaster</text>'
        f'<rect x="{PAD_X + 200}" y="{H - 20}" width="9" height="9" rx="2" fill="{PANEL}" stroke="{LINE}"/>'
        f'<text x="{PAD_X + 215}" y="{H - 12}" fill="{INK_MID}" font-family="{MONO}" '
        f'font-size="10">también manejo</text>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Stack: {esc(', '.join(t for t, _ in TECHS))}">
{panel(W, H, "stack", f"{len(TECHS)} tecnologías")}
{"".join(piezas)}
{leyenda}
</svg>
"""


if __name__ == "__main__":
    write(Path(__file__).resolve().parent.parent / "art" / "stack.svg", build())

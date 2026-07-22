"""art/timemaster.svg — tarjeta a ancho completo del proyecto estrella.

Antes era una tarjeta de 370 al lado de una columna de texto en el README,
y el texto quedaba mucho mas alto que la tarjeta. Metiendo las specs dentro
del propio SVG el bloque queda equilibrado por construccion, y de paso las
specs tambien se pueden animar.
"""
from pathlib import Path

from _style import (ACCENT, BG, GREEN, INK, INK_LOW, INK_MID, LINE, MONO,
                    PANEL, esc, panel, write)

W, H = 860, 300

# Columna izquierda: maquina de estados. Derecha: specs.
COL_X = 400

STATES = [("Pendiente", False), ("En curso", False),
          ("En revisión", False), ("Completada", True)]

SPECS = [
    ("API",    "Spring Boot 3 · arquitectura en capas · DTOs · HikariCP"),
    ("Datos",  "PostgreSQL a través de Spring Data JPA"),
    ("Acceso", "Roles Manager / Operario con Spring Security"),
    ("UI",     "Angular 17 standalone · Tailwind · validación en tiempo real"),
]

CHIPS = ["Java 17", "Spring Boot 3", "Angular 17", "PostgreSQL", "Spring Security"]

CYCLE = 6.0
STEP = 1.1


def build() -> str:
    partes = []

    # ── Maquina de estados (izquierda) ──────────────────────────────────
    y0, gap = 92, 42
    off = (CYCLE - 0.6) / CYCLE

    partes.append(
        f'<text x="30" y="66" fill="{INK_LOW}" font-family="{MONO}" font-size="10.5">'
        f'TaskState — validado en el servidor</text>'
    )

    for i, (label, ok) in enumerate(STATES):
        y = y0 + i * gap
        on = (i * STEP) / CYCLE
        color = GREEN if ok else ACCENT
        kt = f"0;{on:.4f};{on + 0.02:.4f};{off:.4f};{off + 0.03:.4f};1"

        if i < len(STATES) - 1:
            a, b = y + 8, y + gap - 12
            partes.append(
                f'<line x1="46" y1="{a}" x2="46" y2="{b}" stroke="{LINE}" stroke-width="1.5"/>'
                f'<line x1="46" y1="{a}" x2="46" y2="{a}" stroke="{ACCENT}" stroke-width="1.5">'
                f'<animate attributeName="y2" values="{a};{a};{b};{b};{a};{a}" '
                f'keyTimes="0;{on:.4f};{on + 0.09:.4f};{off:.4f};{off + 0.03:.4f};1" '
                f'dur="{CYCLE}s" repeatCount="indefinite"/></line>'
            )

        partes.append(
            f'<circle cx="46" cy="{y}" r="7" fill="{BG}" stroke="{LINE}" stroke-width="1.5"/>'
            f'<circle cx="46" cy="{y}" r="7" fill="{color}">'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" '
            f'dur="{CYCLE}s" repeatCount="indefinite"/></circle>'
            f'<circle cx="46" cy="{y}" r="7" fill="none" stroke="{color}" stroke-width="1.5">'
            f'<animate attributeName="r" values="7;7;18;18" keyTimes="0;{on:.4f};{on + 0.12:.4f};1" '
            f'dur="{CYCLE}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0;0.75;0;0" '
            f'keyTimes="0;{on:.4f};{on + 0.01:.4f};{on + 0.12:.4f};1" '
            f'dur="{CYCLE}s" repeatCount="indefinite"/></circle>'
            f'<text x="70" y="{y + 4.5}" font-family="{MONO}" font-size="12.5" fill="{INK_LOW}">{esc(label)}'
            f'<animate attributeName="fill" values="{INK_LOW};{INK_LOW};{INK};{INK};{INK_LOW};{INK_LOW}" '
            f'keyTimes="{kt}" dur="{CYCLE}s" repeatCount="indefinite"/></text>'
        )

    # Rama de rechazo
    y_rev = y0 + 2 * gap
    partes.append(
        f'<path d="M 46 {y_rev} L 46 {y_rev + 20} L 250 {y_rev + 20}" fill="none" '
        f'stroke="{LINE}" stroke-width="1.5" stroke-dasharray="3 3"/>'
        f'<text x="258" y="{y_rev + 24}" fill="{INK_LOW}" font-family="{MONO}" font-size="11">Rechazada</text>'
    )

    # Separador vertical
    partes.append(f'<line x1="{COL_X - 26}" y1="52" x2="{COL_X - 26}" y2="{H - 52}" stroke="{LINE}"/>')

    # ── Specs (derecha), entran escalonadas ─────────────────────────────
    ys, delay = 74, 0.4
    for k, v in SPECS:
        partes.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.5s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="10 0" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.5s" fill="freeze"/>'
            f'<text x="{COL_X}" y="{ys}" fill="{ACCENT}" font-family="{MONO}" font-size="11.5" '
            f'font-weight="600">{esc(k)}</text>'
            f'<text x="{COL_X}" y="{ys + 18}" fill="{INK_MID}" font-family="{MONO}" '
            f'font-size="11">{esc(v)}</text>'
            f'</g>'
        )
        ys += 46
        delay += 0.16

    # ── Chips de stack, franja inferior a todo el ancho ─────────────────
    # Empiezan en el margen izquierdo: arrancando en COL_X la fila sumaba
    # 467px y el ultimo chip se salia de la tarjeta.
    cx, delay = 30, 1.3
    for c in CHIPS:
        w = len(c) * 6.6 + 16
        partes.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<rect x="{cx:.0f}" y="{H - 46}" width="{w:.0f}" height="21" rx="4" '
            f'fill="{PANEL}" stroke="{LINE}"/>'
            f'<text x="{cx + w / 2:.0f}" y="{H - 31}" text-anchor="middle" fill="{INK_MID}" '
            f'font-family="{MONO}" font-size="10">{esc(c)}</text>'
            f'</g>'
        )
        cx += w + 6
        delay += 0.08

    # ── Linea de barrido: recorre la tarjeta en bucle ───────────────────
    partes.append(
        f'<rect x="0" y="36" width="{W}" height="1.5" fill="url(#scan)" opacity="0.5">'
        f'<animate attributeName="y" values="36;{H - 2};36" dur="9s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;0.45;0.45;0" keyTimes="0;0.1;0.9;1" '
        f'dur="9s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="TimeMaster: plataforma full stack de gestión de tareas. Spring Boot 3, Angular 17, PostgreSQL. Calificado 10 sobre 10, 119 commits.">
<defs>
  <linearGradient id="scan" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0"    stop-color="{ACCENT}" stop-opacity="0"/>
    <stop offset="0.5"  stop-color="{ACCENT}" stop-opacity="1"/>
    <stop offset="1"    stop-color="{ACCENT}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="10"/></clipPath>
</defs>

{panel(W, H, "TimeMaster", "10/10  ·  119 commits")}
<g clip-path="url(#card)">
{"".join(partes)}
</g>
</svg>
"""


if __name__ == "__main__":
    write(Path(__file__).resolve().parent.parent / "art" / "timemaster.svg", build())

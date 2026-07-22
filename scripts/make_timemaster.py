"""Genera art/timemaster.svg — la maquina de estados de TimeMaster.

El articulo original pone aqui un mapa de calor de contribuciones.
Con 55 dias activos de 367 ese grafico sale casi vacio y juega en tu
contra: una tarjeta que enseña un numero bajo hace mas daño que no
ponerla. Esto enseña lo que si tienes — el proyecto — y ademas nadie
mas lo lleva en su perfil.

La animacion recorre los estados como recorreria una tarea real.
"""
from pathlib import Path

W, H = 370, 330

BG      = "#0f0d0c"
PANEL   = "#141110"
LINE    = "#2a2523"
INK     = "#edeae5"
INK_MID = "#a49e97"
INK_LOW = "#8a847c"
ACCENT  = "#ff5a1f"
GREEN   = "#3fb950"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# (etiqueta, es_terminal_ok, es_terminal_ko)
STATES = [
    ("Pendiente",   False, False),
    ("En curso",    False, False),
    ("En revisión", False, False),
    ("Completada",  True,  False),
]

CYCLE = 6.0          # duracion del ciclo completo
STEP  = 1.2          # tiempo entre estados


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build() -> str:
    parts = []
    y0 = 78
    gap = 46

    # Un unico ciclo infinito por elemento, con values/keyTimes normalizados
    # sobre CYCLE. Antes encadenaba dos `begin` sueltos y la secuencia se
    # paraba tras dos vueltas, dejando la mitad de los nodos apagados.
    off = (CYCLE - 0.6) / CYCLE          # instante en que todo vuelve a cero

    for i, (label, ok, _ko) in enumerate(STATES):
        y = y0 + i * gap
        on = (i * STEP) / CYCLE          # instante en que se enciende este nodo
        color = GREEN if ok else ACCENT

        kt = f"0;{on:.4f};{on + 0.02:.4f};{off:.4f};{off + 0.03:.4f};1"

        # Conector hacia el siguiente estado
        if i < len(STATES) - 1:
            y_from, y_to = y + 8, y + gap - 12
            parts.append(
                f'<line x1="42" y1="{y_from}" x2="42" y2="{y_to}" stroke="{LINE}" stroke-width="1.5"/>'
                f'<line x1="42" y1="{y_from}" x2="42" y2="{y_from}" stroke="{ACCENT}" stroke-width="1.5">'
                f'<animate attributeName="y2" values="{y_from};{y_from};{y_to};{y_to};{y_from};{y_from}" '
                f'keyTimes="0;{on:.4f};{on + 0.09:.4f};{off:.4f};{off + 0.03:.4f};1" '
                f'dur="{CYCLE}s" repeatCount="indefinite"/>'
                f"</line>"
            )

        # Nodo: circulo vacio que se rellena cuando la tarea llega
        parts.append(
            f'<circle cx="42" cy="{y}" r="7" fill="{BG}" stroke="{LINE}" stroke-width="1.5"/>'
            f'<circle cx="42" cy="{y}" r="7" fill="{color}">'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" '
            f'dur="{CYCLE}s" repeatCount="indefinite"/>'
            f"</circle>"
            # halo en el momento exacto de activarse
            f'<circle cx="42" cy="{y}" r="7" fill="none" stroke="{color}" stroke-width="1.5">'
            f'<animate attributeName="r" values="7;7;18;18" keyTimes="0;{on:.4f};{on + 0.12:.4f};1" '
            f'dur="{CYCLE}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0;0.75;0;0" '
            f'keyTimes="0;{on:.4f};{on + 0.01:.4f};{on + 0.12:.4f};1" '
            f'dur="{CYCLE}s" repeatCount="indefinite"/>'
            f"</circle>"
        )

        # Etiqueta
        parts.append(
            f'<text x="68" y="{y + 4.5}" font-family="{MONO}" font-size="12.5" fill="{INK_LOW}">{esc(label)}'
            f'<animate attributeName="fill" values="{INK_LOW};{INK_LOW};{INK};{INK};{INK_LOW};{INK_LOW}" '
            f'keyTimes="{kt}" dur="{CYCLE}s" repeatCount="indefinite"/>'
            f"</text>"
        )

    # Rama de rechazo: sale de "En revisión" hacia la derecha
    y_rev = y0 + 2 * gap
    parts.append(
        f'<path d="M 42 {y_rev} L 42 {y_rev + 22} L 250 {y_rev + 22}" fill="none" '
        f'stroke="{LINE}" stroke-width="1.5" stroke-dasharray="3 3"/>'
        f'<text x="258" y="{y_rev + 26}" fill="{INK_LOW}" font-family="{MONO}" font-size="11">Rechazada</text>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="TimeMaster: flujo de estados de una tarea, validado en el servidor. Pendiente, En curso, En revisión, Completada o Rechazada.">
<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="10" fill="none" stroke="{LINE}"/>

<rect x="1" y="1" width="{W - 2}" height="34" rx="10" fill="{PANEL}"/>
<rect x="1" y="26" width="{W - 2}" height="9" fill="{PANEL}"/>
<line x1="0" y1="35" x2="{W}" y2="35" stroke="{LINE}"/>
<text x="26" y="23" fill="{INK}" font-family="{MONO}" font-size="12.5" font-weight="500">TimeMaster</text>
<text x="{W - 26}" y="23" text-anchor="end" fill="{ACCENT}" font-family="{MONO}" font-size="11">10/10</text>

<text x="26" y="58" fill="{INK_LOW}" font-family="{MONO}" font-size="10.5">TaskState — validado en backend</text>

{"".join(parts)}

<line x1="26" y1="{H - 42}" x2="{W - 26}" y2="{H - 42}" stroke="{LINE}"/>
<text x="26" y="{H - 20}" fill="{INK_LOW}" font-family="{MONO}" font-size="10.5">Spring Security · RBAC · 119 commits</text>
</svg>
"""


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "art" / "timemaster.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print(f"escrito {out}  ({out.stat().st_size / 1024:.1f} KB)")

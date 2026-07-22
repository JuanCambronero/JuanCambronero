"""Genera art/contrib-heatmap.svg a partir de data/contributions.json.

Rejilla de 53 semanas x 7 dias. La animacion entra en diagonal
(arriba-izquierda -> abajo-derecha), se reproduce una vez y se congela.

La rampa de color es la naranja de tu identidad, no el verde de GitHub:
el CV, la landing y las otras piezas usan el mismo acento.
"""
import json
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

W = 860
CELL, GAP = 12, 3
STEP = CELL + GAP                 # 15px por semana
PAD_L, PAD_T = 42, 52
H = PAD_T + 7 * STEP + 62

BG      = "#0f0d0c"
PANEL   = "#141110"
LINE    = "#2a2523"
INK     = "#edeae5"
INK_MID = "#a49e97"
INK_LOW = "#8a847c"
ACCENT  = "#ff5a1f"

# nivel 0..4 — el vacio es apenas mas claro que el fondo
RAMP = ["#1a1614", "#4a2410", "#8c3d15", "#c94d1a", "#ff5a1f"]

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
DIAS = {1: "Lun", 3: "Mié", 5: "Vie"}


def build(data: dict) -> str:
    days = data["days"]

    # Alinear la primera columna al dia de la semana real (lunes = 0)
    first = date.fromisoformat(days[0]["date"])
    offset = first.weekday()

    # Una animacion por SEMANA, no por dia: 53 en vez de 371. El navegador
    # tiene que planificar cada <animate> por separado, y con varios SVG
    # animados en la misma pagina el coste se nota.
    columnas: dict[int, list[str]] = {}
    months, seen = [], set()

    for i, d in enumerate(days):
        idx = i + offset
        wk, dow = idx // 7, idx % 7
        if wk > 52:
            break

        x = PAD_L + wk * STEP
        y = PAD_T + dow * STEP

        columnas.setdefault(wk, []).append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" '
            f'fill="{RAMP[d["level"]]}"/>'
        )

        # Etiqueta de mes la primera vez que aparece, en la fila superior
        m = date.fromisoformat(d["date"]).month
        if m not in seen and dow == 0 and wk < 51:
            seen.add(m)
            months.append(
                f'<text x="{x}" y="{PAD_T - 12}" fill="{INK_LOW}" '
                f'font-family="{MONO}" font-size="10">{MESES[m - 1]}</text>'
            )

    cells = [
        f'<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{0.15 + wk * 0.016:.2f}s" dur="0.45s" fill="freeze"/>'
        f'{"".join(rects)}'
        f'</g>'
        for wk, rects in sorted(columnas.items())
    ]

    day_labels = "".join(
        f'<text x="{PAD_L - 8}" y="{PAD_T + r * STEP + 9.5}" text-anchor="end" '
        f'fill="{INK_LOW}" font-family="{MONO}" font-size="9">{lab}</text>'
        for r, lab in DIAS.items()
    )

    # Leyenda
    lx = W - 200
    ly = H - 26
    legend = f'<text x="{lx - 8}" y="{ly + 9}" text-anchor="end" fill="{INK_LOW}" font-family="{MONO}" font-size="10">menos</text>'
    for i, c in enumerate(RAMP):
        legend += (f'<rect x="{lx + i * 15}" y="{ly}" width="11" height="11" rx="2.5" fill="{c}"/>')
    legend += (f'<text x="{lx + len(RAMP) * 15 + 4}" y="{ly + 9}" fill="{INK_LOW}" '
               f'font-family="{MONO}" font-size="10">más</text>')

    stats = (
        f'<text x="{PAD_L}" y="{H - 17}" font-family="{MONO}" font-size="11" fill="{INK_MID}">'
        f'<tspan fill="{ACCENT}" font-weight="500">{data["total"]}</tspan> contribuciones · '
        f'<tspan fill="{ACCENT}" font-weight="500">{data["active_days"]}</tspan> días activos · '
        f'mejor racha <tspan fill="{ACCENT}" font-weight="500">{data["best_streak"]}</tspan>'
        f'</text>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Mapa de contribuciones de {data['user']} del último año: {data['total']} contribuciones en {data['active_days']} días activos.">
<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="10" fill="none" stroke="{LINE}"/>

<rect x="1" y="1" width="{W - 2}" height="34" rx="10" fill="{PANEL}"/>
<rect x="1" y="26" width="{W - 2}" height="9" fill="{PANEL}"/>
<line x1="0" y1="35" x2="{W}" y2="35" stroke="{LINE}"/>
<text x="26" y="23" fill="{INK}" font-family="{MONO}" font-size="12.5" font-weight="500">contribuciones</text>
<text x="{W - 26}" y="23" text-anchor="end" fill="{INK_LOW}" font-family="{MONO}" font-size="11">{data['from']} → {data['to']}</text>

{"".join(months)}
{day_labels}
{"".join(cells)}
{legend}
{stats}
</svg>
"""


if __name__ == "__main__":
    src = ROOT / "data" / "contributions.json"
    if not src.exists():
        print("Falta data/contributions.json — ejecuta antes fetch_contributions.py", file=sys.stderr)
        sys.exit(1)

    data = json.loads(src.read_text(encoding="utf-8"))
    out = ROOT / "art" / "contrib-heatmap.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(data), encoding="utf-8")
    print(f"escrito {out}  ({out.stat().st_size / 1024:.1f} KB)")

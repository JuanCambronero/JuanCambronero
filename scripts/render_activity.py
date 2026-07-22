"""art/activity.svg — grafico de area de la actividad del año.

Equivale a github-readme-activity-graph, servido desde tu repo.
Se agrupa por semanas y se suaviza con una spline de Catmull-Rom
convertida a curvas de Bezier, que es como se dibuja una linea que
pasa exactamente por todos los puntos sin picos.
"""
import json
import sys
from datetime import date
from pathlib import Path

from _style import ACCENT, ACCENT_2, INK_LOW, INK_MID, LINE, MONO, esc, panel, write

ROOT = Path(__file__).resolve().parent.parent

W, H = 860, 240
PAD_L, PAD_R = 46, 26
PAD_T, PAD_B = 62, 44
PLOT_W = W - PAD_L - PAD_R
PLOT_H = H - PAD_T - PAD_B

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


def por_semana(days: list[dict]) -> list[tuple[str, int]]:
    semanas, actual, suma = [], None, 0
    for d in days:
        iso = date.fromisoformat(d["date"]).isocalendar()
        clave = (iso.year, iso.week)
        if clave != actual:
            if actual is not None:
                semanas.append((fecha_ini, suma))
            actual, suma, fecha_ini = clave, 0, d["date"]
        suma += d["count"]
    if actual is not None:
        semanas.append((fecha_ini, suma))
    return semanas


def spline(pts: list[tuple[float, float]]) -> str:
    """Catmull-Rom -> Bezier cubica. La curva pasa por todos los puntos."""
    if len(pts) < 2:
        return ""
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C {c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def build(data: dict) -> str:
    semanas = por_semana(data["days"])
    if not semanas:
        raise SystemExit("sin datos")

    pico = max(v for _, v in semanas) or 1
    n = len(semanas)

    pts = [
        (PAD_L + i * PLOT_W / max(n - 1, 1), PAD_T + PLOT_H - (v / pico) * PLOT_H)
        for i, (_, v) in enumerate(semanas)
    ]

    linea = spline(pts)
    area = f"{linea} L {pts[-1][0]:.1f},{PAD_T + PLOT_H} L {pts[0][0]:.1f},{PAD_T + PLOT_H} Z"

    # Rejilla horizontal
    grid = "".join(
        f'<line x1="{PAD_L}" y1="{PAD_T + PLOT_H * f:.0f}" x2="{W - PAD_R}" '
        f'y2="{PAD_T + PLOT_H * f:.0f}" stroke="{LINE}" stroke-dasharray="2 4"/>'
        for f in (0, 0.5, 1)
    )
    grid += (f'<text x="{PAD_L - 10}" y="{PAD_T + 4}" text-anchor="end" fill="{INK_LOW}" '
             f'font-family="{MONO}" font-size="9.5">{pico}</text>'
             f'<text x="{PAD_L - 10}" y="{PAD_T + PLOT_H + 4}" text-anchor="end" fill="{INK_LOW}" '
             f'font-family="{MONO}" font-size="9.5">0</text>')

    # Etiquetas de mes
    etiquetas, visto = [], set()
    for i, (f, _) in enumerate(semanas):
        m = date.fromisoformat(f).month
        if m not in visto:
            visto.add(m)
            x = PAD_L + i * PLOT_W / max(n - 1, 1)
            if PAD_L <= x <= W - PAD_R - 12:
                etiquetas.append(
                    f'<text x="{x:.0f}" y="{H - 24}" text-anchor="middle" fill="{INK_LOW}" '
                    f'font-family="{MONO}" font-size="9.5">{MESES[m - 1]}</text>'
                )

    # Puntos en los picos
    puntos = "".join(
        f'<circle cx="{pts[i][0]:.1f}" cy="{pts[i][1]:.1f}" r="3" fill="{ACCENT_2}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" begin="{1.6 + i * 0.01:.2f}s" '
        f'dur="0.4s" fill="freeze"/></circle>'
        for i, (_, v) in enumerate(semanas) if v >= pico * 0.55
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Actividad semanal del último año: {data['total']} contribuciones, pico de {pico} en una semana">
<defs>
  <linearGradient id="area" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.42"/>
    <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="reveal">
    <rect x="0" y="0" width="0" height="{H}">
      <animate attributeName="width" from="0" to="{W}" begin="0.25s" dur="1.5s" fill="freeze"/>
    </rect>
  </clipPath>
</defs>

{panel(W, H, "actividad semanal", f"pico {pico}")}
{grid}

<g clip-path="url(#reveal)">
  <path d="{area}" fill="url(#area)"/>
  <path d="{linea}" fill="none" stroke="{ACCENT}" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round"/>
</g>
{puntos}
{"".join(etiquetas)}

<text x="{PAD_L}" y="{H - 8}" fill="{INK_MID}" font-family="{MONO}" font-size="10.5">
  <tspan fill="{ACCENT}" font-weight="500">{data['total']}</tspan> contribuciones · <tspan fill="{ACCENT}" font-weight="500">{data['active_days']}</tspan> días activos · mejor racha <tspan fill="{ACCENT}" font-weight="500">{data['best_streak']}</tspan>
</text>
</svg>
"""


if __name__ == "__main__":
    src = ROOT / "data" / "contributions.json"
    if not src.exists():
        print("Falta data/contributions.json — ejecuta antes fetch_contributions.py", file=sys.stderr)
        sys.exit(1)
    write(ROOT / "art" / "activity.svg", build(json.loads(src.read_text(encoding="utf-8"))))

"""art/stats.svg y art/langs.svg — tarjetas de estadisticas.

Equivalen a github-readme-stats, servidas desde tu repo.

Nota deliberada: NO se muestran estrellas ni seguidores. Con 0 estrellas
esa cifra juega en contra; una tarjeta que enseña un numero bajo hace mas
daño que no ponerla. Se muestran contribuciones, repos y racha, que son
numeros reales y decentes.
"""
import json
import sys
from pathlib import Path

from _style import (ACCENT, ACCENT_2, INK, INK_LOW, INK_MID, LINE, MONO,
                    PANEL, esc, panel, write)

ROOT = Path(__file__).resolve().parent.parent

# Colores oficiales de cada lenguaje (los mismos que usa GitHub)
LANG_COLOR = {
    "Java": "#b07219", "TypeScript": "#3178c6", "HTML": "#e34c26",
    "CSS": "#563d7c", "Python": "#3572A5", "JavaScript": "#f1e05a",
    "Kotlin": "#A97BFF", "Shell": "#89e051", "Dockerfile": "#384d54",
}


def stats_card(st: dict, contrib: dict) -> str:
    W, H = 420, 200
    filas = [
        ("Contribuciones (año)", str(contrib["total"])),
        ("Días activos",         str(contrib["active_days"])),
        ("Mejor racha",          f'{contrib["best_streak"]} días'),
        ("Repositorios",         str(st["repos"])),
        ("Commits en TimeMaster", "119"),
    ]

    out, y, delay = [], 74, 0.3
    for k, v in filas:
        out.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.45s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="-6 0" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.45s" fill="freeze"/>'
            f'<text x="26" y="{y}" fill="{INK_MID}" font-family="{MONO}" font-size="12">{esc(k)}</text>'
            f'<text x="{W - 26}" y="{y}" text-anchor="end" fill="{ACCENT}" font-family="{MONO}" '
            f'font-size="15" font-weight="600">{esc(v)}</text>'
            f'</g>'
        )
        y += 25
        delay += 0.12

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Estadísticas: {contrib['total']} contribuciones, {contrib['active_days']} días activos, {st['repos']} repositorios">
{panel(W, H, "estadísticas", contrib["to"])}
{"".join(out)}
</svg>
"""


def langs_card(st: dict) -> str:
    W, H = 420, 200
    langs = st["languages"][:5]
    total = sum(l["pct"] for l in langs) or 1

    # Barra apilada
    barra, x = [], 26
    ancho_util = W - 52
    for i, l in enumerate(langs):
        w = ancho_util * l["pct"] / total
        c = LANG_COLOR.get(l["name"], ACCENT_2)
        barra.append(
            f'<rect x="{x:.1f}" y="62" width="0" height="11" fill="{c}">'
            f'<animate attributeName="width" from="0" to="{w:.1f}" '
            f'begin="{0.3 + i * 0.12:.2f}s" dur="0.6s" fill="freeze"/>'
            f'</rect>'
        )
        x += w

    filas, y = [], 104
    for i, l in enumerate(langs):
        c = LANG_COLOR.get(l["name"], ACCENT_2)
        delay = 0.5 + i * 0.1
        filas.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<circle cx="31" cy="{y - 4}" r="5" fill="{c}"/>'
            f'<text x="46" y="{y}" fill="{INK_MID}" font-family="{MONO}" font-size="12">{esc(l["name"])}</text>'
            f'<text x="{W - 26}" y="{y}" text-anchor="end" fill="{INK_LOW}" font-family="{MONO}" '
            f'font-size="12">{l["pct"]}%</text>'
            f'</g>'
        )
        y += 21

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Lenguajes más usados: {esc(', '.join(l['name'] for l in langs))}">
{panel(W, H, "lenguajes", f"{st['repos']} repos")}
<rect x="26" y="62" width="{W - 52}" height="11" rx="5.5" fill="{PANEL}"/>
<g clip-path="url(#barra)">{"".join(barra)}</g>
<defs><clipPath id="barra"><rect x="26" y="62" width="{W - 52}" height="11" rx="5.5"/></clipPath></defs>
{"".join(filas)}
</svg>
"""


if __name__ == "__main__":
    s = ROOT / "data" / "stats.json"
    c = ROOT / "data" / "contributions.json"
    if not (s.exists() and c.exists()):
        print("Faltan datos: ejecuta fetch_stats.py y fetch_contributions.py", file=sys.stderr)
        sys.exit(1)

    st = json.loads(s.read_text(encoding="utf-8"))
    contrib = json.loads(c.read_text(encoding="utf-8"))

    write(ROOT / "art" / "stats.svg", stats_card(st, contrib))
    write(ROOT / "art" / "langs.svg", langs_card(st))

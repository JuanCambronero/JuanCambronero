"""art/about.svg y art/about-movil.svg — el texto de "Sobre mí", animado.

Criterio de la animacion: el texto NO se teclea. Doce lineas de prosa con
efecto maquina de escribir se hacen lentas y molestan al leer.

Lo que se anima es el RITMO DE LA NARRACION: los parrafos entran al paso
al que se leen, y el giro de la historia ("se acabo el acceso") llega tras
una pausa y con su propia marca. La animacion refuerza lo que cuenta el
texto en vez de decorarlo.

Dos versiones desde el MISMO texto: en un movil el SVG de 860 se sirve a
~308px (36%), y 13.5px se quedan en menos de 5px reales. La version
estrecha reajusta las lineas para que se lea. El README las combina con
<picture> y una media query.
"""
from pathlib import Path

from _style import (ACCENT, INK, INK_LOW, INK_MID, LINE, MONO, SANS,
                    esc, panel, wrap, write)

# (texto, tipo) — tipo: "n" normal · "giro" inflexion · "clave" remate
# Los tramos entre | van en color de acento: son los datos verificables.
PARRAFOS = [
    ("Hice mis prácticas en |Viewnext (Grupo IBM)|, en el área que trabaja con "
     "|IBM Maximo| — la plataforma con la que las grandes empresas gestionan sus "
     "activos y el trabajo de sus equipos de mantenimiento.", "n"),

    ("Me enganchó cómo estaba pensada. Los flujos de estado. Los roles. "
     "Cada pieza en su sitio.", "n"),

    ("Cuando acabaron las prácticas, se acabó el acceso.", "giro"),

    ("No intenté clonar Maximo. Habría sido ridículo: es enorme, lleva años de "
     "trabajo de mucha gente detrás y hace cosas que yo todavía ni entiendo. Cogí "
     "una sola idea —cómo organiza el trabajo de un equipo— y construí algo "
     "enfocado solo en eso.", "n"),

    ("Eso es |TimeMaster|: Spring Boot 3 detrás, Angular 17 delante, PostgreSQL "
     "debajo. |119 commits|, sin compañeros de equipo. Fue mi Proyecto Final de "
     "Ciclo y sacó un |10/10|.", "clave"),

    ("Me titulé en Desarrollo de Aplicaciones Multiplataforma en junio de 2026 y "
     "ahora curso Ingeniería Informática en la |UNED|. Al ser a distancia, tengo "
     "|plena disponibilidad para jornada completa|.", "n"),
]

CIERRE = ("Lo que se me da bien: coger un problema, entender el dominio que hay "
          "detrás y construirlo entero.")


def tspans(linea: str) -> str:
    """'texto |resaltado| texto' -> tspans con color de acento."""
    out = []
    for i, tramo in enumerate(linea.split("|")):
        if not tramo:
            continue
        if i % 2:
            out.append(f'<tspan fill="{ACCENT}" font-weight="600">{esc(tramo)}</tspan>')
        else:
            out.append(esc(tramo))
    return "".join(out)


def build(W: int, pad: int, cpl: int, size: float, size_giro: float,
          lh: int, gap: int, size_cierre: float, color_cierre: str = INK_LOW) -> str:
    """cpl = caracteres por linea. Todo lo demas escala con el ancho."""
    partes = []
    y = 62
    delay = 0.35

    for texto, tipo in PARRAFOS:
        lineas = wrap(texto, cpl)
        alto = len(lineas) * lh

        # El giro respira antes y despues: es el punto de inflexion.
        if tipo == "giro":
            delay += 0.45
            y += 6

        grupo = [
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" '
            f'dur="0.65s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 7" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.65s" fill="freeze"/>'
        ]

        if tipo == "giro":
            grupo.append(
                f'<rect x="{pad - 13}" y="{y - 13}" width="2.5" height="0" fill="{ACCENT}">'
                f'<animate attributeName="height" from="0" to="{alto - 2}" '
                f'begin="{delay + 0.25:.2f}s" dur="0.5s" fill="freeze"/></rect>'
            )

        fs = size_giro if tipo == "giro" else size
        color = INK if tipo in ("giro", "clave") else INK_MID
        peso = "600" if tipo == "giro" else "400"

        for k, ln in enumerate(lineas):
            grupo.append(
                f'<text x="{pad}" y="{y + k * lh}" fill="{color}" font-family="{SANS}" '
                f'font-size="{fs}" font-weight="{peso}">{tspans(ln)}</text>'
            )

        partes.append(f'<g opacity="0">{"".join(grupo)}</g>')

        y += alto + gap
        delay += 0.28 + len(lineas) * 0.16
        if tipo == "giro":
            y += 6

    # Cierre, separado por una regla que se dibuja sola
    y += 4
    partes.append(
        f'<line x1="{pad}" y1="{y - 8}" x2="{pad}" y2="{y - 8}" stroke="{LINE}">'
        f'<animate attributeName="x2" from="{pad}" to="{W - pad}" begin="{delay:.2f}s" '
        f'dur="0.8s" fill="freeze"/></line>'
    )
    cierre_lineas = wrap(CIERRE, int(cpl * 1.05))
    grupo = [
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay + 0.3:.2f}s" '
        f'dur="0.6s" fill="freeze"/>'
    ]
    for k, ln in enumerate(cierre_lineas):
        grupo.append(
            f'<text x="{pad}" y="{y + 14 + k * (lh - 3)}" fill="{color_cierre}" '
            f'font-family="{MONO}" font-size="{size_cierre}">{esc(ln)}</text>'
        )
    partes.append(f'<g opacity="0">{"".join(grupo)}</g>')

    H = int(y + 14 + len(cierre_lineas) * (lh - 3) + 22)

    # El texto completo va en aria-label: los lectores de pantalla y las
    # herramientas de busqueda siguen teniendo acceso a lo que dice.
    plano = " ".join(t.replace("|", "") for t, _ in PARRAFOS) + " " + CIERRE

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(plano)}">
{panel(W, H, "sobre-mi.md")}
{"".join(partes)}
</svg>
"""


if __name__ == "__main__":
    art = Path(__file__).resolve().parent.parent / "art"

    # Escritorio: 860px de ancho real
    write(art / "about.svg",
          build(W=860, pad=32, cpl=96, size=13.5, size_giro=15,
                lh=21, gap=13, size_cierre=12))

    # Movil: 380px. Se sirve a ~308px (81%), asi que 13px quedan en ~10.5px.
    # El cierre sube a INK_MID: a este tamaño el gris bajo ya no se lee.
    write(art / "about-movil.svg",
          build(W=380, pad=18, cpl=44, size=13, size_giro=14,
                lh=19, gap=12, size_cierre=11.5, color_cierre=INK_MID))

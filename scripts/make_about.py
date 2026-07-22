"""art/about.svg — el texto de "Sobre mí", animado.

Criterio de la animacion: el texto NO se teclea. Doce lineas de prosa
con efecto maquina de escribir se hacen lentas y molestan al leer.

Lo que se anima es el RITMO DE LA NARRACION: los parrafos entran al paso
al que se leen, y el giro de la historia ("se acabo el acceso") llega
tras una pausa y con su propia marca. La animacion refuerza lo que
cuenta el texto en vez de decorarlo.
"""
from pathlib import Path

from _style import ACCENT, INK, INK_LOW, INK_MID, LINE, MONO, SANS, esc, panel, write

W = 860
PAD = 32
LH = 21               # alto de linea
GAP = 13              # separacion entre parrafos

# Cada parrafo: (lineas, tipo)
#   tipo "n" normal · "giro" el punto de inflexion · "clave" el remate
# Los tramos entre | se pintan en acento: son los datos verificables.
PARRAFOS = [
    (["Hice mis prácticas en |Viewnext (Grupo IBM)|, en el área que trabaja con |IBM Maximo| — la plataforma con la que",
      "las grandes empresas gestionan sus activos y el trabajo de sus equipos de mantenimiento."], "n"),

    (["Me enganchó cómo estaba pensada. Los flujos de estado. Los roles. Cada pieza en su sitio."], "n"),

    (["Cuando acabaron las prácticas, se acabó el acceso."], "giro"),

    (["No intenté clonar Maximo. Habría sido ridículo: es enorme, lleva años de trabajo de mucha gente detrás",
      "y hace cosas que yo todavía ni entiendo. Cogí una sola idea —cómo organiza el trabajo de un equipo—",
      "y construí algo enfocado solo en eso."], "n"),

    (["Eso es |TimeMaster|: Spring Boot 3 detrás, Angular 17 delante, PostgreSQL debajo. |119 commits|, sin",
      "compañeros de equipo. Fue mi Proyecto Final de Ciclo y sacó un |10/10|."], "clave"),

    (["Me titulé en Desarrollo de Aplicaciones Multiplataforma en junio de 2026 y ahora curso Ingeniería",
      "Informática en la |UNED|. Al ser a distancia, tengo |plena disponibilidad para jornada completa|."], "n"),
]

CIERRE = "Lo que se me da bien: coger un problema, entender el dominio que hay detrás y construirlo entero."


def tspans(linea: str) -> str:
    """Convierte 'texto |resaltado| texto' en tspans con color de acento."""
    out = []
    for i, tramo in enumerate(linea.split("|")):
        if not tramo:
            continue
        if i % 2:
            out.append(f'<tspan fill="{ACCENT}" font-weight="600">{esc(tramo)}</tspan>')
        else:
            out.append(esc(tramo))
    return "".join(out)


def build() -> str:
    partes = []
    y = 64
    delay = 0.35

    for lineas, tipo in PARRAFOS:
        alto = len(lineas) * LH

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

        # Marca de acento a la izquierda del giro, que se dibuja hacia abajo
        if tipo == "giro":
            grupo.append(
                f'<rect x="{PAD - 14}" y="{y - 14}" width="2.5" height="0" fill="{ACCENT}">'
                f'<animate attributeName="height" from="0" to="{alto - 2}" '
                f'begin="{delay + 0.25:.2f}s" dur="0.5s" fill="freeze"/></rect>'
            )

        size = 15 if tipo == "giro" else 13.5
        color = INK if tipo in ("giro", "clave") else INK_MID
        peso = "600" if tipo == "giro" else "400"

        for k, ln in enumerate(lineas):
            grupo.append(
                f'<text x="{PAD}" y="{y + k * LH}" fill="{color}" font-family="{SANS}" '
                f'font-size="{size}" font-weight="{peso}">{tspans(ln)}</text>'
            )

        partes.append(f'<g opacity="0">{"".join(grupo)}</g>')

        y += alto + GAP
        delay += 0.28 + len(lineas) * 0.16
        if tipo == "giro":
            y += 6

    # Cierre, separado por una regla que se dibuja sola
    y += 6
    partes.append(
        f'<line x1="{PAD}" y1="{y - 8}" x2="{PAD}" y2="{y - 8}" stroke="{LINE}">'
        f'<animate attributeName="x2" from="{PAD}" to="{W - PAD}" begin="{delay:.2f}s" '
        f'dur="0.8s" fill="freeze"/></line>'
    )
    partes.append(
        f'<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay + 0.3:.2f}s" '
        f'dur="0.6s" fill="freeze"/>'
        f'<text x="{PAD}" y="{y + 16}" fill="{INK_LOW}" font-family="{MONO}" '
        f'font-size="12">{esc(CIERRE)}</text>'
        f'</g>'
    )

    H = int(y + 44)

    # El texto completo va en aria-label: asi los lectores de pantalla y las
    # herramientas de busqueda siguen teniendo acceso a lo que dice.
    plano = " ".join(
        " ".join(l.replace("|", "") for l in lineas) for lineas, _ in PARRAFOS
    ) + " " + CIERRE

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(plano)}">
{panel(W, H, "sobre-mi.md")}
{"".join(partes)}
</svg>
"""


if __name__ == "__main__":
    write(Path(__file__).resolve().parent.parent / "art" / "about.svg", build())

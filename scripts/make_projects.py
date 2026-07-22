"""art/proj-*.svg — una tarjeta animada por proyecto.

Un archivo por proyecto y no una rejilla unica: GitHub sirve los SVG del
README dentro de un <img>, donde los <a> internos no son clicables. Con
un archivo por tarjeta se puede envolver cada una en su enlace.

Los textos salen de los README reales de cada repo, no inventados.
"""
from pathlib import Path

from _style import (ACCENT, INK, INK_LOW, INK_MID, LINE, MONO, PANEL,
                    esc, panel, write)

W, H = 420, 172

# (id, titulo, subtitulo, lineas de descripcion, chips, nota)
PROYECTOS = [
    (
        "secmec", "SecMec", "Sistema de gestión clínica",
        ["Aplicación Java de consola que modela un centro",
         "médico: personal sanitario, pacientes e historial",
         "clínico con recetas y pruebas médicas."],
        ["Java", "POO", "Herencia", "MVC"],
        "Modelo de dominio con 10 clases",
    ),
    (
        "basketworld", "BasketWorld", "Web de baloncesto y tienda",
        ["Página web sobre baloncesto con tienda online:",
         "catálogo de productos, filtros, menús y",
         "contenido sobre normas y jugadores."],
        ["HTML5", "CSS3", "JavaScript"],
        "Frontend íntegro, sin frameworks",
    ),
    (
        "colegio", "Sistema Gestión Colegio", "Práctica de POO en Python",
        ["Gestión escolar por consola: alumnos, profesores,",
         "grupos, asignaturas y calificaciones, con altas,",
         "bajas y búsquedas."],
        ["Python", "POO", "CRUD"],
        "Interfaz interactiva de consola",
    ),
    (
        "hormigas", "Simulación de Hormigas", "Algoritmo de colonia",
        ["Simulación en Java del comportamiento colectivo",
         "de una colonia de hormigas sobre una cuadrícula."],
        ["Java", "Simulación", "Estructuras"],
        "",
    ),
]


def build(titulo: str, sub: str, lineas: list[str], chips: list[str], nota: str) -> str:
    partes = []

    # Subtitulo
    partes.append(
        f'<text x="26" y="60" fill="{ACCENT}" font-family="{MONO}" font-size="11">{esc(sub)}</text>'
    )

    # Descripcion, linea a linea con barrido de izquierda a derecha
    clips = []
    y, delay = 84, 0.35
    for i, ln in enumerate(lineas):
        ancho = len(ln) * 6.4 + 10
        clips.append(
            f'<clipPath id="l{i}"><rect x="26" y="{y - 12}" width="0" height="18">'
            f'<animate attributeName="width" from="0" to="{ancho:.0f}" begin="{delay:.2f}s" '
            f'dur="0.5s" fill="freeze"/></rect></clipPath>'
        )
        partes.append(
            f'<text x="26" y="{y}" clip-path="url(#l{i})" fill="{INK_MID}" '
            f'font-family="{MONO}" font-size="10.5" xml:space="preserve">{esc(ln)}</text>'
        )
        y += 16
        delay += 0.16

    # Chips
    cx, cdelay = 26, delay + 0.1
    for c in chips:
        w = len(c) * 6.2 + 15
        partes.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{cdelay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 4" to="0 0" '
            f'begin="{cdelay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<rect x="{cx:.0f}" y="{H - 52}" width="{w:.0f}" height="20" rx="4" '
            f'fill="{PANEL}" stroke="{LINE}"/>'
            f'<text x="{cx + w / 2:.0f}" y="{H - 38}" text-anchor="middle" fill="{INK_MID}" '
            f'font-family="{MONO}" font-size="9.5">{esc(c)}</text>'
            f'</g>'
        )
        cx += w + 5
        cdelay += 0.09

    if nota:
        partes.append(
            f'<text x="26" y="{H - 14}" fill="{INK_LOW}" font-family="{MONO}" font-size="9.5" '
            f'opacity="0">{esc(nota)}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{cdelay + 0.1:.2f}s" '
            f'dur="0.5s" fill="freeze"/></text>'
        )

    # Barra de acento que crece en el borde inferior
    partes.append(
        f'<rect x="0" y="{H - 3}" width="0" height="3" fill="{ACCENT}" opacity="0.75">'
        f'<animate attributeName="width" from="0" to="{W}" begin="0.2s" dur="1.4s" fill="freeze"/>'
        f'</rect>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(titulo)}: {esc(sub)}. {esc(' '.join(lineas))}">
<defs>{"".join(clips)}<clipPath id="c"><rect width="{W}" height="{H}" rx="10"/></clipPath></defs>
{panel(W, H, titulo)}
<g clip-path="url(#c)">{"".join(partes)}</g>
</svg>
"""


if __name__ == "__main__":
    art = Path(__file__).resolve().parent.parent / "art"
    for pid, titulo, sub, lineas, chips, nota in PROYECTOS:
        write(art / f"proj-{pid}.svg", build(titulo, sub, lineas, chips, nota))

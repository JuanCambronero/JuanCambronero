"""art/typing.svg — texto que se teclea y se borra, en bucle.

Equivale a readme-typing-svg, servido desde tu repo.

Cada linea ocupa una franja del ciclo. Dentro de su franja: se escribe
(clip que se ensancha), se mantiene, y se borra. Fuera de su franja su
opacidad es 0. Todo con values/keyTimes normalizados sobre el ciclo, que
es la forma fiable de encadenar animaciones SMIL sin que se descuadren.
"""
from pathlib import Path

from _style import ACCENT, INK, INK_MID, MONO, esc, write

W, H = 700, 54
CHAR = 8.4                       # ancho aproximado por caracter a 15px

# Sin rayas largas (—): en monoespaciada ocupan mas de un caracter y
# descuadran el calculo de ancho, que es lo que coloca el cursor.
LINEAS = [
    "Java 17 + Spring Boot 3 + Angular 17",
    "Construí TimeMaster: 119 commits, 10/10",
    "Ex-Viewnext (Grupo IBM) - IBM Maximo / EAM",
    "Del modelo de datos a la pantalla",
]

SLOT = 3.4                       # segundos por linea
CICLO = SLOT * len(LINEAS)


def build() -> str:
    clips, textos = [], []

    for i, txt in enumerate(LINEAS):
        ancho = len(txt) * CHAR
        x0 = (W - ancho) / 2             # centrado, como readme-typing-svg
        t0 = i * SLOT / CICLO            # inicio de su franja (0..1)
        t1 = (i + 1) * SLOT / CICLO      # fin

        # Dentro de la franja: 25% escribir, 55% mantener, 20% borrar
        esc_ini, esc_fin = t0, t0 + (t1 - t0) * 0.25
        bor_ini, bor_fin = t0 + (t1 - t0) * 0.80, t1

        # El recorte arranca donde arranca el texto; si no, se come el final.
        # +8px de margen: CHAR es una estimacion y una fuente algo mas ancha
        # cortaria el ultimo glifo. Revelar de mas no se nota; de menos, si.
        clips.append(
            f'<clipPath id="c{i}">'
            f'<rect x="{x0:.1f}" y="0" height="{H}" width="0">'
            f'<animate attributeName="width" '
            f'values="0;0;{ancho + 8:.0f};{ancho + 8:.0f};0;0" '
            f'keyTimes="0;{esc_ini:.4f};{esc_fin:.4f};{bor_ini:.4f};{bor_fin:.4f};1" '
            f'dur="{CICLO}s" repeatCount="indefinite"/>'
            f'</rect></clipPath>'
        )

        # calcMode="discrete" es imprescindible: por defecto SMIL INTERPOLA
        # entre fotogramas, asi que la linea siguiente se iba desvaneciendo
        # hacia dentro desde el segundo cero y se veian dos a la vez.
        textos.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" values="0;1;0" '
            f'keyTimes="0;{t0:.4f};{t1:.4f}" calcMode="discrete" '
            f'dur="{CICLO}s" repeatCount="indefinite"/>'
            f'<text x="{W / 2:.0f}" y="34" text-anchor="middle" clip-path="url(#c{i})" '
            f'fill="{INK}" font-family="{MONO}" font-size="15" font-weight="500" '
            f'xml:space="preserve">{esc(txt)}</text>'
            f'<rect x="{x0:.1f}" y="21" width="9" height="17" fill="{ACCENT}">'
            f'<animate attributeName="x" '
            f'values="{x0:.1f};{x0:.1f};{x0 + ancho:.1f};{x0 + ancho:.1f};{x0:.1f};{x0:.1f}" '
            f'keyTimes="0;{esc_ini:.4f};{esc_fin:.4f};{bor_ini:.4f};{bor_fin:.4f};1" '
            f'dur="{CICLO}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;0;1" dur="1.05s" repeatCount="indefinite"/>'
            f'</rect>'
            f'</g>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(' — '.join(LINEAS))}">
<defs>{"".join(clips)}</defs>
{"".join(textos)}
</svg>
"""


if __name__ == "__main__":
    write(Path(__file__).resolve().parent.parent / "art" / "typing.svg", build())

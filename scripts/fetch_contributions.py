"""Descarga las contribuciones publicas y las guarda en data/contributions.json.

Usa el endpoint HTML publico de GitHub — no hace falta token:
    https://github.com/users/<usuario>/contributions
"""
import json
import re
import sys
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

USER = "JuanCambronero"
ROOT = Path(__file__).resolve().parent.parent


def fetch(user: str) -> str:
    req = urllib.request.Request(
        f"https://github.com/users/{user}/contributions",
        headers={"User-Agent": "Mozilla/5.0 (profile-art)"},
    )
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def parse(html: str) -> list[dict]:
    """Cada dia es un <td data-date=... data-level=... id=...>, y el recuento
    exacto vive en un <tool-tip for="ese-id"> aparte:

        <td data-date="2026-02-02" data-level="2" id="contribution-day-...">
        <tool-tip for="contribution-day-...">16 contributions on February 2nd.</tool-tip>

    Ojo al orden de atributos: data-date puede ir antes o despues del id,
    asi que se extrae cada <td> entero y luego se leen sus atributos."""
    counts = {}
    for tid, txt in re.findall(r"<tool-tip[^>]*\bfor=\"([^\"]+)\"[^>]*>(.*?)</tool-tip>", html, re.S):
        m = re.search(r"(\d+)\s+contribution", txt)
        counts[tid] = int(m.group(1)) if m else 0

    out = []
    for td in re.findall(r"<td[^>]*class=\"[^\"]*ContributionCalendar-day[^\"]*\"[^>]*>", html):
        d = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', td)
        lvl = re.search(r'data-level="(\d+)"', td)
        tid = re.search(r'id="([^"]+)"', td)
        if not (d and lvl):
            continue
        out.append({
            "date": d.group(1),
            "level": int(lvl.group(1)),
            "count": counts.get(tid.group(1) if tid else "", 0),
        })

    out.sort(key=lambda x: x["date"])
    return out


def summarise(days: list[dict]) -> dict:
    total = sum(d["count"] for d in days)
    active = [d for d in days if d["level"] > 0]

    best = cur = 0
    for d in days:
        cur = cur + 1 if d["level"] > 0 else 0
        best = max(best, cur)

    streak = 0
    for d in reversed(days):
        if d["level"] > 0:
            streak += 1
        else:
            break

    return {
        "user": USER,
        "generated": date.today().isoformat(),
        "from": days[0]["date"] if days else None,
        "to": days[-1]["date"] if days else None,
        "total": total,
        "active_days": len(active),
        "best_streak": best,
        "current_streak": streak,
        "by_level": dict(sorted(Counter(d["level"] for d in days).items())),
        "days": days,
    }


if __name__ == "__main__":
    days = parse(fetch(USER))
    if not days:
        print("No pude leer las contribuciones; dejo el JSON anterior.", file=sys.stderr)
        sys.exit(0)                      # no rompemos el workflow por esto

    data = summarise(days)
    out = ROOT / "data" / "contributions.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1), encoding="utf-8")

    print(f"{len(days)} dias  ·  {data['total']} contribuciones  ·  "
          f"{data['active_days']} dias activos  ·  mejor racha {data['best_streak']}")
    print(f"escrito {out}")

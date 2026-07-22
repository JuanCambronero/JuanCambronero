"""Descarga estadisticas publicas del perfil -> data/stats.json

Sin token: la API publica de GitHub permite 60 peticiones/hora por IP,
de sobra para una ejecucion diaria.
"""
import json
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

USER = "JuanCambronero"
ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com"


def get(url: str):
    req = urllib.request.Request(
        url, headers={"User-Agent": "profile-art", "Accept": "application/vnd.github+json"}
    )
    return json.load(urllib.request.urlopen(req, timeout=20))


def main() -> None:
    try:
        user = get(f"{API}/users/{USER}")
        repos = get(f"{API}/users/{USER}/repos?per_page=100&sort=pushed")
    except urllib.error.URLError as e:
        print(f"API no disponible ({e}); conservo data/stats.json anterior.", file=sys.stderr)
        return

    # Bytes por lenguaje, sumando todos los repos propios (sin forks)
    langs: Counter[str] = Counter()
    for r in repos:
        if r.get("fork"):
            continue
        try:
            for lang, n in get(r["languages_url"]).items():
                langs[lang] += n
        except Exception:
            continue

    total_bytes = sum(langs.values()) or 1
    top = [
        {"name": k, "pct": round(100 * v / total_bytes, 1)}
        for k, v in langs.most_common(6)
    ]

    own = [r for r in repos if not r.get("fork")]
    data = {
        "user": USER,
        "generated": date.today().isoformat(),
        "repos": user.get("public_repos", 0),
        "followers": user.get("followers", 0),
        "stars": sum(r.get("stargazers_count", 0) for r in own),
        "languages": top,
        "recent": [
            {
                "name": r["name"],
                "desc": (r.get("description") or "")[:70],
                "lang": r.get("language") or "—",
                "stars": r.get("stargazers_count", 0),
            }
            for r in own[:5]
        ],
    }

    out = ROOT / "data" / "stats.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1), encoding="utf-8")

    print(f"repos={data['repos']}  seguidores={data['followers']}  estrellas={data['stars']}")
    print("lenguajes:", ", ".join(f"{l['name']} {l['pct']}%" for l in top))
    print(f"escrito {out}")


if __name__ == "__main__":
    main()

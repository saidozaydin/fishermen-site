"""Builds the static site in docs/ from the page bodies in src/.

Each src/<page>.html starts with a small header, then a line with three dashes, then the
page body (plain HTML):

    title: Privacy Policy
    description: One sentence for search results.
    ---
    <h1>...</h1>

src/index.html becomes docs/index.html; any other src/<name>.html becomes
docs/<name>/index.html, so the address is https://saidozaydin.github.io/fishermen-site/<name>/.
Run:  python build.py
"""

from pathlib import Path
import html

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
SITE = "https://saidozaydin.github.io/fishermen-site/"
APP = "Fishermen: Pixel Fishing Game"

NAV = [("privacy", "Privacy"), ("terms", "Terms"), ("support", "Support")]

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="{base}assets/img/icon_192.png">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{site}assets/img/icon_play_512.png">
<meta name="theme-color" content="#1e2a80">
<link rel="stylesheet" href="{base}assets/site.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{base}"><img class="px" src="{base}assets/img/icon_192.png" alt="" width="36" height="36">Fishermen</a>
    <nav class="links" aria-label="Main">{nav}</nav>
  </div>
</header>
<main>
  <div class="wrap">
{body}
  </div>
</main>
<footer>
  <div class="wrap">
    <span>&copy; 2026 SaOz &middot; {app}</span>
    <span><a href="{base}privacy/">Privacy</a> &middot; <a href="{base}terms/">Terms</a> &middot; <a href="{base}support/">Support</a></span>
  </div>
</footer>
</body>
</html>
"""


def parse(path: Path) -> tuple[dict, str]:
    head, body = path.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = {}
    for line in head.strip().splitlines():
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body.strip("\n")


def build() -> None:
    pages = []
    for path in sorted(SRC.glob("*.html")):
        slug = path.stem
        meta, body = parse(path)
        if slug == "index":
            target, base, url = OUT / "index.html", "", SITE
        elif slug == "404":
            # GitHub Pages serves this at any depth, so it uses absolute links.
            target, base, url = OUT / "404.html", "/fishermen-site/", SITE + "404.html"
        else:
            target, base, url = OUT / slug / "index.html", "../", SITE + slug + "/"
        current = ' aria-current="page"'
        nav = "".join(
            f'<a href="{base}{s}/"{current if s == slug else ""}>{label}</a>'
            for s, label in NAV
        )
        body = "\n".join("    " + line if line else "" for line in body.splitlines())
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            TEMPLATE.format(
                title=html.escape(meta["title"]),
                description=html.escape(meta["description"]),
                url=url, base=base, site=SITE, nav=nav, body=body, app=html.escape(APP),
            ),
            encoding="utf-8", newline="\n",
        )
        if slug != "404":
            pages.append(url)
        print("wrote", target.relative_to(ROOT))

    urls = "\n".join(f"  <url><loc>{u}</loc></url>" for u in pages)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8", newline="\n",
    )
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n",
                                    encoding="utf-8", newline="\n")
    (OUT / ".nojekyll").touch()


if __name__ == "__main__":
    build()

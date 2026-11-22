# Fishermen: Pixel Fishing Game — website

Public privacy policy, terms of use and support pages for the Android game
Fishermen (`com.saoz.fishermen`), needed for the Google Play listing.

Site: https://saidozaydin.github.io/fishermen-site/

- Privacy Policy: https://saidozaydin.github.io/fishermen-site/privacy/
- Terms of Use: https://saidozaydin.github.io/fishermen-site/terms/
- Support: https://saidozaydin.github.io/fishermen-site/support/

## Editing

Page texts live in `src/*.html` (a short `title:` / `description:` header, a `---` line, then
the HTML body). The shared header, footer and navigation are in `build.py`. After editing run

```
python build.py
```

which regenerates `docs/` (plus `sitemap.xml` and `robots.txt`). Styles, the Pixelify Sans
font (SIL OFL 1.1, see `docs/assets/OFL.txt`) and images are in `docs/assets/`.
GitHub Pages serves the `/docs` folder of the `main` branch; pushing to `main` republishes the site.

Update the "Effective" date on the privacy policy and terms whenever their content changes
(for example before adding ads to the game).

The game's source code is not in this repository.

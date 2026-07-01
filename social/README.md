# ARI Data Center Playbook — social cards

Production set of campaign social graphics, matched to the live site
(datacenterplaybook.org) brand. Editable source + rendered PNGs.

## Files
- `cards.html` — the source. **All copy lives in the `CARDS` array** near the
  bottom; edit there and re-render. Each card renders at three sizes.
- `render.py` — Playwright renderer. Screenshots every `.card` at
  **deviceScaleFactor 2** to `output/`.
- `fonts.css` + `fonts/` — the brand webfonts, **self-hosted** as woff2 (see below).
- `assets/` — `ari-logo-white.svg` and `grid-1.jpg` (copied from the repo).
- `output/` — generated PNGs (gitignored; regenerate with `render.py`).

## Render
```
pip3 install playwright && python3 -m playwright install chromium   # one time
python3 render.py                                                   # -> output/
```
Output is named `{card}_{size}.png`, e.g. `2-proof-wi_1200x675.png`.

## Sizes (each card exported in all three, at 2x)
- `1200x675` — X / Twitter
- `1200x627` — LinkedIn
- `1080x1080` — Instagram / square

## Cards
1. `1-resident` — resident how-to
2. `2-proof-wi` — proof: Port Washington, WI (~1,000 signatures)
3. `3-stakes` — what's at stake (bills / grid / neighborhood)
4. `4-role` — find your role (role chips)
5. `5-proof-az` — proof: Pima County, AZ (90-day review)

## Brand assets used (extracted from the repo — nothing approximated)
- **Serif display (headlines/hero):** Fraunces
- **Sans (eyebrows/buttons/chips):** Archivo
- **Serif reading (subhead/italic kicker):** Newsreader
- **Colors:** navy `#151C42` → `#0e1330`, red `#D6234D`, bright text `#eef2f6`,
  muted light-blue text `#c3c7d2`
- **Logo:** `images/ari-logo-white.svg`
- **Background texture:** `images/grid-1.jpg` (transmission/substation), navy
  duotone at ~26% opacity behind a left-weighted scrim

## Note on assets — nothing was missing
Every brand asset was found in the repo and reused exactly; nothing was blocked
or approximated. The three fonts (Fraunces, Newsreader, Archivo) are open-source
(SIL OFL) families the site loads from Google Fonts; they are **self-hosted here
as woff2** so this folder renders offline and is fully portable. If ARI uses a
separately licensed brand typeface beyond these three, supply the file and it
can be swapped into `fonts.css`.

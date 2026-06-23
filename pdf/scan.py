#!/usr/bin/env python3
"""QA gate for the ARI PDFs. Run after pdf/build.py + Chrome render.
Programmatic checks + renders every page to pdf/_review/ for visual review.

  python3 pdf/scan.py

Exits non-zero if any hard check fails (stranded heading, blank page,
text overflow, missing stat value, washed-out cover, white band on a
dark page). Visual review of pdf/_review/*.png is still required before
shipping."""
import fitz, glob, os, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REVIEW = ROOT / "pdf" / "_review"
REVIEW.mkdir(exist_ok=True)
for old in REVIEW.glob("*.png"): old.unlink()

# heading strings from source (to detect stranding precisely)
HEADS = set()
for f in ("guides.html", "playbook.html"):
    for m in re.findall(r'<h[234] class="(?:play-group|subhead|section-title)"[^>]*>(.*?)</h[234]>',
                        (ROOT / f).read_text(), re.S):
        t = re.sub(r'<[^>]+>', '', m).replace('<br />', ' ').replace('&amp;', '&')
        t = re.sub(r'\s+', ' ', t).strip()
        if t:
            HEADS.add(t)

STATS = ['1–2 yrs', '1,500', '250K', '~50']     # playbook stat strip
problems = []

def color_at(pix, x, y):
    i = (y * pix.width + x) * pix.n
    return tuple(pix.samples[i:i+3])

for path in sorted(glob.glob(str(ROOT / "pdf" / "*.pdf"))):
    name = os.path.basename(path)
    d = fitz.open(path)
    H = d[0].rect.height
    full = "".join(d[i].get_text() for i in range(d.page_count))
    is_playbook = "playbook" in name

    if is_playbook:
        for s in STATS:
            if s not in full:
                problems.append(f"{name}: stat value missing: {s}")

    # cover (page 0): photo must not be washed out — center should differ from a corner
    pix0 = d[0].get_pixmap(dpi=72)
    cx = color_at(pix0, pix0.width//2, int(pix0.height*0.35))
    # crude variance across the photo band
    samples = [color_at(pix0, int(pix0.width*fx), int(pix0.height*fy))
               for fx in (0.2,0.5,0.8) for fy in (0.15,0.3,0.45)]
    spread = max(max(s)-min(s) for s in [[c[k] for c in samples] for k in range(3)])
    if spread < 12:
        problems.append(f"{name}: cover photo looks flat/washed (spread {spread})")

    for i in range(d.page_count):
        page = d[i]; W = page.rect.width; ph = page.rect.height
        txt = page.get_text().strip()
        page.get_pixmap(dpi=110).save(str(REVIEW / f"{name.replace('.pdf','')}_p{i+1}.png"))
        if i > 0 and not txt:
            problems.append(f"{name} p{i+1}: BLANK page")
        for blk in page.get_text("dict")["blocks"]:
            for ln in blk.get("lines", []):
                line = "".join(sp["text"] for sp in ln["spans"]).strip()
                x0, y0, x1, y1 = ln["bbox"]
                if i > 0 and line in HEADS and y0 > ph*0.86:
                    problems.append(f"{name} p{i+1}: stranded heading \"{line}\" ({y0/ph*100:.0f}% down)")
                if i > 0 and (x1 > W-16 or x0 < 16) and line:
                    problems.append(f"{name} p{i+1}: text over edge: \"{line[:30]}\"")

    # dark pages: a navy page should not have a white band at top/bottom edge
    for i in range(d.page_count):
        t = d[i].get_text()
        if "ENERGY IMPACTS" in t or "Hyperscalers are proposing" in t:  # dark sections
            pix = d[i].get_pixmap(dpi=72)
            top = color_at(pix, pix.width//2, 2)
            if top[0] > 200 and top[1] > 200:   # white-ish at top edge
                problems.append(f"{name} p{i+1}: white band at top of dark page")

print(f"rendered {len(list(REVIEW.glob('*.png')))} page images to pdf/_review/")
if problems:
    print("\n".join("  ✗ " + p for p in problems))
    print(f"\nFAIL — {len(problems)} issue(s)")
    sys.exit(1)
print("\nPASS — programmatic checks clean. Now eyeball pdf/_review/*.png before shipping.")

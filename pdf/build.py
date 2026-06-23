#!/usr/bin/env python3
"""Assemble print-ready HTML for the ARI playbook PDFs from the live page
content, so PDF interiors match the website exactly. Outputs temp _print_*.html
at the repo root (relative asset paths resolve there); render with Chrome."""
import re, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
playbook = (ROOT / "playbook.html").read_text()
guides   = (ROOT / "guides.html").read_text()

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700'
 '&family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,400..700'
 '&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&display=swap" rel="stylesheet">')

DUO = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
 '<filter id="duo-amber" color-interpolation-filters="sRGB">'
 '<feColorMatrix type="matrix" values="0.299 0.587 0.114 0 0  0.299 0.587 0.114 0 0  0.299 0.587 0.114 0 0  0 0 0 1 0"/>'
 '<feComponentTransfer><feFuncR type="table" tableValues="0.082 0.870"/>'
 '<feFuncG type="table" tableValues="0.110 0.895"/><feFuncB type="table" tableValues="0.259 0.965"/>'
 '</feComponentTransfer></filter></svg>')

EKG = ('<svg class="ekg" viewBox="0 0 1000 120" preserveAspectRatio="none">'
 '<path d="M0,60 L240,60 L268,60 L283,20 L298,100 L313,40 L328,60 L560,60 L588,60 L603,14 '
 'L620,106 L636,34 L652,60 L880,60 L908,60 L923,24 L938,96 L953,44 L968,60 L1000,60"/></svg>')

def page(title, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">{FONTS}'
            f'<link rel="stylesheet" href="styles.css?v=18">'
            f'<link rel="stylesheet" href="pdf/print.css"><title>{title}</title></head>'
            f'<body>{DUO}{body}</body></html>')

def whitepaper_cover():
    return ('<section class="pdf-cover">'
      '<img class="bg" src="images/grid-1.jpg" alt="" aria-hidden="true">'
      '<div class="scrim" aria-hidden="true"></div>'
      '<img class="logo" src="images/ari-logo-white.svg" alt="Americans for Responsible Innovation">'
      '<div class="mid"><hr class="crule"><p class="eyebrow">Advocacy Playbook</p>'
      '<h1>Grid Mitigation <span class="amp">&amp;</span><br>Data Centers</h1>'
      '<p class="standfirst">Federal, state, and local lawmakers have the power to ensure a '
      'responsible data center boom benefits communities and advances U.S. innovation.</p></div>'
      f'<div class="foot">{EKG}'
      '<p class="meta">Americans for Responsible Innovation&nbsp;&nbsp;·&nbsp;&nbsp;June 2026</p></div></section>')

def guide_cover(g):
    op = f' style="opacity:{g["op"]}"' if g.get("op") else ''
    return (f'<section class="pdf-cover guide">'
      f'<img class="bg" src="images/{g["img"]}"{op} alt="" aria-hidden="true">'
      '<div class="scrim" aria-hidden="true"></div>'
      '<img class="logo" src="images/ari-logo-white.svg" alt="Americans for Responsible Innovation">'
      '<div class="mid"><span class="gtag">Field Guide</span><hr class="crule">'
      f'<p class="eyebrow">{g["eyebrow"]}</p><h1>{g["title"]}</h1>'
      f'<p class="standfirst">{g["standfirst"]}</p></div>'
      f'<div class="foot">{EKG}'
      '<p class="meta">Grid Mitigation &amp; Data Centers&nbsp;&nbsp;·&nbsp;&nbsp;June 2026</p></div></section>')

def fill_stats(html):
    """Animated stat counters start at '0' and are filled by JS on the live
    site; static print never runs that, so bake the final values in."""
    def repl(m):
        attrs = m.group(1)
        tgt = re.search(r'data-target="([^"]+)"', attrs)
        pre = re.search(r'data-prefix="([^"]*)"', attrs)
        suf = re.search(r'data-suffix="([^"]*)"', attrs)
        val = f'{int(tgt.group(1)):,}' if tgt else '0'
        return (f'<span class="stat-value"{attrs}>'
                f'{pre.group(1) if pre else ""}{val}{suf.group(1) if suf else ""}</span>')
    return re.sub(r'<span class="stat-value"([^>]*)>\s*0\s*</span>', repl, html)

def keep_with_next(html):
    """Chrome ignores break-after:avoid, so headings can strand at a page
    bottom. Wrap each subhead/play-group together with its following list or
    paragraph in a break-inside:avoid box so the heading travels with it."""
    pat = re.compile(r'(<h([34]) class="(?:play-group|subhead)">.*?</h\2>)\s*'
                     r'(<(ul|p)\b[^>]*>.*?</\4>)', re.S)
    return pat.sub(r'<div class="kwn">\1\3</div>', html)

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def linkify(text):
    parts = re.split(r'(https?://[^\s,)]+)', text)
    out = ''
    for i, part in enumerate(parts):
        if i % 2 == 1:
            url = part.rstrip('.')
            out += f'<a href="{url.replace("&","&amp;")}">{esc(url)}</a>'
        else:
            out += esc(part)
    return out

def place_footnotes(htmltext, fns):
    """PDF-only: insert <sup> markers at each footnote anchor (matched in the
    page's visible text, normalized) and return the html + a list of misses."""
    vis = []                       # (lowercased-or-space char, html index) for visible chars
    intag = False
    for pos, c in enumerate(htmltext):
        if c == '<': intag = True
        elif c == '>': intag = False
        elif not intag: vis.append((c, pos))
    norm = []; npos = []; prev_space = False
    for c, pos in vis:
        if c.isalnum():
            norm.append(c.lower()); npos.append(pos); prev_space = False
        elif not prev_space:
            norm.append(' '); npos.append(pos); prev_space = True
    norm = ''.join(norm)
    inserts = []; missing = []
    for f in fns:
        a = f['anchor']
        p = norm.find(a)
        if p < 0 or norm.find(a, p + 1) != -1:   # not found OR not unique
            missing.append(f['num']); continue
        hp = npos[p + len(a) - 1]                 # html index of anchor's last alnum char
        # advance past trailing punctuation (skipping tags) so the marker sits after it
        i = hp + 1; last = hp; t = False
        while i < len(htmltext):
            c = htmltext[i]
            if c == '<': t = True
            elif c == '>': t = False
            elif not t:
                if c in '.,;:!?")”’]': last = i
                else: break
            i += 1
        inserts.append((last, f['num']))
    for pos, num in sorted(inserts, reverse=True):
        htmltext = htmltext[:pos+1] + f'<sup class="fn">{num}</sup>' + htmltext[pos+1:]
    return htmltext, missing

def match_div(html, open_idx):
    """Return (inner_html, end_idx) for the <div ...> opening at open_idx."""
    i = html.index('>', open_idx) + 1
    depth = 1; start = i
    for m in re.finditer(r'<div\b|</div>', html[i:]):
        if m.group() == '</div>': depth -= 1
        else: depth += 1
        if depth == 0:
            return html[start:i+m.start()], i + m.end()
    raise ValueError("unbalanced div")

# ---- whitepaper ----
main = re.search(r'<main id="top">(.*)</main>', playbook, re.S).group(1)
main = re.sub(r'<!-- ░░ COVER ░░ -->.*?(?=<!-- ░░ EXECUTIVE SUMMARY ░░ -->)', '', main, flags=re.S)
# the "04 Tear-Away Guides" teaser is hidden in the PDF (#guides display:none),
# so renumber the Conclusion 05 -> 04 to keep the section sequence contiguous
main = main.replace('<span class="num">05</span> Conclusion', '<span class="num">04</span> Conclusion')
main = keep_with_next(fill_stats(main))
# PDF-only footnotes: place superscript markers + a Notes section (the website stays clean)
FOOTNOTES = json.loads((ROOT / "pdf" / "playbook-footnotes.json").read_text())
main, _fn_missing = place_footnotes(main, FOOTNOTES)
if _fn_missing:
    print("WARNING: footnotes not placed:", _fn_missing)
_notes = ''.join(f'<li id="fn-{f["num"]}">{linkify(f["cite"])}</li>' for f in FOOTNOTES)
main += ('<section class="section pdf-notes"><div class="container">'
         '<p class="section-label"><span class="num">§</span> References</p>'
         '<h2 class="section-title">Notes</h2>'
         f'<ol class="notes-list">{_notes}</ol></div></section>')
(ROOT / "_print_playbook.html").write_text(page("Grid Mitigation & Data Centers — Advocacy Playbook",
    whitepaper_cover() + '<main>' + main + '</main>'))

# ---- guides ----
GUIDES = [
 ('citizens', {'title':'Residents','eyebrow':'For Residents &amp; Neighbors','img':'family.jpg',
   'standfirst':'How to ensure new data centers bring real benefits to your community — know the risks, get the facts, participate in the process, and use your legal and electoral options.'}),
 ('county', {'title':'County Officials','eyebrow':'For Local Government','img':'zoning.jpg','op':0.62,
   'standfirst':'Zoning, permitting, moratoriums, transparency rules, and enforceable community benefit agreements are tools available to you.'}),
 ('state', {'title':'State Lawmakers','eyebrow':'For State Government','img':'town-hall.jpg','op':0.62,
   'standfirst':'Protect ratepayers through public utility commissions, redesign incentives, plan for stranded assets, and mandate transparency.'}),
 ('cso', {'title':'Civil Society Organizations','eyebrow':'For Civil Society','img':'grassroots.jpg',
   'standfirst':'Bring the technical expertise — independent analysis, PUC intervention, public records requests, and community benefit agreements.'}),
 ('federal', {'title':'Federal Levers','eyebrow':'For Federal Policymakers','img':'capitol.jpg',
   'standfirst':'Use the levers Congress and agencies already hold — EIA, FERC, NERC, DOE, and the EPA — to secure a responsible nationwide buildout.'}),
]
for key, g in GUIDES:
    idx = guides.index(f'data-panel="{key}"')
    open_idx = guides.rfind('<div', 0, idx)
    inner, _ = match_div(guides, open_idx)
    panel = f'<div class="panel is-active">{keep_with_next(inner)}</div>'
    (ROOT / f"_print_guide-{key}.html").write_text(
        page(f'{g["title"]} — ARI Field Guide',
             guide_cover(g) + '<main><section class="section pdf-leadin"><div class="container">' + panel + '</div></section></main>'))

print("built:", [p.name for p in ROOT.glob("_print_*.html")])

# Grid Mitigation & Data Centers — Advocacy Playbook

A narrative, single-page microsite of the **Grid Mitigation & Data Centers: Advocacy Playbook** from *Americans for Responsible Innovation*. It distills the playbook into a long-form, editorial reading experience with an interactive guide for each stakeholder group.

Built with plain HTML, CSS, and vanilla JavaScript — no build step.

## Design

Bold but academic: a warm-paper palette with ink text and a single vermilion signal color; a high-contrast display serif (Fraunces) paired with a screen-optimized reading serif (Newsreader) and a monospace for labels and data (IBM Plex Mono). Fonts load from Google Fonts.

The page is structured as a narrative: cover → executive summary → the incentive trap → energy impacts (a dramatic dark section) → the coalition of stakeholders → role-by-role field guides (tabbed) → conclusion.

## Sections & content

- **Executive summary** with drop cap and editorial lead.
- **01 · The Incentive Trap** — siting dynamics, animated stat strip, an incentives ledger, headline figures, and "field note" case cards (Virginia NDAs, Kentucky).
- **02 · Energy Impacts** — the four "who pays" problems, the ~1,500 MW disconnect, and industrial externalities (xAI Colossus, TN).
- **03 · The Coalition** — the five stakeholder groups.
- **04 · Field Guides** — interactive tabs for County Officials, State Lawmakers, Civil Society, Citizens, and Federal levers, each with strategies and real-world examples.
- **05 · Conclusion** — closing call to action.

## Interactions (`script.js`)

- Reading-progress bar.
- Scroll-spy section nav highlighting.
- Stat counters that animate on scroll.
- Accessible tabbed stakeholder guides (click + arrow-key navigation).

All content lives in the HTML, so it remains fully readable if JavaScript is disabled.

## Project structure

```
.
├── index.html      # Homepage — action landing ("Here's what you can do")
├── playbook.html   # The full verbatim long-read playbook
├── sources.html    # Bibliography (153 sources, A–Z)
├── concepts.html   # Internal brand-exploration page (noindex)
├── styles.css      # Design system: tokens, typography, layout
├── script.js       # Progress bar, scroll-spy, counters, tabs, ?guide deep-link
├── images/         # Duotone-treated photography (+ specs in images/README.md)
└── README.md
```

Brand: "Grid / Energy" — cool charcoal/paper with an amber signal; Fraunces (display), Newsreader (body), Archivo (labels). Imagery uses an amber duotone SVG filter. Bump `styles.css?vN` on any CSS change to bust caches.

## Running locally

It's a static site — open `index.html`, or serve it:

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Customizing

- Colors, fonts, and spacing: edit the `:root` tokens at the top of `styles.css`.
- Copy and sections: edit `index.html`.
- Animated figures: change the `data-target` / `data-prefix` / `data-suffix` attributes on `.stat-value` elements.

## Deploying

Any static host works (GitHub Pages, Netlify, Cloudflare Pages). For GitHub Pages, enable Pages on the repo and point it at the `main` branch root.

# Data Center Microsite

A static landing-page microsite for a fictional data center company (**Meridian Data Centers**). Built with plain HTML, CSS, and vanilla JavaScript — no build step required.

## Features

- Responsive landing page: sticky nav, hero, capabilities grid, animated stat counters, sustainability section, and a contact CTA.
- Animated stat counters that fire on scroll (IntersectionObserver).
- Client-side contact form (demo only — no backend).
- Dark, modern theme driven by CSS custom properties in `styles.css`.

## Project structure

```
.
├── index.html    # Markup and page sections
├── styles.css    # Theme tokens and all styling
├── script.js     # Stat counters, footer year, contact form
└── README.md
```

## Running locally

It's a static site — open `index.html` directly, or serve it:

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Customizing

- Colors and spacing: edit the `:root` variables at the top of `styles.css`.
- Copy and sections: edit `index.html`.
- Stat values: change the `data-target` attributes on `.stat-value` elements.

## Deploying

Any static host works (GitHub Pages, Netlify, Cloudflare Pages, etc.). For GitHub Pages, enable Pages on the repo and point it at the `main` branch root.

#!/usr/bin/env python3
"""Render each .card in cards.html to a PNG at deviceScaleFactor 2 -> output/.
Usage: python3 render.py"""
import pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
HTML = HERE / "cards.html"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_context(device_scale_factor=2).new_page()
    page.goto(HTML.as_uri())
    page.wait_for_function("window.__ready === true")
    # wait for webfonts + background images to finish loading
    page.evaluate("async () => { await document.fonts.ready; }")
    page.wait_for_function(
        "() => Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)"
    )
    page.wait_for_timeout(200)
    cards = page.query_selector_all(".card")
    for c in cards:
        name = c.get_attribute("data-name")
        c.screenshot(path=str(OUT / f"{name}.png"))
        print("rendered", name)
    browser.close()
print(f"\ndone -> {OUT}")

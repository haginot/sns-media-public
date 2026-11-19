#!/usr/bin/env python3
"""Render pstack map HTML drafts to 1920x1080 PNG, plus 400px review crops."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
REV = Path("/tmp/pstack-fig-review")
REV.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

JOBS = ["map_overview_draft", "map_full_draft"]
W, H = 1920, 1080

def overflow_report(page):
    return page.evaluate("""() => {
      const root = document.getElementById('stage');
      const out = [];
      const walk = (el) => {
        const cs = getComputedStyle(el);
        if (cs.display === 'none') return;
        const overflow = (el.scrollWidth > el.clientWidth + 1) || (el.scrollHeight > el.clientHeight + 1);
        if (overflow && el.clientWidth > 0) {
          const t = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 80);
          out.push({
            tag: el.tagName + (el.className ? '.' + String(el.className).trim().split(/\\s+/).slice(0,3).join('.') : ''),
            sw: el.scrollWidth, cw: el.clientWidth, sh: el.scrollHeight, ch: el.clientHeight,
            text: t
          });
        }
        for (const c of el.children) walk(c);
      };
      if (root) walk(root);
      return out.slice(0, 40);
    }""")

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    for name in JOBS:
        html = (SRC / f"{name}.html").resolve()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        page.goto(html.as_uri(), timeout=90000)
        page.evaluate("() => document.fonts.ready")
        page.wait_for_timeout(400)
        ov = overflow_report(page)
        raw = REV / f"{name}_raw.png"
        page.screenshot(path=str(raw), clip={"x": 0, "y": 0, "width": W, "height": H}, type="png")
        page.close()
        im = Image.open(raw).convert("RGB")
        assert im.size == (W * 2, H * 2), im.size
        full = im.resize((W, H), Image.Resampling.LANCZOS)
        dest = OUT / f"{name}.png"
        full.save(dest, "PNG", optimize=True)
        preview = full.resize((400, int(400 * H / W)), Image.Resampling.LANCZOS)
        preview.save(REV / f"{name}_400.png", "PNG", optimize=True)
        # also a slightly larger review (800) for inspection
        mid = full.resize((800, int(800 * H / W)), Image.Resampling.LANCZOS)
        mid.save(REV / f"{name}_800.png", "PNG", optimize=True)
        print(f"{name}: {dest} {dest.stat().st_size} bytes, overflows={len(ov)}")
        for o in ov:
            print("  OV", o)
    browser.close()
print("done")

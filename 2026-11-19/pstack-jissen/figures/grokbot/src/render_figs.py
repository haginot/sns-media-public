#!/usr/bin/env python3
"""Render pstack explainer figures at 1920x1080 and 1280x670, plus 400px reviews."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
REV = Path("/tmp/pstack-fig-gb-review")
REV.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

import sys
JOBS = sys.argv[1:] or ["fig_before_after", "fig_timeline", "fig_timeline_v2", "fig_flow", "map_overview", "map_full"]
SIZES = [(1920, 1080), (1280, 670)]


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


def text_edge_clearance(page, w, h, min_px=40):
    """Return text boxes closer than min_px to the stage edge."""
    return page.evaluate("""({w, h, minPx}) => {
      const root = document.getElementById('stage');
      const hits = [];
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      const rootBox = root.getBoundingClientRect();
      while (walker.nextNode()) {
        const node = walker.currentNode;
        const t = (node.textContent || '').trim();
        if (!t) continue;
        const parent = node.parentElement;
        if (!parent) continue;
        const cs = getComputedStyle(parent);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        for (const r of range.getClientRects()) {
          const left = r.left - rootBox.left;
          const top = r.top - rootBox.top;
          const right = left + r.width;
          const bottom = top + r.height;
          const clr = {
            l: left, t: top, r: w - right, b: h - bottom,
            text: t.slice(0, 60)
          };
          if (clr.l < minPx || clr.t < minPx || clr.r < minPx || clr.b < minPx) {
            hits.push(clr);
          }
        }
      }
      return hits;
    }""", {"w": w, "h": h, "minPx": min_px})


with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    for name in JOBS:
        html = (SRC / f"{name}.html").resolve()
        previews = []
        for w, h in SIZES:
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            page.goto(html.as_uri(), timeout=90000)
            if (w, h) == (1280, 670):
                page.evaluate("""() => {
                  document.documentElement.classList.add('s1280');
                  document.body.classList.add('s1280');
                }""")
            page.evaluate("() => window.gbLayout && window.gbLayout()")
            page.evaluate("() => document.fonts.ready")
            page.wait_for_timeout(400)
            ov = overflow_report(page)
            edges = text_edge_clearance(page, w, h, 40)
            raw = REV / f"{name}_{w}x{h}_raw.png"
            page.screenshot(path=str(raw), clip={"x": 0, "y": 0, "width": w, "height": h}, type="png")
            page.close()
            im = Image.open(raw).convert("RGB")
            assert im.size == (w * 2, h * 2), im.size
            full = im.resize((w, h), Image.Resampling.LANCZOS)
            dest = OUT / f"{name}_{w}x{h}.png"
            full.save(dest, "PNG", optimize=True)
            preview = full.resize((400, int(round(400 * h / w))), Image.Resampling.LANCZOS)
            prev_path = REV / f"{name}_{w}x{h}_400.png"
            preview.save(prev_path, "PNG", optimize=True)
            mid = full.resize((800, int(round(800 * h / w))), Image.Resampling.LANCZOS)
            mid.save(REV / f"{name}_{w}x{h}_800.png", "PNG", optimize=True)
            previews.append((full, w, h, prev_path))
            print(f"{name} {w}x{h}: {dest} {dest.stat().st_size} bytes, overflows={len(ov)}, edge_hits={len(edges)}")
            for o in ov:
                print("  OV", o)
            for e in edges:
                print("  EDGE", {k: (round(v,1) if isinstance(v, float) else v) for k,v in e.items()})
        # contact sheet: 1920 full + 400px of 1920, and 1280-400
        sheet_w = 1920 + 32 + 400
        # stack 1920 and a row for 1280
        img1920 = previews[0][0]
        img1280 = previews[1][0]
        p1920_400 = Image.open(REV / f"{name}_1920x1080_400.png")
        p1280_400 = Image.open(REV / f"{name}_1280x670_400.png")
        # scale 1280 to height ~400 for the sheet? keep actual 1280 on second row cropped? 
        # simpler: first row 1920 + 400preview, second row 1280 + 400preview
        sheet_h = 1080 + 40 + 670 + 40
        sheet = Image.new("RGB", (sheet_w, sheet_h), (40, 40, 40))
        sheet.paste(img1920, (0, 0))
        sheet.paste(p1920_400, (1920 + 32, 0))
        sheet.paste(img1280, (0, 1080 + 40))
        sheet.paste(p1280_400, (1280 + 32, 1080 + 40))
        sheet.save(REV / f"{name}_sheet.png", "PNG", optimize=True)
        print(f"  sheet {REV / f'{name}_sheet.png'}")
    browser.close()
print("done")

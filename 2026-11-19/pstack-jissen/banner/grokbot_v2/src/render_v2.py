#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
REV = Path("/tmp/pstack-banner-v2-review")
REV.mkdir(parents=True, exist_ok=True)

EDGE_JS = """(minPx) => { const st = document.getElementById('stage').getBoundingClientRect(); const hits = [];
  const w = document.createTreeWalker(document.getElementById('stage'), NodeFilter.SHOW_TEXT);
  while (w.nextNode()) { const n = w.currentNode; if (!n.textContent.trim()) continue; const r = document.createRange(); r.selectNodeContents(n);
    for (const b of r.getClientRects()) { const c = {l: Math.round(b.left - st.left), t: Math.round(b.top - st.top), r: Math.round(st.right - b.right), b: Math.round(st.bottom - b.bottom), text: n.textContent.trim().slice(0, 32)};
      if (c.l < minPx || c.t < minPx || c.r < minPx || c.b < minPx) hits.push(c); } } return hits; }"""

JOBS = [
    ("A", "banner_A.html", "note", 1280, 670, 1.0, ""),
    ("A", "banner_A.html", "tech", 1600, 900, 1.0, "カンリー Techブログ"),
    ("A", "banner_A.html", "tech", 1200, 675, 0.75, "カンリー Techブログ"),
    ("B", "banner_B.html", "note", 1280, 670, 1.0, ""),
    ("B", "banner_B.html", "tech", 1600, 900, 1.0, "カンリー Techブログ"),
    ("B", "banner_B.html", "tech", 1200, 675, 0.75, "カンリー Techブログ"),
]

with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome")
    for var, html, mode, w, h, scale, brand in JOBS:
        cw, ch = int(round(w / scale)), int(round(h / scale))
        pg = br.new_page(viewport={"width": cw, "height": ch}, device_scale_factor=2 * scale)
        pg.goto((SRC / html).as_uri())
        pg.evaluate("([m, b]) => renderVariant(m, b)", [mode, brand])
        pg.evaluate("() => document.fonts.ready")
        pg.wait_for_timeout(250)
        edges = pg.evaluate(EDGE_JS, 40 / scale)
        raw = REV / f"raw_{var}_{mode}_{w}x{h}.png"
        pg.screenshot(path=str(raw), clip={"x": 0, "y": 0, "width": cw, "height": ch})
        pg.close()
        im = Image.open(raw).convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
        kind = "note" if mode == "note" else "techblog"
        dest = OUT / f"banner_v2_{var}_{kind}_{w}x{h}.png"
        im.save(dest, optimize=True)
        im.resize((400, round(400 * h / w)), Image.Resampling.LANCZOS).save(REV / f"{dest.stem}_400.png")
        raw.unlink()
        print(dest.name, im.size, "edge_hits:", len(edges))
        for e in edges:
            print("  EDGE", e)
    br.close()

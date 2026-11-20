import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

BASE = Path("/workspace/sns-media-public/2026-11-19/pstack-jissen/banner/grokbot_v3")
SRC = BASE / "src" / "banner_v3.html"
TMP = Path("/tmp/pstack-banner-v3-review")
TMP.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("banner_v3_note_1280x670.png", 1280, 670, "note"),
    ("banner_v3_techblog_1600x900.png", 1600, 900, "techblog"),
    ("banner_v3_techblog_1200x675.png", 1200, 675, "techblog"),
]

EDGE_JS = """
() => {
  const W = window.innerWidth, H = window.innerHeight;
  const hits = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const txt = node.nodeValue.trim();
    if (!txt) continue;
    const el = node.parentElement;
    if (!el || el.closest('svg')) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.left < 40 || r.top < 40 || (W - r.right) < 40 || (H - r.bottom) < 40) {
      hits.push({
        text: txt.slice(0, 30),
        left: Math.round(r.left),
        top: Math.round(r.top),
        rightGap: Math.round(W - r.right),
        bottomGap: Math.round(H - r.bottom),
      });
    }
  }
  return hits;
}
"""

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for fname, w, h, mode in TARGETS:
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        url = f"file://{SRC}?w={w}&h={h}&mode={mode}"
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(150)
        hits = page.evaluate(EDGE_JS)
        out = BASE / fname
        page.screenshot(path=str(out))
        im = Image.open(out)
        thumb = im.resize((400, int(400 * h / w)), Image.LANCZOS)
        thumb.save(TMP / fname.replace(".png", "_400.png"))
        print(f"{fname}: {w}x{h} edge_hits={len(hits)} {hits}")
        page.close()
    browser.close()

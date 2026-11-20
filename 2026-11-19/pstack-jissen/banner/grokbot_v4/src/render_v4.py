from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

BASE = Path("/workspace/sns-media-public/2026-11-19/pstack-jissen/banner/grokbot_v4")
TMP = Path("/tmp/pstack-banner-v4-review")
TMP.mkdir(parents=True, exist_ok=True)

PATTERNS = [
    ("p1_midnight", BASE / "src" / "pattern1_midnight.html"),
    ("p2_split", BASE / "src" / "pattern2_split.html"),
    ("p3_pop", BASE / "src" / "pattern3_pop.html"),
]

SIZES = [
    ("note_1280x670", 1280, 670, "note"),
    ("techblog_1600x900", 1600, 900, "techblog"),
    ("techblog_1200x675", 1200, 675, "techblog"),
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
        text: txt.slice(0, 26),
        left: Math.round(r.left), top: Math.round(r.top),
        rightGap: Math.round(W - r.right), bottomGap: Math.round(H - r.bottom),
      });
    }
  }
  return hits;
}
"""

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for pname, src in PATTERNS:
        for sname, w, h, mode in SIZES:
            fname = f"banner_v4_{pname}_{sname}.png"
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            page.goto(f"file://{src}?w={w}&h={h}&mode={mode}", wait_until="networkidle")
            page.wait_for_timeout(120)
            hits = page.evaluate(EDGE_JS)
            out = BASE / fname
            page.screenshot(path=str(out))
            im = Image.open(out)
            im.resize((400, int(400 * h / w)), Image.LANCZOS).save(TMP / fname.replace(".png", "_400.png"))
            print(f"{fname}: edge_hits={len(hits)} {hits}")
            page.close()
    browser.close()

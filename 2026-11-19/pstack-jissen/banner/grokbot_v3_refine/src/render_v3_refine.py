from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

BASE = Path("/workspace/sns-media-public/2026-11-19/pstack-jissen/banner/grokbot_v3_refine")
TMP = Path("/tmp/pstack-banner-v3r-review")
TMP.mkdir(parents=True, exist_ok=True)

VARIANTS = [
    ("v3A_clean", BASE / "src" / "v3_A_clean.html"),
    ("v3B_contrast", BASE / "src" / "v3_B_contrast.html"),
    ("v3C_motion", BASE / "src" / "v3_C_motion.html"),
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
    for vname, src in VARIANTS:
        for sname, w, h, mode in SIZES:
            fname = f"banner_{vname}_{sname}.png"
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

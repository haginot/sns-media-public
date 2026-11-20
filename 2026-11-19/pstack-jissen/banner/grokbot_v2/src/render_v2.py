#!/usr/bin/env python3
"""Render pstack banner v2 (A: quote impact, B: benefit punch) in Grok Bot tone.
Masters are 1600 wide: tech 1600x900 (also 1200x675 at 0.75), note 1600x838 rendered at 0.8 -> 1280x670.
Outputs: ../ (banner/grokbot_v2/). 400px previews go to /tmp/pstack-banner-v2-review (delete after review).
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
REV = Path("/tmp/pstack-banner-v2-review")
JOBS = [("note", 1280, 670, 0.8), ("techblog", 1600, 900, 1.0), ("techblog", 1200, 675, 0.75)]

def main():
    REV.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(channel="chrome")
        for v in ("A", "B"):
            for name, w, h, scale in JOBS:
                mode = "note" if name == "note" else "tech"
                cw, ch = 1600, int(round(h / scale))
                pg = br.new_page(viewport={"width": cw, "height": ch}, device_scale_factor=2 * scale)
                pg.goto((SRC / "banner_v2.html").as_uri())
                pg.evaluate("(c) => document.body.className = c", f"{mode} {v}")
                pg.evaluate("() => document.fonts.ready"); pg.wait_for_timeout(200)
                pg.evaluate("(v) => build(v)", v); pg.wait_for_timeout(300)
                hits = pg.evaluate("(m) => EDGE(m)", 40 / scale)
                raw = REV / "raw.png"
                pg.screenshot(path=str(raw), clip={"x": 0, "y": 0, "width": cw, "height": ch}); pg.close()
                im = Image.open(raw).convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
                dest = OUT / f"banner_v2_{v}_{name}_{w}x{h}.png"; im.save(dest, optimize=True)
                im.resize((400, round(400 * h / w)), Image.Resampling.LANCZOS).save(REV / f"{dest.stem}_400.png")
                raw.unlink()
                print(dest.name, im.size, "issues:", len(hits)); [print("  ", x) for x in hits]
        br.close()

if __name__ == "__main__":
    main()

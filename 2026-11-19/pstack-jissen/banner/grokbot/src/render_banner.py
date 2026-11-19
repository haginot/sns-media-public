#!/usr/bin/env python3
"""Render the Grok Bot-tone pstack banners (draft). Headline is a variable: edit TITLE or pass --title.

  python3 render_banner.py --title '指示1回・10分で実装から\\nバグ混入テストまでAIが完走'

A newline (or the first 。) splits the headline into two lines. --accent (repeatable) colors phrases blue.
Outputs go next to this folder's parent (banner/grokbot/). Review files: /tmp/pstack-banner-gb-review.
"""
import argparse, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
REV = Path("/tmp/pstack-banner-gb-review")

TITLE = "指示1回・10分で実装から\nバグ混入テストまでAIが完走"   # final headline (HAGINO, 2026-11-20)
ACCENTS = ["指示1回・10分", "バグ混入テスト"]
SUB_NOTE = "10分で読める入門（Claude Code 実演）"                          # shown after the black "pstack" pill
SUB_TECH = "入門／Cursor公式58スキルを Claude Code で実戦"
BRAND = "カンリー Techブログ"
ROWS = [["設計からツール実装まで自律完走", "check_pins.py"], ["自動テスト", "14件すべて通過"], ["わざと壊してテスト検証", "8通り中7通りを検出"]]
CARD_NAME = "Claude Code × pstack"
CARD_PILL = "約10分・人手なし"
JOBS = [("banner_note", "note", 1280, 670, 1.0), ("banner_techblog", "tech", 1600, 900, 1.0), ("banner_techblog", "tech", 1200, 675, 0.75)]

def split(t):
    t = t.replace("\\n", "\n")
    if "\n" in t: return t
    i = t.find("。")
    return t if i < 0 else t[: i + 1] + "\n" + t[i + 1 :]

EDGE_JS = """(minPx) => { const st = document.getElementById('stage').getBoundingClientRect(); const hits = [];
  const w = document.createTreeWalker(document.getElementById('stage'), NodeFilter.SHOW_TEXT);
  while (w.nextNode()) { const n = w.currentNode; if (!n.textContent.trim()) continue; const r = document.createRange(); r.selectNodeContents(n);
    for (const b of r.getClientRects()) { const c = {l: b.left - st.left, t: b.top - st.top, r: st.right - b.right, b: st.bottom - b.bottom, text: n.textContent.trim().slice(0, 30)};
      if (c.l < minPx || c.t < minPx || c.r < minPx || c.b < minPx) hits.push(c); } } return hits; }"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", default=TITLE); ap.add_argument("--accent", action="append", default=None)
    ap.add_argument("--clean-tmp", action="store_true")
    a = ap.parse_args()
    REV.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(channel="chrome")
        for name, mode, w, h, scale in JOBS:
            cw, ch = int(round(w / scale)), int(round(h / scale))
            pg = br.new_page(viewport={"width": cw, "height": ch}, device_scale_factor=2 * scale)
            pg.goto((SRC / "banner.html").as_uri())
            pg.evaluate("(m) => document.body.className = m", mode)
            pg.evaluate("(c) => applyCopy(c)", {"title": split(a.title), "accents": a.accent or ACCENTS, "cardName": CARD_NAME, "cardPill": CARD_PILL,
                         "subtitle": SUB_NOTE if mode == "note" else SUB_TECH, "brand": BRAND if mode == "tech" else "", "rows": ROWS})
            pg.evaluate("() => document.fonts.ready"); pg.wait_for_timeout(300)
            edges = pg.evaluate(EDGE_JS, 40 / scale)
            raw = REV / f"{name}_{w}x{h}_raw.png"
            pg.screenshot(path=str(raw), clip={"x": 0, "y": 0, "width": cw, "height": ch}); pg.close()
            im = Image.open(raw).convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
            dest = OUT / f"{name}_{w}x{h}.png"; im.save(dest, optimize=True)
            im.resize((400, round(400 * h / w)), Image.Resampling.LANCZOS).save(REV / f"{name}_{w}x{h}_400.png")
            raw.unlink()
            print(dest.name, im.size, "edge_hits:", len(edges)); [print("  EDGE", e) for e in edges]
        br.close()
    if a.clean_tmp: shutil.rmtree(REV, ignore_errors=True)

if __name__ == "__main__":
    main()

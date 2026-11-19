#!/usr/bin/env python3
"""Render pstack article banners from a single HTML template.

Title swap (the article title is not final yet):

  1. Edit TITLE / SUBTITLE near the top of this file, then run:

       python3 src/render_banner.py

  2. Or pass them on the command line (does not edit the file):

       python3 src/render_banner.py \\
         --title '人の手なしで、古いリンク27件→0件' \\
         --subtitle 'pstack 10分で読める入門'

A、or a newline splits the title into two lines. A pattern like 27件→0件
on the second line is colored (27件 orange, 0件 teal). If the new title
has no such numbers, it is drawn as plain navy text.

Outputs (written next to this folder's parent):

  banner_note_1280x670.png
  banner_techblog_1600x900.png
  banner_techblog_1200x675.png

The Techブログ variants add the footer 「カンリー Techブログ」.
Temporary review files go under /tmp/pstack-banner-review and can be
removed with --clean-tmp.
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright
from PIL import Image

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
REV = Path("/tmp/pstack-banner-review")
HTML = SRC / "banner.html"

# --- swap the headline here ----------------------------------------------
TITLE = "人の手なしで、古いリンク27件→0件"
SUBTITLE = "pstack 10分で読める入門"
FOOTER_TECH = "カンリー Techブログ"
# -------------------------------------------------------------------------

JOBS = [
    # name, css class, size
    ("banner_note", "note-1280", 1280, 670),
    ("banner_techblog", "tech-1600", 1600, 900),
    ("banner_techblog", "tech-1200", 1200, 675),
]

NUM_RE = re.compile(r"(\d+件)\s*→\s*(\d+件)")


def split_title(title: str) -> tuple[str, str]:
    title = title.replace("\\n", "\n").strip()
    if "\n" in title:
        a, b = title.split("\n", 1)
        return a.strip(), b.strip()
    if "、" in title:
        i = title.index("、")
        return title[: i + 1].strip(), title[i + 1 :].strip()
    return title, ""


def overflow_report(page):
    return page.evaluate(
        """() => {
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
    }"""
    )


def text_edge_clearance(page, w, h, min_px=40):
    return page.evaluate(
        """({w, h, minPx}) => {
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
    }""",
        {"w": w, "h": h, "minPx": min_px},
    )


def apply_copy(page, title: str, subtitle: str, footer: str):
    line1, line2 = split_title(title)
    m = NUM_RE.search(line2) if line2 else None
    page.evaluate(
        """({line1, line2, prefix, nBefore, nAfter, hasNums, subtitle, footer}) => {
      const el1 = document.getElementById('line1');
      const el2 = document.getElementById('line2');
      const h1 = document.getElementById('title');
      el1.textContent = line1;
      if (!line2) {
        el2.style.display = 'none';
      } else if (hasNums) {
        document.getElementById('line2pre').textContent = prefix;
        document.getElementById('nBefore').textContent = nBefore;
        document.getElementById('nAfter').textContent = nAfter;
        h1.classList.remove('plain');
        el2.style.display = '';
      } else {
        el2.replaceChildren(document.createTextNode(line2));
        h1.classList.add('plain');
        el2.style.display = '';
      }
      document.getElementById('subtitle').textContent = subtitle;
      document.getElementById('footerTech').textContent = footer;
    }""",
        {
            "line1": line1,
            "line2": line2,
            "prefix": (line2[: m.start()] if m else line2),
            "nBefore": (m.group(1) if m else ""),
            "nAfter": (m.group(2) if m else ""),
            "hasNums": bool(m),
            "subtitle": subtitle,
            "footer": footer,
        },
    )


def fit_title(page, min_px=40):
    """Shrink h1 a few steps if it overflows its header or approaches the edge."""
    page.evaluate(
        """(minPx) => {
      const h1 = document.getElementById('title');
      const stage = document.getElementById('stage');
      const header = h1.parentElement;
      const cs = getComputedStyle(h1);
      let size = parseFloat(cs.fontSize);
      for (let i = 0; i < 12; i++) {
        const r = h1.getBoundingClientRect();
        const s = stage.getBoundingClientRect();
        const overflow = h1.scrollWidth > h1.clientWidth + 1
          || r.right > s.right - minPx
          || r.left < s.left + minPx;
        if (!overflow) break;
        size -= 2;
        if (size < 40) break;
        h1.style.fontSize = size + 'px';
      }
    }""",
        min_px,
    )


def main():
    ap = argparse.ArgumentParser(description="Render pstack article banners.")
    ap.add_argument("--title", default=TITLE, help="Headline. Use、or a newline to split into two lines.")
    ap.add_argument("--subtitle", default=SUBTITLE)
    ap.add_argument("--footer-tech", default=FOOTER_TECH)
    ap.add_argument("--clean-tmp", action="store_true", help="Delete /tmp/pstack-banner-review after rendering.")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    if REV.exists():
        shutil.rmtree(REV)
    REV.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        for name, css, w, h in JOBS:
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            page.goto(HTML.as_uri(), timeout=90000)
            page.evaluate(
                """(css) => {
                  document.body.className = css;
                  document.documentElement.className = css;
                }""",
                css,
            )
            apply_copy(page, args.title, args.subtitle, args.footer_tech)
            page.evaluate("() => document.fonts.ready")
            page.wait_for_timeout(200)
            fit_title(page, 40)
            page.wait_for_timeout(200)
            ov = overflow_report(page)
            edges = text_edge_clearance(page, w, h, 40)
            raw = REV / f"{name}_{w}x{h}_raw.png"
            page.screenshot(path=str(raw), clip={"x": 0, "y": 0, "width": w, "height": h}, type="png")
            page.close()

            im = Image.open(raw).convert("RGB")
            assert im.size == (w * 2, h * 2), im.size
            full = im.resize((w, h), Image.Resampling.LANCZOS)
            dest = OUT / f"{name}_{w}x{h}.png"
            full.save(dest, "PNG", optimize=True, compress_level=9)
            preview = full.resize((400, int(round(400 * h / w))), Image.Resampling.LANCZOS)
            preview.save(REV / f"{name}_{w}x{h}_400.png", "PNG", optimize=True, compress_level=9)
            # drop the 2x raw immediately to save disk
            raw.unlink(missing_ok=True)
            print(f"{name} {w}x{h}: {dest} {dest.stat().st_size} bytes, overflows={len(ov)}, edge_hits={len(edges)}")
            for o in ov:
                print("  OV", o)
            for e in edges:
                print("  EDGE", {k: (round(v, 1) if isinstance(v, float) else v) for k, v in e.items()})
        browser.close()

    if args.clean_tmp:
        shutil.rmtree(REV, ignore_errors=True)
        print("cleaned", REV)
    print("done")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render 序章 v2 banners (painted bg) at 1280x670 and 1920x1080, plus 400px QA and edge clearance."""
import json, sys, pathlib, urllib.parse, shutil
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

root = pathlib.Path(__file__).resolve().parent
out = root / "out"
out.mkdir(exist_ok=True)
MIN_EDGE = 40

def uri(variant, size):
    q = urllib.parse.urlencode({"v": variant, "size": "1920" if size == 1920 else "1280"})
    return (root / "banner_ch0.html").as_uri() + "?" + q

def measure(page, w, h):
    return page.evaluate(
        """([W, H, MIN]) => {
          const sel = ['.series', '.pivot', '.year', '.h1', '.h2', '.biblio .title', '.biblio .credit', '.headline'];
          const items = [];
          for (const s of sel) {
            const el = document.querySelector(s);
            if (!el) continue;
            const r = el.getBoundingClientRect();
            const cs = getComputedStyle(el);
            const raw = (el.innerText || '').trim();
            items.push({
              sel: s,
              text: raw.split(String.fromCharCode(10)).join(' / '),
              x: r.x, y: r.y, w: r.width, h: r.height,
              right: W - (r.x + r.width),
              bottom: H - (r.y + r.height),
              font: cs.fontSize,
              overflow: r.x < 0 || r.y < 0 || r.x + r.width > W + 0.5 || r.y + r.height > H + 0.5
            });
          }
          const texts = items.filter(i => ['.series', '.pivot', '.year', '.h1', '.h2', '.biblio .title', '.biblio .credit'].includes(i.sel));
          const clearance = texts.map(i => ({
            sel: i.sel, text: i.text,
            minEdge: Math.min(i.x, i.y, i.right, i.bottom),
            left: +i.x.toFixed(1), top: +i.y.toFixed(1),
            right: +i.right.toFixed(1), bottom: +i.bottom.toFixed(1),
            w: +i.w.toFixed(1), h: +i.h.toFixed(1),
            font: i.font, overflow: i.overflow,
            ok: Math.min(i.x, i.y, i.right, i.bottom) >= MIN && !i.overflow
          }));
          const head = items.find(i => i.sel === '.headline');
          return { clearance, fail: clearance.filter(c => !c.ok), headline: head && {
            left: +head.x.toFixed(1), top: +head.y.toFixed(1),
            right: +(W-head.x-head.w).toFixed(1), bottom: +(H-head.y-head.h).toFixed(1),
            w: +head.w.toFixed(1), h: +head.h.toFixed(1)
          }};
        }""",
        [w, h, MIN_EDGE],
    )

def save_png(path, im):
    im = im.convert("RGB")
    im.save(path, optimize=True)
    return im

def main():
    variants = sys.argv[1:] or ["a", "b", "c"]
    report = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            args=["--no-sandbox", "--disable-gpu", "--headless=new"],
        )
        for v in variants:
            for size, wh in [("1280", (1280, 670)), ("1920", (1920, 1080))]:
                w, h = wh
                page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
                page.on("pageerror", lambda e: print("PAGEERROR", e, flush=True))
                page.goto(uri(v, int(size)), wait_until="load")
                page.wait_for_function("window.FIG_READY === true", timeout=15000)
                page.evaluate("document.fonts.ready")
                page.wait_for_timeout(200)
                raw = out / f"banner_ch0_{v.upper()}_{w}x{h}.png"
                page.screenshot(path=str(raw), clip={"x": 0, "y": 0, "width": w, "height": h})
                im = save_png(raw, Image.open(raw))
                dest = root / raw.name
                dest.write_bytes(raw.read_bytes())
                info = measure(page, w, h)
                report[f"{v}_{w}x{h}"] = {"clearance": info["clearance"], "headline": info["headline"]}
                print(f"=== {v} {w}x{h}  size={im.size} bytes={raw.stat().st_size}")
                print("  headline box", info["headline"])
                for c in info["clearance"]:
                    flag = "OK " if c["ok"] else "FAIL"
                    print(f"  {flag} {c['sel']:18} font={c['font']:8} edge={c['minEdge']:.1f} L{c['left']:.0f} T{c['top']:.0f} R{c['right']:.0f} B{c['bottom']:.0f}  {c['text'][:40]}")
                if info["fail"]:
                    print("  CLEARANCE FAILS:", [f["sel"] for f in info["fail"]])
                if size == "1280":
                    h400 = round(670 * 400 / 1280)
                    im.resize((400, h400), Image.LANCZOS).save(out / f"banner_ch0_{v.upper()}_400.png", optimize=True)
                page.close()
        browser.close()

    for v in variants:
        full = Image.open(out / f"banner_ch0_{v.upper()}_1280x670.png")
        p400 = Image.open(out / f"banner_ch0_{v.upper()}_400.png")
        pad, label_h = 16, 36
        sheet = Image.new("RGB", (full.width + pad + p400.width + pad * 2, max(full.height, p400.height) + pad * 2 + label_h), "#222")
        ImageDraw.Draw(sheet).text((pad, 10), f"v2 {v.upper()}  1280x670  +  400px", fill="#eee")
        sheet.paste(full, (pad, label_h + pad))
        sheet.paste(p400, (pad + full.width + pad, label_h + pad))
        sp = out / f"qa_{v.upper()}_full_and_400.png"
        sheet.save(sp, optimize=True)
        print("sheet", sp)
    (out / "clearance.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render all 7 序章〜まとめ banners at 1280x670 and 1920x1080, plus 400px QA and edge clearance."""
import json, sys, pathlib, urllib.parse
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

root = pathlib.Path(__file__).resolve().parent
out = root / "out"
out.mkdir(exist_ok=True)
MIN_EDGE = 40
CHAPTERS = ["ch0", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6"]

def uri(ch, size):
    q = urllib.parse.urlencode({"ch": ch, "size": "1920" if size == 1920 else "1280"})
    return (root / "banner_series.html").as_uri() + "?" + q

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
          const year = items.find(i => i.sel === '.year');
          let yearHead = null;
          if (head && year) {
            const yR = year.x + year.w, yB = year.y + year.h;
            const hR = head.x + head.w, hB = head.y + head.h;
            const dx = yR < head.x ? head.x - yR : (hR < year.x ? year.x - hR : 0);
            const dy = yB < head.y ? head.y - yB : (hB < year.y ? year.y - hB : 0);
            const overlap = dx === 0 && dy === 0;
            const gap = overlap ? 0 : (dx === 0 ? dy : (dy === 0 ? dx : Math.hypot(dx, dy)));
            yearHead = {
              gap: +gap.toFixed(1), dx: +dx.toFixed(1), dy: +dy.toFixed(1),
              overlap: overlap, ok: gap >= MIN && !overlap,
              year: {left:+year.x.toFixed(1), top:+year.y.toFixed(1), w:+year.w.toFixed(1), h:+year.h.toFixed(1)},
              head: {left:+head.x.toFixed(1), top:+head.y.toFixed(1), w:+head.w.toFixed(1), h:+head.h.toFixed(1)}
            };
          }
          return { clearance, fail: clearance.filter(c => !c.ok), headline: head && {
            left: +head.x.toFixed(1), top: +head.y.toFixed(1),
            right: +(W-head.x-head.w).toFixed(1), bottom: +(H-head.y-head.h).toFixed(1),
            w: +head.w.toFixed(1), h: +head.h.toFixed(1)
          }, yearHead};
        }""",
        [w, h, MIN_EDGE],
    )

def save_png(path, im):
    im = im.convert("RGB")
    im.save(path, optimize=True)
    return im

def main():
    chapters = sys.argv[1:] or CHAPTERS
    report = {}
    fails = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            args=["--no-sandbox", "--disable-gpu", "--headless=new"],
        )
        for ch in chapters:
            for size, wh in [("1280", (1280, 670)), ("1920", (1920, 1080))]:
                w, h = wh
                page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
                page.on("pageerror", lambda e: print("PAGEERROR", e, flush=True))
                page.goto(uri(ch, int(size)), wait_until="load")
                page.wait_for_function("window.FIG_READY === true", timeout=15000)
                page.evaluate("document.fonts.ready")
                page.wait_for_timeout(200)
                raw = out / f"banner_{ch}_{w}x{h}.png"
                page.screenshot(path=str(raw), clip={"x": 0, "y": 0, "width": w, "height": h})
                im = save_png(raw, Image.open(raw))
                dest = root / raw.name
                dest.write_bytes(raw.read_bytes())
                info = measure(page, w, h)
                report[f"{ch}_{w}x{h}"] = {"clearance": info["clearance"], "headline": info["headline"], "yearHead": info.get("yearHead")}
                print(f"=== {ch} {w}x{h}  size={im.size} bytes={raw.stat().st_size}")
                print("  headline box", info["headline"])
                yh = info.get("yearHead")
                if yh:
                    flag = "OK " if yh["ok"] else "FAIL"
                    print(f"  {flag} year-headline gap={yh['gap']}px  dx={yh['dx']} dy={yh['dy']} overlap={yh['overlap']}")
                    if not yh["ok"]:
                        fails.append(f"{ch}_{w}x{h}:year-head-gap")
                head = info.get("headline") or {}
                # headline must sit fully below the top band (z-index covers anything under it)
                band_h = 200 if h == 1080 else 122
                if head and head.get("top", 0) < band_h - 1:
                    print(f"  FAIL headline under top band: top={head['top']} band={band_h}")
                    fails.append(f"{ch}_{w}x{h}:headline-under-band")
                for c in info["clearance"]:
                    flag = "OK " if c["ok"] else "FAIL"
                    print(f"  {flag} {c['sel']:18} font={c['font']:8} edge={c['minEdge']:.1f} L{c['left']:.0f} T{c['top']:.0f} R{c['right']:.0f} B{c['bottom']:.0f}  {c['text'][:48]}")
                if info["fail"]:
                    print("  CLEARANCE FAILS:", [f["sel"] for f in info["fail"]])
                    fails.append(f"{ch}_{w}x{h}")
                if size == "1280":
                    h400 = round(670 * 400 / 1280)
                    im.resize((400, h400), Image.LANCZOS).save(out / f"banner_{ch}_400.png", optimize=True)
                page.close()
        browser.close()

    # per-chapter 1280 + 400 QA sheets
    for ch in chapters:
        full = Image.open(out / f"banner_{ch}_1280x670.png")
        p400 = Image.open(out / f"banner_{ch}_400.png")
        pad, label_h = 16, 36
        sheet = Image.new("RGB", (full.width + pad + p400.width + pad * 2, max(full.height, p400.height) + pad * 2 + label_h), "#222")
        ImageDraw.Draw(sheet).text((pad, 10), f"{ch}  1280x670  +  400px", fill="#eee")
        sheet.paste(full, (pad, label_h + pad))
        sheet.paste(p400, (pad + full.width + pad, label_h + pad))
        sp = out / f"qa_{ch}_full_and_400.png"
        sheet.save(sp, optimize=True)
        print("sheet", sp)

    # contact of all 7 at 1280, two rows
    thumbs = [Image.open(out / f"banner_{ch}_1280x670.png") for ch in chapters]
    tw, th = 640, 335
    thumbs = [im.resize((tw, th), Image.LANCZOS) for im in thumbs]
    gap, lab = 8, 28
    cols, rows = 4, 2
    contact = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * (th + lab) + (rows + 1) * gap), "#1B2638")
    d = ImageDraw.Draw(contact)
    labels = ["序章", "第1回", "第2回", "第3回", "第4回", "第5回", "まとめ"]
    for i, (im, labtxt) in enumerate(zip(thumbs, labels)):
        r, c = divmod(i, cols)
        x = gap + c * (tw + gap)
        y = gap + r * (th + lab + gap)
        d.text((x, y), labtxt, fill="#F3E8D2")
        contact.paste(im, (x, y + lab))
    cp = out / "contact_series_banners_1280.jpg"
    contact.convert("RGB").save(cp, quality=90, optimize=True)
    dest_c = root / "contact_series_banners_1280.jpg"
    dest_c.write_bytes(cp.read_bytes())
    print("contact", dest_c)
    (out / "clearance.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if fails:
        print("FAILED", fails)
        sys.exit(1)

if __name__ == "__main__":
    main()

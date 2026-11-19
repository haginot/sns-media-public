#!/usr/bin/env python3
"""Render banner_en.html at 1600x900 and 1200x675, plus 400px QA previews."""
import sys, pathlib, urllib.parse
from playwright.sync_api import sync_playwright
from PIL import Image

root = pathlib.Path(__file__).resolve().parent
out = root / "out"
out.mkdir(exist_ok=True)
params = {}
for a in sys.argv[1:]:
    if "=" in a:
        k, v = a.split("=", 1)
        params[k] = v
qs = ("?" + urllib.parse.urlencode(params)) if params else ""
# theme=dark is default in zlib; pass it explicitly
url = (root / "banner_en.html").as_uri() + (("&" if qs else "?") + "theme=dark" if "theme" not in params else "")
if qs:
    url = (root / "banner_en.html").as_uri() + qs + ("&theme=dark" if "theme" not in params else "")

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome",
                          args=["--no-sandbox", "--disable-gpu", "--headless=new"])
    pg = b.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=1)
    pg.on("pageerror", lambda e: print("PAGEERROR", e, flush=True))
    pg.on("console", lambda m: print("LOG", m.type, m.text, flush=True))
    pg.goto(url)
    pg.wait_for_function("window.FIG_READY === true", timeout=12000)
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(300)
    f = out / "banner_en_1600x900.png"
    pg.screenshot(path=str(f))
    im = Image.open(f).convert("RGB")
    im.save(f, optimize=True)
    im.resize((1200, 675), Image.LANCZOS).save(out / "banner_en_1200x675.png", optimize=True)
    im.resize((400, 225), Image.LANCZOS).save(out / "banner_en_400.png")
    print("1600", im.size, f.stat().st_size)
    # report text metrics if present
    info = pg.evaluate("""() => {
      const t1 = document.querySelector('#hero text');
      const texts = [...document.querySelectorAll('#hero text')].map(t => ({
        text: t.textContent, x: t.getAttribute('x'), y: t.getAttribute('y'),
        bb: (()=>{const b=t.getBBox(); return {x:b.x,y:b.y,w:b.width,h:b.height};})()
      }));
      const kick = document.querySelector('.kick');
      const foot = document.querySelector('.foot');
      const kr = kick ? kick.getBoundingClientRect() : null;
      const fr = foot ? foot.getBoundingClientRect() : null;
      return {texts, kick: kr && {x:kr.x,y:kr.y,w:kr.width,h:kr.height,t:kick.textContent},
              foot: fr && {x:fr.x,y:fr.y,w:fr.width,h:fr.height,t:foot.textContent}};
    }""")
    print(info)
    b.close()

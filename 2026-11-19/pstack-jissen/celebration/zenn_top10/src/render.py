from playwright.sync_api import sync_playwright
from PIL import Image
import os
OUT = os.path.abspath("..")
jobs = [("celebrate_1600x900.html", 1600, 900, "zenn_top10_celebration_1600x900.png"),
        ("celebrate_1080x1080.html", 1080, 1080, "zenn_top10_celebration_1080x1080.png")]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for src, w, h, out in jobs:
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg.goto("file://" + os.path.abspath(src)); pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(OUT, out))
        im = Image.open(os.path.join(OUT, out)); im.thumbnail((400, 400)); im.save("/tmp/thumb_" + out)
    b.close()
print("rendered")

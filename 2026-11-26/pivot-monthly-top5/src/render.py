from playwright.sync_api import sync_playwright
import pathlib
H = pathlib.Path(__file__).parent
OUT = H.parent
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=1)
    pg.goto((H / "a.html").as_uri())
    pg.wait_for_timeout(800)
    dest = OUT / "pivot_monthly_top5_1600x900.png"
    pg.screenshot(path=str(H / "shot_1600.png"), type="png")
    pg.screenshot(path=str(dest), type="png")
    # 400px timeline preview
    pg.set_viewport_size({"width": 400, "height": 225})
    # actually better to scale the 1600 shot
    b.close()
print("wrote", dest)

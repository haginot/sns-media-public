from playwright.sync_api import sync_playwright
import pathlib
H=pathlib.Path(__file__).parent
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=b.new_page(viewport={"width":1600,"height":900})
    pg.goto((H/"a.html").as_uri()); pg.wait_for_timeout(800)
    pg.screenshot(path=str(H.parent/"top3_crystal_1600x900.png")); b.close()

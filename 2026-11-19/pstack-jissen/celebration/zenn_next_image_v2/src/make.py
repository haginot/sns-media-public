# usage: python3 make.py --head "..." [--sub Techトレンド] [--shot shot.png] [--bg bg_podium.jpg] [--hl "left:6px;top:135px;width:312px;height:102px"] --out out.png
# shot = Tech section crop (913px wide like zenn_top3/src/shot_top3.png); hl = article highlight box in px of the 576px-wide card
import argparse,pathlib
from playwright.sync_api import sync_playwright
a=argparse.ArgumentParser();a.add_argument('--head',required=True);a.add_argument('--sub',default='Techトレンド');a.add_argument('--shot',default='shot.png');a.add_argument('--bg',default='bg_podium.jpg');a.add_argument('--hl',default='left:6px;top:135px;width:312px;height:102px');a.add_argument('--out',default='out.png');a.add_argument('--css',default='');o=a.parse_args()
H=pathlib.Path(__file__).parent.resolve()
html=(H/'tpl.html').read_text().replace('__BG__',o.bg).replace('__SUB__',o.sub).replace('__HEAD__',o.head).replace('__SHOT__',o.shot).replace('__HL__',o.hl).replace('__CSS__',o.css)
(H/'_r.html').write_text(html)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome");pg=b.new_page(viewport={"width":1600,"height":900})
    pg.goto((H/'_r.html').as_uri());pg.wait_for_timeout(800);pg.screenshot(path=str(H/o.out));b.close()

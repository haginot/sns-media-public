#!/usr/bin/env python3
"""Render translated slide sources to PNG/GIF.
usage: render.py <srcdir> <outdir> <id>:<kind>:<size>[:gif] ...
kind: kami (sNN.html+css single-slide via kami-slides theme) | page (standalone html)
size: WxH final output; gif: also produce animated GIF of all frames (1400ms, last 3000ms)
"""
import sys, os, re, json, subprocess, tempfile, shutil
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
K = Path('/workspace/kami-slides')
src, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
jobs = [a.split(':') for a in sys.argv[3:]]
def build(sid):
    d = Path(tempfile.mkdtemp(prefix='deck_'))
    shutil.copy(src/f'{sid}.html', d); 
    if (src/f'{sid}.css').exists(): shutil.copy(src/f'{sid}.css', d)
    (d/'deck.json').write_text(json.dumps({'title':sid,'mode':'light','slides':[sid]}))
    return subprocess.check_output(['python3', str(K/'tools/build.py'), str(d)], text=True).strip()
report = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    for j in jobs:
        sid, kind, size = j[0], j[1], j[2]; gif = len(j) > 3
        W, H = map(int, size.split('x'))
        html = build(sid) if kind == 'kami' else str((src/f'{sid}.html').resolve())
        raw = open(html).read()
        nums = [int(x) for x in re.findall(r'\bst st(\d+)\b', raw)]
        N = max(nums) if nums else 1
        pg = b.new_page(viewport={'width':1920,'height':1080}, device_scale_factor=2)
        pg.goto('file://'+html, timeout=90000); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(800)
        pg.evaluate("()=>{ if (typeof show==='function') show(0); (window.__rlDraw||[]).forEach(f=>f()); }"); pg.wait_for_timeout(300)
        frames = []
        for f in range(1, N+1):
            pg.evaluate("(f)=>{const s=document.querySelector('.slide'); for(let i=1;i<=9;i++) s.classList.remove('frame'+i); s.classList.add('frame'+f,'cur');}", f)
            pg.evaluate("()=>{(window.__rlDraw||[]).forEach(f=>f());}")
            pg.wait_for_timeout(250)
            fp = out/f'_{sid}_f{f:02d}.png'
            pg.screenshot(path=str(fp), clip={'x':0,'y':0,'width':1920,'height':1080}); frames.append(fp)
        iss = pg.evaluate("""()=>{const o=[];document.querySelectorAll('.slide .bx,.slide .chip,.slide .num').forEach(e=>{if(e.scrollWidth>e.clientWidth+2||e.scrollHeight>e.clientHeight+2)o.push((e.id||'')+':'+e.textContent.trim().slice(0,40)+` sw${e.scrollWidth}/${e.clientWidth} sh${e.scrollHeight}/${e.clientHeight}`)});
          const t=document.body.innerText; const jp=(t.match(/[\\u3040-\\u30ff\\u4e00-\\u9fff]+/g)||[]).slice(0,10); return {overflow:o, jp};}""")
        report[sid] = {'frames': N, **iss}
        pg.close()
        last = Image.open(frames[-1]).convert('RGB').resize((W, H), Image.LANCZOS)
        last.save(out/f'{sid}.png', optimize=True)
        if gif and N > 1:
            ims = [Image.open(f).convert('RGB').resize((1200, 675), Image.LANCZOS) for f in frames]
            pal = [im.quantize(colors=255, method=Image.MEDIANCUT, dither=Image.NONE) for im in ims]
            pal[0].save(out/f'{sid}.gif', save_all=True, append_images=pal[1:], duration=[1400]*(N-1)+[3000], loop=0, optimize=True)
        for f in frames: f.unlink()
    b.close()
json.dump(report, open(out/'_report.json','a'), ensure_ascii=False, indent=1)
print(json.dumps(report, ensure_ascii=False, indent=1))

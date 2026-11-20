import re,sys,os,json,asyncio
from playwright.async_api import async_playwright
BASE=os.path.dirname(os.path.abspath(__file__))
async def run(model):
    md=open(f"{BASE}/raw/html_app_{model}.md").read()
    m=re.search(r"```html\s*\n(.*?)```",md,re.S)
    html=m.group(1) if m else md
    os.makedirs(f"{BASE}/apps",exist_ok=True)
    path=f"{BASE}/apps/brick_{model}.html"; open(path,"w").write(html)
    errs=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--autoplay-policy=no-user-gesture-required"])
        ctx=await b.new_context(viewport={"width":1100,"height":760},record_video_dir=f"{BASE}/shots/vid_{model}",record_video_size={"width":1100,"height":760})
        pg=await ctx.new_page()
        pg.on("pageerror",lambda e: errs.append(str(e)))
        pg.on("console",lambda m: errs.append("console."+m.type+": "+m.text) if m.type=="error" else None)
        await pg.goto("file://"+path)
        await pg.wait_for_timeout(1000); await pg.screenshot(path=f"{BASE}/shots/{model}_t01.png")
        await pg.wait_for_timeout(5000); await pg.screenshot(path=f"{BASE}/shots/{model}_t06.png")
        await pg.wait_for_timeout(9000); await pg.screenshot(path=f"{BASE}/shots/{model}_t15.png")
        await pg.wait_for_timeout(15000); await pg.screenshot(path=f"{BASE}/shots/{model}_t30.png")
        await ctx.close(); await b.close()
    json.dump({"bytes":len(html),"lines":html.count("\n")+1,"errors":errs[:20]},open(f"{BASE}/shots/{model}_render.json","w"),indent=1)
    print(model,len(html),errs[:5])
asyncio.run(run(sys.argv[1]))

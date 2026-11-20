import sys,os,asyncio,json
from playwright.async_api import async_playwright
BASE=os.path.dirname(os.path.abspath(__file__))
async def run(model):
    errs=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":1100,"height":760})
        pg.on("pageerror",lambda e: errs.append(str(e)))
        await pg.goto(f"file://{BASE}/apps/brick_{model}.html")
        for i in range(1,9):
            await pg.wait_for_timeout(30000)
            await pg.screenshot(path=f"{BASE}/shots/long_{model}_{i*30:03d}s.png")
        await b.close()
    json.dump({"errors":errs},open(f"{BASE}/shots/long_{model}.json","w"))
asyncio.run(run(sys.argv[1]))

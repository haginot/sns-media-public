from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    ctx = b.new_context(viewport={"width":1280,"height":1000}, device_scale_factor=2, locale="ja-JP")
    pg = ctx.new_page()
    pg.goto("https://zenn.dev/", wait_until="networkidle"); pg.wait_for_timeout(1500)
    info = pg.evaluate("""() => {
      const hs=[...document.querySelectorAll('h2,h3')].filter(h=>h.textContent.trim().startsWith('Tech'));
      const h=hs[0]; let sec=h.closest('section')||h.parentElement.parentElement;
      const arts=[...sec.querySelectorAll('article')];
      const r=sec.getBoundingClientRect();
      return {sec:[r.x,r.y+scrollY,r.width,r.height], head:(()=>{const q=h.getBoundingClientRect();return [q.x,q.y+scrollY,q.width,q.height]})(),
        items:arts.map(a=>{const q=a.getBoundingClientRect();const l=a.querySelector('a[href*="/articles/"]');
          return {href:l&&l.getAttribute('href'),title:(a.querySelector('h2,h3')||a).textContent.trim().slice(0,60),rect:[q.x,q.y+scrollY,q.width,q.height],likes:(a.textContent.match(/(\\d+)\\s*$/)||[])[1], text:a.innerText.replace(/\\n/g,' | ').slice(0,200)}})}
    }""")
    json.dump(info, open("dom.json","w"), ensure_ascii=False, indent=1)
    pg.screenshot(path="page_full.png", full_page=True)
    b.close()

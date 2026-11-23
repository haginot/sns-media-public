from math import cos, pi, sin
from pathlib import Path
from random import Random
from string import Template
from tempfile import NamedTemporaryFile

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent


def svg(viewbox, contents, cls="prop"):
    return f'<svg class="{cls}" viewBox="{viewbox}" aria-hidden="true">{contents}</svg>'


def sparkle(x, y, r, color):
    return f'<path d="M{x-r} {y}Q{x} {y-2} {x} {y-r}Q{x+2} {y} {x+r} {y}Q{x} {y+2} {x} {y+r}Q{x-2} {y} {x-r} {y}Z" fill="{color}"/>'


def balloon(x, y, size, light, dark, index):
    return f'''<g transform="translate({x} {y}) scale({size})">
    <defs><radialGradient id="balloon{index}" cx=".33" cy=".25" r=".77">
      <stop stop-color="white"/><stop offset=".37" stop-color="{light}"/><stop offset="1" stop-color="{dark}"/>
    </radialGradient></defs>
    <path d="M0 55c-31 34 32 41 0 81" fill="none" stroke="{dark}" stroke-width="2"/>
    <path d="M0 55C-15 52-42 22-42-5a42 45 0 1 1 84 0c0 27-27 57-42 60l7 8h-14Z" fill="url(#balloon{index})"/>
    <path d="M-29-9q1-19 17-25" fill="none" stroke="white" stroke-opacity=".76" stroke-width="5" stroke-linecap="round"/>
    </g>'''


def fireworks(x, y, size, color):
    rays = []
    for i in range(15):
        angle = i * 2 * pi / 15
        dx, dy = cos(angle), sin(angle)
        end = size * (.77 + i % 3 * .1)
        rays.append(f'<path d="M{x+dx*size*.27} {y+dy*size*.27}l{dx*end*.59} {dy*end*.59}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
        rays.append(sparkle(x + dx * end, y + dy * end, 5, "white"))
    return "".join(rays) + sparkle(x, y, 16, color)


def decoration(theme, w, h):
    square = w == h
    random = Random(f"{theme}{w}")
    parts = []
    if theme == "award":
        origin = w * (.7 if square else .736)
        parts.append(f'''<defs>
        <linearGradient id="beam" x2="0" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="#ffdc87" stop-opacity=".6"/><stop offset="1" stop-color="#f0c06a" stop-opacity="0"/></linearGradient>
        <linearGradient id="carpet" x2="0" y2="1"><stop stop-color="#4d1318"/><stop offset="1" stop-color="#ac202d"/></linearGradient>
        </defs>
        <path d="M{origin-33} 0h66l{w*.27} {h*.75}h{-w*.65}Z" fill="url(#beam)"/>
        <path d="M{w*.37} {h*.63}H{w*.68}L{w*.96} {h}H{w*.04}Z" fill="url(#carpet)" stroke="#d38a49" stroke-width="3"/>
        <rect x="26" y="26" width="{w-52}" height="{h-52}" rx="18" fill="none" stroke="#c7964c" stroke-opacity=".65"/>
        <rect x="35" y="35" width="{w-70}" height="{h-70}" rx="13" fill="none" stroke="#fbe2a2" stroke-opacity=".27"/>''')
        palette = ["#ffdc85", "#ae6c28", "#fff2b7", "#e7a849"]
    elif theme == "party":
        palette = ["#f656a6", "#ffc62f", "#40cfa8", "#55acf3", "#a987ef"]
        cx, cy = w * (.5 if square else .38), h * .42
        for i in range(20):
            a = i * pi / 10
            points = " ".join(f"{cx + cos(t)*w*1.3},{cy + sin(t)*w*1.3}" for t in (a, a+.12))
            parts.append(f'<polygon points="{cx},{cy} {points}" fill="white" opacity=".32"/>')
        for i, (x, y, size) in enumerate([(w*.09,h*.28,1.27),(w*.88,h*.17,1.42),(w*.96,h*.28,1.05),(w*.10,h*.55,.86),(w*.19,h*.14,.72)] if square else [(w*.49,h*.14,1.25),(w*.60,h*.12,.93),(w*.91,h*.16,1.15),(w*.95,h*.26,.93)]):
            parts.append(balloon(x,y,size,["#ffa8da","#fff39a","#adf5e0","#bde8ff","#ffc6df"][i],palette[i],i))
        for i, (x, y, angle) in enumerate([(w*.09,h*.08,30),(w*.93,h*.41,18),(w*.09,h*.70,-24),(w*.84,h*.03,35)] if square else [(w*.07,h*.045,-25),(w*.39,h*.65,28),(w*.69,h*.08,30),(w*.95,h*.73,-20)]):
            parts.append(f'<path d="M0 0q120 22 48 62t48 62" transform="translate({x} {y}) rotate({angle})" stroke="{palette[i]}" stroke-width="14" fill="none" stroke-linecap="round"/>')
        accents = [(112,457),(957,410),(91,765),(914,797),(113,147),(994,625)] if square else [(720,294),(906,205),(1488,371),(716,539),(155,646),(535,583),(1354,60),(812,645)]
        for i, (x,y) in enumerate(accents):
            color = palette[i % len(palette)]
            parts.append(f'<path d="M-18 -12Q0 -2 18 -12v16Q0 18-18 4Z" transform="translate({x} {y}) rotate({(i*71)%180})" fill="{color}" stroke="white" stroke-width="2"/>')
            parts.append(sparkle(x + 31, y - 18, 15, "white"))
        x, y = (78, 777) if square else (755, 614)
        parts.append(f'''<g transform="translate({x} {y}) rotate(-34) scale(.67)">
        <path d="M-28-38h56L15 55q-15 10-30 0Z" fill="#4bcdb0" stroke="white" stroke-width="4"/>
        <path d="M-23-6 23-23l-3 17-41 15m3 15 35-13-2 16-31 12" fill="#fff1a3"/>
        <ellipse cy="-38" rx="28" ry="8" fill="#2b817b" stroke="white" stroke-width="4"/>
        <path d="M-8-48Q-42-60-40-85m52 37q37-21 29-37M2-51q7-20-4-36" fill="none" stroke="#f25fa7" stroke-width="7" stroke-linecap="round"/>
        </g>''')
    else:
        palette = ["#8c68ef", "#fb69a5", "#f3ad32", "#5ac4f4", "#56c9aa"]
        parts.append(f'''<defs><radialGradient id="floor"><stop stop-color="#766de8" stop-opacity=".4"/><stop offset="1" stop-color="#766de8" stop-opacity="0"/></radialGradient></defs>
        <ellipse cx="{w*(.5 if square else .73)}" cy="{h*.76}" rx="{w*.49}" ry="{h*.23}" fill="url(#floor)"/>
        <path d="M0 {h*.72}Q{w*.5} {h*.57} {w} {h*.72}V{h}H0Z" fill="#9387fc" opacity=".12"/>''')
        bursts = [(w*.17,h*.22,78),(w*.81,h*.12,83),(w*.88,h*.36,80)] if square else [(w*.48,h*.13,84),(w*.68,h*.14,100),(w*.94,h*.43,74)]
        for i, (x,y,r) in enumerate(bursts):
            parts.append(fireworks(x,y,r,palette[i]))
        positions = [(w*.095,h*.39,1.05),(w*.91,h*.52,.94),(w*.94,h*.18,.9),(w*.11,h*.65,.8)] if square else [(w*.83,h*.19,1.43),(w*.91,h*.17,1.1),(w*.54,h*.18,.8),(w*.45,h*.59,.96)]
        for i, (x,y,size) in enumerate(positions):
            parts.append(balloon(x,y,size,["#ffc4e3","#bfeaff","#ffed96","#b9fae8"][i],palette[i+1],i))
    for i in range(220 if theme == "award" else 149):
        x, y = random.randrange(42,w-42), random.randrange(35,h-100)
        if square and 230 < x < w-230 and y < 420:
            continue
        if not square and x < 666 and 140 < y < 592:
            continue
        color = random.choice(palette)
        size = random.uniform(2,8 if theme == "award" else 11)
        if i % 3 == 0:
            parts.append(sparkle(x,y,size*1.55,"#fff4c7" if theme == "award" else "white"))
        elif i % 3 == 1:
            parts.append(f'<rect x="{x}" y="{y}" width="{size*1.6}" height="{size*.62}" rx="1" transform="rotate({random.randrange(180)} {x} {y})" fill="{color}"/>')
        else:
            parts.append(f'<circle cx="{x}" cy="{y}" r="{size*.45}" fill="{color}"/>')
    return svg(f"0 0 {w} {h}", "".join(parts), "decor")


TROPHY = svg("0 0 240 250", """
<defs><linearGradient id="gold"><stop stop-color="#8f4714"/><stop offset=".27" stop-color="#ffdf78"/><stop offset=".43" stop-color="#fff4b2"/><stop offset=".63" stop-color="#eca83b"/><stop offset=".82" stop-color="#9a4912"/><stop offset="1" stop-color="#ffd675"/></linearGradient></defs>
<path d="M73 32H31q-9 0-8 12c3 48 18 70 67 75m77-87h42q9 0 8 12c-3 48-18 70-67 75" fill="none" stroke="url(#gold)" stroke-width="12"/>
<path d="M107 136h26l-3 32q1 19 28 25v15H82v-15q27-6 28-25Z" fill="url(#gold)"/>
<path d="M59 24h122c-3 67-16 118-61 125C75 142 62 91 59 24Z" fill="url(#gold)" stroke="#ffde85" stroke-width="2"/>
<ellipse cx="120" cy="24" rx="61" ry="9" fill="#8b4111" stroke="#ffdf85" stroke-width="4"/>
<path d="M75 43q3 60 26 79" fill="none" stroke="#fff7ce" stroke-opacity=".59" stroke-width="5" stroke-linecap="round"/>
<rect x="70" y="203" width="100" height="13" rx="4" fill="url(#gold)"/>
<path d="M64 216h112l12 23H52Z" fill="#260e0c" stroke="#d8a253" stroke-width="3"/>
<path d="m120 59 8 17 19 3-14 13 3 19-16-9-16 9 3-19-14-13 19-3Z" fill="#fff0ae" stroke="#af6a20" stroke-width="2"/>
""" + sparkle(65,27,23,"#fff9dc") + sparkle(164,119,12,"#fff6c6"))

CRACKER = svg("0 0 160 155", """
<defs><linearGradient id="cracker"><stop stop-color="#b3228a"/><stop offset=".25" stop-color="#ff9edd"/><stop offset=".65" stop-color="#f45ab6"/><stop offset="1" stop-color="#ba2985"/></linearGradient></defs>
<g transform="rotate(29 76 105)">
<path d="M49 66h54l-10 78q-17 12-34 0Z" fill="url(#cracker)" stroke="white" stroke-width="3"/>
<path d="m55 98 43-15-2 16-39 15m2 12 35-12-2 15-31 12" fill="#ffe57b"/>
<ellipse cx="76" cy="66" rx="27" ry="9" fill="#70205e" stroke="white" stroke-width="3"/>
<path d="M65 58Q14 35 24 13M75 57Q82 21 70 11M91 59Q138 32 127 13" fill="none" stroke="#4fd3aa" stroke-width="6" stroke-linecap="round"/>
<path d="M53 41 37 12m60 28 10-32" stroke="#f77abc" stroke-width="7" stroke-linecap="round"/>
</g>
""" + sparkle(135,36,13,"white") + sparkle(42,34,14,"#ffcb45"))

PODIUM = svg("0 0 900 267", """
<defs>
  <linearGradient id="top" x2="0" y2="1"><stop stop-color="#c4caff"/><stop offset="1" stop-color="#f8f5ff"/></linearGradient>
  <linearGradient id="face" x2="0" y2="1"><stop stop-color="#b2a0ff"/><stop offset="1" stop-color="#7775df"/></linearGradient>
  <linearGradient id="base" x2="0" y2="1"><stop stop-color="#e0eeff"/><stop offset="1" stop-color="#9caaf4"/></linearGradient>
</defs>
<ellipse cx="450" cy="216" rx="434" ry="45" fill="#5353c7" opacity=".2"/>
<path d="M7 160v32c0 77 886 77 886 0v-32Z" fill="url(#base)"/>
<ellipse cx="450" cy="160" rx="443" ry="65" fill="#dce8ff" stroke="#fff" stroke-width="3"/>
<path d="M35 107v40c0 77 830 77 830 0v-40Z" fill="url(#face)"/>
<ellipse cx="450" cy="107" rx="415" ry="61" fill="url(#top)" stroke="#fefaff" stroke-width="3"/>
<path d="M60 57v38c0 73 780 73 780 0V57Z" fill="url(#face)"/>
<ellipse cx="450" cy="57" rx="390" ry="55" fill="url(#top)" stroke="white" stroke-width="3"/>
<path d="M102 76c135 45 561 45 696 0" fill="none" stroke="#fff" stroke-width="4" opacity=".75"/>
""" + sparkle(156,134,15,"white") + sparkle(747,119,16,"white"))


def render():
    template = Template((HERE / "design.html").read_text())
    patterns = [("award", TROPHY), ("party", CRACKER), ("stage", PODIUM)]
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path="/usr/bin/google-chrome")
        for number, (theme, prop) in enumerate(patterns, 1):
            for width, height in [(1600, 900), (1080, 1080)]:
                html = template.substitute(
                    theme=f"pattern-{theme}", shape="square" if width == height else "wide",
                    width=width, height=height, decor=decoration(theme, width, height), object=prop,
                )
                with NamedTemporaryFile(dir=HERE, suffix=".html", mode="w", encoding="utf-8") as source:
                    source.write(html)
                    source.flush()
                    page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
                    page.goto(Path(source.name).as_uri())
                    page.evaluate("document.fonts.ready")
                    page.screenshot(path=HERE.parent / f"p{number}_{theme}_{width}x{height}.png")
                    page.close()
        browser.close()


if __name__ == "__main__":
    render()

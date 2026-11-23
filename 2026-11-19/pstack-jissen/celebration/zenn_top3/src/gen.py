"""Generate celebration HTML for the Tech trend TOP3 milestone (V3-A world). Usage: python3 gen.py && python3 render.py"""
import math

INK = "#0D0E12"

def eyes_happy(dx, dy, sc=1.0, color="#FFFFFF"):
    w = 17 * sc
    return (f'<g transform="translate({dx},{dy}) scale({sc})">'
            f'<path d="M -52 10 C -46 -20, -14 -20, -8 10" fill="none" stroke="{color}" stroke-width="{w/sc}" stroke-linecap="round"/>'
            f'<path d="M 14 10 C 20 -20, 52 -20, 58 10" fill="none" stroke="{color}" stroke-width="{w/sc}" stroke-linecap="round"/></g>')

def eyes_tall(dx, dy, sc=1.0):
    return (f'<g transform="translate({dx},{dy}) scale({sc})">'
            '<rect x="-56" y="-42" width="32" height="82" rx="16" fill="#FFFFFF"/>'
            '<rect x="8" y="-48" width="32" height="82" rx="16" fill="#FFFFFF"/></g>')

def mouth(dx, dy, sc=1.0):
    return (f'<g transform="translate({dx},{dy}) scale({sc})">'
            '<path d="M -26 0 Q 0 34 26 0 Z" fill="#FFFFFF"/></g>')

def hat(dx, dy, rot, sc, base="#FFD13B", stripe="#FF2B4A", pom="#0E86FF"):
    return (f'<g transform="translate({dx},{dy}) rotate({rot}) scale({sc})">'
            f'<path d="M -46 0 L 0 -120 L 46 0 Q 0 16 -46 0 Z" fill="{base}"/>'
            f'<path d="M -30 -40 L 18 -72 L 24 -56 L -24 -24 Z" fill="{stripe}"/>'
            f'<path d="M -40 -8 L 32 -36 L 38 -18 L -30 6 Z" fill="{stripe}" opacity="1"/>'
            f'<circle cx="0" cy="-124" r="15" fill="{pom}"/></g>')

def arm(color, x1, y1, cx, cy, x2, y2, w=26):
    return (f'<path d="M {x1} {y1} Q {cx} {cy} {x2} {y2}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<circle cx="{x2}" cy="{y2}" r="{w*0.85}" fill="{color}"/>')

def teal(x, y, rot, sc):
    c = "#00B89C"
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">'
            + arm(c, 120, 40, 230, 20, 250, -70)
            + arm(c, 60, 110, 150, 210, 250, 200)
            + f'<path d="M -145 -20 C -160 -85, -105 -140, -40 -130 C -10 -175, 78 -172, 108 -122 C 168 -118, 195 -52, 160 2 C 188 60, 145 128, 82 122 C 45 162, -38 158, -72 115 C -135 120, -178 58, -145 -20 Z" fill="{c}"/>'
            + eyes_happy(36, 18, 1.0) + mouth(40, 64, 1.1)
            + hat(30, -150, 12, 1.0, "#FFD13B", "#FF5E00", "#8A54FF") + '</g>')

def blue(x, y, rot, sc):
    c = "#0E86FF"
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">'
            + arm(c, -170, 40, -290, 0, -300, -110, 30)
            + arm(c, -120, 140, -230, 230, -320, 170, 30)
            + '<path d="M -185 -15 C -215 -92, -150 -178, -58 -168 C 5 -225, 125 -212, 168 -135 C 235 -110, 245 8, 185 80 C 205 162, 118 228, 35 198 C -35 232, -145 198, -165 118 C -225 90, -225 18, -185 -15 Z" fill="#0E86FF"/>'
            + eyes_tall(-72, 10) + mouth(-80, 92, 1.4)
            + hat(-60, -175, -14, 1.15, "#FF5E00", "#FFD13B", "#00B89C") + '</g>')

def black(x, y, rot, sc):
    c = "#0B0C0F"
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">'
            + arm(c, 170, -170, 200, -320, 240, -430, 34)
            + arm(c, -60, -230, -120, -370, -40, -440, 34)
            + f'<ellipse cx="0" cy="0" rx="285" ry="245" fill="{c}"/>'
            + eyes_tall(65, -80, 1.15) + mouth(55, 20, 1.8)
            + hat(70, -238, 8, 1.3, "#00B89C", "#FFFFFF", "#FFD13B") + '</g>')

def orange(x, y, rot, sc):
    c = "#FF5E00"
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">'
            + arm(c, -170, -120, -300, -200, -310, -320, 32)
            + arm(c, -40, -230, -40, -350, 60, -400, 32)
            + '<path d="M -230 140 C -275 45, -210 -125, -85 -220 C 5 -290, 125 -265, 195 -140 C 265 -15, 290 120, 210 215 C 130 310, -185 235, -230 140 Z" fill="#FF5E00"/>'
            + eyes_tall(-75, -45, 1.05) + mouth(-80, 50, 1.6)
            + hat(-40, -250, -18, 1.25, "#8A54FF", "#FFD13B", "#FF2B4A") + '</g>')

def purple(x, y, rot, sc, cracker_dir=1):
    c = "#8A54FF"
    d = cracker_dir
    # cracker: apex in raised hand, opening points outward/up; burst from opening
    cr = (f'<g transform="translate({72*d},-64) rotate({38*d})">'
          '<path d="M 0 0 L -30 -112 Q 0 -122 30 -112 Z" fill="#FFD13B"/>'
          '<path d="M -10 -38 L 10 -38 L 14 -54 L -14 -54 Z" fill="#FF2B4A"/>'
          '<path d="M -19 -74 L 19 -74 L 24 -92 L -24 -92 Z" fill="#FF2B4A"/>'
          '<path d="M 0 -122 C -20 -160, -60 -150, -70 -200" fill="none" stroke="#0E86FF" stroke-width="7" stroke-linecap="round"/>'
          '<path d="M 0 -122 C 10 -170, -10 -190, 6 -240" fill="none" stroke="#00B89C" stroke-width="7" stroke-linecap="round"/>'
          '<path d="M 0 -122 C 30 -160, 70 -150, 76 -200" fill="none" stroke="#FF2B4A" stroke-width="7" stroke-linecap="round"/>'
          '<path d="M 0 -122 C 50 -140, 90 -120, 120 -150" fill="none" stroke="#FFD13B" stroke-width="7" stroke-linecap="round"/>'
          '<rect x="-40" y="-240" width="16" height="16" rx="3" fill="#FF5E00" transform="rotate(20 -40 -240)"/>'
          '<circle cx="44" cy="-235" r="8" fill="#8A54FF"/>'
          '<rect x="100" y="-200" width="14" height="14" rx="3" fill="#00B89C" transform="rotate(-30 100 -200)"/>'
          '<circle cx="-95" cy="-170" r="7" fill="#FFD13B"/>'
          '</g>')
    burst = ""
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">'
            + arm(c, 40*d, -20, 70*d, -40, 72*d, -64, 16)
            + arm(c, -45*d, -15, -80*d, -50, -85*d, -95, 16)
            + cr + burst
            + f'<line x1="0" y1="-60" x2="0" y2="-79" stroke="{c}" stroke-width="8" stroke-linecap="round"/>'
            + f'<circle cx="0" cy="-85" r="10" fill="{c}"/>'
            + f'<circle cx="0" cy="0" r="60" fill="{c}"/>'
            + eyes_happy(-3, 2, 0.5) + mouth(0, 26, 0.6)
            + '</g>')

def heart(x, y, rot, sc):
    c = "#FF2B4A"
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">'
            + arm(c, -55, -10, -90, -40, -100, -80, 15)
            + arm(c, 55, -10, 90, -40, 100, -80, 15)
            + f'<path d="M 0 64 C -46 38, -74 2, -62 -36 C -52 -66, -16 -68, 0 -42 C 16 -68, 52 -66, 62 -36 C 74 2, 46 38, 0 64 Z" fill="{c}"/>'
            + eyes_happy(-3, -6, 0.42) + mouth(0, 18, 0.5)
            + hat(0, -48, 6, 0.42, "#0E86FF", "#FFFFFF", "#FFD13B") + '</g>')

CONF_COLORS = ["#FF5E00", "#0E86FF", "#00B89C", "#FFD13B", "#8A54FF", "#FF2B4A"]

def confetti(points):
    out = []
    for i, (x, y) in enumerate(points):
        c = CONF_COLORS[i % len(CONF_COLORS)]
        k = i % 4
        r = (i * 37) % 90 - 45
        if k == 0:
            out.append(f'<rect x="{x-9}" y="{y-5}" width="18" height="10" rx="2" fill="{c}" transform="rotate({r} {x} {y})"/>')
        elif k == 1:
            out.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{c}"/>')
        elif k == 2:
            out.append(f'<path d="M {x-14} {y} q 7 -10 14 0 t 14 0" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round" transform="rotate({r} {x} {y})"/>')
        else:
            out.append(f'<path d="M {x} {y-12} Q {x} {y} {x+12} {y} Q {x} {y} {x} {y+12} Q {x} {y} {x-12} {y} Q {x} {y} {x} {y-12} Z" fill="{c}"/>')
    return "".join(out)

# Coordinates in the cropped Tech section, around the second-row left card.
SHOT_W, SHOT_H = 913, 350
HL = (12, 222, 442, 326)
CL_W, CL_H = 432, 128

def marker_ellipse(x1, y1, x2, y2, s, color="#FF5E00", w=7):
    """Hand-drawn rounded-rect loop around the row (does not cross row text)."""
    X1, Y1, X2, Y2 = x1 * s - 6, y1 * s - 6, x2 * s + 6, y2 * s + 6
    r = 26
    pts = []
    # perimeter walk with corner arcs, slightly overshooting at the end
    def arc(cx, cy, a0, a1, n=8):
        for i in range(n + 1):
            t = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    pts.append((X1 + r + 10, Y1 + 3))
    arc(X2 - r, Y1 + r, -90, 0)
    arc(X2 - r + 2, Y2 - r, 0, 90)
    arc(X1 + r, Y2 - r + 2, 90, 180)
    arc(X1 + r - 2, Y1 + r, 180, 270)
    pts.append((X1 + r + 60, Y1 - 5))
    out = []
    for i, (px, py) in enumerate(pts):
        j = math.sin(i * 1.7) * 1.6
        out.append(f"{px + j:.1f} {py - j:.1f}")
    return f'<path d="M {" L ".join(out)}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


GOLD, GOLD_D = "#FFC21A", "#E89B00"

def trophy(x, y, rot, sc):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">'
            f'<path d="M -70 -60 C -130 -60, -130 20, -50 30" fill="none" stroke="{GOLD_D}" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M 70 -60 C 130 -60, 130 20, 50 30" fill="none" stroke="{GOLD_D}" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M -78 -80 L 78 -80 C 78 20, 40 60, 0 62 C -40 60, -78 20, -78 -80 Z" fill="{GOLD}"/>'
            f'<path d="M -44 -62 C -44 -10, -30 20, -12 34" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>'
            f'<rect x="-14" y="60" width="28" height="36" fill="{GOLD_D}"/>'
            f'<rect x="-56" y="94" width="112" height="30" rx="8" fill="{GOLD_D}"/>'
            f'<rect x="-72" y="122" width="144" height="34" rx="8" fill="#0D0E12"/>'
            f'<text x="0" y="148" text-anchor="middle" font-family="Inter Tight, Inter, sans-serif" font-weight="900" font-size="26" fill="{GOLD}">TOP3</text>'
            f'<path d="M 0 -50 L 9 -30 L 31 -28 L 14 -13 L 19 9 L 0 -2 L -19 9 L -14 -13 L -31 -28 L -9 -30 Z" fill="#FFFFFF"/>'
            '</g>')

def medal(x, y, rot, sc):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">'
            '<path d="M -40 -120 L -8 -20 L -36 -10 L -70 -112 Z" fill="#0E86FF"/>'
            '<path d="M 40 -120 L 8 -20 L 36 -10 L 70 -112 Z" fill="#FF2B4A"/>'
            f'<circle cx="0" cy="30" r="58" fill="{GOLD_D}"/><circle cx="0" cy="30" r="46" fill="{GOLD}"/>'
            f'<path d="M 0 -6 L 9 14 L 31 16 L 14 31 L 19 53 L 0 42 L -19 53 L -14 31 L -31 16 L -9 14 Z" fill="#FFFFFF"/>'
            '</g>')

def sparkle(x, y, r, c="#FFC21A"):
    return f'<path d="M {x} {y-r} Q {x} {y} {x+r} {y} Q {x} {y} {x} {y+r} Q {x} {y} {x-r} {y} Q {x} {y} {x} {y-r} Z" fill="{c}"/>'

def streamer(x, y, rot, c, sc=1):
    return (f'<path transform="translate({x},{y}) rotate({rot}) scale({sc})" d="M 0 0 c 20 -24 40 24 60 0 s 40 24 60 0 s 40 24 60 0" '
            f'fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round"/>')

STEP_CSS = """
.step { position: absolute; z-index: 22; display: flex; align-items: center; gap: 10px; background: #0D0E12; color: #fff;
  font-weight: 900; border-radius: 999px; padding: 8px 20px; white-space: nowrap; letter-spacing: -0.01em; box-shadow: 6px 7px 0 #FFC21A; }
.step .old { color: #9AA3B2; text-decoration: line-through; text-decoration-thickness: 3px; }
.step .arr { color: #FFC21A; } .step .new { color: #FF5E00; background: #fff; border-radius: 999px; padding: 2px 14px; }
"""

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: %(W)dpx; height: %(H)dpx; overflow: hidden; background: #F9FAF8;
  font-family: "Inter Tight", "Inter", "Noto Sans CJK JP", sans-serif; -webkit-font-smoothing: antialiased; }
.stage { position: relative; width: %(W)dpx; height: %(H)dpx; background: #F9FAF8; overflow: hidden; }
.art { position: absolute; inset: 0; z-index: 1; }
.fore { position: absolute; inset: 0; z-index: 30; pointer-events: none; }
.head { position: absolute; left: 0; right: 0; top: %(head_top)dpx; text-align: center; z-index: 20; }
.pill { display: inline-block; background: #0D0E12; color: #fff; font-weight: 900; font-size: %(pill_fs)dpx;
  padding: 7px 22px; border-radius: 999px; letter-spacing: -0.01em; line-height: 1.15; }
.h1 { font-weight: 900; color: #0D0E12; letter-spacing: -0.035em; line-height: 1.06; margin-top: %(h1_mt)dpx;
  font-feature-settings: "palt"; }
.h1 .a { font-size: %(h1a)dpx; }
.h1 .b { font-size: %(h1b)dpx; }
.h1 .o { color: #FF5E00; }
.h1 .bl { color: #0E86FF; }
.title { margin-top: %(t_mt)dpx; font-size: %(t_fs)dpx; font-weight: 800; color: #3D4452; letter-spacing: -0.01em;
  line-height: 1.35; font-feature-settings: "palt"; }
.card { position: absolute; z-index: 10; background: #fff; border-radius: 22px; padding: 12px;
  border: 2px solid #DDE2EC; box-shadow: 10px 12px 0 #DCE2EC; }
.card img { display: block; border-radius: 12px; }
.card svg { position: absolute; left: 12px; top: 12px; overflow: visible; }
.likes { position: absolute; right: 24px; bottom: 15px; color: #3D4452; font-size: 22px; font-weight: 800; line-height: 1; }
.tag { position: absolute; z-index: 12; background: #FF5E00; color: #fff; font-weight: 900; border-radius: 999px;
  padding: 6px 18px; white-space: nowrap; letter-spacing: -0.01em; box-shadow: 0 5px 0 #E2D2C6; }
.bub { position: absolute; z-index: 25; background: #fff; border: 3.5px solid #0D0E12; border-radius: 22px;
  font-weight: 900; color: #0D0E12; padding: 10px 22px; white-space: nowrap; letter-spacing: -0.02em; line-height: 1.1; }
.bub .o { color: #FF5E00; } .bub .bl { color: #0E86FF; } .bub .r { color: #FF2B4A; }
.footer { position: absolute; bottom: 40px; z-index: 20; font-size: %(f_fs)dpx; font-weight: 700; color: #646D7D; white-space: nowrap; }
"""

def bubble(x, y, text, fs, tail):
    # tail: (side, offset) drawn as svg triangle in .fore layer separately; here return html
    return f'<div class="bub" style="left:{x}px;top:{y}px;font-size:{fs}px">{text}</div>'

def tail_svg(x1, y1, x2, y2, tip_x, tip_y, dirn='down'):
    if dirn == 'up':
        return (f'<path d="M {x1} {y1} L {tip_x} {tip_y} L {x2} {y2}" fill="#FFFFFF" stroke="#0D0E12" stroke-width="3.5" stroke-linejoin="round"/>'
                f'<path d="M {x1+3} {y1+3} L {x2-3} {y2+3}" stroke="#FFFFFF" stroke-width="6"/>')
    # triangle tail with border: base points (x1,y1),(x2,y2) on bubble edge, tip outside
    return (f'<path d="M {x1} {y1} L {tip_x} {tip_y} L {x2} {y2}" fill="#FFFFFF" stroke="#0D0E12" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<path d="M {x1+3} {y1-3 if y1==y2 else y1} L {x2-3} {y2-3 if y1==y2 else y2}" stroke="#FFFFFF" stroke-width="6"/>')

def page(cfg):
    W, H = cfg["W"], cfg["H"]
    css = CSS % cfg + STEP_CSS
    s = cfg["card_w"] / SHOT_W
    sh = SHOT_H * s
    cs = cfg["cl_w"] / CL_W
    ch = CL_H * cs
    card = (f'<div class="card" style="left:{cfg["card_x"]}px;top:{cfg["card_y"]}px;transform:rotate({cfg["card_rot"]}deg)">'
            f'<img src="shot_top3.png" style="width:{cfg["card_w"]}px;height:{sh:.1f}px">'
            f'<svg width="{cfg["card_w"]}" height="{sh:.1f}">{marker_ellipse(*HL, s)}</svg></div>')
    inset = (f'<div class="card" style="left:{cfg["cl_x"]}px;top:{cfg["cl_y"]}px;transform:rotate({cfg["cl_rot"]}deg);padding:10px;border-radius:20px;border:4px solid #FF5E00;box-shadow:8px 10px 0 #F1DCCD">'
             f'<img src="shot_row.png" style="width:{cfg["cl_w"]}px;height:{ch:.1f}px"><span class="likes">♡ 47</span></div>')
    tags = "".join(f'<div class="tag" style="left:{x}px;top:{y}px;font-size:{fs}px;transform:rotate({r}deg)">{t}</div>' for x, y, fs, r, t in cfg["tags"])
    bubs = "".join(bubble(*b[:4], None) for b in cfg["bubbles"])
    tails = "".join(tail_svg(*t) for t in cfg["tails"])
    return f"""<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><style>{css}</style></head><body>
<div class="stage">
<svg class="art" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
{cfg["rings"]}{confetti(cfg["confetti"])}{cfg.get("deco","")}{cfg["chars"]}
</svg>
<div class="head"><span class="pill">カンリー Techブログ</span>
<div class="h1">{cfg["h1_html"]}</div>
<div class="title">{cfg["title_html"]}</div></div>
{card}{inset}{tags}
<div class="step" style="{cfg["step_pos"]};font-size:{cfg["step_fs"]}px"><span class="old">TOP5</span><span class="arr">→</span><span class="new">TOP3</span><span>ランクアップ！</span></div>
<svg class="fore" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{tails}{cfg.get("fore","")}</svg>
{bubs}
<div class="footer" style="{cfg["footer_pos"]}">作図：萩野貴拓</div>
</div></body></html>"""

TITLE = "寝てる間に自動で動くAIエージェントを誰でも作れる：10分でわかる pstack 実践ガイド"


def gold_conf(points):
    return "".join(sparkle(x, y, r) for x, y, r in points)

wide = dict(
    W=1600, H=900, head_top=42, pill_fs=22, h1_mt=8, h1a=91, h1b=91, t_mt=6, t_fs=24, f_fs=19,
    h1_html='<span class="a">Techトレンド <span class="o">TOP3</span>入り！</span>',
    title_html="「" + TITLE + "」",
    card_x=290, card_y=294, card_rot=-2, card_w=740,
    cl_x=1060, cl_y=501, cl_rot=3, cl_w=440,
    tags=[(1080, 467, 22, 3, "拡大")],
    step_pos="left:420px;top:728px", step_fs=27,
    bubbles=[(40, 500, '<span class="o">まだ上がる！</span>', 32),
             (1200, 262, '<span class="o">TOP3！</span>', 42),
             (1160, 722, '<span class="r">ありがとう！</span>', 32)],
    tails=[(170, 558, 210, 558, 236, 590), (1300, 326, 1340, 326, 1380, 356), (1300, 780, 1340, 780, 1372, 810)],
    rings='<path d="M -50 430 C 170 210, 440 105, 770 84 C 1110 62, 1390 175, 1650 375" fill="none" stroke="#E5E9F0" stroke-width="3.5" stroke-dasharray="12 16" stroke-linecap="round"/>'
          '<path d="M -40 610 C 260 770, 560 832, 880 806 C 1180 780, 1420 655, 1660 475" fill="none" stroke="#E5E9F0" stroke-width="3.5" stroke-dasharray="10 16" stroke-linecap="round"/>',
    confetti=[(300, 60), (262, 160), (1310, 70), (1350, 180), (250, 300), (110, 300), (1180, 400), (1460, 410), (1520, 540),
              (60, 460), (290, 470), (1050, 860), (560, 860), (1110, 255), (501, 256), (1440, 300), (640, 885), (40, 700),
              (380, 30), (1220, 40), (160, 400), (1560, 640), (1040, 420), (1100, 870), (720, 30), (900, 245), (240, 640), (1490, 470)],
    deco=streamer(1150, 430, 6, "#FFC21A", 0.7) + streamer(1205, 229, 10, "#FF2B4A", 0.8) + streamer(1020, 690, -10, "#00B89C", 0.7)
         + gold_conf([(200, 120, 18), (1400, 120, 20), (1530, 360, 16), (90, 640, 14), (1080, 760, 14), (700, 870, 12), (330, 240, 11), (125, 355, 9), (1465, 235, 11), (1045, 650, 9), (615, 695, 11), (912, 660, 8), (1180, 825, 10), (1555, 464, 10)]),
    chars=teal(70, 70, 14, 0.78) + blue(1560, 95, -14, 0.78) + black(95, 905, 22, 0.62) + orange(1555, 880, -18, 0.62)
          + purple(170, 429, -14, 0.82) + heart(1010, 800, 12, 0.72),
    fore=trophy(250, 700, -8, 0.78) + medal(1452, 410, 10, 0.62),
    footer_pos="left:50%;transform:translateX(-50%)",
)

square = dict(
    W=1080, H=1080, head_top=40, pill_fs=22, h1_mt=8, h1a=96, h1b=124, t_mt=10, t_fs=25, f_fs=19,
    h1_html='<span class="a">Techトレンド</span><br><span class="b"><span class="o">TOP3</span>入り！</span>',
    title_html="寝てる間に自動で動くAIエージェントを誰でも作れる：<br>10分でわかる pstack 実践ガイド",
    card_x=98, card_y=466, card_rot=-2, card_w=710,
    cl_x=511, cl_y=780, cl_rot=3, cl_w=460,
    tags=[(531, 748, 20, 3, "拡大")],
    step_pos="left:68px;top:815px", step_fs=25,
    bubbles=[(790, 402, '<span class="o">TOP3！</span>', 34),
             (47, 394, '<span class="o">まだ上がる！</span>', 26),
             (752, 963, '<span class="r">ありがとう！</span>', 28)],
    tails=[(110, 396, 140, 396, 118, 364, 'up'), (902, 404, 936, 404, 965, 380, 'up'), (900, 1017, 940, 1017, 975, 1040)], rings="",
    confetti=[(250, 60), (840, 60), (180, 200), (900, 210), (60, 430), (1030, 430), (720, 460), (990, 560), (40, 980),
              (300, 1040), (720, 1040), (620, 990), (1010, 850), (230, 300), (860, 300), (360, 30), (720, 30), (40, 600),
              (1040, 640), (560, 440), (130, 880), (480, 1050)],
    deco=streamer(20, 190, -25, "#FFC21A", 0.6) + streamer(820, 398, -10, "#FF2B4A", 0.6)
         + gold_conf([(206, 130, 12), (1000, 330, 14), (30, 520, 12), (560, 1000, 12), (1030, 760, 12), (55, 310, 9), (970, 150, 12), (68, 505, 8), (855, 693, 12), (365, 785, 10), (1002, 904, 10), (310, 965, 9)]),
    chars=teal(40, 50, 14, 0.58) + blue(1050, 60, -14, 0.58) + black(1085, 1095, -20, 0.5) + orange(1110, 420, -30, 0.36)
          + purple(960, 600, 8, 0.55, -1) + heart(84, 1012, 8, 0.55),
    fore=trophy(243, 928, -8, 0.54) + medal(982, 709, 10, 0.52),
    footer_pos="left:50%;transform:translateX(-50%)",
)

if __name__ == "__main__":
    open("celebrate_1600x900.html", "w").write(page(wide))
    open("celebrate_1080x1080.html", "w").write(page(square))
    print("ok")

import math
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path('/workspace/pivot-monthly-top5-celebration/v2')
SRC = ROOT / 'src'

FONT_CSS = """
@font-face { font-family: 'ShipporiMinchoB1'; src: url('../fonts/ShipporiMinchoB1-SemiBold.ttf'); font-weight: 600; font-style: normal; }
@font-face { font-family: 'ShipporiMinchoB1'; src: url('../fonts/ShipporiMinchoB1-Bold.ttf'); font-weight: 700; font-style: normal; }
@font-face { font-family: 'ShipporiMinchoB1'; src: url('../fonts/ShipporiMinchoB1-ExtraBold.ttf'); font-weight: 800; font-style: normal; }
@font-face { font-family: 'ZenOldMincho'; src: url('../fonts/ZenOldMincho-Bold.ttf'); font-weight: 700; font-style: normal; }
@font-face { font-family: 'ZenOldMincho'; src: url('../fonts/ZenOldMincho-Black.ttf'); font-weight: 900; font-style: normal; }
@font-face { font-family: 'Cinzel'; src: url('../fonts/Cinzel-Variable.ttf'); font-weight: 400 900; font-style: normal; }
@font-face { font-family: 'CinzelDec'; src: url('../fonts/CinzelDecorative-Black.ttf'); font-weight: 900; font-style: normal; }
@font-face { font-family: 'CormorantSC'; src: url('../fonts/CormorantSC-Regular.ttf'); font-weight: 400; font-style: normal; }
@font-face { font-family: 'PlayfairDisplay'; src: url('../fonts/PlayfairDisplay-VariableFont_wght.ttf'); font-weight: 400 900; font-style: normal; }
@font-face { font-family: 'PlayfairSC'; src: url('../fonts/PlayfairDisplaySC-Bold.ttf'); font-weight: 700; font-style: normal; }
"""

GOLD_DEFS = """
<defs>
  <!-- Deep high-contrast metallic champagne gold for crisp legibility on ivory -->
  <linearGradient id="goldTextGrad" x1="0%" y1="0%" x2="8%" y2="100%">
    <stop offset="0%"   stop-color="#fff8dc"/>
    <stop offset="18%"  stop-color="#eccb77"/>
    <stop offset="38%"  stop-color="#b47a1f"/>
    <stop offset="50%"  stop-color="#6e4309"/>
    <stop offset="56%"  stop-color="#a66f19"/>
    <stop offset="74%"  stop-color="#f5d88b"/>
    <stop offset="90%"  stop-color="#b98126"/>
    <stop offset="100%" stop-color="#683e08"/>
  </linearGradient>

  <linearGradient id="goldDiagGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%"   stop-color="#fff6d1"/>
    <stop offset="22%"  stop-color="#e5be63"/>
    <stop offset="46%"  stop-color="#8b560e"/>
    <stop offset="56%"  stop-color="#faecc0"/>
    <stop offset="78%"  stop-color="#b98227"/>
    <stop offset="100%" stop-color="#623a07"/>
  </linearGradient>

  <linearGradient id="goldSpecGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%"   stop-color="#ffffff" stop-opacity="0.88"/>
    <stop offset="26%"  stop-color="#fff4cc" stop-opacity="0.32"/>
    <stop offset="52%"  stop-color="#ffffff" stop-opacity="0.0"/>
    <stop offset="100%" stop-color="#ffffff" stop-opacity="0.0"/>
  </linearGradient>

  <linearGradient id="goldSatin" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%"   stop-color="#f2d68d"/>
    <stop offset="35%"  stop-color="#b9842c"/>
    <stop offset="65%"  stop-color="#eed082"/>
    <stop offset="100%" stop-color="#7c4f11"/>
  </linearGradient>

  <radialGradient id="sealIvory" cx="40%" cy="35%" r="65%">
    <stop offset="0%"   stop-color="#fffdf8"/>
    <stop offset="68%"  stop-color="#f8efe0"/>
    <stop offset="100%" stop-color="#e6d2ad"/>
  </radialGradient>

  <filter id="goldEmbossed" x="-12%" y="-12%" width="124%" height="128%">
    <feDropShadow dx="0" dy="1.4" stdDeviation="0.5" flood-color="#fffef8" flood-opacity="0.95"/>
    <feDropShadow dx="0" dy="4.5" stdDeviation="3.8" flood-color="#4e320b" flood-opacity="0.34"/>
  </filter>

  <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
    <feDropShadow dx="0" dy="6" stdDeviation="6.5" flood-color="#4e3410" flood-opacity="0.20"/>
  </filter>

  <filter id="badgeShadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="#5a3d14" flood-opacity="0.24"/>
  </filter>
</defs>
"""

def laurel_wreath_svg(cx, cy, r_inner=74, n_pairs=11, scale_leaf=1.0):
    paths = []
    for side in (-1, 1):
        pts = []
        for i in range(n_pairs + 1):
            t = i / n_pairs
            a_deg = (90 - side * 10) - side * t * 150
            a = math.radians(a_deg)
            rad = r_inner + math.sin(t * math.pi) * 6
            pts.append((cx + math.cos(a) * rad, cy + math.sin(a) * rad))
        d_stem = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        paths.append(f'<path d="{d_stem}" fill="none" stroke="url(#goldSatin)" stroke-width="{2.2*scale_leaf:.2f}" stroke-linecap="round"/>')

        for i in range(1, n_pairs + 1):
            t = i / n_pairs
            a_deg = (90 - side * 10) - side * t * 150
            a = math.radians(a_deg)
            rad = r_inner + math.sin(t * math.pi) * 6
            bx = cx + math.cos(a) * rad
            by = cy + math.sin(a) * rad
            tang = a_deg - side * 90
            leaf_len = (16 + 4 * math.sin(t * math.pi)) * scale_leaf
            leaf_w = 5.4 * scale_leaf
            for out_dir in (-1, 1):
                ang_l = math.radians(tang + out_dir * side * 34)
                tx = bx + math.cos(ang_l) * leaf_len
                ty = by + math.sin(ang_l) * leaf_len
                perp = ang_l + math.pi / 2
                mx = bx + math.cos(ang_l) * leaf_len * 0.45
                my = by + math.sin(ang_l) * leaf_len * 0.45
                c1x = mx + math.cos(perp) * leaf_w
                c1y = my + math.sin(perp) * leaf_w
                c2x = mx - math.cos(perp) * leaf_w
                c2y = my - math.sin(perp) * leaf_w
                paths.append(
                    f'<path d="M {bx:.1f},{by:.1f} Q {c1x:.1f},{c1y:.1f} {tx:.1f},{ty:.1f} Q {c2x:.1f},{c2y:.1f} {bx:.1f},{by:.1f} Z" '
                    f'fill="url(#goldDiagGrad)" stroke="#7a4e12" stroke-width="0.55"/>'
                )
    ty = cy - r_inner - 4 * scale_leaf
    s = 9.5 * scale_leaf
    paths.append(
        f'<path d="M {cx},{ty-s} L {cx+s*0.32},{ty-s*0.32} L {cx+s},{ty} L {cx+s*0.32},{ty+s*0.32} '
        f'L {cx},{ty+s} L {cx-s*0.32},{ty+s*0.32} L {cx-s},{ty} L {cx-s*0.32},{ty-s*0.32} Z" '
        f'fill="url(#goldDiagGrad)" stroke="#754911" stroke-width="0.6"/>'
    )
    return "\n".join(paths)


def emblem_medallion(cx, cy, radius=92, scale=1.0, ribbon_text="MONTHLY AWARD"):
    r = radius * scale
    laurel = laurel_wreath_svg(cx, cy, r_inner=r * 1.07, n_pairs=11, scale_leaf=scale * 0.96)
    # Wider ribbon so text always has generous padding inside
    rw = 196 * scale
    rh = 32 * scale
    ry = cy + r * 0.85
    ribbon = f'''
    <g filter="url(#softShadow)">
      <path d="M {cx-rw*0.56},{ry+6*scale} L {cx-rw*0.44},{ry+6*scale} L {cx-rw*0.44},{ry+rh+4*scale} L {cx-rw*0.58},{ry+rh+4*scale} L {cx-rw*0.51},{ry+rh*0.52+5*scale} Z" fill="#7c4e11"/>
      <path d="M {cx+rw*0.56},{ry+6*scale} L {cx+rw*0.44},{ry+6*scale} L {cx+rw*0.44},{ry+rh+4*scale} L {cx+rw*0.58},{ry+rh+4*scale} L {cx+rw*0.51},{ry+rh*0.52+5*scale} Z" fill="#7c4e11"/>
      <rect x="{cx-rw/2}" y="{ry}" width="{rw}" height="{rh}" rx="{5*scale}" fill="url(#goldDiagGrad)" stroke="#6f450f" stroke-width="{1.2*scale}"/>
      <rect x="{cx-rw/2+3*scale}" y="{ry+3*scale}" width="{rw-6*scale}" height="{rh-6*scale}" rx="{3*scale}" fill="none" stroke="#fff7da" stroke-opacity="0.72" stroke-width="{0.8*scale}"/>
      <text x="{cx}" y="{ry+rh*0.67}" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="{11.5*scale}" letter-spacing="{2.3*scale}" fill="#321f05">{ribbon_text}</text>
    </g>'''

    return f'''
    <g filter="url(#badgeShadow)">
      {laurel}
      <circle cx="{cx}" cy="{cy}" r="{r*0.92}" fill="url(#goldSatin)" stroke="#6f450f" stroke-width="{1.4*scale}"/>
      <circle cx="{cx}" cy="{cy}" r="{r*0.84}" fill="url(#sealIvory)" stroke="#b88837" stroke-width="{1.2*scale}"/>
      <circle cx="{cx}" cy="{cy}" r="{r*0.77}" fill="none" stroke="#c89b4b" stroke-dasharray="{3*scale} {3*scale}" stroke-width="{0.9*scale}"/>
      <text x="{cx}" y="{cy - 34*scale}" text-anchor="middle" font-family="Cinzel, serif" font-weight="700" font-size="{11.5*scale}" letter-spacing="{3.4*scale}" fill="#6e4e1c">PIVOT</text>
      <line x1="{cx-28*scale}" y1="{cy-26*scale}" x2="{cx+28*scale}" y2="{cy-26*scale}" stroke="#c29747" stroke-width="{1*scale}"/>
      <text x="{cx}" y="{cy - 6*scale}" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="{16.5*scale}" letter-spacing="{3.8*scale}" fill="#3d290c">TOP</text>
      <text x="{cx}" y="{cy + 42*scale}" text-anchor="middle" font-family="CinzelDec, Cinzel, serif" font-weight="900" font-size="{54*scale}" fill="url(#goldDiagGrad)" stroke="#683e08" stroke-width="{1.0*scale}">5</text>
      <text x="{cx}" y="{cy + 62*scale}" text-anchor="middle" font-family="Cinzel, serif" font-weight="700" font-size="{10.5*scale}" letter-spacing="{2.5*scale}" fill="#6e4e1c">2026 . 11</text>
      {ribbon}
    </g>'''


def hero_top5_svg(cx, baseline_y, text_size=76, num_size=108, anchor="middle"):
    """Compose 'トップ 5 入り' with sculptural oversized '5', crisp bronze rim, and balanced vertical alignment."""
    # dy=+1 on 5 and dy=-1 on 入り puts 5 visually centered with JP characters without sinking into lower badges
    return f'''
    <g filter="url(#goldEmbossed)">
      <text x="{cx}" y="{baseline_y}" text-anchor="{anchor}" fill="url(#goldTextGrad)" stroke="#633c09" stroke-width="1.5" paint-order="stroke fill"
            style="font-feature-settings:'palt' 1">
        <tspan font-family="ZenOldMincho, ShipporiMinchoB1, serif" font-weight="900" font-size="{text_size}" letter-spacing="-3">トップ</tspan><tspan dx="5" dy="1" font-family="CinzelDec, PlayfairDisplay, serif" font-weight="900" font-size="{num_size}" fill="url(#goldDiagGrad)">5</tspan><tspan dx="5" dy="-1" font-family="ZenOldMincho, ShipporiMinchoB1, serif" font-weight="900" font-size="{text_size}" letter-spacing="-2">入り</tspan>
      </text>
      <text x="{cx}" y="{baseline_y - 1.0}" text-anchor="{anchor}" fill="url(#goldSpecGrad)"
            style="font-feature-settings:'palt' 1">
        <tspan font-family="ZenOldMincho, ShipporiMinchoB1, serif" font-weight="900" font-size="{text_size}" letter-spacing="-3">トップ</tspan><tspan dx="5" dy="1" font-family="CinzelDec, PlayfairDisplay, serif" font-weight="900" font-size="{num_size}">5</tspan><tspan dx="5" dy="-1" font-family="ZenOldMincho, ShipporiMinchoB1, serif" font-weight="900" font-size="{text_size}" letter-spacing="-2">入り</tspan>
      </text>
    </g>'''


def ranking_ladder_svg(x, y, width=286):
    """Refined 5-slot ranking board highlighting the Top-5 breakthrough without fake titles or standalone rank digits."""
    h_row = 22
    gap = 9
    rows = []
    # Four muted peer slots + highlighted gold fifth slot (equal outer width looks like a clean editorial leaderboard)
    for i in range(5):
        ry = y + 40 + i * (h_row + gap)
        if i == 4:
            rows.append(f'''
              <g filter="url(#softShadow)">
                <rect x="{x-4}" y="{ry-2}" width="{width+8}" height="{h_row+8}" rx="6" fill="url(#goldDiagGrad)" stroke="#6f450f" stroke-width="1.1"/>
                <path d="M {x+14},{ry+6} L {x+16.5},{ry+11.5} L {x+22.5},{ry+12} L {x+18},{ry+16} L {x+19.5},{ry+22} L {x+14},{ry+18.8} L {x+8.5},{ry+22} L {x+10},{ry+16} L {x+5.5},{ry+12} L {x+11.5},{ry+11.5} Z"
                      fill="#fffaf0" stroke="#6f450f" stroke-width="0.6"/>
                <text x="{x+30}" y="{ry+17.5}" font-family="Cinzel, serif" font-weight="800" font-size="11.5" letter-spacing="1.8" fill="#321f05">MUSE · TOP 5 IN</text>
                <text x="{x+width-6}" y="{ry+17}" text-anchor="end" font-family="Cinzel, serif" font-weight="800" font-size="10.5" letter-spacing="1.2" fill="#4b2f08">▲ UP</text>
              </g>''')
        else:
            # Subtle tapering decorative bar inside fixed muted slot
            bar_w = width - 48 - i * 16
            rows.append(f'''
              <rect x="{x}" y="{ry}" width="{width}" height="{h_row}" rx="4.5" fill="#f5ede0" stroke="#dcc7a2" stroke-width="0.9"/>
              <circle cx="{x+13}" cy="{ry+h_row/2}" r="3.2" fill="#c39f61" opacity="0.72"/>
              <rect x="{x+26}" y="{ry+h_row/2-2}" width="{bar_w}" height="4" rx="2" fill="#d8c199" opacity="0.8"/>
            ''')
    total_h = 40 + 5 * (h_row + gap) + 18
    return f'''
    <g>
      <rect x="{x-18}" y="{y-16}" width="{width+36}" height="{total_h}" rx="12"
            fill="#fffdf8" fill-opacity="0.9" stroke="url(#goldSatin)" stroke-width="1.4" filter="url(#softShadow)"/>
      <text x="{x}" y="{y+9}" font-family="Cinzel, serif" font-weight="800" font-size="11" letter-spacing="2.6" fill="#7c5920">MONTHLY OVERALL TOP 5</text>
      <line x1="{x}" y1="{y+21}" x2="{x+width}" y2="{y+21}" stroke="#d9bc82" stroke-width="0.9"/>
      {''.join(rows)}
    </g>'''


def write_A():
    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
      {GOLD_DEFS}
      <rect x="24" y="24" width="1552" height="852" rx="14" fill="none" stroke="url(#goldSatin)" stroke-width="1.1" stroke-opacity="0.48"/>

      <!-- LEFT COLUMN -->
      <g>
        <text x="56" y="84" font-family="Cinzel, serif" font-weight="700" font-size="15.5" letter-spacing="4" fill="#7c5920">PIVOT MONTHLY RANKING</text>
        <text x="56" y="111" font-family="CormorantSC, Cinzel, serif" font-weight="400" font-size="15.5" letter-spacing="4.2" fill="#9a7435">OVERALL  ·  2026.11</text>
        <line x1="56" y1="128" x2="396" y2="128" stroke="url(#goldSatin)" stroke-width="1.5"/>

        <text x="54" y="188" font-family="ShipporiMinchoB1, serif" font-weight="700" font-size="35" letter-spacing="3.5" fill="#231c15"
              style="font-feature-settings:'palt' 1">月間総合ランキング</text>

        {hero_top5_svg(50, 304, text_size=76, num_size=110, anchor="start")}

        <line x1="56" y1="342" x2="396" y2="342" stroke="url(#goldSatin)" stroke-width="1.2"/>
        <circle cx="226" cy="342" r="3.8" fill="url(#goldDiagGrad)" stroke="#754911" stroke-width="0.5"/>

        <rect x="56" y="368" width="340" height="78" rx="10" fill="#fffdf7" fill-opacity="0.92" stroke="url(#goldSatin)" stroke-width="1.4" filter="url(#softShadow)"/>
        <text x="76" y="395" font-family="Cinzel, serif" font-weight="700" font-size="11" letter-spacing="3.2" fill="#825e23">FEATURED EPISODE</text>
        <text x="76" y="427" font-family="ShipporiMinchoB1, serif" font-weight="800" font-size="25.5" letter-spacing="1" fill="#221b14"
              style="font-feature-settings:'palt' 1">Meta「Muse」解説</text>

        <text x="56" y="852" font-family="ShipporiMinchoB1, serif" font-weight="600" font-size="16" letter-spacing="2.2" fill="#6f5d46">作図：萩野貴拓</text>
      </g>

      <!-- RIGHT COLUMN -->
      <g>
        {emblem_medallion(1372, 232, radius=92, scale=1.04, ribbon_text="MONTHLY AWARD")}
        {ranking_ladder_svg(1228, 492, width=286)}
      </g>
    </svg>
    '''
    html = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><style>
{FONT_CSS}
*{{margin:0;box-sizing:border-box}}
body{{width:1600px;height:900px;background:#f7f1e6 url(compA_base.png) left top/1600px 900px no-repeat;position:relative;overflow:hidden}}
svg{{position:absolute;inset:0;width:1600px;height:900px;display:block}}
</style></head><body>{svg}</body></html>'''
    (SRC/'A_v2.html').write_text(html)


def write_C():
    # Move divider/pill down slightly to y=268..296 and card slightly down to top=324 so '5' never touches the pill!
    # Card bottom ~ 324+258 = 582, nameplate top = 606..670, credit = 858. Still plenty of room!
    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
      {GOLD_DEFS}
      <rect x="24" y="24" width="1552" height="852" rx="14" fill="none" stroke="url(#goldSatin)" stroke-width="1.1" stroke-opacity="0.45"/>

      <!-- TOP CENTER CREST & HERO TYPOGRAPHY -->
      <g>
        <line x1="410" y1="54" x2="600" y2="54" stroke="url(#goldSatin)" stroke-width="1.2"/>
        <line x1="1000" y1="54" x2="1190" y2="54" stroke="url(#goldSatin)" stroke-width="1.2"/>
        <text x="800" y="60" text-anchor="middle" font-family="Cinzel, serif" font-weight="700" font-size="15.5" letter-spacing="4.6" fill="#7c5920">PIVOT MONTHLY RANKING · 2026.11</text>

        <text x="800" y="110" text-anchor="middle" font-family="ShipporiMinchoB1, serif" font-weight="700" font-size="36" letter-spacing="6" fill="#231c15"
              style="font-feature-settings:'palt' 1">月間総合ランキング</text>

        {laurel_wreath_svg(472, 192, r_inner=44, n_pairs=8, scale_leaf=0.60)}
        <text x="472" y="187" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="10.5" letter-spacing="2" fill="#755017">TOP</text>
        <text x="472" y="214" text-anchor="middle" font-family="CinzelDec, serif" font-weight="900" font-size="26" fill="url(#goldDiagGrad)" stroke="#6d430b" stroke-width="0.7">5</text>

        {laurel_wreath_svg(1128, 192, r_inner=44, n_pairs=8, scale_leaf=0.60)}
        <text x="1128" y="187" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="10.5" letter-spacing="2" fill="#755017">TOP</text>
        <text x="1128" y="214" text-anchor="middle" font-family="CinzelDec, serif" font-weight="900" font-size="26" fill="url(#goldDiagGrad)" stroke="#6d430b" stroke-width="0.7">5</text>

        {hero_top5_svg(800, 224, text_size=82, num_size=118, anchor="middle")}

        <!-- Gold ribbon divider clearly separated below hero headline -->
        <line x1="510" y1="274" x2="1090" y2="274" stroke="url(#goldSatin)" stroke-width="1.3"/>
        <rect x="698" y="259" width="204" height="30" rx="15" fill="url(#goldDiagGrad)" stroke="#6f450f" stroke-width="1.1" filter="url(#softShadow)"/>
        <text x="800" y="278.5" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="11.5" letter-spacing="3" fill="#321f05">OFFICIAL TOP 5</text>
      </g>

      <!-- EPISODE NAMEPLATE BELOW CARD -->
      <g>
        <rect x="615" y="612" width="410" height="66" rx="10" fill="#fffdf8" fill-opacity="0.94" stroke="url(#goldSatin)" stroke-width="1.4" filter="url(#softShadow)"/>
        <text x="820" y="635" text-anchor="middle" font-family="Cinzel, serif" font-weight="700" font-size="10.5" letter-spacing="3.2" fill="#825e23">PIVOT PROGRAM · NOV 2026</text>
        <text x="820" y="663" text-anchor="middle" font-family="ShipporiMinchoB1, serif" font-weight="800" font-size="24.5" letter-spacing="1.5" fill="#221b14"
              style="font-feature-settings:'palt' 1">Meta「Muse」解説</text>
      </g>

      <text x="820" y="858" text-anchor="middle" font-family="ShipporiMinchoB1, serif" font-weight="600" font-size="16" letter-spacing="2.2" fill="#6f5d46">作図：萩野貴拓</text>
    </svg>
    '''
    html = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><style>
{FONT_CSS}
*{{margin:0;box-sizing:border-box}}
body{{width:1600px;height:900px;background:#f7f1e6 url(compC_base.png) left top/1600px 900px no-repeat;position:relative;overflow:hidden}}
svg.overlay{{position:absolute;inset:0;width:1600px;height:900px;display:block;pointer-events:none;z-index:2}}
.card{{
  position:absolute;left:585px;top:324px;width:470px;padding:9px;
  border-radius:18px;
  background:linear-gradient(135deg,#fff6d8 0%,#d7a74d 28%,#8b5c1a 50%,#fae6aa 74%,#a57428 100%);
  box-shadow:0 24px 48px rgba(78,52,16,.24), inset 0 1px 0 rgba(255,255,255,.85);
  z-index:1;
}}
.card-inner{{padding:2px;border-radius:12px;background:#fffaf0}}
.card img{{width:448px;height:auto;display:block;border-radius:10px}}
.corner-badge{{
  position:absolute;right:-16px;top:-14px;
  padding:6px 15px;border-radius:999px;
  background:linear-gradient(135deg,#fff5cf,#d7a649 48%,#9a681f);
  border:1.5px solid #fff8df;
  box-shadow:0 6px 16px rgba(78,52,16,.28);
  font-family:"Cinzel",serif;font-weight:800;font-size:12px;letter-spacing:2.4px;color:#321f05;
  z-index:3;
}}
</style></head><body>
<div class="card">
  <div class="card-inner"><img src="thumb.png" alt=""></div>
  <div class="corner-badge">TOP 5</div>
</div>
<svg class="overlay" xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">{svg.split('<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',1)[1]}
</body></html>'''
    (SRC/'C_v2.html').write_text(html)


def write_D():
    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
      {GOLD_DEFS}
      <rect x="24" y="24" width="1552" height="852" rx="14" fill="none" stroke="url(#goldSatin)" stroke-width="1.1" stroke-opacity="0.48"/>

      <!-- UPPER MASTHEAD -->
      <g>
        <text x="56" y="82" font-family="Cinzel, serif" font-weight="700" font-size="16" letter-spacing="4.8" fill="#7c5920">PIVOT MONTHLY OVERALL RANKING</text>
        <text x="540" y="82" font-family="CormorantSC, Cinzel, serif" font-weight="400" font-size="16" letter-spacing="4" fill="#9a7435">·  2026.11</text>
        <!-- Extend header hairline toward medallion -->
        <line x1="56" y1="100" x2="1170" y2="100" stroke="url(#goldSatin)" stroke-width="1.3"/>

        <text x="54" y="162" font-family="ShipporiMinchoB1, serif" font-weight="700" font-size="40" letter-spacing="6" fill="#231c15"
              style="font-feature-settings:'palt' 1">月間総合ランキング</text>

        {hero_top5_svg(48, 314, text_size=122, num_size=168, anchor="start")}

        <!-- Clean rule aligned exactly to the thumbnail width below (56..592) -->
        <line x1="56" y1="354" x2="592" y2="354" stroke="url(#goldSatin)" stroke-width="1.4"/>
      </g>

      <!-- TOP RIGHT AWARD MEDALLION -->
      <g>
        {emblem_medallion(1375, 198, radius=94, scale=1.06, ribbon_text="MONTHLY AWARD")}
      </g>

      <!-- EPISODE NAMEPLATE -->
      <g>
        <rect x="56" y="704" width="536" height="74" rx="10" fill="#fffdf8" fill-opacity="0.94" stroke="url(#goldSatin)" stroke-width="1.4" filter="url(#softShadow)"/>
        <text x="78" y="731" font-family="Cinzel, serif" font-weight="700" font-size="11" letter-spacing="3.2" fill="#825e23">FEATURED EPISODE  ·  MONTHLY TOP 5</text>
        <text x="78" y="762" font-family="ShipporiMinchoB1, serif" font-weight="800" font-size="25.5" letter-spacing="1.5" fill="#221b14"
              style="font-feature-settings:'palt' 1">Meta「Muse」解説</text>
      </g>

      <text x="56" y="854" font-family="ShipporiMinchoB1, serif" font-weight="600" font-size="16" letter-spacing="2.2" fill="#6f5d46">作図：萩野貴拓</text>
    </svg>
    '''
    html = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><style>
{FONT_CSS}
*{{margin:0;box-sizing:border-box}}
body{{width:1600px;height:900px;background:#f7f1e6 url(compD_base.png) left top/1600px 900px no-repeat;position:relative;overflow:hidden}}
svg.overlay{{position:absolute;inset:0;width:1600px;height:900px;display:block;pointer-events:none;z-index:2}}
.card{{
  position:absolute;left:56px;top:384px;width:536px;padding:9px;
  border-radius:18px;
  background:linear-gradient(135deg,#fff6d8 0%,#d7a74d 28%,#8b5c1a 50%,#fae6aa 74%,#a57428 100%);
  box-shadow:0 22px 44px rgba(78,52,16,.22), inset 0 1px 0 rgba(255,255,255,.85);
  z-index:1;
}}
.card-inner{{padding:2px;border-radius:12px;background:#fffaf0}}
.card img{{width:514px;height:auto;display:block;border-radius:10px}}
.corner-badge{{
  position:absolute;right:-16px;top:-14px;
  padding:7px 16px;border-radius:999px;
  background:linear-gradient(135deg,#fff5cf,#d7a649 48%,#9a681f);
  border:1.5px solid #fff8df;
  box-shadow:0 6px 16px rgba(78,52,16,.28);
  font-family:"Cinzel",serif;font-weight:800;font-size:13px;letter-spacing:2.4px;color:#321f05;
  z-index:3;
}}
</style></head><body>
<div class="card">
  <div class="card-inner"><img src="thumb.png" alt=""></div>
  <div class="corner-badge">TOP 5</div>
</div>
<svg class="overlay" xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">{svg.split('<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',1)[1]}
</body></html>'''
    (SRC/'D_v2.html').write_text(html)


def render():
    write_A(); write_C(); write_D()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width":1600,"height":900}, device_scale_factor=1)
        for k in ('A','C','D'):
            pg.goto((SRC/f'{k}_v2.html').as_uri())
            pg.evaluate("() => document.fonts.ready")
            pg.wait_for_timeout(400)
            dest = ROOT/f'v2_{k}_1600x900.png'
            pg.screenshot(path=str(dest), type='png')
            im = Image.open(dest)
            im.resize((400,225), Image.Resampling.LANCZOS).save(ROOT/'qc'/f'preview_{k}_400_r2.png')
            # Tight QC crops for badges & text
            if k == 'A':
                im.crop((1180,60,1560,760)).save(ROOT/'qc'/'qc_A_right_r2.png')
                im.crop((30,50,450,480)).save(ROOT/'qc'/'qc_A_left_r2.png')
            elif k == 'C':
                im.crop((350,25,1250,340)).save(ROOT/'qc'/'qc_C_top_r2.png')
            elif k == 'D':
                im.crop((1160,40,1560,360)).save(ROOT/'qc'/'qc_D_badge_r2.png')
            print(k, 'saved', dest, im.size)
        b.close()

if __name__=='__main__':
    render()

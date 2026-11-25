import math
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path('/workspace/pivot-monthly-top5-celebration/v3')
SRC = ROOT / 'src'
QC = ROOT / 'qc'

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
  <radialGradient id="studioBg" cx="52%" cy="42%" r="72%">
    <stop offset="0%"   stop-color="#fffefb"/>
    <stop offset="52%"  stop-color="#faf3e6"/>
    <stop offset="86%"  stop-color="#efe3cd"/>
    <stop offset="100%" stop-color="#e5d4b6"/>
  </radialGradient>

  <radialGradient id="spotWarm" cx="50%" cy="44%" r="48%">
    <stop offset="0%"   stop-color="#ffffff" stop-opacity="0.95"/>
    <stop offset="60%"  stop-color="#fff8e8" stop-opacity="0.45"/>
    <stop offset="100%" stop-color="#fff8e8" stop-opacity="0.0"/>
  </radialGradient>

  <linearGradient id="floorGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%"   stop-color="#efe3cd" stop-opacity="0.35"/>
    <stop offset="14%"  stop-color="#fffcf5" stop-opacity="0.88"/>
    <stop offset="100%" stop-color="#e8d8bc" stop-opacity="0.95"/>
  </linearGradient>

  <linearGradient id="goldTextGrad" x1="0%" y1="0%" x2="8%" y2="100%">
    <stop offset="0%"   stop-color="#fff9e2"/>
    <stop offset="16%"  stop-color="#eed07f"/>
    <stop offset="36%"  stop-color="#b57a1e"/>
    <stop offset="50%"  stop-color="#693e07"/>
    <stop offset="57%"  stop-color="#a8701a"/>
    <stop offset="76%"  stop-color="#f7dc92"/>
    <stop offset="91%"  stop-color="#bb8328"/>
    <stop offset="100%" stop-color="#633a06"/>
  </linearGradient>

  <linearGradient id="goldDiagGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%"   stop-color="#fff7d4"/>
    <stop offset="22%"  stop-color="#e7c167"/>
    <stop offset="46%"  stop-color="#87520b"/>
    <stop offset="56%"  stop-color="#fbefc6"/>
    <stop offset="78%"  stop-color="#b98126"/>
    <stop offset="100%" stop-color="#5e3605"/>
  </linearGradient>

  <linearGradient id="goldRibbonGrad" x1="0%" y1="0%" x2="100%" y2="12%">
    <stop offset="0%"   stop-color="#8f5c14"/>
    <stop offset="14%"  stop-color="#e5be64"/>
    <stop offset="32%"  stop-color="#fff2c4"/>
    <stop offset="50%"  stop-color="#c99031"/>
    <stop offset="70%"  stop-color="#f7dc92"/>
    <stop offset="86%"  stop-color="#b37a20"/>
    <stop offset="100%" stop-color="#76480c"/>
  </linearGradient>

  <linearGradient id="goldRibbonVert" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%"   stop-color="#f9e39e"/>
    <stop offset="22%"  stop-color="#dfb55a"/>
    <stop offset="55%"  stop-color="#b47b21"/>
    <stop offset="85%"  stop-color="#8b5811"/>
    <stop offset="100%" stop-color="#6b4109"/>
  </linearGradient>

  <linearGradient id="goldSpecGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%"   stop-color="#ffffff" stop-opacity="0.90"/>
    <stop offset="28%"  stop-color="#fff4cc" stop-opacity="0.34"/>
    <stop offset="54%"  stop-color="#ffffff" stop-opacity="0.0"/>
    <stop offset="100%" stop-color="#ffffff" stop-opacity="0.0"/>
  </linearGradient>

  <linearGradient id="goldSatin" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%"   stop-color="#f4d992"/>
    <stop offset="35%"  stop-color="#b9832a"/>
    <stop offset="65%"  stop-color="#f0d285"/>
    <stop offset="100%" stop-color="#784b0f"/>
  </linearGradient>

  <linearGradient id="goldWatermark" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%"   stop-color="#d4ad5d" stop-opacity="0.22"/>
    <stop offset="50%"  stop-color="#b58632" stop-opacity="0.14"/>
    <stop offset="100%" stop-color="#d8b56b" stop-opacity="0.24"/>
  </linearGradient>

  <linearGradient id="plinthMuted" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%"   stop-color="#f7efe0"/>
    <stop offset="100%" stop-color="#dfd0b5"/>
  </linearGradient>

  <radialGradient id="sealIvory" cx="38%" cy="32%" r="68%">
    <stop offset="0%"   stop-color="#fffefb"/>
    <stop offset="68%"  stop-color="#f8efe0"/>
    <stop offset="100%" stop-color="#e3cda6"/>
  </radialGradient>

  <filter id="goldEmbossed" x="-14%" y="-14%" width="128%" height="132%">
    <feDropShadow dx="0" dy="1.3" stdDeviation="0.4" flood-color="#fffef9" flood-opacity="0.95"/>
    <feDropShadow dx="1.5" dy="5.5" stdDeviation="4.2" flood-color="#472d08" flood-opacity="0.34"/>
  </filter>

  <filter id="softShadow" x="-18%" y="-18%" width="136%" height="140%">
    <feDropShadow dx="2" dy="8" stdDeviation="7" flood-color="#4a310e" flood-opacity="0.24"/>
  </filter>

  <filter id="deepOverlapShadow" x="-22%" y="-22%" width="144%" height="148%">
    <feDropShadow dx="3" dy="11" stdDeviation="10" flood-color="#3c2609" flood-opacity="0.30"/>
  </filter>

  <filter id="badgeShadow" x="-24%" y="-24%" width="148%" height="148%">
    <feDropShadow dx="2" dy="10" stdDeviation="9" flood-color="#4c320d" flood-opacity="0.28"/>
  </filter>
</defs>
"""


def laurel_wreath_svg(cx, cy, r_inner=74, n_pairs=11, scale_leaf=1.0, opacity=1.0):
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
                    f'fill="url(#goldDiagGrad)" stroke="#73480f" stroke-width="0.55"/>'
                )
    ty = cy - r_inner - 4 * scale_leaf
    s = 9.5 * scale_leaf
    paths.append(
        f'<path d="M {cx},{ty-s} L {cx+s*0.32},{ty-s*0.32} L {cx+s},{ty} L {cx+s*0.32},{ty+s*0.32} '
        f'L {cx},{ty+s} L {cx-s*0.32},{ty+s*0.32} L {cx-s},{ty} L {cx-s*0.32},{ty-s*0.32} Z" '
        f'fill="url(#goldDiagGrad)" stroke="#70450e" stroke-width="0.6"/>'
    )
    return f'<g opacity="{opacity}">' + "\n".join(paths) + "</g>"


def emblem_medallion(cx, cy, radius=92, scale=1.0, ribbon_text="MONTHLY AWARD", hanging_tails=False, tail_len=2.15):
    r = radius * scale
    laurel = laurel_wreath_svg(cx, cy, r_inner=r * 1.08, n_pairs=11, scale_leaf=scale * 0.96)
    rw = 204 * scale
    rh = 32 * scale
    ry = cy + r * 0.85

    tails = ""
    if hanging_tails:
        tails = f'''
        <path d="M {cx-34*scale},{cy+r*0.72} L {cx-66*scale},{cy+r*tail_len} L {cx-34*scale},{cy+r*(tail_len-0.20)} L {cx-6*scale},{cy+r*(tail_len+0.04)} L {cx-6*scale},{cy+r*0.72} Z"
              fill="url(#goldRibbonVert)" stroke="#6d430b" stroke-width="0.9"/>
        <path d="M {cx+6*scale},{cy+r*0.72} L {cx+6*scale},{cy+r*(tail_len+0.04)} L {cx+34*scale},{cy+r*(tail_len-0.20)} L {cx+66*scale},{cy+r*tail_len} L {cx+34*scale},{cy+r*0.72} Z"
              fill="url(#goldRibbonVert)" stroke="#6d430b" stroke-width="0.9"/>
        '''

    ribbon = f'''
    <g filter="url(#softShadow)">
      <path d="M {cx-rw*0.56},{ry+6*scale} L {cx-rw*0.44},{ry+6*scale} L {cx-rw*0.44},{ry+rh+4*scale} L {cx-rw*0.58},{ry+rh+4*scale} L {cx-rw*0.51},{ry+rh*0.52+5*scale} Z" fill="#70440b"/>
      <path d="M {cx+rw*0.56},{ry+6*scale} L {cx+rw*0.44},{ry+6*scale} L {cx+rw*0.44},{ry+rh+4*scale} L {cx+rw*0.58},{ry+rh+4*scale} L {cx+rw*0.51},{ry+rh*0.52+5*scale} Z" fill="#70440b"/>
      <rect x="{cx-rw/2}" y="{ry}" width="{rw}" height="{rh}" rx="{5*scale}" fill="url(#goldRibbonGrad)" stroke="#6c420b" stroke-width="0.9"/>
      <rect x="{cx-rw/2+2*scale}" y="{ry+2*scale}" width="{rw-4*scale}" height="{rh-4*scale}" rx="{3.5*scale}" fill="none" stroke="#fff4cc" stroke-opacity="0.72" stroke-width="0.8"/>
      <text x="{cx}" y="{ry+rh*0.67}" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="{11.5*scale}" letter-spacing="{2.0*scale}" fill="#2b1904">{ribbon_text}</text>
    </g>
    '''
    return f'''
    <g filter="url(#badgeShadow)">
      {tails}
      {laurel}
      <circle cx="{cx}" cy="{cy}" r="{r*0.87}" fill="url(#goldDiagGrad)" stroke="#6b410a" stroke-width="1.5"/>
      <circle cx="{cx}" cy="{cy}" r="{r*0.78}" fill="url(#sealIvory)" stroke="url(#goldSatin)" stroke-width="1.9"/>
      <circle cx="{cx}" cy="{cy}" r="{r*0.70}" fill="none" stroke="#b98632" stroke-width="0.7" stroke-dasharray="2.6,3"/>
      <text x="{cx}" y="{cy-r*0.41}" text-anchor="middle" font-family="Cinzel, serif" font-weight="700" font-size="{11.2*scale}" letter-spacing="{3.2*scale}" fill="#6e4b16">PIVOT</text>
      <line x1="{cx-r*0.30}" y1="{cy-r*0.33}" x2="{cx+r*0.30}" y2="{cy-r*0.33}" stroke="url(#goldSatin)" stroke-width="0.9"/>
      <text x="{cx}" y="{cy-r*0.14}" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="{15.5*scale}" letter-spacing="{3.0*scale}" fill="#2e1e08">TOP</text>
      <text x="{cx}" y="{cy+r*0.38}" text-anchor="middle" font-family="CinzelDec, serif" font-weight="900" font-size="{52*scale}" fill="url(#goldTextGrad)" stroke="#603a07" stroke-width="{0.9*scale}">5</text>
      <text x="{cx}" y="{cy+r*0.58}" text-anchor="middle" font-family="Cinzel, serif" font-weight="700" font-size="{10.5*scale}" letter-spacing="{2.2*scale}" fill="#6b4b1b">2026 . 11</text>
      {ribbon}
    </g>
    '''


def compact_top5_seal(cx, cy, r=42):
    laurel = laurel_wreath_svg(cx, cy, r_inner=r*1.12, n_pairs=8, scale_leaf=0.58)
    return f'''
    <g filter="url(#deepOverlapShadow)">
      {laurel}
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#goldDiagGrad)" stroke="#623a08" stroke-width="1.3"/>
      <circle cx="{cx}" cy="{cy}" r="{r*0.86}" fill="url(#sealIvory)" stroke="url(#goldSatin)" stroke-width="1.3"/>
      <text x="{cx}" y="{cy-8}" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="11.5" letter-spacing="2.2" fill="#5e3d11">TOP</text>
      <text x="{cx}" y="{cy+22}" text-anchor="middle" font-family="CinzelDec, serif" font-weight="900" font-size="30" fill="url(#goldTextGrad)" stroke="#5c3607" stroke-width="0.7">5</text>
    </g>
    '''


def hero_top5_svg(x, y, text_size=76, num_size=112, anchor="start", extra_filter=""):
    # Single <text> with <tspan> so HarfBuzz lays out トップ + 5 + 入り with ZERO collision!
    f_attr = extra_filter or 'filter="url(#goldEmbossed)"'
    ta = "start" if anchor == "start" else "middle"
    gap1 = max(4, round(text_size * 0.06))
    gap2 = max(4, round(text_size * 0.07))

    def layer(fill_ref, stroke="none", sw="0", dy=0):
        return f'''
        <text x="{x}" y="{y+dy}" text-anchor="{ta}" font-family="ZenOldMincho, ShipporiMinchoB1, serif" font-weight="900" font-size="{text_size}" letter-spacing="-3"
              fill="{fill_ref}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" style="font-feature-settings:'palt' 1">トップ<tspan dx="{gap1}" dy="9" font-family="CinzelDec, serif" font-weight="900" font-size="{num_size}" letter-spacing="0">5</tspan><tspan dx="{gap2}" dy="-9" font-family="ZenOldMincho, ShipporiMinchoB1, serif" font-weight="900" font-size="{text_size}" letter-spacing="-2">入り</tspan></text>
        '''

    return f'''
    <g {f_attr}>
      {layer("#5b3506", stroke="#5b3506", sw="2.6", dy=2.2)}
      {layer("url(#goldTextGrad)", stroke="#683f08", sw="1.2", dy=0)}
      {layer("url(#goldSpecGrad)", stroke="none", sw="0", dy=0)}
    </g>
    '''


def star4(cx, cy, s=8):
    return (f'<path d="M {cx},{cy-s} L {cx+s*0.28},{cy-s*0.28} L {cx+s},{cy} L {cx+s*0.28},{cy+s*0.28} '
            f'L {cx},{cy+s} L {cx-s*0.28},{cy+s*0.28} L {cx-s},{cy} L {cx-s*0.28},{cy-s*0.28} Z" '
            f'fill="url(#goldDiagGrad)" stroke="#70450e" stroke-width="0.5"/>')


def studio_backdrop_svg(spot_cx="52%", spot_cy="44%", floor_y=822):
    return f'''
      <rect width="1600" height="900" fill="url(#studioBg)"/>
      <ellipse cx="{spot_cx}" cy="{spot_cy}" rx="760" ry="430" fill="url(#spotWarm)"/>
      <rect x="0" y="{floor_y}" width="1600" height="{900-floor_y}" fill="url(#floorGrad)"/>
      <line x1="0" y1="{floor_y}" x2="1600" y2="{floor_y}" stroke="#caa766" stroke-width="1.0" stroke-opacity="0.45"/>
      <rect x="22" y="22" width="1556" height="856" rx="14" fill="none" stroke="url(#goldSatin)" stroke-width="1.2" stroke-opacity="0.55"/>
      <rect x="30" y="30" width="1540" height="840" rx="10" fill="none" stroke="#c8a258" stroke-width="0.6" stroke-opacity="0.32"/>
    '''


def podium_award_card_svg(x, y, width=444):
    h = 228
    px = x + 36
    base_y = y + 170
    heights = [28, 42, 56, 70, 86]
    col_w = 56
    gap = 18
    bars = []
    for i, bh in enumerate(heights):
        bx = px + i * (col_w + gap)
        by = base_y - bh
        if i < 4:
            bars.append(f'''
            <rect x="{bx}" y="{by}" width="{col_w}" height="{bh}" rx="4" fill="url(#plinthMuted)" stroke="#ceb489" stroke-width="0.9"/>
            <rect x="{bx}" y="{by}" width="{col_w}" height="4" rx="2" fill="url(#goldSatin)" opacity="0.72"/>
            ''')
        else:
            bars.append(f'''
            <g filter="url(#softShadow)">
              <rect x="{bx}" y="{by}" width="{col_w+8}" height="{bh}" rx="5" fill="url(#goldRibbonVert)" stroke="#683f09" stroke-width="1.1"/>
              <rect x="{bx+2}" y="{by+2}" width="{col_w+4}" height="10" rx="3" fill="#fff5cc" fill-opacity="0.55"/>
              <text x="{bx+(col_w+8)/2}" y="{by+bh*0.60}" text-anchor="middle" font-family="CinzelDec, serif" font-weight="900" font-size="23" fill="#2c1904">5</text>
            </g>
            <!-- Sits cleanly below header line (y+42) with 14px breathing room! -->
            <g transform="translate({bx+(col_w+8)/2}, {by-17})">
              <rect x="-48" y="-11" width="96" height="21" rx="10.5" fill="url(#goldRibbonGrad)" stroke="#683f09" stroke-width="0.9"/>
              <text x="0" y="3" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="10" letter-spacing="1.2" fill="#271603">★ TOP 5 IN</text>
            </g>
            ''')

    return f'''
    <g filter="url(#deepOverlapShadow)">
      <rect x="{x}" y="{y}" width="{width}" height="{h}" rx="12" fill="#fffdf8" stroke="url(#goldSatin)" stroke-width="1.9"/>
      <rect x="{x+6}" y="{y+6}" width="{width-12}" height="{h-12}" rx="8" fill="none" stroke="#c8a562" stroke-width="0.7" stroke-opacity="0.5"/>
      <text x="{x+24}" y="{y+29}" font-family="Cinzel, serif" font-weight="800" font-size="11.5" letter-spacing="2.4" fill="#704d19">MONTHLY OVERALL · 2026.11</text>
      <line x1="{x+24}" y1="{y+40}" x2="{x+width-24}" y2="{y+40}" stroke="#d6bc8b" stroke-width="0.9"/>
      {''.join(bars)}
      <line x1="{px-6}" y1="{base_y+1}" x2="{x+width-26}" y2="{base_y+1}" stroke="url(#goldSatin)" stroke-width="1.6"/>
      <rect x="{x+24}" y="{y+182}" width="{width-48}" height="31" rx="6" fill="url(#goldRibbonGrad)" stroke="#6a410a" stroke-width="0.8"/>
      <text x="{x+width/2}" y="{y+202}" text-anchor="middle" font-family="ShipporiMinchoB1, serif" font-weight="800" font-size="14.5" letter-spacing="1.2" fill="#241403" style="font-feature-settings:'palt' 1">PIVOT 月間総合トップ5入り</text>
    </g>
    '''


def write_A():
    svg_back = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
      {GOLD_DEFS}
      {studio_backdrop_svg(spot_cx="50%", spot_cy="43%", floor_y=842)}

      <g opacity="0.92">
        <circle cx="805" cy="365" r="355" fill="none" stroke="url(#goldSatin)" stroke-width="1.8" stroke-opacity="0.48"/>
        <circle cx="805" cy="365" r="372" fill="none" stroke="#c8a25a" stroke-width="0.8" stroke-dasharray="4,6" stroke-opacity="0.45"/>
        <circle cx="805" cy="365" r="308" fill="none" stroke="url(#goldSatin)" stroke-width="0.9" stroke-opacity="0.32"/>
        <text x="805" y="218" text-anchor="middle" font-family="CinzelDec, serif" font-weight="900" font-size="195" letter-spacing="12" fill="url(#goldWatermark)">TOP 5</text>
      </g>

      <!-- Z2: Satin ribbon sash passing BEHIND Jolly & Frame -->
      <g filter="url(#softShadow)">
        <path d="M 38,546 L 1562,546 L 1536,576 L 1562,606 L 38,606 L 64,576 Z" fill="url(#goldRibbonGrad)" stroke="#6e440c" stroke-width="1.0" opacity="0.90"/>
        <line x1="68" y1="552" x2="1532" y2="552" stroke="#fff7d6" stroke-width="0.9" stroke-opacity="0.72"/>
        <line x1="68" y1="600" x2="1532" y2="600" stroke="#75490e" stroke-width="0.8" stroke-opacity="0.55"/>
      </g>

      <!-- Z2.5: Left Masthead (with crisp spacing between プ and 5, rule tucked behind Jolly!) -->
      <g>
        <text x="56" y="84" font-family="Cinzel, serif" font-weight="700" font-size="16" letter-spacing="5.2" fill="#6f4e1c">PIVOT MONTHLY RANKING</text>
        <text x="56" y="112" font-family="Cinzel, serif" font-weight="600" font-size="12.5" letter-spacing="4.2" fill="#8f6c35">OVERALL · 2026.11</text>
        <line x1="56" y1="128" x2="640" y2="128" stroke="url(#goldSatin)" stroke-width="1.6"/>
        {star4(56, 128, 6.5)}

        <text x="54" y="182" font-family="ShipporiMinchoB1, serif" font-weight="700" font-size="35" letter-spacing="3.2" fill="#231c15"
              style="font-feature-settings:'palt' 1">月間総合ランキング</text>

        {hero_top5_svg(50, 300, text_size=76, num_size=112, anchor="start")}

        <line x1="56" y1="342" x2="590" y2="342" stroke="url(#goldSatin)" stroke-width="2.0"/>
        {star4(420, 342, 6)}
      </g>

      <ellipse cx="805" cy="846" rx="225" ry="18" fill="#5c421d" opacity="0.16"/>
    </svg>
    '''

    svg_front = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
      {GOLD_DEFS}

      <!-- Z4: Bottom-Left Episode Plaque overlapping lower-left corner of gold frame -->
      <g filter="url(#deepOverlapShadow)">
        <rect x="56" y="642" width="442" height="96" rx="11" fill="#fffdf8" stroke="url(#goldSatin)" stroke-width="2.0"/>
        <rect x="63" y="649" width="428" height="82" rx="7" fill="none" stroke="#c8a45f" stroke-width="0.75" stroke-opacity="0.55"/>
        <rect x="78" y="661" width="164" height="22" rx="4" fill="url(#goldRibbonGrad)" stroke="#6a410a" stroke-width="0.6"/>
        <text x="160" y="676" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="10.5" letter-spacing="2.0" fill="#281603">FEATURED EPISODE</text>
        <text x="256" y="676" font-family="Cinzel, serif" font-weight="700" font-size="11.5" letter-spacing="2.4" fill="#7c5924">2026.11</text>
        <text x="78" y="715" font-family="ShipporiMinchoB1, serif" font-weight="800" font-size="29" letter-spacing="1.0" fill="#1e1710"
              style="font-feature-settings:'palt' 1">Meta「Muse」解説</text>
      </g>

      <!-- Z4: Top-Right Laurel Medallion overlapping top-right corner of gold frame, tails tuck BEHIND Jolly's right paw (Z5)! -->
      {emblem_medallion(1205, 248, radius=92, scale=1.02, ribbon_text="MONTHLY AWARD", hanging_tails=True, tail_len=2.25)}

      <!-- Z4: Bottom-Right 5-Step Podium Award Card overlapping bottom-right corner of gold frame -->
      {podium_award_card_svg(1096, 560, width=444)}

      <text x="56" y="860" font-family="ShipporiMinchoB1, serif" font-weight="600" font-size="16" letter-spacing="2.2" fill="#634f37">作図：萩野貴拓</text>
    </svg>
    '''

    html = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><style>
{FONT_CSS}
*{{margin:0;box-sizing:border-box}}
body{{width:1600px;height:900px;position:relative;overflow:hidden;background:#faf3e6}}
.layer{{position:absolute;inset:0;width:1600px;height:900px;pointer-events:none}}
.jolly-mid{{filter:drop-shadow(3px 14px 16px rgba(64,42,12,0.28))}}
.paw-fg{{filter:drop-shadow(1px 5px 7px rgba(48,30,8,0.25))}}
</style></head><body>
  <div class="layer" style="z-index:1">{svg_back}</div>
  <img class="layer jolly-mid" style="z-index:3" src="../layers/compA_clean.png"/>
  <div class="layer" style="z-index:4">{svg_front}</div>
  <img class="layer paw-fg" style="z-index:5" src="../layers/A_right_paw.png"/>
</body></html>'''
    (SRC / 'A_v3.html').write_text(html)


def write_C():
    svg_back = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
      {GOLD_DEFS}
      {studio_backdrop_svg(spot_cx="50%", spot_cy="44%", floor_y=824)}

      <circle cx="800" cy="435" r="395" fill="none" stroke="url(#goldSatin)" stroke-width="1.6" stroke-opacity="0.45"/>
      <circle cx="800" cy="435" r="415" fill="none" stroke="#c8a25a" stroke-width="0.7" stroke-dasharray="4,7" stroke-opacity="0.40"/>
      <circle cx="800" cy="435" r="338" fill="none" stroke="url(#goldSatin)" stroke-width="1.0" stroke-opacity="0.32"/>

      <!-- Z2: Wide champagne-gold celebration ribbon wings passing BEHIND the side Jollys -->
      <g filter="url(#softShadow)">
        <path d="M 190,638 L 1410,638 L 1380,676 L 1410,714 L 190,714 L 220,676 Z" fill="url(#goldRibbonGrad)" stroke="#6d430b" stroke-width="1.0" opacity="0.88"/>
        <line x1="228" y1="645" x2="1372" y2="645" stroke="#fff7d4" stroke-width="0.9" stroke-opacity="0.7"/>
        <line x1="228" y1="707" x2="1372" y2="707" stroke="#75490e" stroke-width="0.8" stroke-opacity="0.55"/>
      </g>
    </svg>
    '''

    svg_mid_card_typo = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
      {GOLD_DEFS}

      <g>
        <line x1="418" y1="52" x2="588" y2="52" stroke="url(#goldSatin)" stroke-width="1.3"/>
        <text x="800" y="58" text-anchor="middle" font-family="Cinzel, serif" font-weight="700" font-size="14.5" letter-spacing="4.6" fill="#704d19">PIVOT MONTHLY RANKING · 2026.11</text>
        <line x1="1012" y1="52" x2="1182" y2="52" stroke="url(#goldSatin)" stroke-width="1.3"/>

        <text x="800" y="100" text-anchor="middle" font-family="ShipporiMinchoB1, serif" font-weight="700" font-size="33" letter-spacing="5.5" fill="#231c15"
              style="font-feature-settings:'palt' 1">月間総合ランキング</text>

        <!-- Ornamental gold rules flanking monumental トップ5入り (NO duplicate stacked laurel!) -->
        <line x1="398" y1="168" x2="508" y2="168" stroke="url(#goldSatin)" stroke-width="1.5"/>
        {star4(398, 168, 7)}
        <line x1="1092" y1="168" x2="1202" y2="168" stroke="url(#goldSatin)" stroke-width="1.5"/>
        {star4(1202, 168, 7)}

        {hero_top5_svg(800, 196, text_size=80, num_size=118, anchor="middle")}
      </g>
    </svg>
    '''

    svg_front_badges = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
      {GOLD_DEFS}

      <!-- Z4: Clean single Gold Laurel TOP 5 Seal overlapping Top-Right Corner of Thumbnail Card -->
      {compact_top5_seal(1124, 242, r=44)}

      <!-- Z4: Satin Ribbon Banner wrapping across bottom frame molding (y=574..610) -->
      <g filter="url(#deepOverlapShadow)">
        <path d="M 434,582 L 468,582 L 468,618 L 424,618 L 442,600 Z" fill="#6d430b"/>
        <path d="M 1166,582 L 1132,582 L 1132,618 L 1176,618 L 1158,600 Z" fill="#6d430b"/>
        <rect x="466" y="574" width="668" height="36" rx="6" fill="url(#goldRibbonGrad)" stroke="#683f09" stroke-width="1.1"/>
        <rect x="470" y="578" width="660" height="28" rx="4" fill="none" stroke="#fff6d4" stroke-opacity="0.72" stroke-width="0.8"/>
        <text x="800" y="597" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="13" letter-spacing="4.2" fill="#261503">OFFICIAL TOP 5 · MONTHLY AWARD</text>
      </g>

      <!-- Z4: Sculpted Episode Nameplate (wider wings so both foreground flute & coupe glass cross edges cleanly!) -->
      <g filter="url(#deepOverlapShadow)">
        <rect x="512" y="632" width="576" height="84" rx="12" fill="#fffdf8" stroke="url(#goldSatin)" stroke-width="2.0"/>
        <rect x="519" y="639" width="562" height="70" rx="8" fill="none" stroke="#c8a45f" stroke-width="0.75" stroke-opacity="0.55"/>
        <text x="800" y="660" text-anchor="middle" font-family="Cinzel, serif" font-weight="700" font-size="11.5" letter-spacing="3.0" fill="#7d5922">PIVOT PROGRAM · 2026.11</text>
        <text x="800" y="695" text-anchor="middle" font-family="ShipporiMinchoB1, serif" font-weight="800" font-size="27.5" letter-spacing="1.4" fill="#1e1710"
              style="font-feature-settings:'palt' 1">Meta「Muse」解説</text>
      </g>

      <text x="800" y="862" text-anchor="middle" font-family="ShipporiMinchoB1, serif" font-weight="600" font-size="16" letter-spacing="2.2" fill="#634f37">作図：萩野貴拓</text>
    </svg>
    '''

    html = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><style>
{FONT_CSS}
*{{margin:0;box-sizing:border-box}}
body{{width:1600px;height:900px;position:relative;overflow:hidden;background:#faf3e6}}
.layer{{position:absolute;inset:0;width:1600px;height:900px;pointer-events:none}}
.card{{
  position:absolute;left:470px;top:240px;width:660px;padding:10px;border-radius:16px;
  background:linear-gradient(145deg,#fff6d4 0%,#d7aa50 28%,#7e5012 52%,#f4da90 76%,#74470e 100%);
  box-shadow:0 22px 44px rgba(62,40,10,0.28), 0 4px 12px rgba(72,46,12,0.18), inset 0 2px 3px rgba(255,255,255,0.88);
}}
.card-inner{{padding:3px;border-radius:10px;background:#fffdf8}}
.card img{{display:block;width:100%;height:auto;border-radius:8px}}
.fg-glass{{filter:drop-shadow(-3px 8px 10px rgba(48,30,8,0.28))}}
</style></head><body>
  <div class="layer" style="z-index:1">{svg_back}</div>
  <img class="layer" style="z-index:2" src="../layers/compC_clean.png"/>
  <div class="layer" style="z-index:3">{svg_mid_card_typo}</div>
  <div class="card" style="z-index:3"><div class="card-inner"><img src="thumb.png"/></div></div>
  <div class="layer" style="z-index:4">{svg_front_badges}</div>
  <img class="layer" style="z-index:5" src="../layers/C_fg_left_glass.png"/>
  <img class="layer" style="z-index:5" src="../layers/C_fg_sitting_flute.png"/>
  <img class="layer fg-glass" style="z-index:5;transform:scale(1.035);transform-origin:1360px 900px" src="../layers/C_fg_right.png"/>
</body></html>'''
    (SRC / 'C_v3.html').write_text(html)


def write_D():
    # Card at left=60, top=326, width=620 -> x=60..680, y=326..664 (PIVOT NEWS ends at y~641)
    # Plaque at x=60, y=656 -> overlaps ONLY bottom gold molding (y=656..664), PIVOT NEWS 100% visible!
    # Jolly scaled 1.21x anchored at (1080, 900) -> crown reaches y~268, left shoulder overlaps card right edge x~595..680,
    # raised waving paw (y~485..880) sits IN FRONT OF top-right medallion's hanging ribbon tails!
    svg_back = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
      {GOLD_DEFS}
      {studio_backdrop_svg(spot_cx="62%", spot_cy="46%", floor_y=828)}

      <circle cx="1040" cy="540" r="415" fill="none" stroke="url(#goldSatin)" stroke-width="1.6" stroke-opacity="0.44"/>
      <circle cx="1040" cy="540" r="436" fill="none" stroke="#c8a25a" stroke-width="0.7" stroke-dasharray="4,7" stroke-opacity="0.38"/>

      <!-- Z2: Horizontal champagne-gold magazine sash passing BEHIND Jolly's head & card -->
      <g filter="url(#softShadow)">
        <path d="M 38,360 L 1562,360 L 1538,388 L 1562,416 L 38,416 L 62,388 Z" fill="url(#goldRibbonGrad)" stroke="#6c420b" stroke-width="1.0" opacity="0.82"/>
        <line x1="66" y1="366" x2="1534" y2="366" stroke="#fff7d4" stroke-width="0.8" stroke-opacity="0.7"/>
      </g>

      <!-- Z2: Monumental Masthead (lower flourish & right edge kiss behind Jolly's crown!) -->
      <g>
        <text x="60" y="72" font-family="Cinzel, serif" font-weight="700" font-size="16" letter-spacing="5.2" fill="#6f4e1c">PIVOT MONTHLY OVERALL RANKING · 2026.11</text>
        <line x1="60" y1="88" x2="720" y2="88" stroke="url(#goldSatin)" stroke-width="1.4"/>
        {star4(734, 88, 6)}
        <text x="58" y="142" font-family="ShipporiMinchoB1, serif" font-weight="700" font-size="38" letter-spacing="4.2" fill="#231c15"
              style="font-feature-settings:'palt' 1">月間総合ランキング</text>

        {hero_top5_svg(52, 286, text_size=102, num_size=148, anchor="start")}
      </g>

      <!-- Z2: Top-Right Laurel Medallion whose hanging ribbon tails tuck BEHIND Jolly's raised waving paw (y~485)! -->
      {emblem_medallion(1355, 244, radius=94, scale=1.04, ribbon_text="MONTHLY AWARD", hanging_tails=True, tail_len=3.25)}
    </svg>
    '''

    svg_front = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
      {GOLD_DEFS}

      <!-- Z5: Gold Laurel TOP 5 Seal overlapping Top-Right Corner of Thumbnail Card -->
      {compact_top5_seal(672, 342, r=42)}

      <!-- Z5: Sculpted Episode Nameplate overlapping ONLY bottom gold molding (y=656..664), leaving PIVOT NEWS 100% clear! -->
      <g filter="url(#deepOverlapShadow)">
        <rect x="60" y="664" width="526" height="104" rx="12" fill="#fffdf8" stroke="url(#goldSatin)" stroke-width="2.0"/>
        <rect x="67" y="671" width="512" height="90" rx="8" fill="none" stroke="#c8a45f" stroke-width="0.75" stroke-opacity="0.55"/>
        <rect x="84" y="685" width="224" height="22" rx="4" fill="url(#goldRibbonGrad)" stroke="#6a410a" stroke-width="0.6"/>
        <text x="196" y="700" text-anchor="middle" font-family="Cinzel, serif" font-weight="800" font-size="10.5" letter-spacing="2.0" fill="#281603">FEATURED EPISODE · TOP 5</text>
        <text x="322" y="700" font-family="Cinzel, serif" font-weight="700" font-size="11.5" letter-spacing="2.4" fill="#7c5924">2026.11</text>
        <text x="84" y="742" font-family="ShipporiMinchoB1, serif" font-weight="800" font-size="30.5" letter-spacing="1.2" fill="#1e1710"
              style="font-feature-settings:'palt' 1">Meta「Muse」解説</text>
      </g>

      <text x="60" y="860" font-family="ShipporiMinchoB1, serif" font-weight="600" font-size="16" letter-spacing="2.2" fill="#634f37">作図：萩野貴拓</text>
    </svg>
    '''

    html = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><style>
{FONT_CSS}
*{{margin:0;box-sizing:border-box}}
body{{width:1600px;height:900px;position:relative;overflow:hidden;background:#faf3e6}}
.layer{{position:absolute;inset:0;width:1600px;height:900px;pointer-events:none}}
.card{{
  position:absolute;left:60px;top:334px;width:620px;padding:10px;border-radius:16px;
  background:linear-gradient(145deg,#fff6d4 0%,#d7aa50 28%,#7e5012 52%,#f4da90 76%,#74470e 100%);
  box-shadow:0 22px 42px rgba(62,40,10,0.28), 0 4px 12px rgba(72,46,12,0.18), inset 0 2px 3px rgba(255,255,255,0.88);
}}
.card-inner{{padding:3px;border-radius:10px;background:#fffdf8}}
.card img{{display:block;width:100%;height:auto;border-radius:8px}}
.jolly-fg{{
  transform:scale(1.20);transform-origin:1060px 900px;
  filter:drop-shadow(-8px 10px 18px rgba(48,30,8,0.28));
}}
</style></head><body>
  <div class="layer" style="z-index:1">{svg_back}</div>
  <div class="card" style="z-index:3"><div class="card-inner"><img src="thumb.png"/></div></div>
  <img class="layer jolly-fg" style="z-index:4" src="../layers/compD_clean.png"/>
  <div class="layer" style="z-index:5">{svg_front}</div>
</body></html>'''
    (SRC / 'D_v3.html').write_text(html)


def render_all():
    write_A()
    write_C()
    write_D()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        for k in ('A', 'C', 'D'):
            page = b.new_page(viewport={'width': 1600, 'height': 900}, device_scale_factor=1)
            page.goto(f'file://{SRC}/{k}_v3.html', wait_until='networkidle')
            page.evaluate('() => document.fonts.ready')
            page.wait_for_timeout(350)
            out = ROOT / f'v3_{k}_1600x900.png'
            page.screenshot(path=str(out))
            page.close()

            im = Image.open(out).convert('RGB')
            im.save(out)
            im.resize((400, 225), Image.LANCZOS).save(QC / f'preview_{k}_400.png')
            print(k, im.size, out.stat().st_size)
        b.close()


if __name__ == '__main__':
    render_all()

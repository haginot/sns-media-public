#!/usr/bin/env python3
"""Build Grok Bot-tone copies of the pstack figures from ../../src/*.html (originals untouched)."""
from pathlib import Path
import re
HERE = Path(__file__).resolve().parent
ORIG = HERE.parent.parent / "src"
JOBS = ["fig_before_after", "fig_timeline", "fig_timeline_v2", "fig_flow", "map_overview", "map_full"]
COLORS = {
    "#1A2E3B": "#111111", "#F3EDE0": "#F4F5F7", "#C45C26": "#FF6801", "#5C564E": "#5F6368",
    "#D4CBB8": "#E3E5EA", "#215A7A": "#1386FF", "#3D4A52": "#45484D", "#FFF8EC": "#FFFFFF",
    "#EFE8D6": "#F1F3F6", "#C9897A": "#F4F5F7", "#6B4A2E": "#6E3FE0", "#8A3F16": "#C8166F",
    "#B33A2B": "#D21F3C", "#8A8476": "#A0A4AB",
}
# fact fix (coding teammate, pstack 0.15.43 source): only 7 of 22 playbooks end with opening a pr
TEXT = {
    "どのプレイブックも末尾は opening a pr": "22のうち7つは末尾で opening a pr",
    "opening a pr は他のすべての末尾で呼ばれる。": "opening a pr で終わるのは22のうち7つ。",
    "opening a pr は他のすべてのプレイブックの末尾で呼ばれる。": "opening a pr で終わるのは22のうち7つ。",
}
INJECT_HEAD = '<link rel="stylesheet" href="theme.css">\n'
def inject_body(name):
    s = '<script src="../../../banner/grokbot/src/chars.js"></script>\n<script src="theme.js"></script>\n'
    if (HERE / f"patch_{name}.js").exists():
        s += f'<script src="patch_{name}.js"></script>\n'
    return s
for name in JOBS:
    t = (ORIG / f"{name}.html").read_text()
    for a, b in COLORS.items():
        t = re.sub(re.escape(a), b, t, flags=re.I)
    for a, b in TEXT.items():
        t = t.replace(a, b)
    t = t.replace("</head>", INJECT_HEAD + "</head>", 1)
    t = t.replace("</body>", inject_body(name) + "</body>", 1)
    (HERE / f"{name}.html").write_text(t)
    print("built", name)

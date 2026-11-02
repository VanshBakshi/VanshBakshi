#!/usr/bin/env python3
"""
Builds the animated SVGs used by the profile README.
Run:  python3 generate_assets.py     (writes the .svg files next to this script)

GitHub shows animated SVGs when they are loaded through <img src="...">, so every
animation here is pure SVG (SMIL), with no JavaScript and no external files.
Edit the data lists (SKILLS, RADAR, BARS, ROADMAP) to personalise, then re-run.
"""
import math
import os
import random
from xml.sax.saxutils import escape

OUT = os.path.dirname(os.path.abspath(__file__))

CY, MG, PU, GR, YL, RD, BL = "#00f5ff", "#ff00ff", "#8a2be2", "#00ffb3", "#ffd700", "#ff4b4b", "#00d4ff"
INK, BG, PANEL = "#e6faff", "#070718", "#0b0b2a"

# ---------------------------------------------------------------- editable data
# (orbit rx, ry, seconds per lap, clockwise?, colour, skills)  green=comfortable, yellow=building, blue=exploring
SKILLS = [
    (170, 95, 28, 1, GR, ["Python", "Git", "VS Code"]),
    (290, 160, 44, 0, YL, ["Flask", "FastAPI", "Flutter", "React", "Docker", "scikit-learn"]),
    (410, 235, 62, 1, BL, ["NLP / RAG", "Linux", "Networking", "TensorFlow", "PyTorch", "Postgres"]),
]
# (name, distance from centre 0-190, angle in degrees, colour)
RADAR = [
    ("Python", 35, 30, GR), ("Git", 50, 150, GR), ("Flask", 55, 260, GR), ("VS Code", 30, 330, GR),
    ("Flutter", 90, 70, YL), ("FastAPI", 105, 200, YL), ("scikit-learn", 100, 300, YL),
    ("Docker", 120, 120, YL), ("React", 85, 350, YL),
    ("PyTorch", 150, 20, BL), ("TensorFlow", 170, 100, BL), ("OpenCV", 160, 230, BL), ("Postgres", 145, 320, BL),
]
BARS = [("PYTHON", 80, GR), ("MACHINE LEARNING", 60, YL), ("WEB (FLASK / FASTAPI)", 60, YL),
        ("MOBILE (FLUTTER)", 40, BL), ("SECURITY", 40, BL), ("DSA", 60, YL)]
# (lane, start day, length in days, colour)
ROADMAP = [("AI / ML", 0, 90, CY), ("AI / ML", 90, 75, CY), ("FULL STACK", 31, 90, MG), ("FULL STACK", 121, 60, MG),
           ("MOBILE", 90, 100, GR), ("SECURITY", 120, 120, YL), ("OPEN SOURCE", 59, 270, BL)]


# ---------------------------------------------------------------- helpers
def wrap(w, h, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
        f'<defs>'
        f'<linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CY}"/>'
        f'<stop offset=".5" stop-color="{MG}"/><stop offset="1" stop-color="{PU}"/></linearGradient>'
        f'<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="2.5" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f'<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">'
        f'<path d="M30 0H0V30" fill="none" stroke="#1b1b4a" stroke-width="1"/>'
        f'<animateTransform attributeName="patternTransform" type="translate" from="0 0" to="30 30" dur="4s" repeatCount="indefinite"/>'
        f'</pattern>{defs}</defs>'
        f'<style>text{{font-family:Consolas,"Courier New",monospace}}</style>'
        f'{body}</svg>'
    )


def bg(w, h):
    return (f'<rect width="{w}" height="{h}" rx="16" fill="{BG}"/>'
            f'<rect width="{w}" height="{h}" rx="16" fill="url(#grid)" opacity=".55"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="none" stroke="url(#g)" stroke-width="1.5" opacity=".6"/>')


def text(x, y, s, size=13, fill=INK, anchor="middle", weight="normal", extra=""):
    lines = s.split("\n")
    n = len(lines)
    y0 = y - (n - 1) * size * 0.625 + size * 0.35
    tsp = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else round(size * 1.25, 1)}">{escape(l)}</tspan>'
                  for i, l in enumerate(lines))
    return (f'<text x="{x}" y="{round(y0, 1)}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" {extra}>{tsp}</text>')


def node(x, y, w, h, label, color=CY, delay=0, dur=4, size=13):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{PANEL}" stroke="{color}" stroke-width="2" filter="url(#glow)">'
            f'<animate attributeName="stroke-opacity" values=".35;1;.35" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></rect>'
            + text(x + w / 2, y + h / 2, label, size))


def flow(d, color=CY, dur=1.2, width=2):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="6 6" opacity=".85">'
            f'<animate attributeName="stroke-dashoffset" from="24" to="0" dur="{dur}s" repeatCount="indefinite"/></path>')


def packet(d, color=CY, dur=3, begin=0, r=5):
    begin = -abs(begin)  # negative begin = already mid-cycle at load, so nothing sits at (0,0)
    return (f'<circle r="{r}" fill="{color}" filter="url(#glow)">'
            f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" path="{d}"/></circle>')


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name, f"{len(svg) // 1024 + 1} KB")


# ---------------------------------------------------------------- 1. divider
def divider():
    w, h = 900, 24
    b = f'<rect x="20" y="11" width="860" height="2" rx="1" fill="url(#g)" opacity=".45"/>' + flow("M20 12 H880", CY, 1.5, 1)
    for c, d in [(CY, 6), (MG, 8), (PU, 10)]:
        b += (f'<circle cy="12" r="4" fill="{c}" filter="url(#glow)">'
              f'<animate attributeName="cx" values="20;880;20" dur="{d}s" repeatCount="indefinite"/></circle>')
    b += (f'<rect x="442" y="4" width="16" height="16" fill="none" stroke="url(#g)" stroke-width="2">'
          f'<animateTransform attributeName="transform" type="rotate" from="45 450 12" to="405 450 12" dur="6s" repeatCount="indefinite"/></rect>')
    return wrap(w, h, b)


# ---------------------------------------------------------------- 2. matrix rain
def matrix():
    w, h = 900, 130
    random.seed(11)
    chars = "01<>{}/;=+*#$%&"
    b = bg(w, h)
    for i in range(44):
        x = 14 + i * 20
        col = "".join(f'<tspan x="{x}" dy="15">{escape(random.choice(chars))}</tspan>' for _ in range(9))
        d = random.choice([3, 4, 5, 6, 7])
        begin = -random.random() * d
        color = random.choice([CY, GR, MG])
        b += (f'<g opacity=".55"><text x="{x}" y="0" font-size="14" fill="{color}">{col}'
              f'<animateTransform attributeName="transform" type="translate" values="0 -140;0 140" dur="{d}s" begin="{begin:.2f}s" repeatCount="indefinite"/></text></g>')
    b += (f'<rect width="{w}" height="{h}" rx="16" fill="{BG}" opacity=".35"/>'
          + text(450, 65, "// VANSH_OS  ONLINE //", 26, CY, weight="bold",
                 extra='filter="url(#glow)"')
          )
    return wrap(w, h, b)


# ---------------------------------------------------------------- 3. terminal
def terminal():
    w, h = 900, 300
    lines = [("$ whoami", GR), ("vansh_bakshi // BCA @ MDU Rohtak (2027)", INK), ("$ cat focus.txt", GR),
             ("AI/ML · GenAI · NLP · RAG · Full Stack", INK), ("$ ./status.sh", GR),
             ("[ OK ] learning   [ OK ] building   [ OK ] shipping", CY), ('$ git commit -m "keep improving"', GR)]
    b = bg(w, h) + f'<rect x="20" y="20" width="860" height="260" rx="12" fill="#0a0a1f" stroke="url(#g)" stroke-width="1.5"/>'
    b += (f'<circle cx="44" cy="42" r="6" fill="{RD}"/><circle cx="66" cy="42" r="6" fill="{YL}"/><circle cx="88" cy="42" r="6" fill="{GR}"/>'
          + text(450, 42, "vansh@os:~", 12, "#7f7fb0"))
    clips, body, total = "", "", 18
    for i, (s, c) in enumerate(lines):
        y = 82 + i * 27
        wd = round(len(s) * 9.4 + 12, 1)
        ts = 0.03 + i * 0.1
        te = ts + (0.07 if s.startswith("$") else 0.05)
        clips += (f'<clipPath id="c{i}"><rect x="38" y="{y-17}" height="24" width="0">'
                  f'<animate attributeName="width" values="0;0;{wd};{wd};0" keyTimes="0;{ts:.3f};{te:.3f};.96;1" dur="{total}s" repeatCount="indefinite"/></rect></clipPath>')
        body += f'<g clip-path="url(#c{i})">{text(40, y, s, 15, c, anchor="start")}</g>'
    cy = 82 + len(lines) * 27
    body += (text(40, cy, "$", 15, GR, anchor="start")
             + f'<rect x="58" y="{cy-10}" width="9" height="17" fill="{CY}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>')
    return wrap(w, h, b + body, clips)


# ---------------------------------------------------------------- 4. developer DNA
def dna():
    w, h = 900, 140
    nw, nh, step, x0, y = 135, 46, 182, 20, 30
    cy = y + nh / 2
    labels = ["CURIOSITY", "LEARNING", "EXPERIMENT", "ENGINEERING", "INNOVATION"]
    cols = [CY, BL, PU, MG, GR]
    cxs = [x0 + i * step + nw / 2 for i in range(5)]
    b = bg(w, h)
    for i in range(4):
        b += flow(f"M{x0 + i * step + nw} {cy} H{x0 + (i + 1) * step}", cols[i], 1.0)
    back = f"M{cxs[4]} {y + nh} C{cxs[4]} 130, {cxs[0]} 130, {cxs[0]} {y + nh}"
    b += flow(back, MG, 1.4, 1.5) + packet(back, MG, 6, 0, 4)
    b += packet(f"M{cxs[0]} {cy} H{cxs[4]}", CY, 8, 0, 6)
    for i, l in enumerate(labels):
        b += node(x0 + i * step, y, nw, nh, l, cols[i], i * 1.6, 8, 13)
    b += text(450, 104, "new questions", 11, MG)
    return wrap(w, h, b)


# ---------------------------------------------------------------- 5. boot loop
def boot():
    w, h = 900, 340
    cx, cy, rx, ry = 450, 170, 330, 120
    labels = ["POWER ON", "WARM-UP\nreview notes", "PICK MISSION", "LEARN · BUILD\nPRACTICE · TEACH", "WRITE IT DOWN", "COMMIT + PUSH"]
    cols = [CY, BL, PU, MG, YL, GR]
    path = f"M{cx + rx} {cy} A{rx} {ry} 0 1 1 {cx - rx} {cy} A{rx} {ry} 0 1 1 {cx + rx} {cy}"
    b = bg(w, h) + flow(path, PU, 1.6) + packet(path, CY, 14, 0, 6) + packet(path, MG, 14, -7, 6)
    b += (f'<circle cx="{cx}" cy="{cy}" r="50" fill="none" stroke="{CY}" stroke-width="1.5" stroke-dasharray="4 8">'
          f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="12s" repeatCount="indefinite"/></circle>'
          f'<circle cx="{cx}" cy="{cy}" r="36" fill="none" stroke="{MG}" stroke-width="1.5" stroke-dasharray="2 6">'
          f'<animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="8s" repeatCount="indefinite"/></circle>'
          + text(cx, cy - 6, "VANSH", 18, CY, weight="bold") + text(cx, cy + 14, "OS", 18, MG, weight="bold"))
    for i, l in enumerate(labels):
        a = math.radians(-90 + i * 60)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        b += node(round(x - 78), round(y - 24), 156, 48, l, cols[i], i * 14 / 6, 14, 12)
    return wrap(w, h, b)


# ---------------------------------------------------------------- 6. skill galaxy
def galaxy():
    w, h = 900, 540
    cx, cy = 450, 265
    random.seed(7)
    b = bg(w, h)
    for _ in range(80):
        b += (f'<circle cx="{random.randint(12, w - 12)}" cy="{random.randint(12, h - 12)}" r="{random.choice([.8, 1, 1.4, 1.8])}" fill="#fff">'
              f'<animate attributeName="opacity" values=".1;.9;.1" dur="{random.randint(2, 6)}s" begin="-{random.randint(0, 5)}s" repeatCount="indefinite"/></circle>')
    pl = ""
    for rx, ry, dur, cw, color, names in SKILLS:
        s = 1 if cw else 0
        path = f"M{cx + rx} {cy} A{rx} {ry} 0 1 {s} {cx - rx} {cy} A{rx} {ry} 0 1 {s} {cx + rx} {cy}"
        b += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{color}" stroke-opacity=".35" stroke-dasharray="4 8">'
              f'<animate attributeName="stroke-dashoffset" from="24" to="0" dur="3s" repeatCount="indefinite"/></ellipse>')
        for i, n in enumerate(names):
            pw = 9 * len(n) + 24
            pl += (f'<g><rect x="{-pw / 2}" y="-13" width="{pw}" height="26" rx="13" fill="{PANEL}" stroke="{color}" stroke-width="1.8" filter="url(#glow)"/>'
                   + text(0, 0, n, 12, INK) +
                   f'<animateMotion dur="{dur}s" begin="-{dur * i / len(names):.2f}s" repeatCount="indefinite" path="{path}"/></g>')
    b += (f'<circle cx="{cx}" cy="{cy}" r="44" fill="{PANEL}" stroke="url(#g)" stroke-width="3" filter="url(#glow)">'
          f'<animate attributeName="r" values="40;47;40" dur="3s" repeatCount="indefinite"/></circle>'
          + text(cx, cy, "VANSH", 16, CY, weight="bold"))
    b += pl
    for i, (c, l) in enumerate([(GR, "comfortable"), (YL, "building"), (BL, "exploring")]):
        x = 24 + i * 140
        b += f'<circle cx="{x}" cy="{h - 22}" r="6" fill="{c}"/>' + text(x + 14, h - 22, l, 12, "#9fb4d8", anchor="start")
    return wrap(w, h, b)


# ---------------------------------------------------------------- 7. architecture
def architecture():
    w, h = 900, 390
    b = bg(w, h)
    row1 = [("USER", CY), ("FRONTEND\nReact / Flutter", BL), ("API LAYER\nFlask / FastAPI", PU), ("AUTH +\nVALIDATION", MG), ("SERVICE\nLOGIC", GR)]
    xs = [20, 200, 380, 560, 740]
    nw, nh, y = 140, 58, 50
    cy = y + nh / 2
    for i in range(4):
        d = f"M{xs[i] + nw} {cy} H{xs[i + 1]}"
        b += flow(d, row1[i][1]) + packet(d, CY, 1.8, i * 0.45, 5)
    sc = xs[4] + nw / 2
    row2 = [(290, "MONITORING\nlogs + metrics", YL), (470, "ML / NLP\nMODELS", MG), (650, "DATABASE\nPostgres", CY)]
    for x, l, c in row2:
        tx = x + nw / 2
        d = f"M{sc} {y + nh} C{sc} 190, {tx} 170, {tx} 262"
        b += flow(d, c, 1.4) + packet(d, c, 3.2, (x % 7) * 0.3, 5)
    for x, l, c in row2:
        b += node(x, 262, nw, nh, l, c, x % 5, 4)
    for i, (l, c) in enumerate(row1):
        b += node(xs[i], y, nw, nh, l, c, i * 0.5, 4)
    b += text(190, 30, "CLIENT", 11, "#7f7fb0") + text(650, 30, "BACKEND", 11, "#7f7fb0")
    b += text(540, 350, "INTELLIGENCE + DATA", 11, "#7f7fb0")
    return wrap(w, h, b)


# ---------------------------------------------------------------- 8. ML pipeline
def ml():
    w, h = 900, 280
    names = ["RAW\nDATA", "CLEAN +\nVALIDATE", "FEATURE\nENGINEERING", "STRATIFIED\nSPLIT", "TRAIN\nBASELINE", "EVALUATE\nP · R · F1", "SERVE\nVIA API"]
    cols = [CY, BL, PU, MG, YL, GR, CY]
    nw, nh, y, step, x0 = 100, 52, 24, 128, 20
    cy = y + nh / 2
    cxs = [x0 + i * step + nw / 2 for i in range(7)]
    b = bg(w, h)
    for i in range(6):
        b += flow(f"M{x0 + i * step + nw} {cy} H{x0 + (i + 1) * step}", cols[i], 1.0)
    b += packet(f"M{cxs[0]} {cy} H{cxs[6]}", CY, 7, 0, 6)
    loop = f"M{cxs[5]} {y + nh} C{cxs[5]} 126, {cxs[4]} 126, {cxs[4]} {y + nh}"
    b += flow(loop, MG, 1.2) + packet(loop, MG, 2.4, 0, 4) + text((cxs[4] + cxs[5]) / 2, 118, "tune / rebalance", 11, MG)
    for i, n in enumerate(names):
        b += node(x0 + i * step, y, nw, nh, n, cols[i], i, 7, 11)
    b += text(40, 150, "F1 SCORE  ↑  over iterations", 12, GR, anchor="start")
    b += f'<path d="M40 252 H860 M40 160 V252" stroke="#2b2b66" stroke-width="1" fill="none"/>'
    curve = "M40 240 C140 238 190 215 280 205 S470 175 560 168 S760 150 860 148"
    b += (f'<path d="{curve}" pathLength="1" fill="none" stroke="url(#g)" stroke-width="3" stroke-dasharray="1" filter="url(#glow)">'
          f'<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;.7;.95;1" dur="7s" repeatCount="indefinite"/></path>')
    b += (f'<circle r="6" fill="{GR}" filter="url(#glow)"><animateMotion dur="7s" repeatCount="indefinite" '
          f'keyPoints="0;1;1" keyTimes="0;.7;1" calcMode="linear" path="{curve}"/></circle>')
    return wrap(w, h, b)


# ---------------------------------------------------------------- 9. security gates
def security():
    w, h = 900, 330
    gates = [(170, "TLS"), (290, "RATE\nLIMIT"), (410, "INPUT\nVALIDATION"), (530, "AUTHN"), (650, "AUTHZ"), (770, "AUDIT\nLOG")]
    good_y = 165
    b = bg(w, h)
    b += text(52, 110, "CLIENT", 12, "#7f7fb0") + f'<path d="M30 {good_y} H850" stroke="#1f1f55" stroke-width="2" fill="none"/>'
    for gx, l in gates:
        b += (f'<rect x="{gx - 7}" y="70" width="14" height="190" rx="7" fill="{PANEL}" stroke="{CY}" stroke-width="2" filter="url(#glow)">'
              f'<animate attributeName="stroke" values="{CY};{MG};{CY}" dur="4s" repeatCount="indefinite"/></rect>'
              + text(gx, 285, l, 11, INK))
    b += node(812, 120, 76, 90, "APP\n+ DB", GR, 0, 3, 13)
    # good traffic
    for begin in (0, -2.5):
        b += (f'<g><circle r="6" fill="{CY}" filter="url(#glow)"/>{text(0, -16, "request", 10, CY)}'
              f'<animateTransform attributeName="transform" type="translate" values="30 {good_y};850 {good_y}" dur="5s" begin="{begin - 9 if begin else 0}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;.93;1" dur="5s" begin="{-begin}s" repeatCount="indefinite"/></g>')
    # threats that get blocked
    threats = [("SQL INJECTION", 100, 410, 0), ("BRUTE FORCE", 225, 290, 3), ("STOLEN TOKEN", 100, 650, 6)]
    for label, ly, gx, begin in threats:
        b += (f'<g><circle r="7" fill="{RD}" filter="url(#glow)"/>{text(0, -17, label, 10, RD)}'
              f'<animateTransform attributeName="transform" type="translate" values="30 {ly};{gx - 14} {ly};{gx - 14} {ly}" keyTimes="0;.3;1" dur="9s" begin="{begin - 9 if begin else 0}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.3;.36;1" dur="9s" begin="{begin - 9 if begin else 0}s" repeatCount="indefinite"/></g>')
        b += (f'<circle cx="{gx - 14}" cy="{ly}" fill="none" stroke="{RD}" stroke-width="3">'
              f'<animate attributeName="r" values="0;0;26;26" keyTimes="0;.3;.5;1" dur="9s" begin="{begin - 9 if begin else 0}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.3;.5;1" dur="9s" begin="{begin - 9 if begin else 0}s" repeatCount="indefinite"/></circle>')
        b += (f'<g>{text(gx, 318, "BLOCKED", 10, GR)}'
              f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.3;.36;.6;.7;1" dur="9s" begin="{begin - 9 if begin else 0}s" repeatCount="indefinite"/></g>')
    b += text(450, 28, "DEFENSE IN DEPTH: every request crosses every layer", 13, CY, weight="bold")
    return wrap(w, h, b)


# ---------------------------------------------------------------- 10. tech radar
def radar():
    w, h = 900, 440
    cx, cy, R = 260, 220, 190
    b = bg(w, h)
    for r, c in [(63, GR), (127, YL), (190, BL)]:
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-opacity=".5" stroke-dasharray="3 6"/>'
    b += (f'<path d="M{cx - R} {cy} H{cx + R} M{cx} {cy - R} V{cy + R}" stroke="#25255a" stroke-width="1"/>'
          + text(cx, cy - 56, "ADOPT", 10, GR) + text(cx, cy - 120, "TRIAL", 10, YL) + text(cx, cy - 183, "ASSESS", 10, BL))
    x1, y1 = cx + R * math.cos(math.radians(-35)), cy + R * math.sin(math.radians(-35))
    b += (f'<g><path d="M{cx} {cy} L{cx + R} {cy} A{R} {R} 0 0 0 {x1:.1f} {y1:.1f} Z" fill="{CY}" opacity=".22"/>'
          f'<rect x="{cx}" y="{cy - 1}" width="{R}" height="2" fill="{CY}" filter="url(#glow)"/>'
          f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="6s" repeatCount="indefinite"/></g>')
    for i, (n, r, a, c) in enumerate(RADAR):
        x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        b += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{c}" filter="url(#glow)"/>'
              f'<circle cx="{x:.1f}" cy="{y:.1f}" fill="none" stroke="{c}" stroke-width="2">'
              f'<animate attributeName="r" values="5;18;5" dur="3s" begin="-{i * 0.4:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values=".9;0;.9" dur="3s" begin="-{i * 0.4:.1f}s" repeatCount="indefinite"/></circle>'
              + text(x + 9, y - 9, n, 10, INK, anchor="start"))
    groups = [("ADOPT", GR, "Python · Git/GitHub · Flask · VS Code"), ("TRIAL", YL, "Flutter · FastAPI · Docker\nscikit-learn · React"),
              ("ASSESS", BL, "PyTorch · TensorFlow\nOpenCV · Postgres")]
    b += text(540, 40, "SCAN RESULTS", 14, CY, anchor="start", weight="bold")
    for i, (t, c, items) in enumerate(groups):
        s = 0.05 + i * 0.22
        y = 100 + i * 105
        b += (f'<g opacity="0">{text(540, y, t, 16, c, anchor="start", weight="bold")}{text(540, y + 34, items, 13, INK, anchor="start")}'
              f'<rect x="530" y="{y - 18}" width="4" height="{40 + items.count(chr(10)) * 16 + 14}" fill="{c}"/>'
              f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{s:.2f};{s + .08:.2f};.93;1" dur="10s" repeatCount="indefinite"/></g>')
    return wrap(w, h, b)


# ---------------------------------------------------------------- 11. SOS outbox
def sos():
    w, h = 900, 320
    nw, nh, y = 140, 80, 90
    xs = [20, 200, 380, 560, 740]
    cxs = [x + nw / 2 for x in xs]
    cy = y + nh / 2
    names = [("PHONE\nCitizen App", CY), ("OUTBOX\nlocal queue", MG), ("NETWORK", RD), ("API\nGATEWAY", PU), ("RESPONDER\nDASHBOARD", GR)]
    b = bg(w, h) + text(450, 30, "OFFLINE-FIRST OUTBOX: persist first, sync later", 14, CY, weight="bold")
    for i in range(4):
        b += flow(f"M{xs[i] + nw} {cy} H{xs[i + 1]}", names[i][1], 1.3)
    for i, (l, c) in enumerate(names):
        if i == 2:
            b += (f'<rect x="{xs[i]}" y="{y}" width="{nw}" height="{nh}" rx="10" fill="{PANEL}" stroke-width="2.5" filter="url(#glow)" stroke="{RD}">'
                  f'<animate attributeName="stroke" calcMode="discrete" values="{RD};{GR};{GR}" keyTimes="0;.5;1" dur="10s" repeatCount="indefinite"/></rect>'
                  + text(cxs[i], cy - 6, "NETWORK", 13))
        else:
            b += node(xs[i], y, nw, nh, l, c, i * 0.6, 4)
    b += (f'<g>{text(cxs[2], cy + 16, "OFFLINE", 13, RD, weight="bold")}'
          f'<animate attributeName="opacity" calcMode="discrete" values="1;0;0" keyTimes="0;.5;1" dur="10s" repeatCount="indefinite"/></g>'
          f'<g>{text(cxs[2], cy + 16, "ONLINE", 13, GR, weight="bold")}'
          f'<animate attributeName="opacity" calcMode="discrete" values="0;1;1" keyTimes="0;.5;1" dur="10s" repeatCount="indefinite"/></g>')
    b += (f'<g>{text(cxs[1], y + nh + 26, "retry: 1s → 2s → 4s", 12, YL)}'
          f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.1;.16;.5;.56;1" dur="10s" repeatCount="indefinite"/></g>'
          f'<g>{text(cxs[1], y - 14, "1 queued", 12, MG)}'
          f'<animate attributeName="opacity" calcMode="discrete" values="1;1;0;0" keyTimes="0;.62;.63;1" dur="10s" repeatCount="indefinite"/></g>'
          f'<g>{text(cxs[1], y - 14, "0 queued", 12, GR)}'
          f'<animate attributeName="opacity" calcMode="discrete" values="0;0;1;1" keyTimes="0;.62;.63;1" dur="10s" repeatCount="indefinite"/></g>'
          f'<g>{text(cxs[3], y + nh + 26, "idempotent by UUID", 12, "#9fb4d8")}</g>'
          f'<g>{text(cxs[4], y + nh + 26, "NEW SOS ✓", 13, GR, weight="bold")}'
          f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.8;.84;.92;.95;1" dur="10s" repeatCount="indefinite"/></g>')
    pts = [90, 270, 330, 270, 270, 330, 270, 270, 450, 630, 810, 810, 810]
    kt = [0, .1, .16, .22, .3, .36, .44, .55, .62, .72, .82, .9, 1]
    vals = ";".join(f"{p} {cy}" for p in pts)
    b += (f'<g><circle r="8" fill="{YL}" filter="url(#glow)"/>{text(0, -18, "SOS", 11, YL, weight="bold")}'
          f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{";".join(str(k) for k in kt)}" dur="10s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.02;.88;.92;1" dur="10s" repeatCount="indefinite"/></g>')
    return wrap(w, h, b)


# ---------------------------------------------------------------- 12. skill bars
def skillbars():
    w, h = 900, 330
    b = bg(w, h) + text(30, 34, "SKILL LEVELS  (self-assessed, edit BARS in generate_assets.py)", 13, CY, anchor="start", weight="bold")
    tx, tw = 250, 560
    for i, (n, v, c) in enumerate(BARS):
        y = 70 + i * 40
        fw = tw * v / 100
        b += (text(30, y + 7, n, 12, INK, anchor="start")
              + f'<rect x="{tx}" y="{y}" width="{tw}" height="14" rx="7" fill="#12123a"/>'
              f'<rect x="{tx}" y="{y}" width="0" height="14" rx="7" fill="{c}" filter="url(#glow)">'
              f'<animate attributeName="width" values="0;{fw};{fw};0" keyTimes="0;.25;.9;1" dur="8s" begin="{i * 0.3}s" repeatCount="indefinite"/></rect>'
              f'<g>{text(0, 0, f"{v}%", 12, c, anchor="start")}'
              f'<animateTransform attributeName="transform" type="translate" values="{tx + 8} {y + 7};{tx + fw + 8} {y + 7};{tx + fw + 8} {y + 7};{tx + 8} {y + 7}" keyTimes="0;.25;.9;1" dur="8s" begin="-{i * 0.3}s" repeatCount="indefinite"/></g>')
    return wrap(w, h, b)


# ---------------------------------------------------------------- 13. roadmap
def roadmap():
    w, h = 900, 300
    x0, span = 150, 734
    months = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
    lanes = []
    for l, *_ in ROADMAP:
        if l not in lanes:
            lanes.append(l)
    b = bg(w, h) + text(30, 30, "2026 ROADMAP", 14, CY, anchor="start", weight="bold")
    for i, m in enumerate(months):
        x = x0 + i * span / 12
        b += f'<path d="M{x:.1f} 50 V270" stroke="#1d1d52" stroke-width="1"/>' + text(x + span / 24, 50, m, 10, "#7f7fb0")
    for i, l in enumerate(lanes):
        b += text(30, 88 + i * 42, l, 12, INK, anchor="start")
    for j, (l, start, ln, c) in enumerate(ROADMAP):
        y = 78 + lanes.index(l) * 42
        x = x0 + span * start / 365
        wd = span * ln / 365
        b += (f'<rect x="{x:.1f}" y="{y}" width="0" height="20" rx="10" fill="{c}" opacity=".85" filter="url(#glow)">'
              f'<animate attributeName="width" values="0;{wd:.1f};{wd:.1f};0" keyTimes="0;.2;.93;1" dur="12s" begin="{j * 0.4}s" repeatCount="indefinite"/></rect>')
    b += (f'<g><rect x="-1" y="56" width="2" height="214" fill="{MG}" filter="url(#glow)"/>{text(0, 276, "NOW", 11, MG, weight="bold")}'
          f'<animateTransform attributeName="transform" type="translate" values="{x0} 0;{x0 + span} 0" dur="12s" repeatCount="indefinite"/></g>')
    return wrap(w, h, b)


if __name__ == "__main__":
    for name, fn in [("divider", divider), ("matrix", matrix), ("terminal", terminal), ("dna", dna), ("boot", boot),
                     ("galaxy", galaxy), ("architecture", architecture), ("ml", ml), ("security", security),
                     ("radar", radar), ("sos", sos), ("skillbars", skillbars), ("roadmap", roadmap)]:
        save(f"{name}.svg", fn())

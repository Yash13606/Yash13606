#!/usr/bin/env python3
import datetime
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "contrib-heatmap.svg")

# Modern Premium Palette (Ocean to Cyberpunk Pink/Purple)
PALETTE = ["rgba(255, 255, 255, 0.05)", "#0ea5e9", "#3b82f6", "#6366f1", "#8b5cf6", "#d946ef"]

CELL = 12
GAP = 4
STEP = CELL + GAP
PAD = 32
LEFT_LABEL_W = 30
TOP_LABEL_H = 20
TITLEBAR_H = 0 # No terminal bar

BG_START = "#09090b"
BG_END = "#18181b"
CARD_BORDER = "rgba(255, 255, 255, 0.08)"
MUTED = "#a1a1aa"
TEXT = "#f4f4f5"
ACCENT = "#8b5cf6"
GOLD = "#f59e0b"

# reveal timing
COL_T = 0.015
ROW_T = 0.04
CELL_DUR = 0.3

def level_for(count):
    if count == 0: return 0
    if count <= 5: return 1
    if count <= 15: return 2
    if count <= 30: return 3
    if count <= 50: return 4
    return 5

def build_grid(days):
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7
    grid = []
    col = [None] * lead_pad
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid

def render(data):
    days = data["days"]
    grid = build_grid(days)
    n_cols = len(grid)
    art_w = n_cols * STEP
    art_h = 7 * STEP

    month_labels = []
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None: continue
            date = datetime.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD
    stats_h = 88
    canvas_h = PAD + TOP_LABEL_H + art_h + stats_h + PAD

    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
text {{ font-family: 'Inter', sans-serif; }}
@keyframes cell {{
  0%   {{ opacity: 0; transform: scale(0.9) translateY(-4px); }}
  100% {{ opacity: 1; transform: scale(1) translateY(0); }}
}}
.c {{ opacity: 0; animation: cell {CELL_DUR:.2f}s cubic-bezier(0.23, 1, 0.32, 1) both; }}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG_START}"/><stop offset="1" stop-color="{BG_END}"/></linearGradient>',
        f'<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="#ec4899"/></linearGradient>',
        '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2" result="blur" /><feComposite in="SourceGraphic" in2="blur" operator="over"/></filter>',
        '</defs>',
        
        # Background
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="16" fill="url(#bg)"/>',
        # Glassmorphic Card
        f'<rect x="16" y="16" width="{canvas_w-32}" height="{canvas_h-32}" rx="12" fill="none" stroke="{CARD_BORDER}" stroke-width="1"/>',
    ]

    grid_top = PAD + TOP_LABEL_H
    grid_left = PAD + LEFT_LABEL_W

    for ci, label in month_labels:
        x = grid_left + ci * STEP
        parts.append(f'<text x="{x}" y="{grid_top - 10}" fill="{MUTED}" font-size="11" font-weight="500">{label}</text>')

    for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + wi * STEP + CELL * 0.78
        parts.append(f'<text x="{PAD}" y="{y:.1f}" fill="{MUTED}" font-size="10" font-weight="500">{wname}</text>')

    # the boxes as circles
    for ci, column in enumerate(grid):
        gx = grid_left + ci * STEP
        for ri, cell in enumerate(column):
            if cell is None: continue
            date_s, count, lvl = cell
            gy = grid_top + ri * STEP
            delay = ci * COL_T + ri * ROW_T
            
            # Add glow if high contribution
            glow = ' filter="url(#glow)"' if lvl >= 4 else ''
            
            parts.append(
                f'<rect class="c" x="{gx}" y="{gy}" width="{CELL}" height="{CELL}" rx="{CELL/2}" '
                f'fill="{PALETTE[lvl]}" style="animation-delay:{delay:.3f}s"{glow}>'
                f'<title>{date_s}: {count} contributions</title></rect>'
            )

    # legend: Less OOOOO More
    leg_y = grid_top + art_h + 12
    leg_x = canvas_w - PAD - (len(PALETTE) * (CELL - 1) + 70)
    parts.append(f'<text x="{leg_x}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="11" font-weight="500" text-anchor="end">Less</text>')
    lx = leg_x + 8
    for lvl, color in enumerate(PALETTE):
        parts.append(f'<rect x="{lx}" y="{leg_y}" width="{CELL}" height="{CELL}" rx="{CELL/2}" fill="{color}"/>')
        lx += CELL + 2
    parts.append(f'<text x="{lx + 6}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="11" font-weight="500">More</text>')

    sep_y = leg_y + CELL + 20
    parts.append(f'<line x1="32" y1="{sep_y}" x2="{canvas_w - 32}" y2="{sep_y}" stroke="{CARD_BORDER}" stroke-width="1"/>')

    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    total = data["total_contributions"]
    best = data["best_day"]
    rng = data["range"]

    ly = sep_y + 30
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="14" fill="{TEXT}">'
                 f'<tspan font-weight="700">{total:,}</tspan>'
                 f'<tspan fill="{MUTED}"> contributions in the last year</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" font-weight="500" text-anchor="end">'
                 f'{rng["start"]} &#8594; {rng["end"]}</text>')
    ly += 24
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13" fill="{MUTED}" font-weight="500">Current streak '
                 f'<tspan fill="url(#accent)" font-weight="700">{cs} days</tspan>'
                 f'<tspan fill="{MUTED}">   &#183;   Longest </tspan>'
                 f'<tspan fill="url(#accent)" font-weight="700">{ls} days</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" font-weight="500" text-anchor="end">'
                 f'Best day <tspan fill="{GOLD}" font-weight="700">{best["count"]}</tspan> on {best["date"]}</text>')

    parts.append("</svg>")
    return "".join(parts)

if __name__ == "__main__":
    data = json.load(open(IN_PATH))
    svg = render(data)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(svg)} bytes)")

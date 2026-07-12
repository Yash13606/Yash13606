import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")

W, H = 490, 376
PAD = 32

# Modern Color Palette
BG_START = "#09090b"
BG_END = "#18181b"
CARD_BG = "rgba(255, 255, 255, 0.03)"
CARD_BORDER = "rgba(255, 255, 255, 0.08)"
TEXT_MAIN = "#f4f4f5"
TEXT_MUTED = "#a1a1aa"
ACCENT_START = "#8b5cf6" # Purple
ACCENT_END = "#3b82f6"   # Blue
GREEN = "#10b981"

NAME = "Yash A"
ROLE = "Full Stack Developer"

ROWS = [
    ("kv", "Now", "SDE Intern @ Namo Labs"),
    ("kv", "Also", "Full Stack Intern @ SpazorLabs"),
    ("kv", "Edu", "B.Tech CS @ SRM Institute '28"),
    ("gap",),
    ("sec", "Tech Stack"),
    ("kv", "Frontend", "React, Next.js, TypeScript"),
    ("kv", "Backend", "Node, FastAPI, PostgreSQL"),
    ("kv", "AI / ML", "LLM APIs, RAG, AI Agents"),
    ("gap",),
    ("sec", "Highlights"),
    ("bul", "1st Place at CAD 4.0 Hackathon"),
    ("bul", "Built AI Financial Analytics & Health Surveillance"),
]

def esc(s):
    return html.escape(s)

def rise(inner, i):
    delay = 0.2 + i * 0.05
    return (f'<g opacity="0" transform="translate(0,8) scale(0.98)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.25s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.25s" fill="freeze" calcMode="spline" keySplines="0.23 1 0.32 1" additive="sum"/>'
            f'<animateTransform attributeName="transform" type="scale" from="0.98" to="1" '
            f'begin="{delay:.2f}s" dur="0.25s" fill="freeze" calcMode="spline" keySplines="0.23 1 0.32 1" additive="sum"/></g>')

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<defs>',
    f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG_START}"/><stop offset="1" stop-color="{BG_END}"/></linearGradient>',
    f'<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ACCENT_START}"/><stop offset="1" stop-color="{ACCENT_END}"/></linearGradient>',
    '<style>',
    "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap');",
    "text { font-family: 'Inter', sans-serif; }",
    '</style>',
    '</defs>',
    
    # Background
    f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>',
    
    # Glassmorphic Card
    f'<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="12" fill="{CARD_BG}" stroke="{CARD_BORDER}" stroke-width="1"/>',
    
    # Header Name & Role
    f'<g opacity="0" transform="translate(0,8) scale(0.98)">',
    f'<text x="{PAD}" y="{PAD + 20}" fill="{TEXT_MAIN}" font-size="20" font-weight="700">{esc(NAME)}</text>',
    f'<text x="{PAD}" y="{PAD + 40}" fill="url(#accent)" font-size="13" font-weight="600" letter-spacing="0.5">{esc(ROLE.upper())}</text>',
    f'<animate attributeName="opacity" from="0" to="1" begin="0.1s" dur="0.3s" fill="freeze"/>',
    f'<animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" begin="0.1s" dur="0.3s" fill="freeze" calcMode="spline" keySplines="0.23 1 0.32 1" additive="sum"/>',
    f'<animateTransform attributeName="transform" type="scale" from="0.98" to="1" begin="0.1s" dur="0.3s" fill="freeze" calcMode="spline" keySplines="0.23 1 0.32 1" additive="sum"/>',
    f'</g>'
]

y = PAD + 70
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += 12
        continue
    elif kind == "sec":
        title = esc(row[1])
        inner = (f'<text x="{PAD}" y="{y}" fill="{TEXT_MAIN}" font-size="14" font-weight="600">{title}</text>'
                 f'<rect x="{PAD}" y="{y+6}" width="24" height="2" rx="1" fill="url(#accent)"/>')
        y += 24
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (f'<rect x="{PAD}" y="{y-12}" width="70" height="20" rx="4" fill="{CARD_BG}" stroke="{CARD_BORDER}"/>'
                 f'<text x="{PAD + 35}" y="{y+2}" fill="{TEXT_MUTED}" font-size="11" font-weight="500" text-anchor="middle">{key}</text>'
                 f'<text x="{PAD + 84}" y="{y+2}" fill="{TEXT_MAIN}" font-size="13" font-weight="400">{val}</text>')
        y += 26
    elif kind == "bul":
        txt = esc(row[1])
        inner = (f'<circle cx="{PAD + 6}" cy="{y-4}" r="4" fill="url(#accent)"/>'
                 f'<text x="{PAD + 20}" y="{y+1}" fill="{TEXT_MAIN}" font-size="13" font-weight="400">{txt}</text>')
        y += 22
    else:
        continue
        
    parts.append(rise(inner, i))

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes")

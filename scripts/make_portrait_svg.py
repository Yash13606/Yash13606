import os
import sys
import base64

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-prepped.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "portrait.svg")

W, H = 370, 376

BG_START = "#09090b"
BG_END = "#18181b"
CARD_BORDER = "rgba(255, 255, 255, 0.08)"

with open(SRC, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    image_data = f"data:image/png;base64,{encoded_string}"

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<defs>',
    f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG_START}"/><stop offset="1" stop-color="{BG_END}"/></linearGradient>',
    
    # Animated Blob Gradients
    '<linearGradient id="blob1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#ec4899"/></linearGradient>',
    '<linearGradient id="blob2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b82f6"/><stop offset="1" stop-color="#14b8a6"/></linearGradient>',
    
    '<filter id="blur"><feGaussianBlur stdDeviation="30" result="blur" /></filter>',
    '</defs>',
    
    # Background
    f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>',
    f'<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="12" fill="none" stroke="{CARD_BORDER}" stroke-width="1"/>',
    
    # Glowing Blobs with CSS rotation
    f'<g style="mix-blend-mode: screen; filter: url(#blur);">',
    f'  <circle cx="{W/2 - 40}" cy="{H/2}" r="70" fill="url(#blob1)">',
    f'    <animateTransform attributeName="transform" type="rotate" from="0 {W/2} {H/2}" to="360 {W/2} {H/2}" dur="20s" repeatCount="indefinite" />',
    f'  </circle>',
    f'  <circle cx="{W/2 + 40}" cy="{H/2}" r="70" fill="url(#blob2)">',
    f'    <animateTransform attributeName="transform" type="rotate" from="360 {W/2} {H/2}" to="0 {W/2} {H/2}" dur="25s" repeatCount="indefinite" />',
    f'  </circle>',
    f'</g>',
    
    # Base64 Image with Floating Animation and entrance scaling
    f'<g opacity="0" transform="translate(0, 15) scale(0.95)">',
    f'  <image href="{image_data}" x="30" y="30" width="{W-60}" height="{H-60}" preserveAspectRatio="xMidYMax meet">',
    f'    <animate attributeName="y" values="30;20;30" dur="6s" repeatCount="indefinite" />',
    f'  </image>',
    f'  <animate attributeName="opacity" from="0" to="1" begin="0.1s" dur="0.4s" fill="freeze" />',
    f'  <animateTransform attributeName="transform" type="translate" from="0 15" to="0 0" begin="0.1s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.23 1 0.32 1" additive="sum"/>',
    f'  <animateTransform attributeName="transform" type="scale" from="0.95" to="1" begin="0.1s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.23 1 0.32 1" additive="sum"/>',
    f'</g>',
    
    '</svg>'
]

svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes")

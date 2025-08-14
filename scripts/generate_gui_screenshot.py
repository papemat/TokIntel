#!/usr/bin/env python3
"""
Generate a placeholder GUI screenshot for TokIntel Quick Start
"""

import os, sys

IMG_DIR = "docs/images"
PNG_PATH = os.path.join(IMG_DIR, "tokintel_gui_home.png")
SVG_FALLBACK = os.path.join(IMG_DIR, "tokintel_gui_home.svg")

os.makedirs(IMG_DIR, exist_ok=True)

def make_png():
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (1200, 720), (16, 18, 24))
        d = ImageDraw.Draw(img)
        title = "TokIntel GUI – Home"
        subtitle = "Placeholder screenshot"
        d.rectangle([40, 40, 1160, 120], outline=(80,80,80), width=2)
        d.text((60,60), title, fill=(230,230,230))
        d.text((60,92), subtitle, fill=(180,180,180))
        d.rectangle([40, 160, 1160, 680], outline=(70,70,70), width=2)
        d.text((60,180), "Dashboard • Collections • Health • Logs", fill=(210,210,210))
        img.save(PNG_PATH)
        return True
    except Exception as e:
        return False

def make_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720">
      <rect width="100%" height="100%" fill="#101218"/>
      <text x="60" y="90" fill="#e6e6e6" font-family="system-ui" font-size="36">TokIntel GUI – Home</text>
      <text x="60" y="130" fill="#b4b4b4" font-family="system-ui" font-size="22">Placeholder screenshot (SVG fallback)</text>
      <rect x="40" y="160" width="1120" height="520" fill="none" stroke="#474747" stroke-width="2"/>
      <text x="60" y="200" fill="#d2d2d2" font-family="system-ui" font-size="20">Dashboard • Collections • Health • Logs</text>
    </svg>'''
    with open(SVG_FALLBACK, "w", encoding="utf-8") as f:
        f.write(svg)

if not make_png():
    make_svg()

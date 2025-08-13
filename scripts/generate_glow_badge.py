import sys, os, textwrap
os.makedirs("docs/badges", exist_ok=True)

def write_badge(name, left="Status", right="OK", color="#2ea043", filename=None):
    if not filename:
        filename = f"docs/badges/{name}.svg"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="210" height="28" role="img" aria-label="{left}: {right}">
  <title>{left}: {right}</title>
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#555"/>
      <stop offset="100%" stop-color="#555"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2.2" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      @keyframes pulse {{0%{{opacity:.65}}50%{{opacity:1}}100%{{opacity:.65}}}}
      .left{{fill:url(#grad)}} .right{{fill:{color}}}
      .label{{fill:#fff;font:600 11px system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif}}
      .value{{fill:#fff;font:700 12px system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif}}
      .glow{{filter:url(#glow);animation:pulse 2.4s ease-in-out infinite}}
    </style>
  </defs>
  <rect class="left" x="0" y="0" width="110" height="28" rx="4"/>
  <rect class="right glow" x="110" y="0" width="100" height="28" rx="4"/>
  <g aria-hidden="true">
    <text class="label" x="55" y="18" text-anchor="middle">{left}</text>
    <text class="value" x="160" y="18" text-anchor="middle">{right}</text>
  </g>
</svg>'''
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✅ Badge scritto: {filename}")

if __name__ == "__main__":
    # esempi standard (non sovrascrive se già esistono, a meno di --force)
    write_badge("quickstart_ready_glow", "Quick Start", "READY", "#2ea043")
    # aggiungi qui altri badge se vuoi standardizzarli

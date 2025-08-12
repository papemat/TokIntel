#!/usr/bin/env python3
"""
Genera un'immagine di esempio della sezione Monitoraggio CI per il README
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Configurazione per output di alta qualità
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

# Crea figura
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')

# Colori
colors = {
    'green': '#28a745',
    'red': '#dc3545',
    'gray': '#6c757d',
    'blue': '#007bff',
    'orange': '#fd7e14',
    'background': '#f8f9fa',
    'border': '#dee2e6',
    'text': '#212529'
}

# Sfondo
ax.add_patch(patches.Rectangle((0, 0), 12, 8, facecolor=colors['background'], edgecolor='none'))

# Titolo
ax.text(6, 7.5, '📊 Monitoraggio CI', fontsize=20, fontweight='bold', 
        ha='center', va='center', color=colors['text'])

# Descrizione
ax.text(6, 7, 'Questa sezione mostra lo stato in tempo reale dei workflow CI/CD per TokIntel', 
        fontsize=12, ha='center', va='center', color=colors['text'], style='italic')

# Tabella header
headers = ['Badge', 'Descrizione', 'Frequenza', 'Artifact Principali']
header_y = 6.2
for i, header in enumerate(headers):
    x = 1 + i * 2.5
    ax.add_patch(FancyBboxPatch((x-0.4, header_y-0.2), 1.8, 0.4, 
                               boxstyle="round,pad=0.1", 
                               facecolor=colors['blue'], 
                               edgecolor=colors['border'], 
                               linewidth=1))
    ax.text(x, header_y, header, fontsize=10, fontweight='bold', 
            ha='center', va='center', color='white')

# Righe della tabella
badges = [
    ('E2E', 'Test End-to-End completi', 'Ad ogni push e PR', 'E2E Artifacts'),
    ('Exports', 'Verifica export aggiornati', 'Giornaliero + manuale', 'Latest Exports'),
    ('Lint Makefile', 'Controlla TAB Makefile', 'Ad ogni PR', 'Solo log'),
    ('Smoke Test', 'Heartbeat giornaliero', 'Giornaliero + manuale', 'Latest Exports')
]

badge_colors = [colors['green'], colors['green'], colors['green'], colors['gray']]

for row, (badge, desc, freq, artifact) in enumerate(badges):
    y = 5.5 - row * 0.8
    
    # Badge (cerchio colorato)
    badge_x = 1
    ax.add_patch(plt.Circle((badge_x, y), 0.15, facecolor=badge_colors[row], edgecolor='black', linewidth=1))
    ax.text(badge_x, y, badge, fontsize=8, fontweight='bold', ha='center', va='center', color='white')
    
    # Descrizione
    ax.text(3.5, y, desc, fontsize=9, ha='left', va='center', color=colors['text'])
    
    # Frequenza
    ax.text(6, y, freq, fontsize=9, ha='left', va='center', color=colors['text'])
    
    # Artifact
    ax.text(8.5, y, artifact, fontsize=9, ha='left', va='center', color=colors['text'])

# Legenda badge
legend_y = 2.5
ax.text(1, legend_y + 0.3, 'ℹ️ Come interpretare i badge:', fontsize=12, fontweight='bold', 
        ha='left', va='center', color=colors['text'])

legend_items = [
    ('Verde', colors['green'], 'tutto OK'),
    ('Rosso', colors['red'], 'errore nel workflow'),
    ('Grigio', colors['gray'], 'workflow non ancora eseguito')
]

for i, (label, color, desc) in enumerate(legend_items):
    y = legend_y - i * 0.3
    ax.add_patch(plt.Circle((1, y), 0.1, facecolor=color, edgecolor='black', linewidth=1))
    ax.text(1.3, y, f'{label} → {desc}', fontsize=10, ha='left', va='center', color=colors['text'])

# Aggiungi frecce e annotazioni per evidenziare elementi
arrow_props = dict(arrowstyle='->', color=colors['orange'], lw=2, alpha=0.7)

# Freccia verso badge E2E
ax.annotate('', xy=(1, 5.5), xytext=(0.5, 6.5), arrowprops=arrow_props)
ax.text(0.3, 6.7, 'Badge\nE2E', fontsize=8, ha='center', va='center', 
        color=colors['orange'], fontweight='bold')

# Freccia verso tabella
ax.annotate('', xy=(6, 6.2), xytext=(4, 7.2), arrowprops=arrow_props)
ax.text(3.8, 7.4, 'Tabella\nmonitoraggio', fontsize=8, ha='center', va='center', 
        color=colors['orange'], fontweight='bold')

# Freccia verso legenda
ax.annotate('', xy=(1, 2.5), xytext=(3, 1.5), arrowprops=arrow_props)
ax.text(3.2, 1.3, 'Legenda\nbadge', fontsize=8, ha='center', va='center', 
        color=colors['orange'], fontweight='bold')

# Aggiungi watermark
ax.text(11.5, 0.5, 'TokIntel\nCI Monitoring', fontsize=8, ha='right', va='bottom', 
        color=colors['gray'], alpha=0.5, style='italic')

# Salva immagine
plt.tight_layout()
plt.savefig('docs/images/monitoraggio-ci-example.png', 
            bbox_inches='tight', 
            facecolor=colors['background'],
            edgecolor='none',
            pad_inches=0.2)
plt.close()

print("✅ Immagine di esempio generata: docs/images/monitoraggio-ci-example.png")

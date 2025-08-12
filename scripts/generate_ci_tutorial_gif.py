#!/usr/bin/env python3
"""
Genera una GIF tutorial animata per la sezione Monitoraggio CI
Mostra il processo: click badge → workflow → run → artifact
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Configurazione
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['font.size'] = 10

# Colori
colors = {
    'green': '#28a745',
    'blue': '#007bff',
    'orange': '#fd7e14',
    'red': '#dc3545',
    'gray': '#6c757d',
    'background': '#f8f9fa',
    'border': '#dee2e6',
    'text': '#212529',
    'highlight': '#ffc107'
}

def create_frame(frame_num, total_frames=60):
    """Crea un frame dell'animazione"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Sfondo
    ax.add_patch(patches.Rectangle((0, 0), 12, 8, facecolor=colors['background'], edgecolor='none'))
    
    # Timeline dell'animazione
    progress = frame_num / total_frames
    
    # Fase 1: README con badge (0-25%)
    if progress <= 0.25:
        phase_progress = progress / 0.25
        
        # Titolo README
        ax.text(6, 7.5, '📊 Monitoraggio CI', fontsize=16, fontweight='bold', 
                ha='center', va='center', color=colors['text'])
        
        # Badge (appare gradualmente)
        badge_alpha = min(1.0, phase_progress * 3)
        badge_y = 6.5
        
        # Badge E2E (verde)
        ax.add_patch(Circle((2, badge_y), 0.3, facecolor=colors['green'], 
                           edgecolor='black', linewidth=2, alpha=badge_alpha))
        ax.text(2, badge_y, 'E2E', fontsize=10, fontweight='bold', 
                ha='center', va='center', color='white', alpha=badge_alpha)
        
        # Badge Exports (verde)
        ax.add_patch(Circle((4, badge_y), 0.3, facecolor=colors['green'], 
                           edgecolor='black', linewidth=2, alpha=badge_alpha))
        ax.text(4, badge_y, 'Exports', fontsize=8, fontweight='bold', 
                ha='center', va='center', color='white', alpha=badge_alpha)
        
        # Badge Smoke Test (grigio) - questo sarà cliccato
        smoke_alpha = min(1.0, max(0, (phase_progress - 0.5) * 2))
        ax.add_patch(Circle((6, badge_y), 0.3, facecolor=colors['gray'], 
                           edgecolor='black', linewidth=2, alpha=smoke_alpha))
        ax.text(6, badge_y, 'Smoke', fontsize=8, fontweight='bold', 
                ha='center', va='center', color='white', alpha=smoke_alpha)
        
        # Cursore che si muove verso il badge Smoke Test
        if phase_progress > 0.7:
            cursor_x = 2 + (6 - 2) * (phase_progress - 0.7) / 0.3
            cursor_y = 7.2
            ax.add_patch(Circle((cursor_x, cursor_y), 0.1, facecolor=colors['orange'], 
                               edgecolor='black', linewidth=2))
            ax.text(cursor_x, cursor_y + 0.2, '👆', fontsize=12, ha='center', va='center')
    
    # Fase 2: Transizione (25-35%)
    elif progress <= 0.35:
        transition_progress = (progress - 0.25) / 0.1
        
        # Fade out README
        alpha = 1 - transition_progress
        ax.text(6, 7.5, '📊 Monitoraggio CI', fontsize=16, fontweight='bold', 
                ha='center', va='center', color=colors['text'], alpha=alpha)
        
        # Fade in "Navigando..." 
        ax.text(6, 4, 'Navigando verso GitHub Actions...', fontsize=14, fontweight='bold', 
                ha='center', va='center', color=colors['blue'], alpha=transition_progress)
    
    # Fase 3: Pagina GitHub Actions (35-70%)
    elif progress <= 0.70:
        phase_progress = (progress - 0.35) / 0.35
        
        # Header GitHub Actions
        ax.text(6, 7.5, 'GitHub Actions - Smoke Test Workflow', fontsize=14, fontweight='bold', 
                ha='center', va='center', color=colors['text'])
        
        # Lista dei run
        runs = [
            ('✅ Run #1234', '2 min ago', 'success'),
            ('✅ Run #1233', '1 hour ago', 'success'),
            ('❌ Run #1232', '2 hours ago', 'failure'),
            ('✅ Run #1231', '3 hours ago', 'success')
        ]
        
        for i, (run_name, time_ago, status) in enumerate(runs):
            y = 6.5 - i * 0.8
            color = colors['green'] if status == 'success' else colors['red']
            
            # Evidenzia il primo run (quello che verrà cliccato)
            if i == 0 and phase_progress > 0.3:
                ax.add_patch(FancyBboxPatch((1.5, y-0.3), 9, 0.6, 
                                           boxstyle="round,pad=0.1", 
                                           facecolor=colors['highlight'], 
                                           edgecolor=colors['orange'], 
                                           linewidth=2, alpha=0.3))
            
            ax.text(2, y, run_name, fontsize=10, fontweight='bold', 
                    ha='left', va='center', color=color)
            ax.text(8, y, time_ago, fontsize=9, ha='left', va='center', color=colors['text'])
        
        # Cursore che si muove verso il primo run
        if phase_progress > 0.5:
            cursor_x = 1.5 + (2 - 1.5) * (phase_progress - 0.5) / 0.2
            cursor_y = 6.2
            ax.add_patch(Circle((cursor_x, cursor_y), 0.1, facecolor=colors['orange'], 
                               edgecolor='black', linewidth=2))
            ax.text(cursor_x, cursor_y + 0.2, '👆', fontsize=12, ha='center', va='center')
    
    # Fase 4: Pagina del run (70-85%)
    elif progress <= 0.85:
        phase_progress = (progress - 0.70) / 0.15
        
        # Header del run
        ax.text(6, 7.5, 'Run #1234 - Smoke Test', fontsize=14, fontweight='bold', 
                ha='center', va='center', color=colors['text'])
        
        # Status del run
        ax.text(6, 7, '✅ Success - All checks passed', fontsize=12, 
                ha='center', va='center', color=colors['green'])
        
        # Sezione Artifacts
        ax.text(2, 6, '📦 Artifacts', fontsize=12, fontweight='bold', 
                ha='left', va='center', color=colors['text'])
        
        artifacts = [
            ('📄 latest-exports', 'CSV, JSON files'),
            ('📋 streamlit-log', 'Application logs'),
            ('📊 test-results', 'Test reports')
        ]
        
        for i, (artifact_name, description) in enumerate(artifacts):
            y = 5.5 - i * 0.6
            ax.text(2.5, y, artifact_name, fontsize=10, fontweight='bold', 
                    ha='left', va='center', color=colors['blue'])
            ax.text(6, y, description, fontsize=9, ha='left', va='center', color=colors['text'])
        
        # Cursore che si muove verso il primo artifact
        if phase_progress > 0.5:
            cursor_x = 1.5 + (2.5 - 1.5) * (phase_progress - 0.5) / 0.5
            cursor_y = 5.2
            ax.add_patch(Circle((cursor_x, cursor_y), 0.1, facecolor=colors['orange'], 
                               edgecolor='black', linewidth=2))
            ax.text(cursor_x, cursor_y + 0.2, '👆', fontsize=12, ha='center', va='center')
    
    # Fase 5: Download completato (85-100%)
    else:
        completion_progress = (progress - 0.85) / 0.15
        
        # Messaggio di successo
        ax.text(6, 4.5, '✅ Download completato!', fontsize=16, fontweight='bold', 
                ha='center', va='center', color=colors['green'])
        
        # File scaricati
        ax.text(6, 4, '📄 latest-exports.zip', fontsize=12, 
                ha='center', va='center', color=colors['blue'])
        
        # Istruzioni
        ax.text(6, 3.5, 'Ora puoi estrarre e analizzare i file di export', fontsize=10, 
                ha='center', va='center', color=colors['text'], style='italic')
        
        # Animazione di successo
        if completion_progress > 0.5:
            ax.text(6, 2.5, '🎉 Tutorial completato!', fontsize=14, fontweight='bold', 
                    ha='center', va='center', color=colors['orange'])
    
    # Watermark
    ax.text(11.5, 0.5, 'TokIntel\nCI Tutorial', fontsize=8, ha='right', va='bottom', 
            color=colors['gray'], alpha=0.5, style='italic')
    
    plt.tight_layout()
    return fig

def generate_gif():
    """Genera la GIF tutorial"""
    print("🎬 Generazione GIF tutorial CI Monitoring...")
    
    # Crea i frame
    frames = []
    total_frames = 60
    
    for i in range(total_frames):
        fig = create_frame(i, total_frames)
        
        # Converti in immagine PIL
        fig.canvas.draw()
        img = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        frames.append(img)
        plt.close(fig)
        
        if (i + 1) % 10 == 0:
            print(f"  Frame {i+1}/{total_frames}")
    
    # Salva come GIF
    output_path = 'docs/images/ci-monitoring-tutorial.gif'
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,  # 100ms per frame = 6 secondi totali
        loop=0,
        optimize=True
    )
    
    print(f"✅ GIF tutorial generata: {output_path}")
    print(f"📊 Dimensione: {os.path.getsize(output_path) / 1024:.1f} KB")

if __name__ == "__main__":
    generate_gif()

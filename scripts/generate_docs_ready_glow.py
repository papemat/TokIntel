#!/usr/bin/env python3
"""
Genera un'immagine con effetto glow per il badge Docs Ready
Crea un'anteprima visiva del badge con glow verde neon
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
from pathlib import Path

def create_docs_ready_badge_with_glow():
    """
    Crea un badge Docs Ready con effetto glow
    """
    print("✨ Generazione badge Docs Ready con glow...")
    
    # Dimensioni dell'immagine
    width, height = 400, 200
    
    # Crea immagine di base
    img = Image.new('RGBA', (width, height), (248, 249, 250, 255))  # Sfondo grigio chiaro
    draw = ImageDraw.Draw(img)
    
    # Colori
    green_color = (40, 167, 69)  # Verde GitHub
    glow_color = (0, 255, 0)     # Verde neon per glow
    text_color = (255, 255, 255) # Testo bianco
    
    # Posizione del badge
    badge_x, badge_y = width // 2, height // 2
    badge_width, badge_height = 200, 60
    
    # Crea effetto glow (cerchi multipli con blur)
    for i in range(5, 0, -1):
        glow_radius = 20 + i * 3
        glow_alpha = 50 - i * 8
        
        # Disegna cerchio glow
        glow_draw = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        glow_draw_draw = ImageDraw.Draw(glow_draw)
        
        glow_draw_draw.rounded_rectangle(
            [badge_x - badge_width//2 - glow_radius, 
             badge_y - badge_height//2 - glow_radius,
             badge_x + badge_width//2 + glow_radius, 
             badge_y + badge_height//2 + glow_radius],
            radius=15,
            fill=(glow_color[0], glow_color[1], glow_color[2], glow_alpha)
        )
        
        # Applica blur
        glow_draw = glow_draw.filter(ImageFilter.GaussianBlur(radius=i))
        
        # Combina con l'immagine principale
        img = Image.alpha_composite(img, glow_draw)
    
    # Disegna il badge principale
    draw.rounded_rectangle(
        [badge_x - badge_width//2, badge_y - badge_height//2,
         badge_x + badge_width//2, badge_y + badge_height//2],
        radius=10,
        fill=green_color,
        outline=(255, 255, 255, 100),
        width=2
    )
    
    # Testo del badge
    try:
        # Prova a usare un font di sistema
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
    except:
        try:
            # Fallback per Linux
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except:
            # Fallback per font di default
            font = ImageFont.load_default()
    
    # Testo "Docs Ready"
    text = "Docs Ready"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = badge_x - text_width // 2
    text_y = badge_y - text_height // 2
    
    # Disegna testo con ombra
    draw.text((text_x + 1, text_y + 1), text, fill=(0, 0, 0, 100), font=font)
    draw.text((text_x, text_y), text, fill=text_color, font=font)
    
    # Aggiungi icona 📚
    icon_text = "📚"
    icon_bbox = draw.textbbox((0, 0), icon_text, font=font)
    icon_width = icon_bbox[2] - icon_bbox[0]
    
    icon_x = badge_x - badge_width//2 + 20
    icon_y = badge_y - text_height // 2
    
    draw.text((icon_x, icon_y), icon_text, fill=text_color, font=font)
    
    # Aggiungi testo "PASSING" sotto
    status_text = "PASSING"
    status_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12) if os.path.exists("/System/Library/Fonts/Arial.ttf") else ImageFont.load_default()
    
    status_bbox = draw.textbbox((0, 0), status_text, font=status_font)
    status_width = status_bbox[2] - status_bbox[0]
    
    status_x = badge_x - status_width // 2
    status_y = badge_y + badge_height//2 - 15
    
    draw.text((status_x, status_y), status_text, fill=text_color, font=status_font)
    
    # Aggiungi watermark
    watermark_text = "TokIntel Docs Ready"
    watermark_font = ImageFont.load_default()
    draw.text((width - 150, height - 20), watermark_text, fill=(108, 117, 125, 150), font=watermark_font)
    
    return img

def generate_docs_ready_glow():
    """
    Genera l'immagine del badge Docs Ready con glow
    """
    # Crea directory se non esiste
    docs_images_dir = Path('docs/images')
    docs_images_dir.mkdir(parents=True, exist_ok=True)
    
    # Genera l'immagine
    img = create_docs_ready_badge_with_glow()
    
    # Salva l'immagine
    output_path = docs_images_dir / 'docs-ready-badge-glow.png'
    img.save(output_path, 'PNG', optimize=True)
    
    # Verifica dimensione
    file_size = os.path.getsize(output_path) / 1024
    print(f"✅ Badge Docs Ready con glow generato: {output_path}")
    print(f"📊 Dimensione: {file_size:.1f} KB")
    
    return str(output_path)

if __name__ == "__main__":
    generate_docs_ready_glow()

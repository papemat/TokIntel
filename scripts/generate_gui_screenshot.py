#!/usr/bin/env python3
"""
Generate a placeholder GUI screenshot for TokIntel Quick Start
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_gui_screenshot():
    """Create a placeholder GUI screenshot"""
    
    # Create image
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='#1E1E1E')  # Dark theme
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 32)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header
    draw.text((width//2, 80), "TokIntel", fill='#00FF88', font=font_large, anchor="mm")
    draw.text((width//2, 120), "Analisi Multimodale di Video", fill='#CCCCCC', font=font_medium, anchor="mm")
    
    # Main content area
    content_y = 200
    draw.rectangle([50, content_y, width-50, height-100], outline='#444444', width=2)
    
    # Sidebar
    sidebar_width = 200
    draw.rectangle([50, content_y, 50+sidebar_width, height-100], fill='#2A2A2A', outline='#444444')
    
    # Sidebar items
    sidebar_items = ["🏠 Home", "📊 Dashboard", "🔍 Ricerca", "📁 Esporta", "⚙️ Config"]
    for i, item in enumerate(sidebar_items):
        y = content_y + 30 + i * 40
        draw.text((70, y), item, fill='#FFFFFF', font=font_small)
    
    # Main content
    main_x = 50 + sidebar_width + 20
    draw.text((main_x, content_y + 30), "Benvenuto in TokIntel", fill='#FFFFFF', font=font_medium)
    draw.text((main_x, content_y + 70), "• Analisi multimodale di video", fill='#CCCCCC', font=font_small)
    draw.text((main_x, content_y + 95), "• Estrazione audio con Whisper", fill='#CCCCCC', font=font_small)
    draw.text((main_x, content_y + 120), "• OCR e analisi visiva", fill='#CCCCCC', font=font_small)
    draw.text((main_x, content_y + 145), "• Ricerca semantica unificata", fill='#CCCCCC', font=font_small)
    
    # Status bar
    status_y = height - 50
    draw.rectangle([50, status_y, width-50, height-20], fill='#2A2A2A')
    draw.text((70, status_y + 15), "✅ GUI Pronta | Porta: 8501 | Status: Online", fill='#00FF88', font=font_small)
    
    # Save image
    output_path = "docs/images/tokintel_gui_home.png"
    img.save(output_path)
    print(f"✅ Screenshot placeholder creato: {output_path}")
    
    return output_path

if __name__ == "__main__":
    create_gui_screenshot()

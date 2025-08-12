#!/usr/bin/env python3
"""
Genera un'anteprima dei badge CI con effetto glow verde neon
Evidenzia i badge "passing" con un effetto luminoso
"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
import os

def create_glow_effect(image, color=(0, 255, 0), intensity=2.0, blur_radius=10):
    """
    Crea un effetto glow attorno ai badge verdi
    """
    # Converti in RGB se necessario
    if image.mode == 'RGBA':
        image_rgb = image.convert('RGB')
    else:
        image_rgb = image
    
    # Crea una maschera per i pixel verdi (badge passing)
    img_array = np.array(image_rgb)
    
    # Definisci il range di verde per i badge "passing"
    # Badge verdi GitHub hanno valori RGB simili a (40, 167, 69)
    green_lower = np.array([30, 150, 50])
    green_upper = np.array([60, 200, 100])
    
    # Crea maschera per i pixel verdi
    green_mask = np.all((img_array >= green_lower) & (img_array <= green_upper), axis=2)
    
    # Crea immagine glow
    glow_img = Image.new('RGBA', image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    
    # Disegna glow attorno ai badge verdi
    for y in range(image.height):
        for x in range(image.width):
            if green_mask[y, x]:
                # Disegna cerchio glow
                glow_draw.ellipse(
                    [x-15, y-15, x+15, y+15],
                    fill=(color[0], color[1], color[2], 100),
                    outline=(color[0], color[1], color[2], 150)
                )
    
    # Applica blur per effetto glow
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Combina con l'immagine originale
    result = image.convert('RGBA')
    result = Image.alpha_composite(result, glow_img)
    
    return result

def enhance_badges(image):
    """
    Migliora la visibilità dei badge
    """
    # Aumenta leggermente la saturazione
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.2)
    
    # Aumenta leggermente il contrasto
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.1)
    
    return image

def generate_ci_badges_preview():
    """
    Genera l'anteprima dei badge CI con glow
    """
    print("✨ Generazione anteprima badge CI con glow...")
    
    # Percorso dell'immagine originale
    input_path = 'docs/images/monitoraggio-ci-example.png'
    output_path = 'docs/images/ci-badges-preview.png'
    
    # Verifica che l'immagine originale esista
    if not os.path.exists(input_path):
        print(f"❌ Immagine originale non trovata: {input_path}")
        print("💡 Esegui prima: make ci-screenshot")
        return False
    
    try:
        # Carica l'immagine originale
        original_img = Image.open(input_path)
        print(f"📸 Immagine caricata: {original_img.size}")
        
        # Migliora i badge
        enhanced_img = enhance_badges(original_img)
        
        # Applica effetto glow
        glow_img = create_glow_effect(enhanced_img)
        
        # Salva l'immagine con glow
        glow_img.save(output_path, 'PNG', optimize=True)
        
        # Verifica dimensione
        file_size = os.path.getsize(output_path) / 1024
        print(f"✅ Anteprima badge CI generata: {output_path}")
        print(f"📊 Dimensione: {file_size:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante la generazione: {e}")
        return False

if __name__ == "__main__":
    success = generate_ci_badges_preview()
    if not success:
        exit(1)

"""
Script per creare immagini demo per testare la ricerca da immagine
"""

from PIL import Image, ImageDraw, ImageFont
import pathlib

def create_demo_image(text: str, filename: str, size: tuple = (400, 300), bg_color: str = "lightblue"):
    """Create a demo image with text"""
    # Create image
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fallback to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill="black", font=font)
    
    # Save
    output_path = pathlib.Path("demo_images") / filename
    img.save(output_path)
    print(f"✓ Creata immagine demo: {output_path}")

def main():
    """Create demo images"""
    # Create demo_images directory
    demo_dir = pathlib.Path("demo_images")
    demo_dir.mkdir(exist_ok=True)
    
    # Create demo images
    create_demo_image(
        "YOGA\nBREATHING\nEXERCISE",
        "yoga_breathing.jpg",
        (400, 300),
        "lightgreen"
    )
    
    create_demo_image(
        "PILATES\nCORE\nWORKOUT",
        "pilates_core.jpg",
        (400, 300),
        "lightcoral"
    )
    
    create_demo_image(
        "MARKETING\nCONVERSION\nSTRATEGY",
        "marketing_conversion.jpg",
        (400, 300),
        "lightyellow"
    )
    
    print("\n🎬 Immagini demo create in demo_images/")
    print("Puoi usare queste immagini per testare la ricerca da immagine nel dashboard!")

if __name__ == "__main__":
    main()

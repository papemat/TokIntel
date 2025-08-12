from PIL import Image, ImageDraw, ImageFont
import pathlib

def create_demo_frames():
    """Generate demo frames with text for testing OCR and CLIP"""
    texts = [
        ("vid_00000", ["Yoga Friday", "New Class", "Breath & Flow"]),
        ("vid_00001", ["Pilates Core", "3 tricks", "Neutral spine"]),
        ("vid_00002", ["CTA that Converts", "One ask", "One benefit"])
    ]
    
    root = pathlib.Path("data/frames")
    root.mkdir(parents=True, exist_ok=True)
    
    for dirname, lines in texts:
        d = root / dirname
        d.mkdir(parents=True, exist_ok=True)
        
        for i, line in enumerate(lines, start=1):
            # Create image with white background
            img = Image.new("RGB", (800, 450), (255, 255, 255))
            drw = ImageDraw.Draw(img)
            
            # Try to use a default font, fallback to basic if not available
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position to center it
            bbox = drw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (800 - text_width) // 2
            y = (450 - text_height) // 2
            
            # Draw text
            drw.text((x, y), line, fill=(0, 0, 0), font=font)
            
            # Save frame
            img.save(d / f"frame_{i:05d}.jpg")
    
    print("✓ Visual demo frames creati.")

if __name__ == "__main__":
    create_demo_frames()

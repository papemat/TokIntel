from __future__ import annotations
import json
import pathlib
import easyocr

def run_ocr_on_frames(frames: list[str], langs: list[str], out_json: str):
    """Run OCR on a list of frame images and save results to JSON"""
    if not frames:
        pathlib.Path(out_json).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(out_json).write_text(
            json.dumps({"frames": [], "combined_text": ""}, ensure_ascii=False, indent=2), 
            encoding="utf-8"
        )
        return {"frames": [], "combined_text": ""}
    
    reader = easyocr.Reader(langs, gpu=False)
    items = []
    
    for f in frames:
        try:
            res = reader.readtext(f, detail=0)  # solo testo
            items.append({"frame": f, "text": " ".join(res)})
        except Exception as e:
            print(f"Errore OCR su {f}: {e}")
            items.append({"frame": f, "text": ""})
    
    combined = " ".join([it["text"] for it in items]).strip()
    data = {"frames": items, "combined_text": combined}
    
    pathlib.Path(out_json).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out_json).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    
    return data

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run OCR on frame images")
    parser.add_argument("frames_dir", help="Directory containing frame images")
    parser.add_argument("out_json", help="Output JSON file")
    parser.add_argument("--langs", nargs="+", default=["it", "en"], help="OCR languages")
    
    args = parser.parse_args()
    
    frames_dir = pathlib.Path(args.frames_dir)
    frames = sorted([str(p) for p in frames_dir.glob("*.jpg")])
    
    data = run_ocr_on_frames(frames, args.langs, args.out_json)
    print(f"✓ OCR completato: {len(data['frames'])} frame, {len(data['combined_text'])} caratteri")

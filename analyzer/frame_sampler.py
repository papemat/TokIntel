from __future__ import annotations
import pathlib
import subprocess
from PIL import Image

def sample_frames_ffmpeg(video_path: str, out_dir: str, mode: str="scene", fps: float=0.5, 
                        scene_threshold: float=0.4, max_frames: int=40, resize_width: int=512):
    """Extract frames from video using ffmpeg with scene detection or fixed FPS"""
    outd = pathlib.Path(out_dir)
    outd.mkdir(parents=True, exist_ok=True)
    
    # Estrai frame con ffmpeg: o fps fisso, o rilevamento cambi scena
    if mode == "fps":
        vf = f"fps={fps}"
    else:
        vf = f"select='gt(scene,{scene_threshold})',showinfo"
    
    # Scrive frame numerati
    cmd = ["ffmpeg", "-y", "-i", video_path, "-vf", vf, "-vsync", "vfr", 
           f"{out_dir}/frame_%05d.jpg"]
    
    try:
        subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Errore ffmpeg: {e}")
        return []
    
    # Resize & limit
    frames = sorted(pathlib.Path(out_dir).glob("frame_*.jpg"))
    if not frames:
        return []
    
    keep = frames[:max_frames]
    for p in keep:
        try:
            img = Image.open(p)
            w, h = img.size
            if w > resize_width:
                nh = int(h * resize_width / w)
                img = img.resize((resize_width, nh))
                img.save(p, quality=90)
        except Exception:
            pass
    
    # Rimuovi eventuali extra oltre max_frames
    for p in frames[max_frames:]:
        try:
            p.unlink()
        except:
            pass
    
    return [str(p) for p in sorted(pathlib.Path(out_dir).glob("frame_*.jpg"))]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract frames from video")
    parser.add_argument("video_path", help="Path to video file")
    parser.add_argument("out_dir", help="Output directory for frames")
    parser.add_argument("--mode", default="scene", choices=["scene", "fps"], help="Sampling mode")
    parser.add_argument("--fps", type=float, default=0.5, help="FPS for fps mode")
    parser.add_argument("--scene-threshold", type=float, default=0.4, help="Scene detection threshold")
    parser.add_argument("--max-frames", type=int, default=40, help="Maximum frames to extract")
    parser.add_argument("--resize-width", type=int, default=512, help="Resize width")
    
    args = parser.parse_args()
    frames = sample_frames_ffmpeg(
        args.video_path, args.out_dir, args.mode, args.fps,
        args.scene_threshold, args.max_frames, args.resize_width
    )
    print(f"✓ Estratti {len(frames)} frame in {args.out_dir}")

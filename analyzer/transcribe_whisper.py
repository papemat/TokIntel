#!/usr/bin/env python3
"""
Transcription script using OpenAI Whisper with per-file timeout support.
"""

import argparse
import json
import signal
import sys
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

try:
    import whisper
except ImportError:
    print("❌ Whisper non installato. Installa con: pip install openai-whisper", file=sys.stderr)
    sys.exit(1)


@contextmanager
def time_limit(seconds: int):
    """Context manager per timeout cross-platform."""
    if not seconds or seconds <= 0:
        yield
        return
    
    # POSIX systems (Linux/macOS) - timeout hard
    if hasattr(signal, 'SIGALRM'):
        def _raise(*_): 
            raise TimeoutError("per-file transcription timeout")
        
        signal.signal(signal.SIGALRM, _raise)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
    
    # Windows - timeout soft con thread
    else:
        # Su Windows usiamo un approccio più semplice
        # Il timeout sarà "soft" - non interrompe il processo
        start_time = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start_time
            if elapsed > seconds:
                print(f"⚠️  Attenzione: trascrizione durata {elapsed:.1f}s > {seconds}s (timeout soft su Windows)", 
                      file=sys.stderr)


def transcribe_file(model, audio_path: str, lang_hint: Optional[str] = None) -> dict:
    """Transcribe un singolo file audio usando Whisper."""
    result = model.transcribe(
        audio_path,
        language=lang_hint,
        verbose=False
    )
    return result


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files with Whisper")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory con file audio")
    parser.add_argument("--output_dir", type=str, help="Directory output (default: input_dir/transcriptions)")
    parser.add_argument("--model", type=str, default="base", choices=["tiny", "base", "small", "medium", "large"], 
                       help="Modello Whisper da usare")
    parser.add_argument("--gpu", type=str, default="auto", choices=["on", "off", "auto"], 
                       help="Usa GPU (on/off/auto)")
    parser.add_argument("--lang_hint", type=str, help="Hint lingua (es. 'it', 'en')")
    parser.add_argument("--limit", type=int, help="Limita numero file da processare")
    parser.add_argument("--max_duration", type=int, help="Durata massima file in secondi")
    parser.add_argument("--timeout_sec", type=int, default=120, help="timeout per file (0=disattivato)")
    
    args = parser.parse_args()
    
    # Setup input/output
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"❌ Directory input non trovata: {input_dir}", file=sys.stderr)
        sys.exit(1)
    
    output_dir = Path(args.output_dir) if args.output_dir else input_dir / "transcriptions"
    output_dir.mkdir(exist_ok=True)
    
    # Setup GPU
    if args.gpu == "off":
        import os
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    elif args.gpu == "on":
        # Forza uso GPU se disponibile
        pass
    
    # Carica modello
    print(f"🔄 Caricamento modello {args.model}...")
    model = whisper.load_model(args.model)
    print(f"✅ Modello caricato: {args.model}")
    
    # Trova file audio
    audio_extensions = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".webm", ".mp4"}
    audio_files = [f for f in input_dir.iterdir() 
                   if f.is_file() and f.suffix.lower() in audio_extensions]
    
    if args.limit:
        audio_files = audio_files[:args.limit]
    
    print(f"🎵 Trovati {len(audio_files)} file audio")
    print(f"⏱️  Timeout per file: {args.timeout_sec}s" if args.timeout_sec > 0 else "⏱️  Timeout disattivato")
    
    # Processa file
    count = 0
    for audio in audio_files:
        out_json = output_dir / f"{audio.stem}.json"
        
        # Skip se già processato
        if out_json.exists():
            print(f"⏭️  {audio.name} già processato, salto")
            continue
        
        # Controllo durata se specificato
        if args.max_duration:
            try:
                import librosa
                duration = librosa.get_duration(path=str(audio))
                if duration > args.max_duration:
                    print(f"⏭️  {audio.name} troppo lungo ({duration:.1f}s > {args.max_duration}s), salto")
                    continue
            except ImportError:
                print("⚠️  librosa non installato, salto controllo durata")
        
        print(f"🎤 Transcribing {audio.name}...")
        
        try:
            with time_limit(args.timeout_sec):
                result = transcribe_file(model, str(audio), args.lang_hint)
            out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            count += 1
            print(f"✅ {audio.name} -> {out_json.name}")
        except TimeoutError:
            print(f"⏰ timeout su {audio.name} (>{args.timeout_sec}s), salto.", file=sys.stderr)
        except Exception as e:
            print(f"❌ errore su {audio.name}: {e}", file=sys.stderr)
    
    print(f"\n🎉 Completato! {count}/{len(audio_files)} file trascritti")


if __name__ == "__main__":
    main()

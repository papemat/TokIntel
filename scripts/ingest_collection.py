from __future__ import annotations
import argparse
import subprocess
import sys
import logging
from typing import Optional, Callable
from PIL import Image

# Setup logging
from utils.logging_setup import setup_logging
setup_logging()
log = logging.getLogger('tokintel.ingest')

# Import timing utilities
from utils.timing import timed_step, timed_ingest

def run(cmd: list[str], desc: str):
    log.info(f"Iniziando: {desc}")
    print(f"[TokIntel] {desc} ...")
    code = subprocess.call(cmd)
    if code != 0:
        log.error(f"Step fallito: {desc} (exit={code})")
        print(f"[TokIntel] Step fallito: {desc} (exit={code})", file=sys.stderr)
        sys.exit(code)
    log.info(f"Completato: {desc}")

def main(
    collection_url: Optional[str] = None,
    max_items: int = 100,
    gpu_mode: str = "auto",
    download_limit: Optional[int] = None,
    timeout_sec: int = 120,
    audio_only: bool = False,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    status_callback: Optional[Callable[[str], None]] = None,
    thumbnail_callback: Optional[Callable[[Image.Image], None]] = None
):
    """
    Main ingest function with optional callback support for live feedback
    """
    # Handle command line arguments if called directly
    if collection_url is None:
        ap = argparse.ArgumentParser()
        ap.add_argument("--url", required=True, help="URL raccolta TikTok")
        ap.add_argument("--max", type=int, default=100)
        ap.add_argument("--gpu", default="auto")     # auto|on|off
        ap.add_argument("--download-limit", type=int, default=None)
        ap.add_argument("--timeout_sec", type=int, default=120, help="timeout trascrizione per file (0=disattivato)")
        ap.add_argument("--audio_only", action="store_true", help="modalità solo audio: salta OCR e analisi visiva")
        args = ap.parse_args()
        
        collection_url = args.url
        max_items = args.max
        gpu_mode = args.gpu
        download_limit = args.download_limit
        timeout_sec = args.timeout_sec
        audio_only = args.audio_only

    # Calcola step totali in base alla modalità
    total_steps = 3 if audio_only else 5
    current_step = 0

    # Helper function to update progress
    def update_progress(step_description: str):
        nonlocal current_step
        current_step += 1
        log.info(f"Step {current_step}/{total_steps}: {step_description}")
        if progress_callback:
            progress_callback(current_step, total_steps)
        if status_callback:
            status_callback(step_description)
        print(f"[TokIntel] {step_description} ...")

    # Wrappa tutto il processo con timing
    with timed_ingest(log):
        # 1) Collezione → DB
        with timed_step(log, "Raccolta URL"):
            update_progress("Raccolta URL")
            run(["python","-m","collector.collect_tiktok_collection","--url",collection_url,"--max",str(max_items)], "Raccolta URL")

        # 2) Download mp4 mancanti con thumbnail extraction
        with timed_step(log, "Download video"):
            update_progress("Download video")
            import sys
            sys.path.append('.')
            from downloader.fetch_many import fetch_missing_with_callbacks
            fetch_missing_with_callbacks(
                limit=download_limit,
                thumbnail_callback=thumbnail_callback,
                status_callback=status_callback
            )

        # 3) Indice visivo (frame+OCR+CLIP è dentro build_visual_index) - SKIP se audio_only
        if not audio_only:
            with timed_step(log, "Estrazione frame e OCR"):
                update_progress("Estrazione frame e OCR")
                run(["python","-m","analyzer.build_visual_index","--gpu",gpu_mode], "Indice visivo")
        else:
            log.info("Modalità AUDIO ONLY: saltati OCR e analisi visiva")
            print("[AUDIO ONLY] Modalità attiva: saltati OCR e analisi visiva")

        # 4) Trascrizione audio (batch su data/media) + NLP
        with timed_step(log, "Trascrizione audio"):
            update_progress("Trascrizione audio")
            run([
                "python","-m","analyzer.transcribe_whisper",
                "--input_dir","data/media/video",
                "--gpu",gpu_mode,
                "--model","small",
                "--limit","50",
                "--max_duration","180",
                "--timeout_sec",str(timeout_sec)
            ], "Trascrizione")

        # 5) Indice testuale
        with timed_step(log, "Costruzione indice testuale"):
            update_progress("Costruzione indice testuale")
            run(["python","-m","analyzer.index_faiss","--gpu",gpu_mode], "Indice testuale")

    print("✓ Ingest completato.")

if __name__ == "__main__":
    main()

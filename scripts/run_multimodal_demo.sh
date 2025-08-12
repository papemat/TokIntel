#!/usr/bin/env bash

# TokIntel Multimodal Demo Script
echo "🚀 Avvio demo multimodale TokIntel..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "📦 Attivazione virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment non trovato. Assicurati di averlo creato con 'python -m venv .venv'"
fi

# Create demo frames
echo "🎬 Creazione frame demo..."
python scripts/make_visual_demo.py

# Run OCR on demo frames
echo "🔍 Esecuzione OCR sui frame demo..."
python - <<'PY'
import glob
import json
import os
import pathlib
import yaml
from analyzer.ocr_extractor import run_ocr_on_frames

# Load config
cfg = yaml.safe_load(open("config/settings.yaml", "r", encoding="utf-8"))
frames_root = pathlib.Path(cfg["visual"]["frames_dir"])
ocr_out = pathlib.Path(cfg["ocr"]["out_dir"])
ocr_out.mkdir(parents=True, exist_ok=True)

# Process each video directory
for d in sorted(frames_root.glob("vid_*")):
    frames = sorted([str(p) for p in d.glob("*.jpg")])
    out_json = ocr_out / (d.name + ".json")
    data = run_ocr_on_frames(frames, cfg["ocr"]["langs"], str(out_json))
    print(f"  {d.name} OCR: {data['combined_text'][:80]}...")
PY

# Build visual index
echo "🎯 Costruzione indice visivo..."
python -m analyzer.build_visual_index --gpu auto

echo "✅ Demo multimodale completata!"
echo ""
echo "📁 File generati:"
echo "  - Frame demo: data/frames/"
echo "  - OCR results: data/ocr/"
echo "  - Visual index: data/indexes/visual.index"
echo "  - Visual map: data/indexes/visual_map.json"

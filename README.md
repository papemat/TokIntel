# TokIntel - Analisi Multimodale di Video

[![Prod Check CI](https://img.shields.io/badge/prod--check-passing-brightgreen?style=flat&logo=github-actions)](https://github.com/papemat/TokIntel/actions/workflows/prod-check.yml)
[![Perf Nightly](https://img.shields.io/badge/perf--nightly-scheduled-blue?style=flat&logo=clock)](https://github.com/papemat/TokIntel/actions/workflows/perf-nightly.yml)
[![Go‑Live Docs](https://img.shields.io/badge/docs-go--live-brightgreen)](docs/GO_LIVE_CHECKLIST.md)
[![Enterprise Setup](https://img.shields.io/badge/docs-enterprise--setup-informational)](docs/ENTERPRISE_SETUP.md)
[![Performance Dashboard](https://img.shields.io/badge/dashboard-perf--trends-orange?style=flat&logo=chart-line)](http://localhost:8502)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](#)

TokIntel è un sistema di analisi multimodale per video che combina:
- **Estrazione audio** (Whisper)
- **Estrazione visiva** (OCR + CLIP)
- **Indicizzazione semantica** (FAISS)
- **Ricerca unificata** (testo + visivo)

## 🚀 Setup Rapido

```bash
# 1. Setup ambiente
make setup

# 2. Demo multimodale (genera frame finti, OCR, indice visivo)
make multimodal-demo

# 3. Rindicizza il testo (include OCR)
make index-cpu

# 4. Cerca (testuale + OCR)
make search q="CTA che converte"
```

## 📁 Struttura del Progetto

```
TokIntel/
├── config/
│   └── settings.yaml          # Configurazione multimodale
├── analyzer/
│   ├── frame_sampler.py       # Estrazione frame con ffmpeg
│   ├── ocr_extractor.py       # OCR con EasyOCR
│   ├── vision_clip.py         # Embedding CLIP
│   ├── build_visual_index.py  # Indice visivo FAISS
│   ├── index_faiss.py         # Indice testuale (include OCR)
│   └── run_multimodal.py      # Setup schema multimodale
├── downloader/
│   └── fetch_video.py         # Download video con yt-dlp
├── scripts/
│   ├── make_visual_demo.py    # Genera frame demo
│   └── run_multimodal_demo.sh # Demo completa
├── tests/
│   ├── test_ocr_and_frames.py # Test OCR
│   └── test_vision_clip.py    # Test CLIP
└── data/
    ├── frames/                # Frame estratti
    ├── ocr/                   # Risultati OCR
    ├── indexes/               # Indici FAISS
    └── media/video/           # Video scaricati
```

## 🔧 Configurazione

Modifica `config/settings.yaml` per personalizzare:

```yaml
visual:
  sampling_mode: "scene"     # "scene" | "fps"
  fps: 0.5                   # FPS per sampling fisso
  scene_threshold: 0.4       # Soglia rilevamento scene
  max_frames: 40             # Max frame per video

ocr:
  enabled: true
  langs: ["it","en"]         # Lingue OCR

vision:
  clip_model: "clip-ViT-B-32"
  batch_size: 32
  use_gpu_faiss: false       # GPU per FAISS
```

## 🎯 Comandi Principali

### Setup e Demo
```bash
make setup              # Virtual environment + dipendenze
make multimodal-demo    # Demo completa con frame finti
make test              # Test unitari
```

### Indici
```bash
make visual-index      # Indice visivo (CLIP)
make index-cpu         # Indice testuale (CPU)
make index-gpu         # Indice testuale (GPU)
```

### Pipeline Completa
```bash
# Per un video specifico
make download URL="https://tiktok.com/@user/video/123"
make pipeline URL="https://tiktok.com/@user/video/123"
```

### Utility
```bash
make clean             # Pulisce file generati
make help              # Mostra tutti i comandi
```

## 🎬 Funzionalità Multimodali

### 1. Estrazione Frame
- **Scene Detection**: Estrae frame quando cambia la scena
- **FPS Fisso**: Estrae frame a intervalli regolari
- **Resize Automatico**: Ridimensiona per ottimizzare CLIP

### 2. OCR (EasyOCR)
- **Multi-lingua**: Italiano + Inglese
- **Testo Combinato**: Unisce testo di tutti i frame
- **JSON Output**: Risultati strutturati

### 3. Embedding Visivi (CLIP)
- **CLIP ViT-B-32**: Modello bilanciato velocità/qualità
- **Pooling**: Media degli embedding dei frame
- **GPU/CPU**: Fallback automatico

### 4. Indici FAISS
- **Testuale**: Include OCR nel corpus di ricerca
- **Visivo**: Embedding CLIP per ricerca per similarità
- **Unificato**: Ricerca cross-modale

## 🔍 Ricerca

La ricerca ora include:
- **Testo trascritto** (Whisper)
- **Testo OCR** (EasyOCR)
- **Tag visivi** (CLIP)
- **Metadati** (titolo, hook, takeaways)

## 🧪 Test

```bash
# Test OCR
python -m pytest tests/test_ocr_and_frames.py -v

# Test CLIP
python -m pytest tests/test_vision_clip.py -v

# Tutti i test
make test
```

## 📊 Performance

- **OCR**: ~2-5s per video (CPU)
- **CLIP**: ~10-30s per video (GPU: ~5-15s)
- **Indici**: ~1-5s per 100 video
- **Ricerca**: <100ms per query

## 🛠️ Dipendenze

- **Core**: FastAPI, SQLite, PyYAML
- **Audio**: OpenAI Whisper, ffmpeg
- **Visual**: OpenCV, EasyOCR, Pillow
- **AI/ML**: SentenceTransformers, PyTorch, FAISS
- **Utility**: requests, python-dotenv

## 🚨 Note

- **GPU**: Opzionale ma raccomandato per CLIP
- **FFmpeg**: Richiesto per estrazione frame
- **yt-dlp**: Per download video
- **Spazio**: ~100MB per video (frame + embedding)

## 🔄 Workflow Tipico

1. **Setup**: `make setup`
2. **Demo**: `make multimodal-demo`
3. **Video Reale**: `make download URL="..."`
4. **Analisi**: `make pipeline URL="..."`
5. **Ricerca**: Implementa interfaccia di ricerca

---

**TokIntel** - Analisi intelligente di contenuti video multimodali 🎬🔍

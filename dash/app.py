"""
TokIntel Multimodal Dashboard
Dashboard Streamlit per ricerca multimodale (testo + visione)
"""

import streamlit as st

# Health check endpoint for E2E testing
if st.query_params.get("health") == "1":
    st.write("OK"); st.stop()

# Trigger search for E2E testing (without UI clicks)
if st.query_params.get("trigger_search") == "1":
    query = "e2e-smoke"
    try:
        # Call existing search pipeline
        results = search_by_text(query, alpha=0.6, top_k=5)
        if results:
            st.write("TRIGGER_OK")
        else:
            st.write("TRIGGER_EMPTY")
    except Exception as e:
        st.write(f"TRIGGER_ERROR: {str(e)}")
    st.stop()

import yaml
import json
import pathlib
import faiss
import sqlite3
import pandas as pd
from PIL import Image
import io
import base64
from typing import List, Dict, Optional
from enum import Enum
import html
from collections import Counter
import os
import time
import platform

# Feature Flags via environment variables
FF_DISABLE_CACHE = os.getenv("FF_DISABLE_CACHE", "0") == "1"
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "0"))  # 0 = infinito

# Sprint 3: Environment variables for testing and export
TI_PORT = int(os.getenv("TI_PORT", "8510"))
TI_AUTO_EXPORT = os.getenv("TI_AUTO_EXPORT", "0") == "1"
TI_EXPORT_DIR = os.getenv("TI_EXPORT_DIR", "exports")
USE_NUMPY_INDEX = os.getenv("TOKINTEL_USE_NUMPY_INDEX", "0") == "1"
EMBED_MODE = os.getenv("TOKINTEL_EMBEDDING_MODE", "default")

# Create directories
os.makedirs(TI_EXPORT_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Structured logging setup
import logging
from datetime import datetime
log_filename = f"logs/streamlit_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

if FF_DISABLE_CACHE:
    # wrapper no-op per usare la stessa API
    def cache_data(*args, **kwargs):
        def decorator(fn): return fn
        return decorator
    st_cache_data = cache_data
else:
    st_cache_data = st.cache_data

# Import TokIntel modules
import sys
sys.path.append('.')
from analyzer.search_multimodal import search_text, search_visual, combine_results
from analyzer.vision_clip import image_paths_to_embeddings, device_from_pref
from analyzer.index_faiss import build_text_index
from analyzer.build_visual_index import build_index

# Diagnostics helper
def db_info(path="data/db.sqlite"):
    """Get database file information"""
    try:
        sz = os.path.getsize(path)
        mt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(path)))
        return {"path": path, "size_mb": round(sz/1_048_576, 2), "modified": mt}
    except OSError:
        return {"path": path, "size_mb": 0, "modified": "n/a"}

def optimize_sqlite_connection(conn):
    """Apply SQLite performance optimizations for dashboard usage"""
    try:
        cur = conn.cursor()
        # WAL mode for better concurrency (reads don't block writes)
        cur.execute("PRAGMA journal_mode=WAL")
        # NORMAL sync for good balance between safety and performance
        cur.execute("PRAGMA synchronous=NORMAL")
        # Use memory for temp storage
        cur.execute("PRAGMA temp_store=MEMORY")
        # Optional: memory mapping for large databases (if OS supports it)
        try:
            cur.execute("PRAGMA mmap_size=30000000000")  # 30GB
        except sqlite3.OperationalError:
            pass  # Not supported on this system
        conn.commit()
    except Exception:
        # Fail silently - optimizations are optional
        pass

# Centralized Status System
class Status(Enum):
    OK = "ok"
    TIMEOUT = "timeout"
    SKIPPED = "skipped"
    ERROR = "error"
    PENDING = "pending"

_STATUS_META = {
    Status.OK.value:      {"emoji": "✅", "bg": "#12B886", "fg": "white", "title": "Elaborazione completata"},
    Status.TIMEOUT.value: {"emoji": "🟡", "bg": "#FAB005", "fg": "black", "title": "Timeout durante la trascrizione"},
    Status.SKIPPED.value: {"emoji": "🔵", "bg": "#228BE6", "fg": "white", "title": "Video saltato"},
    Status.ERROR.value:   {"emoji": "🔴", "bg": "#FA5252", "fg": "white", "title": "Errore di elaborazione"},
    Status.PENDING.value: {"emoji": "🟣", "bg": "#7048E8", "fg": "white", "title": "In coda / in corso"},
}

# Status ranking for intelligent sorting
_STATUS_RANK = {"error": 0, "pending": 1, "timeout": 2, "skipped": 3, "ok": 4}

def norm_status(raw: str) -> str:
    """Normalize status string to valid enum value with strong validation"""
    s = (raw or "").strip().lower()
    return s if s in _STATUS_META else Status.PENDING.value

def get_status_badge(status: str, small: bool = False) -> str:
    """Generate HTML badge for video status with robust escaping"""
    s = norm_status(status)
    meta = _STATUS_META.get(s, _STATUS_META[Status.PENDING.value])
    pad = "2px 6px" if small else "3px 8px"
    fs = "11px" if small else "12px"
    return (
        f'<span data-status="{html.escape(s)}" '
        f'style="display:inline-flex;align-items:center;gap:6px;'
        f'background:{meta["bg"]};color:{meta["fg"]};'
        f'border-radius:999px;padding:{pad};font-weight:600;'
        f'font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto;'
        f'font-size:{fs}" title="{html.escape(meta["title"])}">'
        f'{meta["emoji"]}<span style="letter-spacing:.2px;text-transform:uppercase;">{html.escape(s)}</span>'
        f'</span>'
    )

def render_title_with_status(title: str, status: str) -> str:
    """Render title with status badge safely"""
    safe_title = html.escape(title or "")
    return f'{get_status_badge(status)}&nbsp;&nbsp;<span>{safe_title}</span>'

def sort_videos(videos: List[Dict]) -> List[Dict]:
    """Sort videos by status priority (error/pending first) then by title with stable tie-breaker"""
    def key(v):
        s = norm_status(v.get("status"))
        title = (v.get("title") or "").lower()
        # Tie-breaker deterministico per evitare "saltelli" UI
        tb = v.get("id") or v.get("added_at") or 0
        return (_STATUS_RANK.get(s, 5), title, tb)
    return sorted(videos, key=key)

def get_state(key: str, default):
    """Get persistent state from session_state"""
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]

def safe_status(v): 
    """Safely get status with fallback"""
    return norm_status(v.get("status"))

def render_metrics(videos):
    """Render metrics with fail-soft handling"""
    counts = Counter(safe_status(v) for v in videos)
    cols = st.columns(len(_STATUS_META))
    for i, (status, meta) in enumerate(_STATUS_META.items()):
        with cols[i]:
            st.metric(f"{meta['emoji']} {status.upper()}", counts.get(status, 0))

def status_filter_ui(items: List[Dict]) -> List[str]:
    """Status filter UI with dynamic legend and persistence"""
    if not items:
        return []
    
    all_statuses = sorted({safe_status(i) for i in items})
    counts = Counter(safe_status(i) for i in items)
    
    # Get persistent state
    selected_status = get_state("selected_status", all_statuses)

    with st.container():
        st.caption("Filtra per stato")
        selected = st.multiselect(
            "Stati",
            options=all_statuses,
            default=selected_status,
            format_func=lambda s: f'{s} ({counts[s]})',
            label_visibility="collapsed",
        )
        
        # Persist selection
        st.session_state["selected_status"] = selected

        # Legenda compatta
        if all_statuses:
            st.markdown(
                " ".join(get_status_badge(s, small=True) + f' <sup>{counts[s]}</sup>' for s in all_statuses),
                unsafe_allow_html=True
            )
    return selected

# Page config
st.set_page_config(
    page_title="TokIntel Multimodal Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-box {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 0.25rem 0;
    }
    .result-card {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: white;
    }
    .thumbnail {
        max-width: 200px;
        border-radius: 0.25rem;
    }
    [data-status] { 
        transition: transform .08s ease; 
        cursor: pointer;
    }
    [data-status]:hover { 
        transform: translateY(-1px); 
        filter: brightness(1.02); 
    }
    [data-status]:focus { 
        outline: 2px solid rgba(125,125,255,.6); 
        outline-offset: 2px;
    }
</style>
""", unsafe_allow_html=True)

def _db_mtime(path: str) -> float:
    """Get database modification time for cache invalidation"""
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0

@st_cache_data(ttl=CACHE_TTL_SECONDS)
def load_config():
    """Load configuration from settings.yaml"""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@st_cache_data(show_spinner=False, ttl=CACHE_TTL_SECONDS)
def load_database_cached(db_path: str, _sig: float):
    """Load database with cache invalidation based on file modification time"""
    # Load and normalize
    con = sqlite3.connect(db_path)
    optimize_sqlite_connection(con)
    df = pd.read_sql_query("SELECT * FROM videos", con)
    con.close()
    
    # Normalize status
    def _norm(s): 
        s = (str(s or "")).strip().lower()
        return s if s in _STATUS_META else "pending"
    
    if "status" not in df.columns:
        df["status"] = "pending"
    df["status"] = df["status"].map(_norm)
    
    return df.to_dict(orient="records")

def load_database(db_path="data/db.sqlite"):
    """Load video database with cache invalidation"""
    cfg = load_config()
    db_path = cfg["database"]["path"]
    sig = _db_mtime(db_path)
    return load_database_cached(db_path, sig)

def load_database_df():
    """Load video database as DataFrame for export functionality"""

    cfg = load_config()
    db_path = cfg["database"]["path"]
    
    pathlib.Path("data").mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    optimize_sqlite_connection(con)
    cur = con.cursor()

    # Assicura tabelle minime
    cur.execute("""CREATE TABLE IF NOT EXISTS videos(
      id INTEGER PRIMARY KEY,
      collection_id TEXT, collection_name TEXT, url TEXT UNIQUE,
      title TEXT, author TEXT, duration_sec INTEGER,
      published_at TEXT, added_at TEXT DEFAULT CURRENT_TIMESTAMP,
      status TEXT DEFAULT 'ok'
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS insights(
      video_url TEXT PRIMARY KEY,
      topic_macro TEXT, topic_micro TEXT, hook TEXT,
      takeaways TEXT, tags TEXT, language TEXT,
      ocr_text TEXT,
      updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    con.commit()

    # Carica dati
    df_v = pd.read_sql_query("SELECT * FROM videos", con)
    try:
        df_i = pd.read_sql_query("SELECT * FROM insights", con)
    except Exception:
        # fallback: nessuna insights, crea df vuoto
        df_i = pd.DataFrame(columns=[
            "video_url","topic_macro","topic_micro","hook",
            "takeaways","tags","language","ocr_text","updated_at"
        ])

    # Merge
    df = df_v.merge(df_i, how="left", left_on="url", right_on="video_url")

    # Colonne di sicurezza
    for col in ["hook","topic_micro","tags","ocr_text"]:
        if col not in df.columns:
            df[col] = ""

    con.close()
    return df

def load_database():
    """Load video database with robust schema handling"""
    df = load_database_df()
    
    # Converti in formato compatibile con il resto del codice
    videos = []
    for _, row in df.iterrows():
        videos.append({
            "id": row.get("id", 0),
            "url": row.get("url", ""),
            "title": row.get("title", "No title"),
            "hook": row.get("hook", ""),
            "takeaways": row.get("takeaways", ""),
            "tags": row.get("tags", ""),
            "ocr_text": row.get("ocr_text", ""),
            "status": norm_status(row.get("status"))
        })
    
    return videos

def get_available_tags(videos: List[Dict]) -> List[str]:
    """Extract unique tags from videos"""
    tags = set()
    for video in videos:
        if video["tags"]:
            for tag in video["tags"].split(","):
                tags.add(tag.strip())
    return sorted(list(tags))

THUMBS_DIR = pathlib.Path("data/thumbnails")

def thumbnail_for_url(url: str) -> Optional[str]:
    """Get persistent thumbnail for a video URL"""
    # prova a mappare URL → id (ultima parte)
    vid = url.rstrip("/").split("/")[-1]
    jpg = THUMBS_DIR / f"{vid}.jpg"
    if jpg.exists():
        return str(jpg)
    return None

def get_frame_thumbnails(video_id: int, max_frames: int = 3) -> List[str]:
    """Get frame thumbnails for a video"""
    cfg = load_config()
    frames_dir = pathlib.Path(cfg["visual"]["frames_dir"])
    video_frames_dir = frames_dir / f"vid_{video_id:05d}"
    
    if not video_frames_dir.exists():
        return []
    
    frame_files = sorted(video_frames_dir.glob("*.jpg"))[:max_frames]
    thumbnails = []
    
    for frame_file in frame_files:
        try:
            img = Image.open(frame_file)
            img.thumbnail((200, 200))
            
            # Convert to base64 for display
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            thumbnails.append(f"data:image/jpeg;base64,{img_str}")
        except Exception as e:
            st.warning(f"Errore caricamento frame {frame_file}: {e}")
    
    return thumbnails

def search_by_text(query: str, alpha: float, top_k: int = 10) -> List[Dict]:
    """Perform text-based multimodal search"""
    cfg = load_config()
    
    # Determine device
    device = device_from_pref(cfg["compute"]["gpu_mode"])
    
    try:
        # Text search
        text_results = search_text(
            query,
            cfg["search"]["index_path"],
            cfg["search"]["map_path"],
            cfg["search"]["model"],
            device,
            top_k
        )
        
        # Visual search
        visual_results = search_visual(
            query,
            cfg["vision"]["image_index_path"],
            cfg["vision"]["image_map_path"],
            cfg["vision"]["clip_model"],
            device,
            top_k
        )
        
        # Combine results
        combined_results = combine_results(
            text_results, visual_results,
            weight_text=alpha, weight_visual=1-alpha
        )
        
        return combined_results[:top_k]
        
    except Exception as e:
        st.error(f"Errore durante la ricerca: {e}")
        return []

def search_by_image(uploaded_file, top_k: int = 10) -> List[Dict]:
    """Perform image-based visual search"""
    cfg = load_config()
    
    if uploaded_file is None:
        return []
    
    try:
        # Load image
        image = Image.open(uploaded_file)
        
        # Save temporarily
        temp_path = pathlib.Path("temp_upload.jpg")
        image.save(temp_path)
        
        # Generate embedding
        device = device_from_pref(cfg["compute"]["gpu_mode"])
        embedding = image_paths_to_embeddings(
            [str(temp_path)],
            cfg["vision"]["clip_model"],
            device,
            batch_size=1,
            normalize=True
        )
        
        # Load visual index
        index = faiss.read_index(cfg["vision"]["image_index_path"])
        with open(cfg["vision"]["image_map_path"], 'r', encoding='utf-8') as f:
            url_map = json.load(f)
        
        # Search
        scores, indices = index.search(embedding, min(top_k, index.ntotal))
        
        # Clean up
        temp_path.unlink(missing_ok=True)
        
        # Format results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:
                results.append({
                    "url": url_map[str(idx)],
                    "score": float(score),
                    "type": "visual"
                })
        
        return results
        
    except Exception as e:
        st.error(f"Errore durante la ricerca per immagine: {e}")
        return []

def rebuild_text_index():
    """Rebuild text index"""
    try:
        with st.spinner("Ricostruzione indice testuale..."):
            build_text_index(gpu_pref="auto")
        st.success("✅ Indice testuale ricostruito!")
    except Exception as e:
        st.error(f"Errore ricostruzione indice testuale: {e}")

def rebuild_visual_index():
    """Rebuild visual index"""
    try:
        with st.spinner("Ricostruzione indice visivo..."):
            # Get all videos from database
            videos = load_database()
            urls = [video["url"] for video in videos]
            
            if not urls:
                st.warning("Nessun video trovato nel database")
                return
            
            cfg = load_config()
            build_index(urls, cfg, gpu_pref="auto")
        st.success("✅ Indice visivo ricostruito!")
    except Exception as e:
        st.error(f"Errore ricostruzione indice visivo: {e}")

def display_results(results: List[Dict], videos: List[Dict], score_threshold: float = 0.0):
    """Display search results"""
    if not results:
        st.info("Nessun risultato trovato")
        return
    
    # Filter by score threshold
    filtered_results = [r for r in results if r.get("combined_score", r.get("score", 0)) >= score_threshold]
    
    if not filtered_results:
        st.info(f"Nessun risultato sopra la soglia di {score_threshold}")
        return
    
    # Create URL to video mapping
    url_to_video = {video["url"]: video for video in videos}
    
    for i, result in enumerate(filtered_results, 1):
        url = result["url"]
        video = url_to_video.get(url, {})
        
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Thumbnails - 1) thumb persistente se esiste; 2) fallback al frame dalla cartella frames
                preview = thumbnail_for_url(url)
                if not preview and video.get("id"):
                    thumbnails = get_frame_thumbnails(video["id"])
                    if thumbnails:
                        preview = thumbnails[0]
                
                if preview:
                    st.image(preview, caption="Thumbnail", use_column_width=True)
                else:
                    st.image("https://via.placeholder.com/200x150?text=No+Frame", 
                            caption="No frame", use_column_width=True)
            
            with col2:
                # Video info with status badge
                status = video.get('status', 'pending')
                st.markdown(render_title_with_status(f"{i}. {video.get('title', 'No title')}", status), unsafe_allow_html=True)
                st.markdown(f"**URL:** {url}")
                
                # Status indicator with new badge system
                st.markdown(f"**Stato:** {get_status_badge(status)}", unsafe_allow_html=True)
                
                # Scores
                if "combined_score" in result:
                    st.markdown(f"""
                    <div class="score-box">
                        <strong>Score Combinato:</strong> {result['combined_score']:.3f}<br>
                        <strong>Score Testuale:</strong> {result.get('text_score', 0):.3f}<br>
                        <strong>Score Visivo:</strong> {result.get('visual_score', 0):.3f}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="score-box">
                        <strong>Score:</strong> {result.get('score', 0):.3f}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Video details
                if video.get("hook"):
                    st.markdown(f"**Hook:** {video['hook']}")
                if video.get("takeaways"):
                    st.markdown(f"**Takeaways:** {video['takeaways']}")
                if video.get("tags"):
                    st.markdown(f"**Tags:** {video['tags']}")
                if video.get("ocr_text"):
                    with st.expander("OCR Text"):
                        st.text(video["ocr_text"][:500] + "..." if len(video["ocr_text"]) > 500 else video["ocr_text"])
        
        st.divider()

def main():
    """Main dashboard function"""
    st.markdown('<h1 class="main-header">🎬 TokIntel Multimodal Dashboard</h1>', unsafe_allow_html=True)
    
    # Diagnostics panel
    with st.expander("ℹ️ Diagnostics", expanded=False):
        info = db_info()
        st.write({
            "app_version": os.getenv("TOKINTEL_VERSION", "local"),
            "python": platform.python_version(),
            "streamlit": st.__version__,
            "db": info,
            "cache_enabled": not FF_DISABLE_CACHE,
            "cache_ttl": CACHE_TTL_SECONDS if CACHE_TTL_SECONDS > 0 else "∞",
        })
        if st.button("🔁 Forza refresh cache", on_click=lambda: st.cache_data.clear()):
            st.success("Cache invalidata!")
    
    # Load data
    cfg = load_config()
    videos = load_database()
    # Sort videos intelligently by status priority
    videos = sort_videos(videos)
    available_tags = get_available_tags(videos)
    
    # Status metrics overview - compact auto-layout with fail-soft
    if videos:
        render_metrics(videos)
    
    # Sidebar
    st.sidebar.title("🔧 Controlli")
    
    # Ingest 1-click section
    with st.sidebar:
        st.subheader("Ingest da Raccolta TikTok (1‑click)")
        default_url = "https://www.tiktok.com/@matteo_papetti/collection/IA-7503112747077372694"
        coll_url = st.text_input("URL raccolta pubblica", value=default_url)
        max_items = st.number_input("Max video", min_value=1, max_value=500, value=100, step=10)
        dl_limit = st.number_input("Limite download", min_value=0, max_value=500, value=50, step=10, help="0 = nessun limite")
        use_gpu = st.selectbox("GPU", options=["auto","on","off"], index=0)
        timeout_sec = st.number_input("Timeout trascrizione (sec)", min_value=0, max_value=600, value=120, step=30,
                                      help="0 = disattivato. Su Windows è 'soft timeout'.")
        audio_only = st.checkbox("Solo audio", value=False, 
                                 help="Modalità solo audio: salta OCR e analisi visiva, fa solo trascrizione")

        # Progress components
        progress_bar = st.progress(0)
        status_text = st.empty()
        thumbnail_placeholder = st.empty()
        
        if st.button("Esegui ingest 1‑click"):
            try:
                # Import the ingest function
                from scripts.ingest_collection import main as ingest_main
                
                # Define callback functions
                def progress_callback(step, total_steps):
                    progress = step / total_steps
                    progress_bar.progress(progress)
                
                def status_callback(message):
                    status_text.write(f"🔄 {message}")
                
                def thumbnail_callback(image):
                    if image:
                        thumbnail_placeholder.image(image, caption="Ultimo video processato", width=200)
                
                # Run ingest with callbacks
                with st.spinner("Ingest in corso..."):
                    ingest_main(
                        collection_url=coll_url,
                        max_items=int(max_items),
                        gpu_mode=use_gpu,
                        download_limit=dl_limit if dl_limit > 0 else None,
                        timeout_sec=int(timeout_sec),
                        audio_only=audio_only,
                        progress_callback=progress_callback,
                        status_callback=status_callback,
                        thumbnail_callback=thumbnail_callback
                    )
                
                # Success message
                progress_bar.progress(1.0)
                status_text.success("✅ Ingest completato! Ora puoi fare ricerche.")
                
            except Exception as e:
                st.error(f"Errore durante l'ingest: {e}")
                status_text.error("❌ Ingest fallito")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Ricerca Testuale", "🖼️ Ricerca da Immagine", "⚙️ Gestione Indici"])
    
    with tab1:
        st.header("🔍 Ricerca Testuale Multimodale")
        
        # Search controls
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Get persistent query
            query_text = get_state("query_text", "")
            query = st.text_input("Query di ricerca:", value=query_text, placeholder="Es: yoga breathing, marketing conversion...")
            # Persist query
            st.session_state["query_text"] = query
        
        with col2:
            alpha = st.slider("Peso Testo vs Visivo", 0.0, 1.0, 0.6, 0.1, 
                            help="0.0 = solo visivo, 1.0 = solo testo")
        
        with col3:
            top_k = st.number_input("Numero risultati", 1, 50, 10)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_tags = st.multiselect("Filtra per tag:", available_tags)
        
        with col2:
            score_threshold = st.slider("Soglia score minimo", 0.0, 1.0, 0.0, 0.1)
        
        with col3:
            selected_status = status_filter_ui(videos)
        
        # Search button
        if st.button("🔍 Cerca", type="primary"):
            if query.strip():
                # Sprint 3: Structured logging and auto-export
                import uuid
                import re
                from datetime import datetime
                
                query_id = str(uuid.uuid4())[:8]
                start_time = time.time()
                
                # Create slugified query for filename
                query_slug = re.sub(r'[^a-zA-Z0-9]', '_', query.strip())[:30]
                
                logger.info(f"Search started - query_id: {query_id}, query: '{query}', alpha: {alpha}, top_k: {top_k}")
                
                with st.spinner("Ricerca in corso..."):
                    results = search_by_text(query, alpha, top_k)
                    
                    # Filter by tags and status if selected
                    filtered_videos = videos
                    if selected_tags:
                        filtered_videos = [v for v in filtered_videos if any(tag in v.get("tags", "") for tag in selected_tags)]
                    if selected_status:
                        filtered_videos = [v for v in filtered_videos if norm_status(v.get("status")) in selected_status]
                    
                    video_urls = {v["url"] for v in filtered_videos}
                    results = [r for r in results if r["url"] in video_urls]
                    
                    # Arricchisci risultati con metadati per export
                    df_data = load_database_df()
                    export_rows = []
                    for rr in results:
                        row = df_data[df_data["url"] == rr["url"]].head(1)
                        export_rows.append({
                            "url": rr["url"],
                            "score_combined": round(rr.get("combined_score", rr.get("score", 0)), 4),
                            "text_score": round(rr.get("text_score", 0), 4),
                            "visual_score": round(rr.get("visual_score", 0), 4),
                            "title": "" if row.empty else (row["title"].iloc[0] or ""),
                            "author": "" if row.empty else (row["author"].iloc[0] or ""),
                            "topic_micro": "" if row.empty else (row["topic_micro"].iloc[0] or ""),
                            "hook": "" if row.empty else (row["hook"].iloc[0] or ""),
                            "tags": "" if row.empty else (row["tags"].iloc[0] or ""),
                            "ocr_text": "" if row.empty else ((row["ocr_text"].iloc[0] or "")[:500]),
                        })
                    st.session_state["last_results"] = export_rows
                    
                    display_results(results, videos, score_threshold)
                    
                    # Sprint 3: Structured logging and auto-export
                    end_time = time.time()
                    duration_ms = int((end_time - start_time) * 1000)
                    results_count = len(export_rows)
                    
                    logger.info(f"Search completed - query_id: {query_id}, duration_ms: {duration_ms}, results_count: {results_count}")
                    
                    # Auto-export if enabled
                    if TI_AUTO_EXPORT and export_rows:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        csv_filename = f"{timestamp}_{query_slug}.csv"
                        json_filename = f"{timestamp}_{query_slug}.json"
                        
                        csv_path = os.path.join(TI_EXPORT_DIR, csv_filename)
                        json_path = os.path.join(TI_EXPORT_DIR, json_filename)
                        
                        # CSV export
                        df_export = pd.DataFrame(export_rows)
                        df_export.to_csv(csv_path, index=False, encoding="utf-8")
                        
                        # JSON export
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(export_rows, f, ensure_ascii=False, indent=2)
                        
                        logger.info(f"Auto-export completed - query_id: {query_id}, csv: {csv_filename}, json: {json_filename}")
                        print(f"Search completed. Export saved to {csv_path} and {json_path}")
                    
                    # Export button
                    st.markdown("---")
                    if "last_results" in st.session_state and st.session_state["last_results"]:
                        df_export = pd.DataFrame(st.session_state["last_results"])
                        csv_bytes = df_export.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "⬇️ Esporta risultati (CSV)",
                            data=csv_bytes,
                            file_name="tokintel_search_results.csv",
                            mime="text/csv"
                        )
            else:
                st.warning("Inserisci una query di ricerca")
    
    with tab2:
        st.header("🖼️ Ricerca da Immagine")
        
        # Image upload
        uploaded_file = st.file_uploader(
            "Carica un'immagine (JPG/PNG):",
            type=['jpg', 'jpeg', 'png'],
            help="Carica un'immagine per trovare video simili"
        )
        
        if uploaded_file:
            # Display uploaded image
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image(uploaded_file, caption="Immagine caricata", use_column_width=True)
            
            with col2:
                top_k_img = st.number_input("Numero risultati immagine", 1, 50, 10, key="img_top_k")
                score_threshold_img = st.slider("Soglia score minimo", 0.0, 1.0, 0.0, 0.1, key="img_threshold")
                
                if st.button("🔍 Cerca Simili", type="primary"):
                    with st.spinner("Ricerca per similarità visiva..."):
                        results = search_by_image(uploaded_file, top_k_img)
                        display_results(results, videos, score_threshold_img)
    
    with tab3:
        st.header("⚙️ Gestione Indici")
        
        st.markdown("### 📊 Stato Indici")
        
        # Check index status
        text_index_exists = pathlib.Path(cfg["search"]["index_path"]).exists()
        visual_index_exists = pathlib.Path(cfg["vision"]["image_index_path"]).exists()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if text_index_exists:
                st.success("✅ Indice Testuale: Presente")
            else:
                st.error("❌ Indice Testuale: Mancante")
            
            if st.button("🔄 Ricostruisci Indice Testuale", type="secondary"):
                rebuild_text_index()
        
        with col2:
            if visual_index_exists:
                st.success("✅ Indice Visivo: Presente")
            else:
                st.error("❌ Indice Visivo: Mancante")
            
            if st.button("🔄 Ricostruisci Indice Visivo", type="secondary"):
                rebuild_visual_index()
        
        # Database info
        st.markdown("### 📁 Informazioni Database")
        st.info(f"Video nel database: {len(videos)}")
        
        # Export with status
        if videos:
            st.markdown("### 📤 Export Dati")
            col1, col2 = st.columns(2)
            
            with col1:
                # Export CSV with timestamp
                ts = time.strftime("%Y%m%d_%H%M%S")
                df_export = pd.DataFrame(videos)
                csv_bytes = df_export.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Export CSV con Stati",
                    data=csv_bytes,
                    file_name=f"tokintel_videos_{ts}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Export JSON with timestamp
                import json
                json_bytes = json.dumps(videos, ensure_ascii=False, indent=2).encode("utf-8")
                st.download_button(
                    "⬇️ Export JSON con Stati",
                    data=json_bytes,
                    file_name=f"tokintel_videos_{ts}.json",
                    mime="application/json"
                )
            
            with st.expander("📋 Lista Video"):
                for video in videos[:10]:  # Show first 10
                    st.markdown(f"**{video['title']}** - {video['url']}")
                if len(videos) > 10:
                    st.markdown(f"... e altri {len(videos) - 10} video")
    
    # Footer
    st.markdown("---")
    st.markdown("🎬 **TokIntel** - Dashboard Multimodale per Analisi Video")

# Sprint 3: Health check endpoint for E2E tests
if st.query_params.get("health") == "1":
    st.write("OK")

if __name__ == "__main__":
    main()

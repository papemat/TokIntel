import os, json
from pathlib import Path
import pandas as pd
import streamlit as st

# Fail-soft import per matplotlib
try:
    import matplotlib.pyplot as plt
except ImportError:
    st.error("""
    **Matplotlib non è installato.** 
    
    Esegui:
    ```bash
    pip install matplotlib
    ```
    
    Oppure:
    ```bash
    pip install -r requirements.txt
    ```
    """)
    st.stop()

st.set_page_config(page_title="TokIntel – Performance Trends", layout="wide")

st.title("📈 TokIntel – Performance Trends")
st.caption("Storico dei benchmark generati da perf_bench.py (nightly e locali).")

reports_dir = Path(st.text_input("Reports directory", value="reports"))
history_csv = reports_dir / "perf_history.csv"

def load_history():
    if history_csv.exists():
        df = pd.read_csv(history_csv)
    else:
        # fallback: aggrega al volo dai JSON locali
        js_files = sorted(reports_dir.glob("perf_*.json"))
        data = []
        for js in js_files:
            d = json.loads(js.read_text(encoding="utf-8"))
            meta = d.get("meta", {})
            perf = d.get("perf", {})
            data.append({
                "ts": meta.get("ts"),
                "videos_count": perf.get("videos_count"),
                "add_indexes_ms": perf.get("add_indexes_ms"),
                "sql_read_500": perf.get("sql_read_500"),
                "export_csv": perf.get("export_csv"),
                "export_json": perf.get("export_json"),
            })
        df = pd.DataFrame(data)
    if not df.empty and "ts" in df.columns:
        df = df.sort_values("ts").reset_index(drop=True)
    return df

df = load_history()
if df.empty:
    st.warning("Nessun dato trovato. Esegui il nightly o genera report locali (perf_bench.py).")
    st.stop()

st.subheader("Overview")
st.dataframe(df.tail(20), use_container_width=True)

def plot_metric(df, col, title):
    fig, ax = plt.subplots()
    ax.plot(df["ts"], df[col], marker="o")
    ax.set_title(title)
    ax.set_xlabel("timestamp")
    ax.set_ylabel("ms")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

col1, col2 = st.columns(2)
with col1: plot_metric(df, "sql_read_500", "SQL read 500 (ms)")
with col2: plot_metric(df, "add_indexes_ms", "Add indexes (ms)")

col3, col4 = st.columns(2)
with col3: plot_metric(df, "export_csv", "Export CSV (ms)")
with col4: plot_metric(df, "export_json", "Export JSON (ms)")

st.caption("Suggerimento: usa `FF_DISABLE_CACHE=1` per debug live di performance.")

from __future__ import annotations
import argparse
import json
import pathlib
import sqlite3
import yaml

def load_cfg():
    """Load configuration from settings.yaml"""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_insights_columns():
    """Ensure insights table has required columns for multimodal data"""
    con = sqlite3.connect("data/db.sqlite")
    cur = con.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS insights(
      video_url TEXT PRIMARY KEY,
      topic_macro TEXT, topic_micro TEXT, hook TEXT,
      takeaways TEXT, tags TEXT, language TEXT,
      ocr_text TEXT,
      updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # aggiungi colonna ocr_text se manca
    try:
        cur.execute("ALTER TABLE insights ADD COLUMN ocr_text TEXT")
    except Exception:
        pass  # Column already exists
    
    con.commit()
    con.close()

def fuse_ocr_into_extended():
    """Fuse OCR data into extended text for better search"""
    # qui non scriviamo un nuovo campo; sfruttiamo ocr_text e il patch di index_faiss (che lo include).
    pass

def main():
    """Main function for multimodal setup"""
    ensure_insights_columns()
    print("✓ Schema pronto per multimodale (OCR).")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Add database indexes for better performance with column existence checks
"""

import sqlite3
import yaml
import pathlib
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def column_exists(cur, table, col):
    """Check if a column exists in a table"""
    cur.execute(f"PRAGMA table_info({table})")
    return any(r[1].lower() == col.lower() for r in cur.fetchall())

def index_exists(cur, name):
    """Check if an index already exists"""
    cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND name=?", (name,))
    return cur.fetchone() is not None

def add_database_indexes():
    """Add indexes to database for better performance with column checks"""
    
    # Load config
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    db_path = cfg["database"]["path"]
    db_file = pathlib.Path(db_path)
    
    if not db_file.exists():
        print(f"[skip] DB non trovato: {db_path}")
        return 0
    
    print("🔄 Aggiunta indici database per performance...")
    
    # Ensure data directory exists
    pathlib.Path("data").mkdir(parents=True, exist_ok=True)
    
    # Connect to database
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # Define indexes to add with table and column info
    INDEX_PLAN = [
        ("idx_videos_status", "videos", "status"),
        ("idx_videos_title", "videos", "title"),
        ("idx_videos_url", "videos", "url"),
        ("idx_videos_added_at", "videos", "added_at"),  # opzionale
        ("idx_videos_collid", "videos", "collection_id"),  # opzionale
        ("idx_insights_video_url", "insights", "video_url"),
    ]
    
    added_count = 0
    for index_name, table, column in INDEX_PLAN:
        # Check if column exists
        if not column_exists(cur, table, column):
            print(f"[skip] {index_name}: colonna {table}.{column} assente")
            continue
        
        # Check if index already exists
        if index_exists(cur, index_name):
            print(f"[ok]   {index_name} già presente")
            continue
        
        # Create index
        try:
            cur.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table}({column})")
            print(f"[new]  creato {index_name} su {table}({column})")
            added_count += 1
        except Exception as e:
            print(f"[err]  errore creazione {index_name}: {e}")
    
    # Commit changes
    con.commit()
    con.close()
    
    print(f"✅ Operazione completata. Aggiunti {added_count} nuovi indici.")
    
    # Show database info
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # Count videos
    cur.execute("SELECT COUNT(*) FROM videos")
    video_count = cur.fetchone()[0]
    
    # Count by status
    cur.execute("SELECT status, COUNT(*) FROM videos GROUP BY status")
    status_counts = dict(cur.fetchall())
    
    print("\n📊 Database info:")
    print(f"  Video totali: {video_count}")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
    
    con.close()
    return 0

if __name__ == "__main__":
    sys.exit(add_database_indexes())

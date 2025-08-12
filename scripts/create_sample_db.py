#!/usr/bin/env python3
"""
Script per creare un database di test con video che hanno stati diversi
per testare i badge di stato nella dashboard.
"""

import sqlite3
import pathlib
import yaml
import argparse
import sys
from datetime import datetime, timedelta

def create_sample_database(staging=False, large=False):
    """Crea un database di test con video con stati diversi"""
    
    # Carica configurazione
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    if staging:
        db_path = "data/staging_db.sqlite"
        print("🔧 Modalità staging: usando data/staging_db.sqlite")
    else:
        db_path = cfg["database"]["path"]
    
    if large:
        print("📊 Modalità large: creando dataset esteso per performance test")
    
    # Assicura che la directory esista
    pathlib.Path("data").mkdir(parents=True, exist_ok=True)
    
    # Connessione al database
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # Crea tabelle se non esistono
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
    
    # Pulisci dati esistenti
    cur.execute("DELETE FROM insights")
    cur.execute("DELETE FROM videos")
    
    # Dati di test con stati diversi
    base_videos = [
        {
            "id": 1,
            "collection_id": "test_collection_1",
            "collection_name": "Test Collection",
            "url": "https://www.tiktok.com/@test_user/video/1234567890123456789",
            "title": "Yoga Breathing Techniques for Beginners",
            "author": "yoga_master",
            "duration_sec": 45,
            "published_at": "2024-01-15T10:30:00Z",
            "status": "ok",
            "hook": "Respirazione profonda per ridurre lo stress",
            "takeaways": "Tecniche di respirazione, riduzione stress, benessere",
            "tags": "yoga,breathing,wellness,stress-relief",
            "language": "it",
            "ocr_text": "Respirazione profonda per ridurre lo stress. Inspira lentamente dal naso..."
        },
        {
            "id": 2,
            "collection_id": "test_collection_1",
            "collection_name": "Test Collection",
            "url": "https://www.tiktok.com/@test_user/video/1234567890123456790",
            "title": "Marketing Conversion Strategies",
            "author": "marketing_expert",
            "duration_sec": 120,
            "published_at": "2024-01-16T14:20:00Z",
            "status": "timeout",
            "hook": "Strategie per aumentare le conversioni",
            "takeaways": "Marketing, conversioni, strategie digitali",
            "tags": "marketing,conversion,digital-strategy",
            "language": "it",
            "ocr_text": "Strategie per aumentare le conversioni. Il primo passo è..."
        },
        {
            "id": 3,
            "collection_id": "test_collection_1",
            "collection_name": "Test Collection",
            "url": "https://www.tiktok.com/@test_user/video/1234567890123456791",
            "title": "Pilates Core Workout",
            "author": "fitness_trainer",
            "duration_sec": 60,
            "published_at": "2024-01-17T09:15:00Z",
            "status": "skipped",
            "hook": "Allenamento core con Pilates",
            "takeaways": "Pilates, core, fitness, allenamento",
            "tags": "pilates,core,fitness,workout",
            "language": "it",
            "ocr_text": "Allenamento core con Pilates. Inizia in posizione supina..."
        },
        {
            "id": 4,
            "collection_id": "test_collection_2",
            "collection_name": "Another Test Collection",
            "url": "https://www.tiktok.com/@test_user/video/1234567890123456792",
            "title": "Healthy Breakfast Ideas",
            "author": "nutrition_coach",
            "duration_sec": 90,
            "published_at": "2024-01-18T08:00:00Z",
            "status": "ok",
            "hook": "Idee per una colazione sana e nutriente",
            "takeaways": "Nutrizione, colazione, salute, ricette",
            "tags": "nutrition,breakfast,health,recipes",
            "language": "it",
            "ocr_text": "Idee per una colazione sana e nutriente. Inizia con..."
        },
        {
            "id": 5,
            "collection_id": "test_collection_2",
            "collection_name": "Another Test Collection",
            "url": "https://www.tiktok.com/@test_user/video/1234567890123456793",
            "title": "Productivity Tips for Remote Work",
            "author": "productivity_guru",
            "duration_sec": 180,
            "published_at": "2024-01-19T11:45:00Z",
            "status": "timeout",
            "hook": "Consigli per aumentare la produttività nel lavoro remoto",
            "takeaways": "Produttività, lavoro remoto, organizzazione",
            "tags": "productivity,remote-work,organization",
            "language": "it",
            "ocr_text": "Consigli per aumentare la produttività nel lavoro remoto. Il primo consiglio è..."
        }
    ]
    
    # Espandi dataset per performance test
    if large:
        print("🔄 Espandendo dataset per performance test...")
        sample_videos = []
        for i in range(50):  # 50x più dati per stress test
            for base_video in base_videos:
                video_copy = base_video.copy()
                video_copy["id"] = len(sample_videos) + 1
                video_copy["url"] = f"{base_video['url']}_clone_{i}"
                video_copy["title"] = f"{base_video['title']} (Clone {i})"
                video_copy["collection_id"] = f"perf_test_collection_{i % 5}"
                video_copy["collection_name"] = f"Performance Test Collection {i % 5}"
                sample_videos.append(video_copy)
    else:
        sample_videos = base_videos
    
    # Inserisci video
    for video in sample_videos:
        cur.execute("""
            INSERT INTO videos (
                id, collection_id, collection_name, url, title, author, 
                duration_sec, published_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            video["id"], video["collection_id"], video["collection_name"],
            video["url"], video["title"], video["author"],
            video["duration_sec"], video["published_at"], video["status"]
        ))
        
        # Inserisci insights
        cur.execute("""
            INSERT INTO insights (
                video_url, topic_macro, topic_micro, hook, takeaways, 
                tags, language, ocr_text
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            video["url"], "Test Topic", video["title"], video["hook"],
            video["takeaways"], video["tags"], video["language"], video["ocr_text"]
        ))
    
    # Commit e chiudi
    con.commit()
    con.close()
    
    print(f"✅ Database di test creato con {len(sample_videos)} video")
    
    if large:
        print("📊 Dataset esteso per performance test:")
        print(f"  📈 {len(sample_videos)} video totali")
        print(f"  🗂️  {len(set(v['collection_id'] for v in sample_videos))} collezioni")
        print("  ⚡ Pronto per stress test di caching e performance")
    else:
        print("📊 Distribuzione stati:")
        print("  🟢 OK: 2 video")
        print("  🟡 TIMEOUT: 2 video") 
        print("  🔵 SKIPPED: 1 video")
    
    if staging:
        print(f"\n🔧 Database staging salvato in: {db_path}")
    else:
        print("\n🚀 Ora puoi testare i badge con: make dash")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crea database di test per TokIntel")
    parser.add_argument("--staging", action="store_true", help="Crea database di staging")
    parser.add_argument("--large", action="store_true", help="Crea dataset esteso per performance test")
    args = parser.parse_args()
    
    create_sample_database(staging=args.staging, large=args.large)

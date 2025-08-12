#!/usr/bin/env python3
"""
Script di migrazione automatica dello schema TokIntel
Gestisce la compatibilità tra vecchi e nuovi schemi del database
"""

import sqlite3
import pathlib
import sys
from typing import Optional

def migrate_schema(db_path: str = "data/db.sqlite") -> bool:
    """
    Migra automaticamente lo schema del database per compatibilità
    """
    print(f"🔄 Migrazione schema per: {db_path}")
    
    # Assicura directory esiste
    pathlib.Path("data").mkdir(parents=True, exist_ok=True)
    
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        # 1. Crea tabella videos se non esiste
        print("  📋 Verifica tabella videos...")
        cur.execute("""CREATE TABLE IF NOT EXISTS videos(
          id INTEGER PRIMARY KEY,
          collection_id TEXT, collection_name TEXT, url TEXT UNIQUE,
          title TEXT, author TEXT, duration_sec INTEGER,
          published_at TEXT, added_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        
        # 2. Crea tabella insights se non esiste
        print("  📋 Verifica tabella insights...")
        cur.execute("""CREATE TABLE IF NOT EXISTS insights(
          video_url TEXT PRIMARY KEY,
          topic_macro TEXT, topic_micro TEXT, hook TEXT,
          takeaways TEXT, tags TEXT, language TEXT,
          ocr_text TEXT,
          updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        
        # 3. Migra dati da ocr_data a insights se necessario
        print("  🔄 Verifica migrazione OCR data...")
        try:
            # Controlla se esiste ocr_data
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ocr_data'")
            ocr_data_exists = cur.fetchone() is not None
            
            if ocr_data_exists:
                print("    📥 Trovata tabella ocr_data, migrazione in corso...")
                
                # Migra dati da ocr_data a insights
                cur.execute("""
                    INSERT OR IGNORE INTO insights (video_url, ocr_text)
                    SELECT v.url, o.combined_text
                    FROM ocr_data o
                    JOIN videos v ON o.video_id = v.id
                    WHERE o.combined_text IS NOT NULL AND o.combined_text != ''
                """)
                
                migrated_count = cur.rowcount
                print(f"    ✅ Migrati {migrated_count} record OCR")
                
                # Opzionale: rimuovi ocr_data dopo migrazione
                # cur.execute("DROP TABLE ocr_data")
                # print("    🗑️  Tabella ocr_data rimossa")
                
        except Exception as e:
            print(f"    ⚠️  Nessuna migrazione OCR necessaria: {e}")
        
        # 4. Crea vista compatibile se richiesta
        print("  🔄 Verifica vista compatibilità...")
        try:
            cur.execute("""
                CREATE VIEW IF NOT EXISTS ocr_data AS 
                SELECT video_url AS url, ocr_text AS text 
                FROM insights 
                WHERE ocr_text IS NOT NULL AND ocr_text != ''
            """)
            print("    ✅ Vista ocr_data creata per compatibilità")
        except Exception as e:
            print(f"    ⚠️  Vista già esistente: {e}")
        
        # 5. Aggiungi colonne mancanti se necessario
        print("  🔄 Verifica colonne mancanti...")
        try:
            # Controlla colonne in videos
            cur.execute("PRAGMA table_info(videos)")
            columns = [col[1] for col in cur.fetchall()]
            
            # Colonne da aggiungere se mancanti
            missing_columns = []
            if 'collection_id' not in columns:
                missing_columns.append("collection_id TEXT")
            if 'collection_name' not in columns:
                missing_columns.append("collection_name TEXT")
            if 'author' not in columns:
                missing_columns.append("author TEXT")
            if 'duration_sec' not in columns:
                missing_columns.append("duration_sec INTEGER")
            if 'published_at' not in columns:
                missing_columns.append("published_at TEXT")
            if 'hook' not in columns:
                missing_columns.append("hook TEXT")
            if 'takeaways' not in columns:
                missing_columns.append("takeaways TEXT")
            if 'tags' not in columns:
                missing_columns.append("tags TEXT")
            if 'status' not in columns:
                missing_columns.append("status TEXT DEFAULT 'ok'")
            
            # Aggiungi colonne mancanti
            for col_def in missing_columns:
                col_name = col_def.split()[0]
                cur.execute(f"ALTER TABLE videos ADD COLUMN {col_def}")
                print(f"    ✅ Aggiunta colonna {col_name} a videos")
                
        except Exception as e:
            print(f"    ⚠️  Verifica colonne: {e}")
        
        con.commit()
        con.close()
        
        print("✅ Migrazione schema completata con successo!")
        return True
        
    except Exception as e:
        print(f"❌ Errore durante migrazione: {e}")
        return False

def verify_schema(db_path: str = "data/db.sqlite") -> bool:
    """
    Verifica che lo schema sia corretto
    """
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        # Verifica tabelle essenziali
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('videos', 'insights')")
        tables = [row[0] for row in cur.fetchall()]
        
        if len(tables) < 2:
            print(f"❌ Tabelle mancanti: {tables}")
            return False
        
        # Verifica colonne essenziali
        cur.execute("PRAGMA table_info(videos)")
        video_columns = [col[1] for col in cur.fetchall()]
        
        cur.execute("PRAGMA table_info(insights)")
        insight_columns = [col[1] for col in cur.fetchall()]
        
        required_video_cols = ['id', 'url', 'title']
        required_insight_cols = ['video_url', 'ocr_text']
        
        missing_video = [col for col in required_video_cols if col not in video_columns]
        missing_insight = [col for col in required_insight_cols if col not in insight_columns]
        
        if missing_video or missing_insight:
            print(f"❌ Colonne mancanti - videos: {missing_video}, insights: {missing_insight}")
            return False
        
        con.close()
        print("✅ Schema verificato correttamente!")
        return True
        
    except Exception as e:
        print(f"❌ Errore verifica schema: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        success = verify_schema()
        sys.exit(0 if success else 1)
    else:
        success = migrate_schema()
        if success:
            verify_schema()
        sys.exit(0 if success else 1)

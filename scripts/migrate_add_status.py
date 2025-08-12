#!/usr/bin/env python3
"""
Script di migrazione per aggiungere colonna status al database videos
"""

import sqlite3
import yaml
import sys
from pathlib import Path

def load_config():
    """Carica configurazione"""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def migrate_database():
    """Aggiunge colonna status se non esiste"""
    print("🔄 Migrazione database: aggiunta colonna status...")
    
    cfg = load_config()
    db_path = cfg["database"]["path"]
    
    # Assicura che la directory esista
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    try:
        # Controlla se la colonna status esiste già
        cur.execute("PRAGMA table_info(videos)")
        columns = [col[1] for col in cur.fetchall()]
        
        if "status" in columns:
            print("✅ Colonna 'status' già presente nel database")
            return True
        
        # Aggiungi colonna status con default 'ok'
        print("📝 Aggiunta colonna 'status' alla tabella videos...")
        cur.execute("ALTER TABLE videos ADD COLUMN status TEXT DEFAULT 'ok'")
        
        # Aggiorna tutti i record esistenti a 'ok'
        cur.execute("UPDATE videos SET status = 'ok' WHERE status IS NULL")
        
        # Commit delle modifiche
        con.commit()
        
        # Verifica
        cur.execute("SELECT COUNT(*) FROM videos")
        total_videos = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM videos WHERE status = 'ok'")
        ok_videos = cur.fetchone()[0]
        
        print(f"✅ Migrazione completata!")
        print(f"   - Totale video: {total_videos}")
        print(f"   - Video con status 'ok': {ok_videos}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante la migrazione: {e}")
        con.rollback()
        return False
    finally:
        con.close()

def main():
    """Funzione principale"""
    print("🚀 Migrazione Database TokIntel")
    print("=" * 40)
    
    success = migrate_database()
    
    if success:
        print("\n🎉 Migrazione completata con successo!")
        sys.exit(0)
    else:
        print("\n❌ Migrazione fallita!")
        sys.exit(1)

if __name__ == "__main__":
    main()

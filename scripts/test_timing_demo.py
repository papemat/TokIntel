#!/usr/bin/env python3
"""
Script di demo per testare il sistema di timing dell'ingest.
Simula un ingest completo con timing di ogni step.
"""

import sys
import time
import logging

# Aggiungi il path del progetto per gli import
sys.path.append('.')

from utils.logging_setup import setup_logging
from utils.timing import timed_step, timed_ingest

# Setup logging
setup_logging()
log = logging.getLogger('tokintel.ingest')


def simulate_ingest():
    """Simula un ingest completo con timing"""
    
    with timed_ingest(log):
        # Step 1: Raccolta URL
        with timed_step(log, "Raccolta URL"):
            log.info("Scraping TikTok collection...")
            time.sleep(2.5)  # Simula scraping
            log.info("Trovati 50 video nella collezione")
        
        # Step 2: Download video
        with timed_step(log, "Download video"):
            log.info("Iniziando download di 50 video...")
            for i in range(5):  # Simula download di 5 video
                time.sleep(0.8)
                log.info(f"Download completato: video {i+1}/5")
        
        # Step 3: Estrazione frame e OCR
        with timed_step(log, "Estrazione frame e OCR"):
            log.info("Estraendo frame da video...")
            time.sleep(8.2)  # Simula estrazione frame
            log.info("Applicando OCR...")
            time.sleep(3.1)  # Simula OCR
            log.info("Estratti 150 frame con OCR")
        
        # Step 4: Trascrizione audio
        with timed_step(log, "Trascrizione audio"):
            log.info("Trascrivendo audio con Whisper...")
            time.sleep(12.7)  # Simula trascrizione
            log.info("Trascritti 50 file audio")
        
        # Step 5: Costruzione indice testuale
        with timed_step(log, "Costruzione indice testuale"):
            log.info("Costruendo indice FAISS...")
            time.sleep(4.3)  # Simula costruzione indice
            log.info("Indice testuale completato")


def simulate_fast_ingest():
    """Simula un ingest veloce"""
    
    with timed_ingest(log):
        # Step 1: Raccolta URL
        with timed_step(log, "Raccolta URL"):
            log.info("Scraping TikTok collection...")
            time.sleep(0.5)
            log.info("Trovati 10 video nella collezione")
        
        # Step 2: Download video
        with timed_step(log, "Download video"):
            log.info("Iniziando download di 10 video...")
            for i in range(3):
                time.sleep(0.2)
                log.info(f"Download completato: video {i+1}/3")
        
        # Step 3: Estrazione frame e OCR
        with timed_step(log, "Estrazione frame e OCR"):
            log.info("Estraendo frame da video...")
            time.sleep(1.5)
            log.info("Applicando OCR...")
            time.sleep(0.8)
            log.info("Estratti 30 frame con OCR")
        
        # Step 4: Trascrizione audio
        with timed_step(log, "Trascrizione audio"):
            log.info("Trascrivendo audio con Whisper...")
            time.sleep(2.1)
            log.info("Trascritti 10 file audio")
        
        # Step 5: Costruzione indice testuale
        with timed_step(log, "Costruzione indice testuale"):
            log.info("Costruendo indice FAISS...")
            time.sleep(0.9)
            log.info("Indice testuale completato")


def simulate_slow_ingest():
    """Simula un ingest lento"""
    
    with timed_ingest(log):
        # Step 1: Raccolta URL
        with timed_step(log, "Raccolta URL"):
            log.info("Scraping TikTok collection...")
            time.sleep(5.2)
            log.info("Trovati 100 video nella collezione")
        
        # Step 2: Download video
        with timed_step(log, "Download video"):
            log.info("Iniziando download di 100 video...")
            for i in range(10):
                time.sleep(1.5)
                log.info(f"Download completato: video {i+1}/10")
        
        # Step 3: Estrazione frame e OCR
        with timed_step(log, "Estrazione frame e OCR"):
            log.info("Estraendo frame da video...")
            time.sleep(25.7)
            log.info("Applicando OCR...")
            time.sleep(18.3)
            log.info("Estratti 300 frame con OCR")
        
        # Step 4: Trascrizione audio
        with timed_step(log, "Trascrizione audio"):
            log.info("Trascrivendo audio con Whisper...")
            time.sleep(45.2)
            log.info("Trascritti 100 file audio")
        
        # Step 5: Costruzione indice testuale
        with timed_step(log, "Costruzione indice testuale"):
            log.info("Costruendo indice FAISS...")
            time.sleep(12.8)
            log.info("Indice testuale completato")


def main():
    """Main function per eseguire i test di timing"""
    print("🧪 Test Sistema Timing TokIntel")
    print("=" * 50)
    
    # Test 1: Ingest normale
    print("\n1️⃣ Test Ingest Normale:")
    simulate_ingest()
    
    time.sleep(2)
    
    # Test 2: Ingest veloce
    print("\n2️⃣ Test Ingest Veloce:")
    simulate_fast_ingest()
    
    time.sleep(2)
    
    # Test 3: Ingest lento
    print("\n3️⃣ Test Ingest Lento:")
    simulate_slow_ingest()
    
    print("\n✅ Tutti i test completati!")
    print("Controlla i log per vedere le durate colorate nella dashboard.")


if __name__ == "__main__":
    main()

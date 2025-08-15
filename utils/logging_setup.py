import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    """
    Configura il sistema di logging per TokIntel con rotazione automatica.
    
    - Percorso: ~/.tokintel/logs/ingest.log
    - Rotazione: max 2MB, 3 backup
    - Livello: da variabile d'ambiente LOG_LEVEL (default: INFO)
    """
    # Crea la directory dei log se non esiste
    log_dir = Path.home() / ".tokintel" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "ingest.log"
    
    # Determina il livello di log dalla variabile d'ambiente
    log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    # Configura il logger root
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Rimuovi handler esistenti per evitare duplicati
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Handler per file con rotazione
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=2*1024*1024,  # 2MB
        backupCount=3,
        encoding='utf-8'
    )
    
    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Handler per console (solo per DEBUG)
    if log_level <= logging.DEBUG:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    logger.addHandler(file_handler)
    
    # Log di avvio
    logger.info(f"Logging system initialized - Level: {log_level_str}, File: {log_file}")
    
    return logger


def get_logger(name='tokintel'):
    """
    Restituisce un logger configurato per il modulo specificato.
    
    Args:
        name (str): Nome del logger/modulo
        
    Returns:
        logging.Logger: Logger configurato
    """
    return logging.getLogger(name)

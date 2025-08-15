from pathlib import Path
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = Path.home() / ".tokintel" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
INGEST_LOG = LOG_DIR / "ingest.log"

_configured = False

def setup_logging():
    global _configured
    if _configured:
        return INGEST_LOG
    
    # Get log level from environment variable
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    log_level = log_level_map.get(log_level_str, logging.INFO)
    
    logger = logging.getLogger("tokintel.ingest")
    logger.setLevel(log_level)
    # Evita doppie linee se già configurato
    if not any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        handler = RotatingFileHandler(INGEST_LOG, maxBytes=2_000_000, backupCount=3, encoding="utf-8")
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    _configured = True
    return INGEST_LOG

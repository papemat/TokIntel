from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = Path.home() / ".tokintel" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
INGEST_LOG = LOG_DIR / "ingest.log"

_configured = False

def setup_logging():
    global _configured
    if _configured:
        return INGEST_LOG
    logger = logging.getLogger("tokintel.ingest")
    logger.setLevel(logging.INFO)
    # Evita doppie linee se già configurato
    if not any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        handler = RotatingFileHandler(INGEST_LOG, maxBytes=2_000_000, backupCount=3, encoding="utf-8")
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    _configured = True
    return INGEST_LOG

import time
from contextlib import contextmanager
from typing import Optional


@contextmanager
def timed_step(logger, step_name: str):
    """
    Context manager per misurare la durata di un singolo step dell'ingest.
    
    Args:
        logger: Logger instance per loggare i messaggi
        step_name: Nome descrittivo dello step
    
    Yields:
        None
        
    Example:
        with timed_step(log, "Raccolta URL"):
            # codice dello step
            pass
    """
    start = time.time()
    logger.info(f"⏳ Iniziando: {step_name}")
    try:
        yield
    finally:
        elapsed = time.time() - start
        logger.info(f"✅ Completato: {step_name} (durata: {elapsed:.2f}s)")


@contextmanager
def timed_ingest(logger):
    """
    Context manager per misurare il tempo totale dell'ingest.
    
    Args:
        logger: Logger instance per loggare i messaggi
    
    Yields:
        None
        
    Example:
        with timed_ingest(log):
            with timed_step(log, "Step 1"):
                pass
            with timed_step(log, "Step 2"):
                pass
    """
    total_start = time.time()
    logger.info("🚀 Ingest avviato")
    try:
        yield
    finally:
        total_elapsed = time.time() - total_start
        logger.info(f"🏁 Ingest completato in {total_elapsed:.2f}s totali")


def format_duration(seconds: float) -> str:
    """
    Formatta una durata in secondi in un formato leggibile.
    
    Args:
        seconds: Durata in secondi
        
    Returns:
        String formattata (es. "1m 30s" o "45.2s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.0f}s"
    else:
        hours = int(seconds // 3600)
        remaining_minutes = int((seconds % 3600) // 60)
        return f"{hours}h {remaining_minutes}m"

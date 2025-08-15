import os

def _to_float(val: str, default: float) -> float:
    try:
        return float(val)
    except Exception:
        return default

FAST = _to_float(os.getenv("TIMING_FAST", "30"), 30.0)
SLOW = _to_float(os.getenv("TIMING_SLOW", "60"), 60.0)

def color_for_duration(seconds: float) -> str:
    """Return 'green' | 'orange' | 'red' based on FAST/SLOW thresholds."""
    if seconds < FAST:
        return "green"
    if seconds <= SLOW:
        return "orange"
    return "red"

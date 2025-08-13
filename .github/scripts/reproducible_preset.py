import os
os.environ.setdefault("PYTHONHASHSEED", "0")
os.environ.setdefault("DOCS_BUILD_DATE", "2024-01-01")
try:
    import numpy as _np
    _np.random.seed(0)
except Exception:
    pass
try:
    import random as _r
    _r.seed(0)
except Exception:
    pass

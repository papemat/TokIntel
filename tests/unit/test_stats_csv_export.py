from io import StringIO
import pandas as pd

def test_csv_has_expected_columns():
    df_stats = pd.DataFrame([
        {"step":"OCR","avg":11.3,"min":2.3,"max":44.0,"runs":7},
        {"step":"ASR","avg":12.7,"min":2.1,"max":45.2,"runs":7},
    ])
    buf = StringIO()
    df_stats.to_csv(buf, index=False)
    csv = buf.getvalue()
    header = csv.splitlines()[0]
    assert header == "step,avg,min,max,runs"
    assert "OCR" in csv and "ASR" in csv

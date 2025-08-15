# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# dipendenze di sistema utili (curl per healthcheck, build deps minime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# copia requirements se esiste e installa
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    (test -f /app/requirements.txt && pip install --no-cache-dir -r /app/requirements.txt || pip install --no-cache-dir streamlit)

# copia il progetto (in alternativa usa volumi in compose per dev)
COPY . /app

ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

EXPOSE 8501
CMD ["python", "-m", "streamlit", "run", "dash/app.py", "--server.address=0.0.0.0", "--server.port=8501"]

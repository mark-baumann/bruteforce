FROM python:3.11-slim

# Installiere erforderliche Systempakete
RUN apt-get update && apt-get install -y \
    tor \
    chromium \
    chromium-driver \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Setze Arbeitsverzeichnis
WORKDIR /app

# Kopiere Anforderungen und installiere
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Code
COPY . .

# Erstelle Verzeichnis für Logs
RUN mkdir -p /app/logs

# Starte Tor und das Bruteforce-Skript
CMD ["python", "docker_runner.py"]

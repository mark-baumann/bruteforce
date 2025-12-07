FROM python:3.11

# Installiere Systemabhängigkeiten für Tor und Browser
RUN apt-get update && apt-get install -y \
    tor \
    chromium \
    chromium-driver \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libcurl4 \
    libdbus-1-3 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxrandr2 \
    libxrender1 \
    xdg-utils \
    --no-install-recommends \
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

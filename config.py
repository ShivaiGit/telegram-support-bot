"""Конфигурация приложения"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Класс для хранения конфигурации"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # Email
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    EMAIL_TO = os.getenv("EMAIL_TO")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tickets.db")
    
    # Files
    FILES_DIR = os.getenv("FILES_DIR", "files")
    
    @classmethod
    def validate(cls):
        """Проверка обязательных параметров"""
        required = [
            "TELEGRAM_BOT_TOKEN",
            "TELEGRAM_CHAT_ID",
            "SMTP_USER",
            "SMTP_PASSWORD",
            "EMAIL_TO"
        ]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Отсутствуют обязательные параметры: {', '.join(missing)}")


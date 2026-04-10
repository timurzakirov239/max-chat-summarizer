"""Конфигурация приложения.

Загружает настройки из переменных окружения (.env файл).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class BotConfig:
    """Настройки бота MAX."""
    TOKEN: str = os.getenv("MAX_BOT_TOKEN", "")


class DatabaseConfig:
    """Настройки базы данных."""
    PATH: str = os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "bot.db"))


class MLConfig:
    """Настройки ML моделей."""
    MODEL_PATH: str = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "rut5-chat-summary"))
    MAX_INPUT_TOKENS: int = int(os.getenv("MAX_INPUT_TOKENS", "512"))
    EXTRACTIVE_TOP_K: int = 10
    ABSTRACTIVE_MAX_LENGTH: int = 150
    ABSTRACTIVE_MIN_LENGTH: int = 30


class SummaryConfig:
    """Настройки суммаризации."""
    DEFAULT_HOURS: int = int(os.getenv("DEFAULT_SUMMARY_HOURS", "24"))
    DEFAULT_TOP_N: int = int(os.getenv("DEFAULT_TOP_MESSAGES", "5"))


class LogConfig:
    """Настройки логирования."""
    LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


bot_config = BotConfig()
db_config = DatabaseConfig()
ml_config = MLConfig()
summary_config = SummaryConfig()
log_config = LogConfig()

"""Точка входа приложения MAX Chat Summarizer."""

import asyncio
import logging

from loguru import logger

from config import bot_config, log_config, db_config


def setup_logging() -> None:
    """Настройка логирования."""
    logging.basicConfig(level=getattr(logging, log_config.LEVEL))
    logger.info("Логирование настроено, уровень: {}", log_config.LEVEL)


async def main() -> None:
    """Главная асинхронная функция приложения."""
    setup_logging()

    if not bot_config.TOKEN:
        logger.error("BOT_TOKEN не задан! Укажите MAX_BOT_TOKEN в .env файле.")
        return

    logger.info("Запуск MAX Chat Summarizer...")

    # Инициализация базы данных
    from database.repository import DatabaseRepository
    db = DatabaseRepository(db_config.PATH)
    await db.initialize()
    logger.info("База данных инициализирована: {}", db_config.PATH)

    # Инициализация ML pipeline
    from summarizer.pipeline import SummarizationPipeline
    summarizer = SummarizationPipeline()
    logger.info("ML Pipeline инициализирован")

    # Запуск бота
    from bot.handlers import create_bot
    bot, dp = create_bot(db=db, summarizer=summarizer)
    logger.info("Бот запущен, ожидание сообщений...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

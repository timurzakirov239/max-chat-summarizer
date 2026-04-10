"""Обработчики команд бота MAX.

Реализует команды: /start, /help, /summary, /top, /add_chat, /chats.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, Command, MessageCreated

from config import bot_config, summary_config
from bot.keyboards import get_main_keyboard

if TYPE_CHECKING:
    from database.repository import DatabaseRepository
    from summarizer.pipeline import SummarizationPipeline


def create_bot(
    db: DatabaseRepository,
    summarizer: SummarizationPipeline,
) -> tuple[Bot, Dispatcher]:
    """Создаёт и настраивает бота и диспетчер."""
    bot = Bot(bot_config.TOKEN)
    dp = Dispatcher()

    @dp.bot_started()
    async def handle_start(event: BotStarted) -> None:
        await event.bot.send_message(
            chat_id=event.chat_id,
            text=(
                "\ud83d\udc4b Привет! Я — **MAX Chat Summarizer**.\n\n"
                "Я делаю краткий пересказ сообщений из групповых чатов "
                "и нахожу самые важные сообщения.\n\n"
                "Отправь /help чтобы увидеть список команд."
            ),
        )

    @dp.message_created(Command("start"))
    async def cmd_start(event: MessageCreated) -> None:
        await event.message.answer(
            "\ud83d\udc4b Привет! Я — **MAX Chat Summarizer**.\n\n"
            "Отправь /help для списка команд.",
        )

    @dp.message_created(Command("help"))
    async def cmd_help(event: MessageCreated) -> None:
        help_text = (
            "\ud83d\udcd6 **Доступные команды:**\n\n"
            "/summary [N] — Пересказ сообщений за N часов "
            f"(по умолчанию {summary_config.DEFAULT_HOURS})\n"
            "/top [N] — Топ-N важных сообщений "
            f"(по умолчанию {summary_config.DEFAULT_TOP_N})\n"
            "/add_chat <id> — Добавить чат для мониторинга\n"
            "/chats — Список отслеживаемых чатов\n"
            "/help — Эта справка"
        )
        await event.message.answer(help_text)

    @dp.message_created(Command("summary"))
    async def cmd_summary(event: MessageCreated) -> None:
        hours = summary_config.DEFAULT_HOURS
        await event.message.answer(
            f"\u23f3 Генерирую пересказ за последние {hours} ч...\n"
            "Это может занять несколько секунд."
        )
        # TODO: Реализация pipeline

    @dp.message_created(Command("top"))
    async def cmd_top(event: MessageCreated) -> None:
        top_n = summary_config.DEFAULT_TOP_N
        await event.message.answer(f"\ud83d\udd0d Ищу топ-{top_n} важных сообщений...")
        # TODO: Реализация ranker

    @dp.message_created(Command("chats"))
    async def cmd_chats(event: MessageCreated) -> None:
        chats = await db.get_chats()
        if not chats:
            await event.message.answer("\ud83d\udced Нет отслеживаемых чатов.")
            return
        text = "\ud83d\udccb **Отслеживаемые чаты:**\n\n"
        for chat in chats:
            text += f"\u2022 {chat['chat_title']} (ID: {chat['chat_id']})\n"
        await event.message.answer(text)

    return bot, dp

"""Сохранение собранных сообщений в хранилище."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from database.repository import DatabaseRepository


class MessageStorage:
    """Сохраняет полученные сообщения в БД."""

    def __init__(self, db: DatabaseRepository) -> None:
        self.db = db

    async def store_messages(self, chat_id: int, messages: list[dict[str, Any]]) -> int:
        """Сохраняет список сообщений в БД."""
        saved_count = 0
        for msg in messages:
            try:
                message_data = {
                    "chat_id": chat_id,
                    "message_id": str(msg.get("body", {}).get("mid", "")),
                    "sender_id": msg.get("sender", {}).get("user_id", 0),
                    "sender_name": msg.get("sender", {}).get("name", "Unknown"),
                    "text": msg.get("body", {}).get("text", ""),
                    "timestamp": msg.get("timestamp", 0),
                    "reply_to_id": msg.get("link", {}).get("mid"),
                    "has_attachments": bool(msg.get("body", {}).get("attachments")),
                }
                if not message_data["text"]:
                    continue
                await self.db.save_message(message_data)
                saved_count += 1
            except Exception as e:
                logger.warning("Ошибка сохранения сообщения: {}", e)
        logger.info("Сохранено {} новых сообщений из {} для чата {}", saved_count, len(messages), chat_id)
        return saved_count

"""Репозиторий для работы с SQLite: CRUD-операции."""

from __future__ import annotations
from pathlib import Path
from typing import Any

import aiosqlite
from loguru import logger
from database.models import ALL_DDL


class DatabaseRepository:
    """Асинхронный репозиторий SQLite."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._db: aiosqlite.Connection | None = None

    async def initialize(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._db = await aiosqlite.connect(self.db_path)
        self._db.row_factory = aiosqlite.Row
        for ddl in ALL_DDL:
            await self._db.execute(ddl)
        await self._db.commit()
        logger.info("БД инициализирована: {}", self.db_path)

    async def _get_db(self) -> aiosqlite.Connection:
        if self._db is None:
            await self.initialize()
        assert self._db is not None
        return self._db

    async def add_chat(self, chat_id: int, title: str = "Unknown") -> None:
        db = await self._get_db()
        await db.execute("INSERT OR IGNORE INTO chats (chat_id, chat_title) VALUES (?, ?)", (chat_id, title))
        await db.commit()

    async def get_chats(self) -> list[dict[str, Any]]:
        db = await self._get_db()
        cursor = await db.execute("SELECT * FROM chats ORDER BY added_at DESC")
        return [dict(row) for row in await cursor.fetchall()]

    async def save_message(self, message: dict[str, Any]) -> None:
        db = await self._get_db()
        await db.execute(
            "INSERT OR IGNORE INTO messages (chat_id, message_id, sender_id, sender_name, text, timestamp, reply_to_id, has_attachments) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (message["chat_id"], message["message_id"], message.get("sender_id"), message.get("sender_name"),
             message.get("text"), message.get("timestamp"), message.get("reply_to_id"), message.get("has_attachments", False)),
        )
        await db.commit()

    async def get_messages(self, chat_id: int, from_ts: int | None = None, to_ts: int | None = None) -> list[dict[str, Any]]:
        db = await self._get_db()
        query = "SELECT * FROM messages WHERE chat_id = ?"
        params: list[Any] = [chat_id]
        if from_ts is not None:
            query += " AND timestamp >= ?"
            params.append(from_ts)
        if to_ts is not None:
            query += " AND timestamp <= ?"
            params.append(to_ts)
        query += " ORDER BY timestamp ASC"
        cursor = await db.execute(query, params)
        return [dict(row) for row in await cursor.fetchall()]

    async def save_summary(self, chat_id: int, period_from: int, period_to: int, summary: str, msg_count: int) -> None:
        db = await self._get_db()
        await db.execute(
            "INSERT INTO summaries (chat_id, period_from, period_to, summary, msg_count) VALUES (?, ?, ?, ?, ?)",
            (chat_id, period_from, period_to, summary, msg_count),
        )
        await db.commit()

    async def close(self) -> None:
        if self._db:
            await self._db.close()
            self._db = None

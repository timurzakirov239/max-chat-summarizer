"""Получение сообщений из чатов мессенджера MAX.

Использует MAX Bot API (platform-api.max.ru).
"""

from __future__ import annotations

import time
from typing import Any

import aiohttp
from loguru import logger

from config import bot_config

MAX_API_BASE = "https://platform-api.max.ru"


class MessageFetcher:
    """Класс для получения сообщений из MAX чатов."""

    def __init__(self, token: str | None = None) -> None:
        self.token = token or bot_config.TOKEN
        self.session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={"Authorization": self.token}
            )
        return self.session

    async def fetch_messages(
        self, chat_id: int, from_ts: int | None = None,
        to_ts: int | None = None, count: int = 100,
    ) -> list[dict[str, Any]]:
        """Получает сообщения из чата."""
        session = await self._get_session()
        params: dict[str, Any] = {"chat_id": chat_id, "count": min(count, 100)}
        if from_ts:
            params["from"] = from_ts
        if to_ts:
            params["to"] = to_ts
        try:
            async with session.get(f"{MAX_API_BASE}/messages", params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    messages = data.get("messages", [])
                    logger.info("Получено {} сообщений из чата {}", len(messages), chat_id)
                    return messages
                else:
                    logger.error("Ошибка API MAX: {} - {}", resp.status, await resp.text())
                    return []
        except Exception as e:
            logger.error("Ошибка при получении сообщений: {}", e)
            return []

    async def fetch_all_messages(self, chat_id: int, hours: int = 24) -> list[dict[str, Any]]:
        """Получает все сообщения за указанный период с пагинацией."""
        to_ts = int(time.time() * 1000)
        from_ts = to_ts - (hours * 3600 * 1000)
        all_messages: list[dict[str, Any]] = []
        current_to = to_ts
        while True:
            batch = await self.fetch_messages(chat_id=chat_id, from_ts=from_ts, to_ts=current_to, count=100)
            if not batch:
                break
            all_messages.extend(batch)
            earliest_ts = min(m.get("timestamp", 0) for m in batch)
            if earliest_ts <= from_ts:
                break
            current_to = earliest_ts - 1
        logger.info("Всего получено {} сообщений за {} ч из чата {}", len(all_messages), hours, chat_id)
        return all_messages

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

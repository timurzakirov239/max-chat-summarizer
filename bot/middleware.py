"""Middleware для бота MAX: rate limiting и логирование."""

import time
from collections import defaultdict
from typing import Any

from loguru import logger


class RateLimiter:
    """Ограничитель частоты запросов."""

    def __init__(self, limit: int = 5, window: int = 60) -> None:
        self.limit = limit
        self.window = window
        self._requests: dict[int, list[float]] = defaultdict(list)

    def is_allowed(self, user_id: int) -> bool:
        """Проверяет, разрешён ли запрос пользователю."""
        now = time.time()
        self._requests[user_id] = [
            ts for ts in self._requests[user_id] if now - ts < self.window
        ]
        if len(self._requests[user_id]) >= self.limit:
            logger.warning("Rate limit exceeded for user {}", user_id)
            return False
        self._requests[user_id].append(now)
        return True


def log_event(event_type: str, data: dict[str, Any]) -> None:
    """Логирует событие бота."""
    logger.info("Event: {} | Data: {}", event_type, {k: v for k, v in data.items() if k != "text"})

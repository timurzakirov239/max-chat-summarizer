"""Дедупликация сообщений."""

from __future__ import annotations

from difflib import SequenceMatcher

from loguru import logger


class MessageDeduplicator:
    """Удаляет дубликаты и похожие сообщения."""

    def __init__(self, similarity_threshold: float = 0.85) -> None:
        self.similarity_threshold = similarity_threshold

    def deduplicate(self, messages: list[str]) -> list[str]:
        """Удаляет дублирующиеся сообщения."""
        if not messages:
            return []
        unique: list[str] = []
        for msg in messages:
            is_duplicate = False
            for existing in unique:
                if self._is_similar(msg, existing):
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique.append(msg)
        removed = len(messages) - len(unique)
        if removed > 0:
            logger.info("Дедупликация: удалено {} из {} сообщений", removed, len(messages))
        return unique

    def _is_similar(self, text1: str, text2: str) -> bool:
        ratio = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        return ratio >= self.similarity_threshold

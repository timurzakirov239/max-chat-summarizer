"""Извлечение признаков сообщений для ранжирования."""

from __future__ import annotations

import re
from typing import Any

import numpy as np


class FeatureExtractor:
    """Извлекает числовые признаки из сообщений."""

    QUESTION_PATTERN = re.compile(r"\?")
    URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)

    def extract(self, message: dict[str, Any], context: dict[str, Any] | None = None) -> np.ndarray:
        text = message.get("text", "")
        context = context or {}
        features = [
            self._reply_count(message, context), self._message_length(text, context),
            self._has_question(text), self._has_link(text),
            self._word_count(text), self._unique_word_ratio(text),
            self._position_score(message, context), self._has_attachments(message),
        ]
        return np.array(features, dtype=np.float32)

    def extract_batch(self, messages: list[dict[str, Any]]) -> np.ndarray:
        if not messages:
            return np.array([])
        context = self._build_context(messages)
        return np.stack([self.extract(msg, context) for msg in messages])

    def get_feature_names(self) -> list[str]:
        return ["reply_count", "message_length_norm", "has_question", "has_link",
                "word_count", "unique_word_ratio", "position_score", "has_attachments"]

    @staticmethod
    def _reply_count(message: dict, context: dict) -> float:
        msg_id = message.get("message_id", "")
        replies = context.get("reply_counts", {})
        return replies.get(msg_id, 0) / max(context.get("max_replies", 1), 1)

    @staticmethod
    def _message_length(text: str, context: dict) -> float:
        return len(text) / max(context.get("max_length", 1), 1)

    def _has_question(self, text: str) -> float:
        return 1.0 if self.QUESTION_PATTERN.search(text) else 0.0

    def _has_link(self, text: str) -> float:
        return 1.0 if self.URL_PATTERN.search(text) else 0.0

    @staticmethod
    def _word_count(text: str) -> float:
        return np.log1p(len(text.split()))

    @staticmethod
    def _unique_word_ratio(text: str) -> float:
        words = text.lower().split()
        return len(set(words)) / len(words) if words else 0.0

    @staticmethod
    def _position_score(message: dict, context: dict) -> float:
        ts = message.get("timestamp", 0)
        min_ts, max_ts = context.get("min_timestamp", 0), context.get("max_timestamp", 1)
        return (ts - min_ts) / (max_ts - min_ts) if max_ts != min_ts else 0.5

    @staticmethod
    def _has_attachments(message: dict) -> float:
        return 1.0 if message.get("has_attachments", False) else 0.0

    def _build_context(self, messages: list[dict]) -> dict:
        reply_counts: dict[str, int] = {}
        for msg in messages:
            reply_to = msg.get("reply_to_id")
            if reply_to:
                reply_counts[reply_to] = reply_counts.get(reply_to, 0) + 1
        timestamps = [msg.get("timestamp", 0) for msg in messages]
        lengths = [len(msg.get("text", "")) for msg in messages]
        return {
            "reply_counts": reply_counts,
            "max_replies": max(reply_counts.values()) if reply_counts else 0,
            "min_timestamp": min(timestamps) if timestamps else 0,
            "max_timestamp": max(timestamps) if timestamps else 0,
            "max_length": max(lengths) if lengths else 1,
        }

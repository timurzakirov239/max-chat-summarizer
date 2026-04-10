"""Скоринг важности сообщений."""

from __future__ import annotations
from typing import Any

import numpy as np
from loguru import logger

from ranker.features import FeatureExtractor
from ranker.model import ImportanceModel


class ImportanceScorer:
    """Оценка важности сообщений."""

    def __init__(self, model_path: str | None = None) -> None:
        self.feature_extractor = FeatureExtractor()
        self.model = ImportanceModel(model_path)

    def score_messages(self, messages: list[dict[str, Any]]) -> list[tuple[dict, float]]:
        if not messages:
            return []
        features = self.feature_extractor.extract_batch(messages)
        scores = self.model.predict(features)
        scored = list(zip(messages, scores))
        scored.sort(key=lambda x: x[1], reverse=True)
        logger.info("Ранжировано {} сообщений", len(scored))
        return scored

    def get_top_messages(self, messages: list[dict[str, Any]], top_n: int = 5) -> list[dict]:
        scored = self.score_messages(messages)
        return [msg for msg, _ in scored[:top_n]]

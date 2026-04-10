"""ML-модель ранжирования важности (XGBoost + эвристический fallback)."""

from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
from loguru import logger


class ImportanceModel:
    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path
        self._model = None
        self._loaded = False

    def load(self) -> None:
        if self.model_path and Path(self.model_path).exists():
            try:
                with open(self.model_path, "rb") as f:
                    self._model = pickle.load(f)
                self._loaded = True
                logger.info("Модель ранжирования загружена: {}", self.model_path)
            except Exception as e:
                logger.error("Ошибка загрузки: {}", e)
        else:
            logger.warning("Модель не найдена, эвристический скоринг")

    def predict(self, features: np.ndarray) -> np.ndarray:
        if not self._loaded:
            self.load()
        if self._loaded and self._model is not None:
            try:
                return self._model.predict_proba(features)[:, 1]
            except Exception as e:
                logger.error("Ошибка предсказания: {}", e)
        return self._heuristic_score(features)

    @staticmethod
    def _heuristic_score(features: np.ndarray) -> np.ndarray:
        weights = np.array([0.25, 0.10, 0.15, 0.10, 0.10, 0.10, 0.10, 0.10])
        if features.ndim == 1:
            features = features.reshape(1, -1)
        n = min(features.shape[1], len(weights))
        scores = features[:, :n] @ weights[:n]
        mn, mx = scores.min(), scores.max()
        return (scores - mn) / (mx - mn) if mx > mn else np.full_like(scores, 0.5)

    def save(self, path: str) -> None:
        if self._model is not None:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, "wb") as f:
                pickle.dump(self._model, f)
            logger.info("Модель сохранена: {}", path)

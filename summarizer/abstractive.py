"""Abstractive суммаризация на основе ruT5."""

from __future__ import annotations

from pathlib import Path

import torch
from loguru import logger

from config import ml_config


class AbstractiveSummarizer:
    """Abstractive суммаризация с помощью ruT5."""

    def __init__(self, model_path: str | None = None, device: str | None = None) -> None:
        self.model_path = model_path or ml_config.MODEL_PATH
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._model = None
        self._tokenizer = None
        self._loaded = False

    def load_model(self) -> None:
        """Загружает модель и токенизатор."""
        try:
            from transformers import T5ForConditionalGeneration, T5Tokenizer
            model_path = Path(self.model_path)
            if model_path.exists():
                logger.info("Загрузка fine-tuned модели из {}", self.model_path)
                self._tokenizer = T5Tokenizer.from_pretrained(self.model_path)
                self._model = T5ForConditionalGeneration.from_pretrained(self.model_path)
            else:
                logger.warning("Fine-tuned модель не найдена. Загрузка ai-forever/ruT5-base")
                self._tokenizer = T5Tokenizer.from_pretrained("ai-forever/ruT5-base")
                self._model = T5ForConditionalGeneration.from_pretrained("ai-forever/ruT5-base")
            self._model.to(self.device)
            self._model.eval()
            self._loaded = True
            logger.info("Модель загружена на {}", self.device)
        except Exception as e:
            logger.error("Ошибка загрузки модели: {}", e)
            self._loaded = False

    def summarize(self, text: str) -> str:
        """Генерирует абстрактивный пересказ."""
        if not self._loaded:
            self.load_model()
        if not self._loaded or self._model is None or self._tokenizer is None:
            logger.error("Модель не загружена, возвращаю исходный текст")
            return text
        try:
            input_text = f"summarize: {text}"
            inputs = self._tokenizer(input_text, max_length=ml_config.MAX_INPUT_TOKENS, truncation=True, return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self._model.generate(
                    **inputs, max_length=ml_config.ABSTRACTIVE_MAX_LENGTH,
                    min_length=ml_config.ABSTRACTIVE_MIN_LENGTH,
                    num_beams=4, length_penalty=1.0,
                    no_repeat_ngram_size=3, early_stopping=True,
                )
            summary = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            logger.info("Abstractive: {} -> {} символов", len(text), len(summary))
            return summary
        except Exception as e:
            logger.error("Ошибка abstractive суммаризации: {}", e)
            return text

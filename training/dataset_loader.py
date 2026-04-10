"""Загрузчик датасетов: Gazeta (HuggingFace) + собственный датасет чатов."""

from __future__ import annotations
from typing import Any
from loguru import logger


def load_gazeta_dataset(split: str = "train", max_samples: int | None = None) -> Any:
    from datasets import load_dataset
    logger.info("Загрузка Gazeta dataset, split={}...", split)
    dataset = load_dataset("IlyaGusev/gazeta", split=split)
    if max_samples is not None:
        dataset = dataset.select(range(min(max_samples, len(dataset))))
    logger.info("Загружено {} примеров", len(dataset))
    return dataset


def load_chat_dataset(path: str) -> list[dict[str, str]]:
    import json
    from pathlib import Path
    data_path = Path(path)
    if not data_path.exists():
        logger.warning("Датасет не найден: {}", path)
        return []
    samples = []
    with open(data_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                samples.append(json.loads(line.strip()))
    logger.info("Загружено {} примеров из {}", len(samples), path)
    return samples


def prepare_tokenized_dataset(dataset: Any, tokenizer: Any, max_input_length: int = 512, max_target_length: int = 150, text_column: str = "text", summary_column: str = "summary") -> Any:
    def tokenize_function(examples: dict) -> dict:
        inputs = [f"summarize: {text}" for text in examples[text_column]]
        model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True, padding="max_length")
        labels = tokenizer(examples[summary_column], max_length=max_target_length, truncation=True, padding="max_length")
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    tokenized = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)
    logger.info("Датасет токенизирован: {} примеров", len(tokenized))
    return tokenized

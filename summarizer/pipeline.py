"""Объединённый pipeline суммаризации: extractive + abstractive."""

from __future__ import annotations

from loguru import logger

from preprocessing.cleaner import TextCleaner
from preprocessing.tokenizer import TextTokenizer
from preprocessing.deduplicator import MessageDeduplicator
from summarizer.extractive import ExtractiveSummarizer
from summarizer.abstractive import AbstractiveSummarizer
from config import ml_config


class SummarizationPipeline:
    """Двухэтапный pipeline суммаризации."""

    def __init__(self) -> None:
        self.cleaner = TextCleaner()
        self.tokenizer = TextTokenizer()
        self.deduplicator = MessageDeduplicator()
        self.extractive = ExtractiveSummarizer(top_k=ml_config.EXTRACTIVE_TOP_K)
        self.abstractive = AbstractiveSummarizer()

    def summarize_messages(self, messages: list[str]) -> str:
        """Полный pipeline суммаризации."""
        if not messages:
            return "Нет сообщений для пересказа."
        logger.info("Pipeline: начало, {} сообщений", len(messages))
        cleaned = [self.cleaner.clean(msg) for msg in messages if self.cleaner.is_meaningful(msg)]
        if not cleaned:
            return "Не найдено содержательных сообщений."
        unique = self.deduplicator.deduplicate(cleaned)
        document = self.tokenizer.merge_messages_to_document(unique)
        sentences = self.tokenizer.split_sentences(document)
        key_sentences = self.extractive.summarize(sentences)
        extractive_text = " ".join(key_sentences)
        summary = self.abstractive.summarize(extractive_text)
        logger.info("Финальный пересказ: {} символов", len(summary))
        return summary

    def extractive_only(self, messages: list[str], top_k: int = 5) -> list[str]:
        """Только extractive суммаризация (fallback)."""
        cleaned = [self.cleaner.clean(msg) for msg in messages if self.cleaner.is_meaningful(msg)]
        unique = self.deduplicator.deduplicate(cleaned)
        document = self.tokenizer.merge_messages_to_document(unique)
        sentences = self.tokenizer.split_sentences(document)
        self.extractive.top_k = top_k
        return self.extractive.summarize(sentences)

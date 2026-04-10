"""Токенизация текста на русском языке."""

import re

import nltk

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)


class TextTokenizer:
    """Токенизатор текста на русском языке."""

    def split_sentences(self, text: str) -> list[str]:
        """Разбивает текст на предложения."""
        if not text:
            return []
        sentences = nltk.sent_tokenize(text, language="russian")
        result = []
        for sent in sentences:
            parts = sent.strip().split("\n")
            result.extend(p.strip() for p in parts if p.strip())
        return result

    def tokenize_words(self, text: str) -> list[str]:
        """Разбивает текст на слова."""
        if not text:
            return []
        return nltk.word_tokenize(text, language="russian")

    def merge_messages_to_document(self, messages: list[str]) -> str:
        """Объединяет список сообщений в единый документ."""
        return " ".join(msg.strip() for msg in messages if msg.strip())

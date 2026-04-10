"""Очистка текстовых данных: удаление ссылок, эмодзи, нормализация."""

import re


class TextCleaner:
    """Очистка и нормализация текста сообщений."""

    URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
    EMOJI_PATTERN = re.compile(
        "[" "\U0001F600-\U0001F64F" "\U0001F300-\U0001F5FF" "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF" "\U00002702-\U000027B0" "\U000024C2-\U0001F251" "]+",
        flags=re.UNICODE,
    )
    MENTION_PATTERN = re.compile(r"@\w+")
    MULTIPLE_SPACES = re.compile(r"\s+")
    MULTIPLE_NEWLINES = re.compile(r"\n{3,}")

    def clean(self, text: str) -> str:
        """Полная очистка текста."""
        if not text:
            return ""
        text = self.remove_urls(text)
        text = self.remove_mentions(text)
        text = self.remove_emoji(text)
        text = self.normalize_whitespace(text)
        return text.strip()

    def remove_urls(self, text: str) -> str:
        return self.URL_PATTERN.sub("", text)

    def remove_mentions(self, text: str) -> str:
        return self.MENTION_PATTERN.sub("", text)

    def remove_emoji(self, text: str) -> str:
        return self.EMOJI_PATTERN.sub("", text)

    def normalize_whitespace(self, text: str) -> str:
        text = self.MULTIPLE_NEWLINES.sub("\n\n", text)
        text = self.MULTIPLE_SPACES.sub(" ", text)
        return text

    def is_meaningful(self, text: str, min_length: int = 5) -> bool:
        """Проверяет, содержит ли текст полезную информацию."""
        cleaned = self.clean(text)
        if len(cleaned) < min_length:
            return False
        noise_patterns = [r"^[\+\-]+$", r"^\W+$", r"^(ок|ага|да|нет|ну|лол|хах[а]*|кек)$"]
        for pattern in noise_patterns:
            if re.match(pattern, cleaned, re.IGNORECASE):
                return False
        return True

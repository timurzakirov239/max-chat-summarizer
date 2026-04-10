"""Тесты модуля предобработки текста."""

from preprocessing.cleaner import TextCleaner
from preprocessing.deduplicator import MessageDeduplicator
from preprocessing.tokenizer import TextTokenizer


class TestTextCleaner:
    def setup_method(self):
        self.cleaner = TextCleaner()

    def test_remove_urls(self):
        assert "https://" not in self.cleaner.remove_urls("Смотри https://example.com тут")

    def test_remove_mentions(self):
        assert "@user" not in self.cleaner.remove_mentions("@user привет")

    def test_is_meaningful(self):
        assert self.cleaner.is_meaningful("Завтра собрание в 15:00")
        assert not self.cleaner.is_meaningful("ок")
        assert not self.cleaner.is_meaningful("+++")
        assert not self.cleaner.is_meaningful("")


class TestMessageDeduplicator:
    def setup_method(self):
        self.dedup = MessageDeduplicator(similarity_threshold=0.85)

    def test_exact_duplicates(self):
        result = self.dedup.deduplicate(["Привет мир", "Привет мир", "Другое"])
        assert len(result) == 2

    def test_empty(self):
        assert self.dedup.deduplicate([]) == []


class TestTextTokenizer:
    def setup_method(self):
        self.tokenizer = TextTokenizer()

    def test_split_sentences(self):
        sentences = self.tokenizer.split_sentences("Первое. Второе! Третье?")
        assert len(sentences) >= 2

    def test_merge(self):
        result = self.tokenizer.merge_messages_to_document(["Привет", "Мир"])
        assert "Привет" in result and "Мир" in result

    def test_empty(self):
        assert self.tokenizer.split_sentences("") == []

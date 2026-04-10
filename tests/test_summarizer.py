"""Тесты extractive суммаризации."""

from summarizer.extractive import ExtractiveSummarizer


class TestExtractiveSummarizer:
    def setup_method(self):
        self.summarizer = ExtractiveSummarizer(top_k=3)

    def test_summarize_basic(self):
        sentences = [
            "Машинное обучение является частью искусственного интеллекта.",
            "Python популярный язык для анализа данных.",
            "Нейронные сети используются для NLP.",
            "Завтра будет хорошая погода.",
            "Трансформеры революционизировали NLP.",
        ]
        result = self.summarizer.summarize(sentences)
        assert len(result) == 3

    def test_empty(self):
        assert self.summarizer.summarize([]) == []

    def test_fewer_than_top_k(self):
        assert len(self.summarizer.summarize(["Коротко.", "Ещё."])) == 2

"""Extractive суммаризация на основе TextRank."""

from __future__ import annotations

import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from loguru import logger


class ExtractiveSummarizer:
    """Extractive суммаризация методом TextRank."""

    def __init__(self, top_k: int = 10) -> None:
        self.top_k = top_k
        self._vectorizer = TfidfVectorizer(max_features=5000)

    def summarize(self, sentences: list[str]) -> list[str]:
        """Извлекает ключевые предложения."""
        if not sentences:
            return []
        if len(sentences) <= self.top_k:
            return sentences
        try:
            tfidf_matrix = self._vectorizer.fit_transform(sentences)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            graph = nx.from_numpy_array(similarity_matrix)
            scores = nx.pagerank(graph, max_iter=100)
            ranked_indices = sorted(scores, key=scores.get, reverse=True)[:self.top_k]
            ranked_indices.sort()
            result = [sentences[i] for i in ranked_indices]
            logger.info("Extractive: отобрано {} из {} предложений", len(result), len(sentences))
            return result
        except Exception as e:
            logger.error("Ошибка extractive суммаризации: {}", e)
            return sentences[:self.top_k]

    def get_sentence_scores(self, sentences: list[str]) -> list[tuple[str, float]]:
        """Возвращает предложения с TextRank скорами."""
        if not sentences:
            return []
        try:
            tfidf_matrix = self._vectorizer.fit_transform(sentences)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            graph = nx.from_numpy_array(similarity_matrix)
            scores = nx.pagerank(graph, max_iter=100)
            scored = [(sentences[i], scores[i]) for i in range(len(sentences))]
            scored.sort(key=lambda x: x[1], reverse=True)
            return scored
        except Exception as e:
            logger.error("Ошибка получения скоров: {}", e)
            return [(s, 0.0) for s in sentences]

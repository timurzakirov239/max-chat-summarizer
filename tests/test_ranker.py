"""Тесты модуля ранжирования."""

import numpy as np
from ranker.features import FeatureExtractor
from ranker.model import ImportanceModel


class TestFeatureExtractor:
    def setup_method(self):
        self.extractor = FeatureExtractor()

    def test_extract_single(self):
        msg = {"text": "Важная встреча завтра?", "message_id": "1", "timestamp": 1000}
        features = self.extractor.extract(msg)
        assert isinstance(features, np.ndarray)
        assert len(features) == 8

    def test_extract_batch(self):
        messages = [
            {"text": "Привет", "message_id": "1", "timestamp": 100},
            {"text": "Встреча", "message_id": "2", "timestamp": 200},
        ]
        features = self.extractor.extract_batch(messages)
        assert features.shape == (2, 8)

    def test_has_question(self):
        f1 = self.extractor.extract({"text": "Как дела?", "message_id": "1", "timestamp": 0})
        f2 = self.extractor.extract({"text": "Всё ок", "message_id": "2", "timestamp": 0})
        assert f1[2] == 1.0
        assert f2[2] == 0.0


class TestImportanceModel:
    def test_heuristic_fallback(self):
        model = ImportanceModel()
        features = np.random.rand(5, 8).astype(np.float32)
        scores = model.predict(features)
        assert len(scores) == 5
        assert all(0 <= s <= 1 for s in scores)

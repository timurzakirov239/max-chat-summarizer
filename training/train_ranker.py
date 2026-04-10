"""Скрипт обучения модели ранжирования (XGBoost).

Usage:
    python -m training.train_ranker --data data/labeled_messages.jsonl --output models/ranker.pkl
"""

from __future__ import annotations
import argparse
import json
import pickle
from pathlib import Path

import numpy as np
from loguru import logger
from ranker.features import FeatureExtractor


def load_labeled_data(path: str) -> tuple[list[dict], list[int]]:
    messages, labels = [], []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line.strip())
            label = data.pop("label", 0)
            messages.append(data)
            labels.append(label)
    logger.info("Загружено {} размеченных примеров", len(messages))
    return messages, labels


def train_ranker(data_path: str, output_path: str, n_estimators: int = 100, max_depth: int = 5) -> None:
    from xgboost import XGBClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, roc_auc_score

    messages, labels = load_labeled_data(data_path)
    extractor = FeatureExtractor()
    features = extractor.extract_batch(messages)
    X_train, X_test, y_train, y_test = train_test_split(features, np.array(labels), test_size=0.2, random_state=42, stratify=labels)
    model = XGBClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=0.1, random_state=42, eval_metric="logloss")
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=True)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    logger.info("\n{}", classification_report(y_test, y_pred))
    logger.info("ROC AUC: {:.4f}", roc_auc_score(y_test, y_proba))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        pickle.dump(model, f)
    logger.info("Модель сохранена: {}", output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Обучение модели ранжирования")
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", default="models/ranker.pkl")
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=5)
    args = parser.parse_args()
    train_ranker(data_path=args.data, output_path=args.output, n_estimators=args.n_estimators, max_depth=args.max_depth)


if __name__ == "__main__":
    main()

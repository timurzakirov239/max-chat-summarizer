"""Оценка качества ML-моделей (ROUGE, F1, ROC AUC).

Usage:
    python -m training.evaluate --model models/rut5-chat-summary --max_samples 100
"""

from __future__ import annotations
import argparse
from loguru import logger


def evaluate_summarizer(model_path: str, max_samples: int = 100) -> dict[str, float]:
    from rouge_score import rouge_scorer
    from transformers import T5ForConditionalGeneration, T5Tokenizer
    from training.dataset_loader import load_gazeta_dataset

    logger.info("Оценка модели: {}", model_path)
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    model.eval()
    dataset = load_gazeta_dataset("test", max_samples)
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    metrics: dict[str, list[float]] = {"rouge1": [], "rouge2": [], "rougeL": []}
    for example in dataset:
        inputs = tokenizer(f"summarize: {example['text']}", max_length=512, truncation=True, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=150, num_beams=4)
        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
        scores = scorer.score(example["summary"], prediction)
        for key in metrics:
            metrics[key].append(scores[key].fmeasure)

    avg_metrics = {key: sum(values) / len(values) for key, values in metrics.items()}
    logger.info("=== Результаты ===")
    for key, value in avg_metrics.items():
        logger.info("  {}: {:.4f}", key, value)
    return avg_metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Оценка качества ML-моделей")
    parser.add_argument("--model", required=True)
    parser.add_argument("--max_samples", type=int, default=100)
    args = parser.parse_args()
    evaluate_summarizer(model_path=args.model, max_samples=args.max_samples)


if __name__ == "__main__":
    main()

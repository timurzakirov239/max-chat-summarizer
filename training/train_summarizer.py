"""Скрипт fine-tuning ruT5-base для суммаризации.

Usage:
    python -m training.train_summarizer --output_dir models/rut5-chat-summary --epochs 3
"""

from __future__ import annotations
import argparse
import torch
from loguru import logger


def train_on_gazeta(output_dir: str, epochs: int = 3, batch_size: int = 8, learning_rate: float = 3e-5, max_samples: int | None = None) -> None:
    from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, TrainingArguments
    from training.dataset_loader import load_gazeta_dataset, prepare_tokenized_dataset

    logger.info("=== Fine-tuning ruT5 на Gazeta ===")
    model_name = "ai-forever/ruT5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    train_dataset = load_gazeta_dataset("train", max_samples)
    eval_dataset = load_gazeta_dataset("test", max_samples=500)
    train_tokenized = prepare_tokenized_dataset(train_dataset, tokenizer)
    eval_tokenized = prepare_tokenized_dataset(eval_dataset, tokenizer)

    training_args = TrainingArguments(
        output_dir=output_dir, num_train_epochs=epochs,
        per_device_train_batch_size=batch_size, per_device_eval_batch_size=batch_size,
        warmup_steps=500, weight_decay=0.01, learning_rate=learning_rate,
        logging_dir=f"{output_dir}/logs", logging_steps=100,
        eval_strategy="epoch", save_strategy="epoch",
        load_best_model_at_end=True, fp16=torch.cuda.is_available(),
    )
    trainer = Trainer(model=model, args=training_args, train_dataset=train_tokenized, eval_dataset=eval_tokenized)
    logger.info("Начало обучения...")
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    logger.info("Модель сохранена: {}", output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tuning ruT5 для суммаризации чатов")
    parser.add_argument("--output_dir", default="models/rut5-chat-summary")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--learning_rate", type=float, default=3e-5)
    parser.add_argument("--max_samples", type=int, default=None)
    args = parser.parse_args()
    train_on_gazeta(output_dir=args.output_dir, epochs=args.epochs, batch_size=args.batch_size, learning_rate=args.learning_rate, max_samples=args.max_samples)


if __name__ == "__main__":
    main()

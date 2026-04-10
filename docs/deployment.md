# Развёртывание

## Требования
- Python 3.11+
- Токен бота MAX (получить через @MasterBot)
- GPU (рекомендуется для обучения)

## Локальный запуск

```bash
git clone https://github.com/timurzakirov239/max-chat-summarizer.git
cd max-chat-summarizer
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
# Укажите MAX_BOT_TOKEN в .env
python main.py
```

## Обучение модели

```bash
# Fine-tuning ruT5 на Gazeta
python -m training.train_summarizer --output_dir models/rut5-chat-summary --epochs 3

# Оценка качества
python -m training.evaluate --model models/rut5-chat-summary --max_samples 100

# Обучение ранжирования
python -m training.train_ranker --data data/labeled_messages.jsonl --output models/ranker.pkl
```

## Тестирование

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --cov=.
```

## Production (Webhook)

```bash
pip install maxapi[webhook]
# Настройте HTTPS с валидным SSL-сертификатом
```

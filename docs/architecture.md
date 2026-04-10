# Архитектура системы MAX Chat Summarizer

## Общая схема

```
Пользователь MAX  →  MAX Bot API  →  Bot Handler
                                        ↓
                                   Message Collector  →  SQLite
                                        ↓
                                   Preprocessor
                                        ↓
                              ┌─────────┴─────────┐
                         Summarizer          Importance Ranker
                        (TextRank +          (Feature Extraction +
                         ruT5-base)           XGBoost)
                              └─────────┬─────────┘
                                        ↓
                                Response Formatter  →  Ответ пользователю
```

## Компоненты

### 1. Bot Handler (`bot/`)
- Приём команд от пользователей через MAX Bot API
- Маршрутизация: /start, /help, /summary, /top, /chats
- Inline-клавиатуры и callback-обработчики
- Rate limiting через middleware

### 2. Message Collector (`collector/`)
- **fetcher.py** — HTTP-клиент для `GET /messages` на `platform-api.max.ru`
- **storage.py** — адаптер между API и SQLite
- Пагинация для получения всех сообщений за период

### 3. Preprocessor (`preprocessing/`)
- **cleaner.py** — удаление URL, эмодзи, @mentions, нормализация
- **tokenizer.py** — разбиение на предложения (NLTK, русский язык)
- **deduplicator.py** — удаление дубликатов (SequenceMatcher, порог 0.85)

### 4. Summarizer (`summarizer/`)
- **extractive.py** — TextRank на TF-IDF + PageRank (networkx)
- **abstractive.py** — ruT5-base (fine-tuned) для генерации пересказа
- **pipeline.py** — двухэтапный pipeline: extractive → abstractive

### 5. Importance Ranker (`ranker/`)
- **features.py** — 8 числовых признаков сообщения
- **model.py** — XGBoost классификатор + эвристический fallback
- **scorer.py** — объединение features + model

### 6. Database (`database/`)
- **models.py** — DDL схемы: chats, messages, summaries
- **repository.py** — асинхронный CRUD через aiosqlite

### 7. Training (`training/`)
- **train_summarizer.py** — fine-tuning ruT5 на Gazeta dataset
- **train_ranker.py** — обучение XGBoost на размеченных данных
- **evaluate.py** — оценка ROUGE-1/2/L

## Поток данных

1. Пользователь отправляет `/summary 24` в чат с ботом
2. Bot Handler парсит команду
3. MessageFetcher получает сообщения за 24ч через MAX API
4. Preprocessor очищает, дедуплицирует, токенизирует
5. ExtractiveSummarizer отбирает top-K предложений
6. AbstractiveSummarizer генерирует связный пересказ
7. Результат отправляется пользователю

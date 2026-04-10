# 📝 MAX Chat Summarizer

**Система автоматического реферирования сообщений из чатов мессенджера MAX**

> Курсовая работа — КФУ, ИВМиИТ, кафедра анализа данных и технологий программирования
> Направление: 09.03.03 «Прикладная информатика»
> Студент: Закиров Тимур Айратович, группа 09-352
> Руководитель: Ахмедова Альфира Мазитовна

---

## 🎯 Описание

Чат-бот для мессенджера **MAX** (VK Team), который выполняет:
- **Автоматический краткий пересказ** сообщений из групповых чатов без повторов
- **Ранжирование сообщений по важности** на основе ML-алгоритмов

Используется собственный двухэтапный алгоритм суммаризации:
1. **Extractive** — TextRank для отбора ключевых предложений
2. **Abstractive** — Fine-tuned ruT5-base для генерации связного пересказа

## 🏗️ Архитектура

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

## 🚀 Быстрый старт

### 1. Клонирование
```bash
git clone https://github.com/timurzakirov239/max-chat-summarizer.git
cd max-chat-summarizer
```

### 2. Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Настройка
```bash
cp .env.example .env
# Отредактируйте .env и укажите BOT_TOKEN
```

### 4. Запуск
```bash
python main.py
```

## 🤖 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие и инструкция |
| `/help` | Список доступных команд |
| `/summary [N]` | Пересказ сообщений за последние N часов (по умолчанию 24) |
| `/top [N]` | Топ-N самых важных сообщений (по умолчанию 5) |
| `/add_chat <id>` | Добавить чат для мониторинга |
| `/chats` | Список отслеживаемых чатов |

## 🧠 ML-стек

| Компонент | Технология |
|-----------|------------|
| Extractive Summarization | TextRank (networkx + TF-IDF) |
| Abstractive Summarization | ai-forever/ruT5-base (fine-tuned) |
| Importance Ranking | XGBoost / LightGBM |
| Обучающие датасеты | Gazeta (60K+), собственный датасет чатов |
| Метрики | ROUGE-1/2/L, BERTScore |

## 📁 Структура проекта

```
max-chat-summarizer/
├── main.py                 # Точка входа
├── config.py               # Конфигурация
├── bot/                    # Модуль бота MAX
├── collector/              # Сбор сообщений
├── preprocessing/          # Предобработка текста
├── summarizer/             # Суммаризация (extractive + abstractive)
├── ranker/                 # Оценка важности сообщений
├── database/               # Работа с SQLite
├── training/               # Обучение ML-моделей
├── tests/                  # Тесты
├── notebooks/              # Jupyter-ноутбуки
└── docs/                   # Документация
```

## 🛠️ Технологии

- **Python 3.11+**
- **maxapi** — библиотека MAX Bot API
- **PyTorch + HuggingFace Transformers** — ML-фреймворк
- **NLTK + NetworkX** — TextRank
- **SQLite (aiosqlite)** — хранилище
- **pytest** — тестирование

## 📊 Метрики качества

| Метрика | Целевое значение |
|---------|------------------|
| ROUGE-1 | ≥ 0.30 |
| ROUGE-L | ≥ 0.25 |
| Время ответа | < 10 сек |
| Покрытие тестами | ≥ 70% |

## 📄 Лицензия

MIT License

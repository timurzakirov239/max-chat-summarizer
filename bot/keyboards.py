"""Inline-клавиатуры для бота MAX."""


def get_main_keyboard() -> dict:
    """Возвращает основную inline-клавиатуру."""
    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": [
                [
                    {"type": "callback", "text": "\ud83d\udcdd Пересказ за 24ч", "payload": "summary_24"},
                    {"type": "callback", "text": "\ud83d\udd1d Топ-5 важных", "payload": "top_5"},
                ],
                [
                    {"type": "callback", "text": "\ud83d\udccb Мои чаты", "payload": "list_chats"},
                    {"type": "callback", "text": "\u2753 Помощь", "payload": "help"},
                ],
            ]
        },
    }


def get_period_keyboard() -> dict:
    """Возвращает клавиатуру выбора периода."""
    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": [
                [
                    {"type": "callback", "text": "1 час", "payload": "summary_1"},
                    {"type": "callback", "text": "6 часов", "payload": "summary_6"},
                    {"type": "callback", "text": "12 часов", "payload": "summary_12"},
                ],
                [
                    {"type": "callback", "text": "24 часа", "payload": "summary_24"},
                    {"type": "callback", "text": "48 часов", "payload": "summary_48"},
                ],
            ]
        },
    }

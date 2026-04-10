# MAX Bot API — Используемые эндпоинты

## Базовый URL

```
https://platform-api.max.ru
```

## Авторизация

Токен передаётся в заголовке:
```
Authorization: <token>
```

> Передача токена через query-параметры больше не поддерживается.

## Эндпоинты

| Метод | URL | Назначение |
|--------|-----|----------|
| `GET` | `/me` | Информация о боте |
| `GET` | `/chats` | Список групповых чатов |
| `GET` | `/chats/{chatId}` | Информация о чате |
| `GET` | `/messages?chat_id={id}&from={ts}&to={ts}&count=100` | Получение сообщений из чата |
| `GET` | `/messages/{messageId}` | Получение одного сообщения |
| `POST` | `/messages` | Отправка сообщения |
| `GET` | `/updates` | Long polling |
| `POST` | `/subscriptions` | Webhook-подписка |
| `POST` | `/answers` | Ответ на callback |

## Rate Limits

- Максимум: **30 RPS** на `platform-api.max.ru`

## Пример запроса сообщений

```bash
curl -X GET "https://platform-api.max.ru/messages?chat_id=123&count=50" \
     -H "Authorization: your_token_here"
```

## Способы получения обновлений

- **Long Polling** (`GET /updates`) — для разработки/тестирования
- **Webhook** (`POST /subscriptions`) — для production (только HTTPS)

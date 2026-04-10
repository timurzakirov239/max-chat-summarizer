"""Схемы таблиц базы данных SQLite."""

CREATE_CHATS_TABLE = """
CREATE TABLE IF NOT EXISTS chats (
    chat_id     INTEGER PRIMARY KEY,
    chat_title  TEXT NOT NULL DEFAULT 'Unknown',
    added_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id         INTEGER NOT NULL REFERENCES chats(chat_id),
    message_id      TEXT UNIQUE NOT NULL,
    sender_id       INTEGER,
    sender_name     TEXT,
    text            TEXT,
    timestamp       INTEGER,
    reply_to_id     TEXT,
    has_attachments BOOLEAN DEFAULT FALSE,
    collected_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_SUMMARIES_TABLE = """
CREATE TABLE IF NOT EXISTS summaries (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id     INTEGER NOT NULL REFERENCES chats(chat_id),
    period_from INTEGER NOT NULL,
    period_to   INTEGER NOT NULL,
    summary     TEXT NOT NULL,
    msg_count   INTEGER DEFAULT 0,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_messages_chat_time ON messages(chat_id, timestamp);",
    "CREATE INDEX IF NOT EXISTS idx_messages_reply ON messages(reply_to_id);",
    "CREATE INDEX IF NOT EXISTS idx_summaries_chat ON summaries(chat_id, period_from);",
]

ALL_DDL = [CREATE_CHATS_TABLE, CREATE_MESSAGES_TABLE, CREATE_SUMMARIES_TABLE, *CREATE_INDEXES]

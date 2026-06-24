"""SQLite-backed memory and conversation history."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(slots=True)
class Message:
    role: str
    content: str
    created_at: str


class SQLiteMemory:
    """Persist conversations, messages, and durable memories in SQLite."""

    def __init__(self, database_path: Path | str) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(conversation_id) REFERENCES conversations(id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    namespace TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(namespace, key)
                )
                """
            )

    def ensure_conversation(self, conversation_id: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO conversations(id, created_at) VALUES (?, ?)",
                (conversation_id, _now()),
            )

    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        self.ensure_conversation(conversation_id)
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages(conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
                (conversation_id, role, content, _now()),
            )

    def get_messages(self, conversation_id: str, limit: int = 20) -> list[Message]:
        self.ensure_conversation(conversation_id)
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT role, content, created_at FROM messages
                WHERE conversation_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (conversation_id, limit),
            ).fetchall()
        return [Message(*row) for row in reversed(rows)]

    def remember(self, namespace: str, key: str, value: str) -> None:
        now = _now()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO memories(namespace, key, value, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(namespace, key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
                """,
                (namespace, key, value, now, now),
            )

    def recall(self, namespace: str, query: str = "", limit: int = 10) -> list[str]:
        pattern = f"%{query}%"
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT key, value FROM memories
                WHERE namespace = ? AND (? = '' OR key LIKE ? OR value LIKE ?)
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (namespace, query, pattern, pattern, limit),
            ).fetchall()
        return [f"{key}: {value}" for key, value in rows]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

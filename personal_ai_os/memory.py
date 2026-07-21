"""SQLite-backed conversation memory."""

from __future__ import annotations

import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class Message:
    """A persisted conversation message."""

    role: str
    content: str
    created_at: str


class SQLiteConversationMemory:
    """Persist conversation history in SQLite."""

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
        logger.debug("SQLite conversation memory initialized at %s", self.database_path)

    def ensure_conversation(self, conversation_id: str) -> None:
        """Create a conversation record if it does not already exist."""
        with self._connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO conversations(id, created_at) VALUES (?, ?)",
                (conversation_id, _now()),
            )

    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        """Persist a message for a conversation."""
        if role not in {"system", "user", "assistant"}:
            raise ValueError(f"Unsupported message role: {role}")
        self.ensure_conversation(conversation_id)
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages(conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
                (conversation_id, role, content, _now()),
            )
        logger.debug("Stored %s message for conversation %s", role, conversation_id)

    def get_messages(self, conversation_id: str, limit: int = 20) -> list[Message]:
        """Return recent conversation messages in chronological order."""
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


SQLiteMemory = SQLiteConversationMemory


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

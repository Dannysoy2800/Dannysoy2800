"""Memory tools exposed to the model."""

from __future__ import annotations

from personal_ai_os.memory import SQLiteMemory


class MemoryTools:
    def __init__(self, memory: SQLiteMemory) -> None:
        self.memory = memory

    def remember(self, namespace: str, key: str, value: str) -> str:
        self.memory.remember(namespace, key, value)
        return f"Stored memory '{key}' in namespace '{namespace}'."

    def recall(self, namespace: str, query: str = "", limit: int = 10) -> str:
        memories = self.memory.recall(namespace, query, limit)
        return "\n".join(memories) if memories else "No matching memories."

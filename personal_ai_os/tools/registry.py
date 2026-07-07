"""Tool registry and OpenAI function schemas."""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from personal_ai_os.memory import SQLiteMemory
from personal_ai_os.tools.files import FileTools
from personal_ai_os.tools.memory import MemoryTools
from personal_ai_os.tools.search import SearchTools

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable[..., str]

    def openai_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "strict": False,
        }


class ToolRegistry:
    """Holds executable tools and converts them to model schemas."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, definition: ToolDefinition) -> None:
        self._tools[definition.name] = definition

    def schemas(self) -> list[dict[str, Any]]:
        return [tool.openai_schema() for tool in self._tools.values()]

    def call(self, name: str, arguments: str | dict[str, Any]) -> str:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        parsed = json.loads(arguments) if isinstance(arguments, str) else arguments
        logger.info("Calling tool %s with keys=%s", name, sorted(parsed))
        return self._tools[name].handler(**parsed)


def build_default_registry(workspace: Path, memory: SQLiteMemory, *, enable_writes: bool = False) -> ToolRegistry:
    files = FileTools(workspace, writes_enabled=enable_writes)
    search = SearchTools()
    memory_tools = MemoryTools(memory)
    registry = ToolRegistry()
    registry.register(ToolDefinition("search_web", "Search the web using DuckDuckGo.", _object_schema({"query": "string", "max_results": "integer"}, ["query"]), search.search_web))
    registry.register(ToolDefinition("read_file", "Read a UTF-8 text file from the configured workspace.", _object_schema({"path": "string"}, ["path"]), files.read_file))
    registry.register(ToolDefinition("write_file", "Write a UTF-8 text file inside the configured workspace.", _object_schema({"path": "string", "content": "string", "approval_id": "string"}, ["path", "content", "approval_id"]), files.write_file))
    registry.register(ToolDefinition("list_files", "List files in a workspace directory.", _object_schema({"path": "string"}, []), files.list_files))
    registry.register(ToolDefinition("remember", "Save a durable memory by namespace and key.", _object_schema({"namespace": "string", "key": "string", "value": "string"}, ["namespace", "key", "value"]), memory_tools.remember))
    registry.register(ToolDefinition("recall", "Recall durable memories by namespace and optional query.", _object_schema({"namespace": "string", "query": "string", "limit": "integer"}, ["namespace"]), memory_tools.recall))
    return registry


def _object_schema(properties: dict[str, str], required: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {name: {"type": kind} for name, kind in properties.items()},
        "required": required,
        "additionalProperties": False,
    }

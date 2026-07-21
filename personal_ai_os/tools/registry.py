"""Tool registry and OpenAI function schemas."""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from personal_ai_os.tools.search import DuckDuckGoSearchTool

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ToolDefinition:
    """A callable tool exposed to an OpenAI Responses API model."""

    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable[..., str]

    def openai_schema(self) -> dict[str, Any]:
        """Return the function schema expected by the Responses API."""
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


class ToolRegistry:
    """Holds executable tools and converts them to model schemas."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, definition: ToolDefinition) -> None:
        """Register a tool definition by name."""
        self._tools[definition.name] = definition

    def schemas(self) -> list[dict[str, Any]]:
        """Return all registered tools as OpenAI-compatible schemas."""
        return [tool.openai_schema() for tool in self._tools.values()]

    def call(self, name: str, arguments: str | dict[str, Any]) -> str:
        """Execute a registered tool with JSON or dictionary arguments."""
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        parsed = json.loads(arguments) if isinstance(arguments, str) else arguments
        logger.info("Calling tool %s", name)
        return self._tools[name].handler(**parsed)


def build_default_registry() -> ToolRegistry:
    """Build the v2 tool registry with DuckDuckGo web search only."""
    search = DuckDuckGoSearchTool()
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="search_web",
            description="Search the web using DuckDuckGo and return titles, URLs, and snippets.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "minimum": 1, "maximum": 10},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
            handler=search.search_web,
        )
    )
    return registry

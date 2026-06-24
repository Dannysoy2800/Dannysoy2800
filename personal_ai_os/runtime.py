"""Runtime assembly for a configured AI operating system."""

from __future__ import annotations

from personal_ai_os.config import Settings, load_settings
from personal_ai_os.memory import SQLiteMemory
from personal_ai_os.providers.openai_responses import OpenAIResponsesAgent
from personal_ai_os.tools import build_default_registry

DEFAULT_SYSTEM_PROMPT = """You are a Personal AI Operating System.
Act as a manager agent that can research, code, write, review, remember preferences,
search the web, and read or write files when useful. Be concise, cite URLs from search
results when you use web information, and ask before destructive file operations.
"""


def build_agent(settings: Settings | None = None) -> OpenAIResponsesAgent:
    settings = settings or load_settings()
    memory = SQLiteMemory(settings.database_path)
    tools = build_default_registry(settings.workspace_path, memory)
    return OpenAIResponsesAgent(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        memory=memory,
        tools=tools,
        max_tool_rounds=settings.max_tool_rounds,
    )

"""Runtime assembly for the OpenAI-powered Personal AI OS."""

from __future__ import annotations

from personal_ai_os.config import Settings, load_settings
from personal_ai_os.memory import SQLiteConversationMemory
from personal_ai_os.providers.openai_responses import OpenAIResponsesAgent
from personal_ai_os.tools import build_default_registry

DEFAULT_SYSTEM_PROMPT = """You are Personal AI OS v2.
Help the user plan, research, code, write, and review work. Use DuckDuckGo search when
fresh web information is needed. Be concise, cite URLs from search results when used,
and preserve useful context through the conversation history.
"""


def build_agent(settings: Settings | None = None) -> OpenAIResponsesAgent:
    """Assemble the OpenAI agent with centralized configuration."""
    settings = settings or load_settings()
    memory = SQLiteConversationMemory(settings.database_path)
    tools = build_default_registry()
    return OpenAIResponsesAgent(
        model=settings.openai_model,
        api_key=settings.require_openai_api_key(),
        memory=memory,
        tools=tools,
        max_tool_rounds=settings.max_tool_rounds,
    )

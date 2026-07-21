from types import SimpleNamespace

import pytest

from personal_ai_os.memory import SQLiteConversationMemory
from personal_ai_os.providers.openai_responses import OpenAIResponsesAgent
from personal_ai_os.tools import ToolRegistry, build_default_registry
from personal_ai_os.tools.registry import ToolDefinition


def test_sqlite_conversation_memory_persists_messages(tmp_path):
    memory = SQLiteConversationMemory(tmp_path / "conversations.sqlite3")
    memory.add_message("c1", "user", "hello")
    memory.add_message("c1", "assistant", "hi")

    messages = memory.get_messages("c1")
    assert [message.role for message in messages] == ["user", "assistant"]
    assert [message.content for message in messages] == ["hello", "hi"]


def test_sqlite_conversation_memory_rejects_unknown_roles(tmp_path):
    memory = SQLiteConversationMemory(tmp_path / "conversations.sqlite3")

    with pytest.raises(ValueError, match="Unsupported message role"):
        memory.add_message("c1", "tool", "not supported")


def test_default_registry_exposes_duckduckgo_search_only():
    registry = build_default_registry()
    schemas = registry.schemas()

    assert [schema["name"] for schema in schemas] == ["search_web"]
    assert schemas[0]["parameters"]["required"] == ["query"]


def test_openai_responses_agent_executes_search_tool_call(tmp_path):
    memory = SQLiteConversationMemory(tmp_path / "conversations.sqlite3")
    tools = ToolRegistry()
    tools.register(
        ToolDefinition(
            name="search_web",
            description="Test search",
            parameters={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            handler=lambda query, max_results=5: f"Result for {query} ({max_results})",
        )
    )
    client = _FakeClient()
    agent = OpenAIResponsesAgent(model="test-model", memory=memory, tools=tools, client=client)

    answer = agent.respond("c1", "search for Python", "system")

    assert answer == "I found one result."
    assert client.tool_output == "Result for Python (5)"
    assert [message.role for message in memory.get_messages("c1")] == ["user", "assistant"]


class _FakeClient:
    def __init__(self):
        self.responses = self
        self.calls = 0
        self.tool_output = None

    def create(self, **kwargs):
        self.calls += 1
        if self.calls == 1:
            return SimpleNamespace(
                id="resp_1",
                output_text="",
                output=[
                    SimpleNamespace(
                        type="function_call",
                        call_id="call_1",
                        name="search_web",
                        arguments='{"query":"Python"}',
                    )
                ],
            )
        self.tool_output = kwargs["input"][0]["output"]
        assert kwargs["input"][0]["type"] == "function_call_output"
        return SimpleNamespace(id="resp_2", output_text="I found one result.", output=[])

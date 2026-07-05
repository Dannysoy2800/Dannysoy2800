from types import SimpleNamespace

import pytest

from personal_ai_os.memory import SQLiteMemory
from personal_ai_os.providers.openai_responses import OpenAIResponsesAgent
from personal_ai_os.tools import build_default_registry


def test_sqlite_memory_persists_messages_and_memories(tmp_path):
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    memory.add_message("c1", "user", "hello")
    memory.remember("profile", "name", "Ada")

    assert memory.get_messages("c1")[0].content == "hello"
    assert memory.recall("profile", "Ada") == ["name: Ada"]


def test_file_tools_are_workspace_scoped(tmp_path):
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    tools = build_default_registry(tmp_path, memory)

    assert "Wrote" in tools.call("write_file", {"path": "note.txt", "content": "hello"})
    assert tools.call("read_file", {"path": "note.txt"}) == "hello"


def test_file_tools_reject_paths_outside_workspace(tmp_path):
    workspace = tmp_path / "workspace"
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    tools = build_default_registry(workspace, memory)

    with pytest.raises(ValueError, match="Path escapes configured workspace"):
        tools.call("write_file", {"path": "../outside.txt", "content": "nope"})

    assert not (tmp_path / "outside.txt").exists()


def test_file_tools_reject_sibling_with_workspace_prefix(tmp_path):
    workspace = tmp_path / "workspace"
    prefixed_sibling = tmp_path / "workspace_evil"
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    tools = build_default_registry(workspace, memory)

    with pytest.raises(ValueError, match="Path escapes configured workspace"):
        tools.call("write_file", {"path": "../workspace_evil/owned.txt", "content": "nope"})

    assert not prefixed_sibling.exists()


def test_openai_responses_agent_executes_tool_call(tmp_path):
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    tools = build_default_registry(tmp_path, memory)
    client = _FakeClient()
    agent = OpenAIResponsesAgent(model="test-model", memory=memory, tools=tools, client=client)

    answer = agent.respond("c1", "remember my name", "system")

    assert answer == "Stored it."
    assert memory.recall("profile", "name") == ["name: Ada"]


class _FakeClient:
    def __init__(self):
        self.responses = self
        self.calls = 0

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
                        name="remember",
                        arguments='{"namespace":"profile","key":"name","value":"Ada"}',
                    )
                ],
            )
        assert kwargs["input"][0]["type"] == "function_call_output"
        return SimpleNamespace(id="resp_2", output_text="Stored it.", output=[])

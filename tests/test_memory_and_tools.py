from types import SimpleNamespace

import pytest

from personal_ai_os.memory import SQLiteMemory
from personal_ai_os.providers.openai_responses import OpenAIResponsesAgent
from personal_ai_os.tools import build_default_registry
from personal_ai_os.tools.files import FileTools


def test_sqlite_memory_persists_messages_and_memories(tmp_path):
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    memory.add_message("c1", "user", "hello")
    memory.remember("profile", "name", "Ada")

    assert memory.get_messages("c1")[0].content == "hello"
    assert memory.recall("profile", "Ada") == ["name: Ada"]


def test_file_tools_read_files_are_workspace_scoped(tmp_path):
    (tmp_path / "note.txt").write_text("hello", encoding="utf-8")
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    tools = build_default_registry(tmp_path, memory)

    assert tools.call("read_file", {"path": "note.txt"}) == "hello"


def test_model_write_file_is_disabled_by_default(tmp_path):
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    tools = build_default_registry(tmp_path, memory)

    with pytest.raises(PermissionError, match="disabled by configuration"):
        tools.call("write_file", {"path": "note.txt", "content": "hello", "approval_id": "anything"})

    assert not (tmp_path / "note.txt").exists()


def test_write_file_requires_prior_approval_when_writes_enabled(tmp_path):
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    tools = build_default_registry(tmp_path, memory, enable_writes=True)

    with pytest.raises(PermissionError, match="requires a prior approval_id"):
        tools.call("write_file", {"path": "note.txt", "content": "hello"})

    assert not (tmp_path / "note.txt").exists()


def test_write_file_rejects_approval_for_different_content(tmp_path):
    files = FileTools(tmp_path, writes_enabled=True)
    approval_id = files.approve_write_file("note.txt", "approved")

    with pytest.raises(PermissionError, match="invalid for the requested write"):
        files.write_file("note.txt", "tampered", approval_id=approval_id)

    assert not (tmp_path / "note.txt").exists()


def test_write_file_accepts_one_time_exact_approval(tmp_path):
    files = FileTools(tmp_path, writes_enabled=True)
    approval_id = files.approve_write_file("note.txt", "hello")

    assert "Wrote" in files.write_file("note.txt", "hello", approval_id=approval_id)
    assert (tmp_path / "note.txt").read_text(encoding="utf-8") == "hello"
    with pytest.raises(PermissionError, match="invalid for the requested write"):
        files.write_file("note.txt", "hello", approval_id=approval_id)


def test_file_tools_reject_paths_outside_workspace(tmp_path):
    workspace = tmp_path / "workspace"
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    tools = build_default_registry(workspace, memory)

    with pytest.raises(ValueError, match="Path escapes configured workspace"):
        tools.call("write_file", {"path": "../outside.txt", "content": "nope", "approval_id": "anything"})

    assert not (tmp_path / "outside.txt").exists()


def test_file_tools_reject_sibling_with_workspace_prefix(tmp_path):
    workspace = tmp_path / "workspace"
    prefixed_sibling = tmp_path / "workspace_evil"
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    tools = build_default_registry(workspace, memory)

    with pytest.raises(ValueError, match="Path escapes configured workspace"):
        tools.call("write_file", {"path": "../workspace_evil/owned.txt", "content": "nope", "approval_id": "anything"})

    assert not prefixed_sibling.exists()


def test_openai_responses_agent_executes_tool_call(tmp_path):
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    tools = build_default_registry(tmp_path, memory)
    client = _FakeClient()
    agent = OpenAIResponsesAgent(model="test-model", memory=memory, tools=tools, client=client)

    answer = agent.respond("c1", "remember my name", "system")

    assert answer == "Stored it."
    assert memory.recall("profile", "name") == ["name: Ada"]


def test_openai_responses_agent_blocks_unapproved_model_write(tmp_path):
    memory = SQLiteMemory(tmp_path / "memory.sqlite3")
    tools = build_default_registry(tmp_path, memory, enable_writes=True)
    client = _FakeWriteClient()
    agent = OpenAIResponsesAgent(model="test-model", memory=memory, tools=tools, client=client)

    answer = agent.respond("c1", "write a file", "system")

    assert answer == "Write blocked."
    assert not (tmp_path / "note.txt").exists()
    assert "requires a prior approval_id" in client.tool_output


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


class _FakeWriteClient:
    def __init__(self):
        self.responses = self
        self.calls = 0
        self.tool_output = ""

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
                        name="write_file",
                        arguments='{"path":"note.txt","content":"hello"}',
                    )
                ],
            )
        self.tool_output = kwargs["input"][0]["output"]
        return SimpleNamespace(id="resp_2", output_text="Write blocked.", output=[])

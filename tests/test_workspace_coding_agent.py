from agents.coding_agent import CodingAgent
from main import main


def test_coding_agent_creates_reads_updates_explains_and_detects_bugs(tmp_path):
    agent = CodingAgent(tmp_path)

    agent.create_file("app.py", "def greet(name):\n    print(name)\n")
    assert agent.read_file("app.py") == "def greet(name):\n    print(name)\n"

    agent.update_file("app.py", "print(name)", "return name")
    assert "return name" in agent.read_file("app.py")
    assert "def greet(name):" in agent.explain_code("app.py")

    agent.update_file("app.py", "def greet(name):", "def greet(name)")
    issues = agent.detect_simple_bugs("app.py")
    assert any("missing a trailing colon" in issue.message for issue in issues)


def test_workspace_code_command_without_action_shows_capabilities(capsys):
    exit_code = main(["code"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Danny Coding Agent is ready" in captured.out
    assert "Capabilities" in captured.out


def test_workspace_code_cli_can_create_and_read_file(tmp_path, capsys):
    exit_code = main(["code", "--workspace", str(tmp_path), "create", "note.py", "print('hi')"])
    assert exit_code == 0
    assert "Created note.py" in capsys.readouterr().out

    exit_code = main(["code", "--workspace", str(tmp_path), "read", "note.py"])
    assert exit_code == 0
    assert "print('hi')" in capsys.readouterr().out

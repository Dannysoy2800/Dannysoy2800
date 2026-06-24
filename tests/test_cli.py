from personal_ai_os.cli import main


def test_research_command_outputs_agent_name(capsys):
    exit_code = main(["research", "plan", "a", "demo"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Research Agent" in captured.out


def test_manager_run_outputs_all_agents(capsys):
    exit_code = main(["run", "build", "an", "ai", "os"])

    captured = capsys.readouterr()
    assert exit_code == 0
    for name in ["Manager Agent", "Research Agent", "Coding Agent", "Writing Agent", "Review Agent"]:
        assert name in captured.out

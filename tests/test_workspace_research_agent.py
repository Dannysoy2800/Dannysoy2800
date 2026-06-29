from agents.research_agent import ResearchAgent, ResearchResult
from main import main


class FakeResearchAgent(ResearchAgent):
    def search_github_repositories(self, query, *, limit=5):
        return [ResearchResult("github", "danny/repo", "https://github.com/danny/repo", f"Repo for {query}")]

    def search_documentation(self, query, *, limit=5):
        return [ResearchResult("docs", "Docs", "https://docs.example.com", f"Docs for {query}")]

    def search_web_pages(self, query, *, limit=5):
        return [ResearchResult("web", "Article", "https://example.com", f"Article about {query}")]


def test_research_agent_searches_all_sources(tmp_path):
    agent = FakeResearchAgent(tmp_path)

    results = agent.search("python agents")

    assert [result.source for result in results] == ["github", "docs", "web"]
    assert results[0].title == "danny/repo"


def test_research_agent_summarizes_and_saves_notes(tmp_path):
    agent = FakeResearchAgent(tmp_path)

    summary = agent.summarize("python agents")
    assert "# Research summary: python agents" in summary
    assert "GitHub" in summary
    assert "Key takeaways" in summary

    path = agent.save("python agents")
    assert path == tmp_path / "memory" / "knowledge" / "python-agents.md"
    saved = path.read_text(encoding="utf-8")
    assert "query: python agents" in saved
    assert "https://github.com/danny/repo" in saved


def test_research_agent_formats_results_when_empty(tmp_path):
    agent = ResearchAgent(tmp_path)

    assert agent.format_results([]) == "No results found."


def test_research_cli_save_uses_workspace_and_writes_note(tmp_path, monkeypatch, capsys):
    class CliResearchAgent(FakeResearchAgent):
        pass

    monkeypatch.setattr("main.ResearchAgent", CliResearchAgent)

    exit_code = main(["research", "--workspace", str(tmp_path), "save", "python agents"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Saved research notes to memory/knowledge/python-agents.md" in captured.out
    assert (tmp_path / "memory" / "knowledge" / "python-agents.md").exists()


def test_research_cli_search_prints_results(tmp_path, monkeypatch, capsys):
    class CliResearchAgent(FakeResearchAgent):
        pass

    monkeypatch.setattr("main.ResearchAgent", CliResearchAgent)

    exit_code = main(["research", "--workspace", str(tmp_path), "search", "python agents"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "[github] danny/repo" in captured.out
    assert "[docs] Docs" in captured.out
    assert "[web] Article" in captured.out

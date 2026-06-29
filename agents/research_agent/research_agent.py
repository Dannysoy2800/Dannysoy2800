"""Local-first Research Agent for Danny AI Workspace.

The agent gathers lightweight research results from GitHub, documentation-focused
web searches, and general web searches. Network access is isolated behind a small
fetcher method so tests can run deterministically without external calls.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote_plus
from urllib.error import URLError
from urllib.request import Request, urlopen
import json
import re


@dataclass(frozen=True)
class ResearchResult:
    """A single research result from GitHub, docs, or the web."""

    source: str
    title: str
    url: str
    snippet: str


class ResearchAgent:
    """Search, summarize, and persist research notes for a workspace."""

    def __init__(self, workspace: str | Path = ".", *, timeout: float = 8.0) -> None:
        self.workspace = Path(workspace).resolve()
        self.timeout = timeout
        self.knowledge_dir = self.workspace / "memory" / "knowledge"

    def search(self, query: str, *, limit: int = 5) -> list[ResearchResult]:
        """Search GitHub repositories, documentation pages, and web pages."""
        results: list[ResearchResult] = []
        results.extend(self.search_github_repositories(query, limit=limit))
        results.extend(self.search_documentation(query, limit=limit))
        results.extend(self.search_web_pages(query, limit=limit))
        return results[: limit * 3]

    def search_github_repositories(self, query: str, *, limit: int = 5) -> list[ResearchResult]:
        """Search GitHub repositories using the public GitHub Search API."""
        url = f"https://api.github.com/search/repositories?q={quote_plus(query)}&per_page={limit}"
        try:
            payload = self._fetch_json(url)
        except (OSError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            return [self._error_result("github", query, exc)]
        results: list[ResearchResult] = []
        for item in payload.get("items", [])[:limit]:
            results.append(
                ResearchResult(
                    source="github",
                    title=item.get("full_name") or item.get("name") or "Untitled repository",
                    url=item.get("html_url", ""),
                    snippet=item.get("description") or "No repository description provided.",
                )
            )
        return results

    def search_documentation(self, query: str, *, limit: int = 5) -> list[ResearchResult]:
        """Search documentation-oriented pages with a documentation-biased query."""
        docs_query = f"{query} documentation OR docs OR guide"
        try:
            return self._search_duckduckgo(docs_query, source="docs", limit=limit)
        except (OSError, URLError, TimeoutError) as exc:
            return [self._error_result("docs", query, exc)]

    def search_web_pages(self, query: str, *, limit: int = 5) -> list[ResearchResult]:
        """Search general web pages."""
        try:
            return self._search_duckduckgo(query, source="web", limit=limit)
        except (OSError, URLError, TimeoutError) as exc:
            return [self._error_result("web", query, exc)]

    def summarize(self, query: str, *, limit: int = 5) -> str:
        """Search and return a compact Markdown summary."""
        results = self.search(query, limit=limit)
        return self.summarize_results(query, results)

    def summarize_results(self, query: str, results: list[ResearchResult]) -> str:
        """Summarize a set of already-collected results as Markdown."""
        if not results:
            return f"# Research summary: {query}\n\nNo results found."

        lines = [f"# Research summary: {query}", ""]
        grouped = self._group_by_source(results)
        for source, source_results in grouped.items():
            display_source = self._display_source(source)
            lines.append(f"## {display_source} results")
            for result in source_results:
                lines.append(f"- [{result.title}]({result.url}) — {result.snippet}")
            lines.append("")

        lines.append("## Key takeaways")
        lines.append(f"- Found {len(results)} total results across {len(grouped)} source types.")
        for source, source_results in grouped.items():
            lines.append(f"- {self._display_source(source)}: {source_results[0].title}")
        return "\n".join(lines).strip()

    def save(self, query: str, *, limit: int = 5) -> Path:
        """Search, summarize, and save notes under memory/knowledge/."""
        summary = self.summarize(query, limit=limit)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        path = self.knowledge_dir / f"{self._slugify(query)}.md"
        timestamp = datetime.now(timezone.utc).isoformat()
        path.write_text(f"---\nquery: {query}\ncreated_at: {timestamp}\n---\n\n{summary}\n", encoding="utf-8")
        return path

    def format_results(self, results: list[ResearchResult]) -> str:
        """Format raw search results for CLI output."""
        if not results:
            return "No results found."
        lines: list[str] = []
        for result in results:
            lines.append(f"[{result.source}] {result.title}\n{result.url}\n{result.snippet}")
        return "\n\n".join(lines)

    def _error_result(self, source: str, query: str, exc: Exception) -> ResearchResult:
        return ResearchResult(
            source=source,
            title=f"{self._display_source(source)} search unavailable",
            url="",
            snippet=f"Could not search for '{query}': {exc}",
        )

    def _search_duckduckgo(self, query: str, *, source: str, limit: int) -> list[ResearchResult]:
        url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
        html = self._fetch_text(url)
        return _DuckDuckGoParser(source=source, limit=limit).parse(html)

    def _fetch_json(self, url: str) -> dict:
        text = self._fetch_text(url, accept="application/vnd.github+json")
        return json.loads(text)

    def _fetch_text(self, url: str, *, accept: str = "text/html") -> str:
        request = Request(url, headers={"User-Agent": "DannyAIWorkspaceResearchAgent/1.0", "Accept": accept})
        with urlopen(request, timeout=self.timeout) as response:  # nosec: workspace research tool
            return response.read().decode("utf-8", errors="replace")

    def _display_source(self, source: str) -> str:
        return "GitHub" if source == "github" else source.title()

    def _group_by_source(self, results: list[ResearchResult]) -> dict[str, list[ResearchResult]]:
        grouped: dict[str, list[ResearchResult]] = {}
        for result in results:
            grouped.setdefault(result.source, []).append(result)
        return grouped

    def _slugify(self, query: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")
        return slug or "research-note"


class _DuckDuckGoParser(HTMLParser):
    """Parse DuckDuckGo HTML result pages into ResearchResult objects."""

    def __init__(self, *, source: str, limit: int) -> None:
        super().__init__()
        self.source = source
        self.limit = limit
        self.results: list[ResearchResult] = []
        self._in_title = False
        self._in_snippet = False
        self._current_url = ""
        self._current_title: list[str] = []
        self._current_snippet: list[str] = []

    def parse(self, html: str) -> list[ResearchResult]:
        self.feed(html)
        self._flush_result()
        return self.results[: self.limit]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get("class", "") or ""
        if tag == "a" and "result__a" in class_name:
            self._flush_result()
            self._in_title = True
            self._current_url = attrs_dict.get("href", "") or ""
            self._current_title = []
            self._current_snippet = []
        elif tag in {"a", "div"} and "result__snippet" in class_name:
            self._in_snippet = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._in_title:
            self._in_title = False
        elif tag in {"a", "div"} and self._in_snippet:
            self._in_snippet = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._current_title.append(data.strip())
        elif self._in_snippet:
            self._current_snippet.append(data.strip())

    def _flush_result(self) -> None:
        if len(self.results) >= self.limit or not self._current_url or not self._current_title:
            return
        title = " ".join(part for part in self._current_title if part).strip()
        snippet = " ".join(part for part in self._current_snippet if part).strip()
        self.results.append(
            ResearchResult(
                source=self.source,
                title=title or "Untitled result",
                url=self._current_url,
                snippet=snippet or "No snippet provided.",
            )
        )
        self._current_url = ""
        self._current_title = []
        self._current_snippet = []

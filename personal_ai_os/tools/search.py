"""Web search tools."""

from __future__ import annotations

class SearchTools:
    """Search the web using DuckDuckGo."""

    def search_web(self, query: str, max_results: int = 5) -> str:
        max_results = max(1, min(max_results, 10))
        try:
            from duckduckgo_search import DDGS
        except ModuleNotFoundError as exc:
            raise RuntimeError("Install dependencies with `pip install -r requirements.txt` to use web search.") from exc
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return "No results found."
        lines = []
        for index, result in enumerate(results, start=1):
            title = result.get("title", "Untitled")
            href = result.get("href", "")
            body = result.get("body", "")
            lines.append(f"{index}. {title}\nURL: {href}\nSnippet: {body}")
        return "\n\n".join(lines)

"""DuckDuckGo web search tool."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class DuckDuckGoSearchTool:
    """Search the web with DuckDuckGo."""

    def search_web(self, query: str, max_results: int = 5) -> str:
        """Return search results as plain text for model consumption."""
        if not query.strip():
            raise ValueError("Search query cannot be empty")
        max_results = max(1, min(max_results, 10))
        try:
            from duckduckgo_search import DDGS
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Install dependencies with `pip install -r requirements.txt` to use DuckDuckGo search."
            ) from exc

        logger.info("Searching DuckDuckGo for query=%r max_results=%s", query, max_results)
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


SearchTools = DuckDuckGoSearchTool

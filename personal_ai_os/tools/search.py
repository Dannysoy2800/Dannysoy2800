"""DuckDuckGo web search tool."""

from __future__ import annotations

import importlib
import importlib.util
import logging

logger = logging.getLogger(__name__)


class DuckDuckGoSearchTool:
    """Search the web with DuckDuckGo."""

    def search_web(self, query: str, max_results: int = 5) -> str:
        """Return search results as plain text for model consumption."""
        if not query.strip():
            raise ValueError("Search query cannot be empty")
        max_results = max(1, min(max_results, 10))
        if importlib.util.find_spec("duckduckgo_search") is None:
            raise RuntimeError(
                "Install dependencies with `pip install -r requirements.txt` to use DuckDuckGo search."
            )

        duckduckgo_module = importlib.import_module("duckduckgo_search")
        logger.info("Searching DuckDuckGo for query=%r max_results=%s", query, max_results)
        with duckduckgo_module.DDGS() as ddgs:
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

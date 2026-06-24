"""Output formatting helpers."""

from __future__ import annotations

from personal_ai_os.agents.base import AgentResult


def render_results(results: list[AgentResult]) -> str:
    """Render one or more agent results as Markdown."""
    return "\n\n---\n\n".join(result.as_markdown() for result in results)

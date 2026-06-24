"""Base agent primitives used by all specialized agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable


@dataclass(slots=True)
class AgentResult:
    """Structured output produced by an agent."""

    agent: str
    summary: str
    artifacts: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )

    def as_markdown(self) -> str:
        """Render the result as readable Markdown."""
        sections = [f"## {self.agent}", self.summary]
        if self.artifacts:
            sections.append("### Artifacts\n" + _bullet_list(self.artifacts))
        if self.next_steps:
            sections.append("### Next steps\n" + _bullet_list(self.next_steps))
        sections.append(f"_Created: {self.created_at}_")
        return "\n\n".join(sections)


class Agent:
    """Base class for deterministic local agents."""

    name = "Agent"
    role = "General purpose assistant"

    def run(self, task: str, context: Iterable[AgentResult] | None = None) -> AgentResult:
        """Execute a task and return structured output."""
        raise NotImplementedError

    def _context_summary(self, context: Iterable[AgentResult] | None) -> str:
        if not context:
            return "No prior context."
        return "\n".join(f"- {item.agent}: {item.summary}" for item in context)


def _bullet_list(items: Iterable[str]) -> str:
    return "\n".join(f"- {item}" for item in items)

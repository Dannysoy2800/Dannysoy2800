"""Research agent for scoping problems and collecting local knowledge."""

from __future__ import annotations

from personal_ai_os.agents.base import Agent, AgentResult


class ResearchAgent(Agent):
    name = "Research Agent"
    role = "Clarifies goals, assumptions, constraints, and information gaps."

    def run(self, task: str, context=None) -> AgentResult:
        keywords = _keywords(task)
        return AgentResult(
            agent=self.name,
            summary=(
                "Research brief prepared for the task. "
                f"Primary focus areas: {', '.join(keywords) or 'general planning'}."
            ),
            artifacts=[
                f"Task statement: {task}",
                "Assumptions: local-first execution, modular design, reproducible CLI workflow.",
                "Open questions: preferred LLM provider, persistence backend, and automation permissions.",
            ],
            next_steps=[
                "Confirm external integrations before adding networked tools.",
                "Convert the brief into implementation tasks.",
            ],
        )


def _keywords(task: str) -> list[str]:
    words = [word.strip(".,:;!?()[]{}").lower() for word in task.split()]
    ignored = {"the", "and", "for", "with", "that", "this", "build", "create", "make"}
    return [word for word in dict.fromkeys(words) if len(word) > 3 and word not in ignored][:6]

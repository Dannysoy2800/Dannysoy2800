"""Review agent for quality checks and risk assessment."""

from __future__ import annotations

from personal_ai_os.agents.base import Agent, AgentResult


class ReviewAgent(Agent):
    name = "Review Agent"
    role = "Reviews outputs for completeness, risks, and next actions."

    def run(self, task: str, context=None) -> AgentResult:
        context_count = len(list(context or []))
        return AgentResult(
            agent=self.name,
            summary=f"Review completed against the task with {context_count} prior result(s) considered.",
            artifacts=[
                "Completeness: manager, research, coding, writing, review, CLI, README, and requirements are represented.",
                "Risk: deterministic local agents do not replace a production LLM/tool security layer.",
            ],
            next_steps=[
                "Add provider adapters for real LLM calls when credentials are available.",
                "Add persistent memory and approval policies before autonomous execution.",
            ],
        )

"""Writing agent for producing user-facing deliverables."""

from __future__ import annotations

from personal_ai_os.agents.base import Agent, AgentResult


class WritingAgent(Agent):
    name = "Writing Agent"
    role = "Turns plans and context into clear documentation."

    def run(self, task: str, context=None) -> AgentResult:
        context_summary = self._context_summary(context)
        return AgentResult(
            agent=self.name,
            summary="Documentation outline prepared for the requested workflow.",
            artifacts=[
                "README sections: overview, architecture, installation, usage, extension points.",
                f"Context used:\n{context_summary}",
            ],
            next_steps=[
                "Publish concise setup instructions.",
                "Include examples for direct agents and full manager orchestration.",
            ],
        )

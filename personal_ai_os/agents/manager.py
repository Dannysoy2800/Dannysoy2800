"""Manager agent that orchestrates the Personal AI OS workflow."""

from __future__ import annotations

from personal_ai_os.agents.base import Agent, AgentResult
from personal_ai_os.agents.coding import CodingAgent
from personal_ai_os.agents.research import ResearchAgent
from personal_ai_os.agents.review import ReviewAgent
from personal_ai_os.agents.writing import WritingAgent


class ManagerAgent(Agent):
    name = "Manager Agent"
    role = "Routes tasks to specialized agents and combines their outputs."

    def __init__(self) -> None:
        self.research = ResearchAgent()
        self.coding = CodingAgent()
        self.writing = WritingAgent()
        self.review = ReviewAgent()

    def run(self, task: str, context=None) -> AgentResult:
        results = self.run_workflow(task)
        return AgentResult(
            agent=self.name,
            summary="Manager workflow completed across research, coding, writing, and review agents.",
            artifacts=[result.as_markdown() for result in results],
            next_steps=["Use individual CLI commands to iterate on any specialized area."],
        )

    def run_workflow(self, task: str) -> list[AgentResult]:
        """Run the full multi-agent workflow in a deliberate order."""
        results: list[AgentResult] = []
        results.append(self.research.run(task))
        results.append(self.coding.run(task, results))
        results.append(self.writing.run(task, results))
        results.append(self.review.run(task, results))
        return results

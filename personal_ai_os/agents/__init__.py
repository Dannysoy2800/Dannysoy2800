"""Agent implementations for the Personal AI Operating System."""

from personal_ai_os.agents.base import Agent, AgentResult
from personal_ai_os.agents.coding import CodingAgent
from personal_ai_os.agents.manager import ManagerAgent
from personal_ai_os.agents.research import ResearchAgent
from personal_ai_os.agents.review import ReviewAgent
from personal_ai_os.agents.writing import WritingAgent

__all__ = [
    "Agent",
    "AgentResult",
    "CodingAgent",
    "ManagerAgent",
    "ResearchAgent",
    "ReviewAgent",
    "WritingAgent",
]

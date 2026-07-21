"""Provider interfaces and shared errors."""

from abc import ABC, abstractmethod

from omnirouter_ai.schemas import ChatRequest, ChatResponse


class ProviderError(RuntimeError):
    """Raised when an upstream provider cannot serve a request."""


class AIProvider(ABC):
    """Abstract interface implemented by all model providers."""

    name: str

    @property
    @abstractmethod
    def is_configured(self) -> bool:
        """Return whether the provider has enough configuration to run."""

    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Send a chat request to the upstream provider."""

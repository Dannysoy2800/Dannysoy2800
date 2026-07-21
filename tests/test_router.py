"""Tests for provider fallback routing."""

import asyncio

from omnirouter_ai.providers.base import AIProvider, ProviderError
from omnirouter_ai.router import AIRouter
from omnirouter_ai.schemas import ChatRequest, ChatResponse


class FakeProvider(AIProvider):
    def __init__(self, name: str, configured: bool = True, fail: bool = False) -> None:
        self.name = name
        self.configured = configured
        self.fail = fail

    @property
    def is_configured(self) -> bool:
        return self.configured

    async def chat(self, request: ChatRequest) -> ChatResponse:
        if self.fail:
            raise ProviderError("temporary failure")
        return ChatResponse(provider=self.name, model=request.model or "fake", content="ok")


def test_router_falls_back_to_next_configured_provider() -> None:
    async def run() -> None:
        router = AIRouter(
            providers=[FakeProvider("first", fail=True), FakeProvider("second")],
            provider_order=["first", "second"],
        )
        request = ChatRequest(messages=[{"role": "user", "content": "hello"}])

        response = await router.chat(request)

        assert response.provider == "second"
        assert response.content == "ok"
        assert response.fallback_attempts == ["first"]

    asyncio.run(run())


def test_router_reports_when_no_provider_can_run() -> None:
    async def run() -> None:
        router = AIRouter(
            providers=[FakeProvider("first", configured=False)],
            provider_order=["first"],
        )
        request = ChatRequest(messages=[{"role": "user", "content": "hello"}])

        try:
            await router.chat(request)
        except ProviderError as exc:
            assert "not configured" in str(exc)
        else:
            raise AssertionError("Expected ProviderError")

    asyncio.run(run())

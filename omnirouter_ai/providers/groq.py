"""Groq provider using its OpenAI-compatible chat completions API."""

import httpx

from omnirouter_ai.config import Settings
from omnirouter_ai.providers.base import AIProvider, ProviderError
from omnirouter_ai.schemas import ChatRequest, ChatResponse


class GroqProvider(AIProvider):
    """Groq chat provider."""

    name = "groq"
    endpoint = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def is_configured(self) -> bool:
        return bool(self.settings.groq_api_key)

    async def chat(self, request: ChatRequest) -> ChatResponse:
        if not self.is_configured:
            raise ProviderError("Groq API key is not configured.")

        model = request.model or self.settings.groq_model
        payload: dict[str, object] = {
            "model": model,
            "messages": [message.model_dump() for message in request.messages],
            "temperature": request.temperature,
        }
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        headers = {"Authorization": f"Bearer {self.settings.groq_api_key}"}
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.post(self.endpoint, json=payload, headers=headers)

        if response.status_code >= 400:
            raise ProviderError(f"Groq request failed with HTTP {response.status_code}.")

        data = response.json()
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("Groq returned an unexpected response shape.") from exc

        return ChatResponse(provider=self.name, model=model, content=content)

"""Google Gemini provider using the Generative Language REST API."""

import httpx

from omnirouter_ai.config import Settings
from omnirouter_ai.providers.base import AIProvider, ProviderError
from omnirouter_ai.schemas import ChatRequest, ChatResponse


class GeminiProvider(AIProvider):
    """Gemini chat provider."""

    name = "gemini"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def is_configured(self) -> bool:
        return bool(self.settings.gemini_api_key)

    async def chat(self, request: ChatRequest) -> ChatResponse:
        if not self.is_configured:
            raise ProviderError("Gemini API key is not configured.")

        model = request.model or self.settings.gemini_model
        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/{model}:generateContent"
        )
        params = {"key": self.settings.gemini_api_key}
        payload: dict[str, object] = {
            "contents": [
                {
                    "role": "model" if message.role == "assistant" else "user",
                    "parts": [{"text": f"{message.role}: {message.content}"}],
                }
                for message in request.messages
                if message.role != "system"
            ],
            "generationConfig": {"temperature": request.temperature},
        }
        system_messages = [message.content for message in request.messages if message.role == "system"]
        if system_messages:
            payload["systemInstruction"] = {
                "parts": [{"text": "\n".join(system_messages)}]
            }
        if request.max_tokens is not None:
            payload["generationConfig"]["maxOutputTokens"] = request.max_tokens  # type: ignore[index]

        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.post(endpoint, json=payload, params=params)

        if response.status_code >= 400:
            raise ProviderError(f"Gemini request failed with HTTP {response.status_code}.")

        data = response.json()
        try:
            content = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("Gemini returned an unexpected response shape.") from exc

        return ChatResponse(provider=self.name, model=model, content=content)

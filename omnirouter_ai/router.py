"""Provider selection and fallback routing."""

from collections.abc import Iterable

from omnirouter_ai.providers.base import AIProvider, ProviderError
from omnirouter_ai.schemas import ChatRequest, ChatResponse


class AIRouter:
    """Route chat requests through configured providers with automatic fallback."""

    def __init__(self, providers: Iterable[AIProvider], provider_order: list[str]) -> None:
        self.providers = {provider.name: provider for provider in providers}
        self.provider_order = provider_order

    def available_providers(self) -> list[str]:
        """Return configured providers in routing order."""

        return [
            name
            for name in self.provider_order
            if name in self.providers and self.providers[name].is_configured
        ]

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Return the first successful provider response."""

        route = [request.provider] if request.provider else self.provider_order
        attempts: list[str] = []
        errors: list[str] = []

        for provider_name in route:
            if not provider_name:
                continue
            provider = self.providers.get(provider_name)
            if provider is None:
                errors.append(f"{provider_name}: provider is not registered")
                attempts.append(provider_name)
                continue
            if not provider.is_configured:
                errors.append(f"{provider_name}: provider is not configured")
                attempts.append(provider_name)
                continue

            try:
                response = await provider.chat(request)
            except ProviderError as exc:
                errors.append(f"{provider_name}: {exc}")
                attempts.append(provider_name)
                continue

            response.fallback_attempts = attempts
            return response

        detail = "; ".join(errors) if errors else "No providers are registered."
        raise ProviderError(f"No provider completed the request. {detail}")

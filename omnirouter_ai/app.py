"""FastAPI application factory."""

from fastapi import Depends, FastAPI, HTTPException, status

from omnirouter_ai.config import Settings, get_settings
from omnirouter_ai.providers import GeminiProvider, GroqProvider, OpenRouterProvider, ProviderError
from omnirouter_ai.router import AIRouter
from omnirouter_ai.schemas import ChatRequest, ChatResponse


def build_router(settings: Settings) -> AIRouter:
    """Create the provider router from application settings."""

    return AIRouter(
        providers=[
            GeminiProvider(settings),
            GroqProvider(settings),
            OpenRouterProvider(settings),
        ],
        provider_order=settings.provider_order,
    )


def create_app() -> FastAPI:
    """Create and configure the FastAPI app."""

    app = FastAPI(
        title="OmniRouter AI",
        description="A provider-agnostic AI router with Gemini, Groq, and OpenRouter fallback.",
        version="0.1.0",
    )

    @app.get("/health")
    async def health(settings: Settings = Depends(get_settings)) -> dict[str, object]:
        router = build_router(settings)
        return {
            "status": "ok",
            "environment": settings.environment,
            "providers": router.available_providers(),
        }

    @app.post("/v1/chat", response_model=ChatResponse)
    async def chat(
        request: ChatRequest, settings: Settings = Depends(get_settings)
    ) -> ChatResponse:
        router = build_router(settings)
        try:
            return await router.chat(request)
        except ProviderError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            ) from exc

    return app


app = create_app()

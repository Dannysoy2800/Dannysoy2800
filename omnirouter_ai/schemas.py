"""API request and response schemas."""

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single chat message."""

    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    """Request body for routed chat completion."""

    messages: list[ChatMessage] = Field(..., min_length=1)
    provider: str | None = Field(default=None, description="Optional preferred provider name.")
    model: str | None = Field(default=None, description="Optional model override.")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, gt=0)


class ChatResponse(BaseModel):
    """Successful routed chat response."""

    provider: str
    model: str
    content: str
    fallback_attempts: list[str] = Field(default_factory=list)

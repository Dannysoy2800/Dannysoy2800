"""OpenAI Responses API provider with local tool execution."""

from __future__ import annotations

import logging
from typing import Any

from personal_ai_os.memory import SQLiteMemory
from personal_ai_os.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


class OpenAIResponsesAgent:
    """Production-oriented OpenAI Responses API agent runtime."""

    def __init__(
        self,
        *,
        model: str,
        memory: SQLiteMemory,
        tools: ToolRegistry,
        api_key: str | None = None,
        max_tool_rounds: int = 6,
        client: Any | None = None,
    ) -> None:
        self.model = model
        self.memory = memory
        self.tools = tools
        self.max_tool_rounds = max_tool_rounds
        if client is not None:
            self.client = client
        else:
            try:
                from openai import OpenAI
            except ModuleNotFoundError as exc:
                raise RuntimeError("Install dependencies with `pip install -r requirements.txt` to use OpenAI mode.") from exc
            self.client = OpenAI(api_key=api_key)

    def respond(self, conversation_id: str, user_message: str, system_prompt: str) -> str:
        """Generate a response, persist history, and execute requested tools."""
        self.memory.add_message(conversation_id, "user", user_message)
        response_input = self._build_input(conversation_id, system_prompt)
        response = self._create_response(response_input)

        for _ in range(self.max_tool_rounds):
            tool_calls = _extract_tool_calls(response)
            if not tool_calls:
                break
            response_input = []
            for call in tool_calls:
                try:
                    output = self.tools.call(call["name"], call.get("arguments") or "{}")
                except Exception as exc:  # Deliberately return tool errors to the model.
                    logger.exception("Tool call failed: %s", call["name"])
                    output = f"Tool error: {exc}"
                response_input.append(
                    {
                        "type": "function_call_output",
                        "call_id": call["call_id"],
                        "output": output,
                    }
                )
            response = self._create_response(response_input, previous_response_id=response.id)

        assistant_text = _response_text(response)
        self.memory.add_message(conversation_id, "assistant", assistant_text)
        return assistant_text

    def _build_input(self, conversation_id: str, system_prompt: str) -> list[dict[str, str]]:
        messages = [{"role": "system", "content": system_prompt}]
        for message in self.memory.get_messages(conversation_id):
            messages.append({"role": message.role, "content": message.content})
        return messages

    def _create_response(self, input_items: list[dict[str, Any]], previous_response_id: str | None = None) -> Any:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "input": input_items,
            "tools": self.tools.schemas(),
        }
        if previous_response_id:
            kwargs["previous_response_id"] = previous_response_id
        logger.info("Creating OpenAI response model=%s previous=%s", self.model, bool(previous_response_id))
        return self.client.responses.create(**kwargs)


def _extract_tool_calls(response: Any) -> list[dict[str, str]]:
    calls: list[dict[str, str]] = []
    for item in getattr(response, "output", []) or []:
        item_type = _get(item, "type")
        if item_type == "function_call":
            calls.append(
                {
                    "call_id": _get(item, "call_id") or _get(item, "id"),
                    "name": _get(item, "name"),
                    "arguments": _get(item, "arguments") or "{}",
                }
            )
    return calls


def _response_text(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if text:
        return text
    chunks: list[str] = []
    for item in getattr(response, "output", []) or []:
        for content in _get(item, "content") or []:
            value = _get(content, "text")
            if value:
                chunks.append(value)
    return "\n".join(chunks).strip()


def _get(item: Any, key: str) -> Any:
    if isinstance(item, dict):
        return item.get(key)
    return getattr(item, key, None)

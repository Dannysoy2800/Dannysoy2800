"""Tool implementations exposed to AI agents."""

from personal_ai_os.tools.registry import ToolRegistry, build_default_registry
from personal_ai_os.tools.search import DuckDuckGoSearchTool

__all__ = ["DuckDuckGoSearchTool", "ToolRegistry", "build_default_registry"]

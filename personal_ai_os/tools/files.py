"""Workspace-scoped file tools."""

from __future__ import annotations

from pathlib import Path


class FileTools:
    """Read and write files below a configured workspace directory."""

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()

    def read_file(self, path: str) -> str:
        target = self._safe_path(path)
        return target.read_text(encoding="utf-8")

    def write_file(self, path: str, content: str) -> str:
        target = self._safe_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} characters to {target.relative_to(self.workspace)}"

    def list_files(self, path: str = ".") -> str:
        target = self._safe_path(path)
        if target.is_file():
            return str(target.relative_to(self.workspace))
        files = sorted(p.relative_to(self.workspace).as_posix() for p in target.iterdir())
        return "\n".join(files)

    def _safe_path(self, path: str) -> Path:
        target = (self.workspace / path).resolve()
        try:
            target.relative_to(self.workspace)
        except ValueError as exc:
            raise ValueError("Path escapes configured workspace") from exc
        return target

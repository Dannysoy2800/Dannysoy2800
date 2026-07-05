"""Workspace-scoped file tools."""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WriteApproval:
    """Approval for one exact write operation."""

    token: str
    path: str
    content: str


class FileTools:
    """Read and write files below a configured workspace directory."""

    def __init__(self, workspace: Path, *, writes_enabled: bool = False) -> None:
        self.workspace = workspace.resolve()
        self.writes_enabled = writes_enabled
        self._approvals: dict[str, WriteApproval] = {}

    def read_file(self, path: str) -> str:
        target = self._safe_path(path)
        return target.read_text(encoding="utf-8")

    def approve_write_file(self, path: str, content: str) -> str:
        """Create a one-time approval token for an exact write operation."""
        if not self.writes_enabled:
            raise PermissionError("Model-triggered file writes are disabled by configuration")
        self._safe_path(path)
        token = secrets.token_urlsafe(32)
        self._approvals[token] = WriteApproval(token=token, path=path, content=content)
        return token

    def write_file(self, path: str, content: str, approval_id: str | None = None) -> str:
        target = self._safe_path(path)
        self._require_write_approval(path, content, approval_id)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} characters to {target.relative_to(self.workspace)}"

    def list_files(self, path: str = ".") -> str:
        target = self._safe_path(path)
        if target.is_file():
            return str(target.relative_to(self.workspace))
        files = sorted(p.relative_to(self.workspace).as_posix() for p in target.iterdir())
        return "\n".join(files)

    def _require_write_approval(self, path: str, content: str, approval_id: str | None) -> None:
        if not self.writes_enabled:
            raise PermissionError("Model-triggered file writes are disabled by configuration")
        if not approval_id:
            raise PermissionError("write_file requires a prior approval_id for the exact path and content")
        approval = self._approvals.pop(approval_id, None)
        if approval is None or approval.path != path or approval.content != content:
            raise PermissionError("write_file approval_id is invalid for the requested write")

    def _safe_path(self, path: str) -> Path:
        target = (self.workspace / path).resolve()
        try:
            target.relative_to(self.workspace)
        except ValueError as exc:
            raise ValueError("Path escapes configured workspace") from exc
        return target

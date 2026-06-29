"""A small, local-first coding agent for Danny AI Workspace.

The agent intentionally avoids shell execution and network access. It focuses on
safe, workspace-scoped file operations plus lightweight code explanation and bug
heuristics that are useful before handing work to a larger model or a human.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CodeIssue:
    """A simple issue detected in a source file."""

    line: int
    message: str


class CodingAgent:
    """Read, create, update, explain, and inspect files inside a workspace."""

    TEXT_EXTENSIONS = {
        ".css",
        ".html",
        ".js",
        ".json",
        ".md",
        ".py",
        ".toml",
        ".txt",
        ".yaml",
        ".yml",
    }

    def __init__(self, workspace: str | Path = ".") -> None:
        self.workspace = Path(workspace).resolve()

    def read_file(self, relative_path: str) -> str:
        """Return the UTF-8 contents of a workspace file."""
        path = self._resolve(relative_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {relative_path}")
        return path.read_text(encoding="utf-8")

    def create_file(self, relative_path: str, content: str, *, overwrite: bool = False) -> Path:
        """Create a new UTF-8 file, making parent directories as needed."""
        path = self._resolve(relative_path)
        if path.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {relative_path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def update_file(self, relative_path: str, old: str, new: str) -> Path:
        """Replace text in an existing file."""
        content = self.read_file(relative_path)
        if old not in content:
            raise ValueError(f"Text to replace was not found in {relative_path}")
        path = self._resolve(relative_path)
        path.write_text(content.replace(old, new, 1), encoding="utf-8")
        return path

    def explain_code(self, relative_path: str) -> str:
        """Return a short explanation of the file based on lightweight parsing."""
        content = self.read_file(relative_path)
        lines = content.splitlines()
        definitions = [line.strip() for line in lines if line.lstrip().startswith(("def ", "class "))]
        imports = [line.strip() for line in lines if line.lstrip().startswith(("import ", "from "))]

        summary = [f"{relative_path} has {len(lines)} lines."]
        if imports:
            summary.append(f"It imports: {', '.join(imports[:5])}.")
        if definitions:
            summary.append(f"It defines: {', '.join(definitions[:8])}.")
        if not imports and not definitions:
            summary.append("No Python imports, functions, or classes were detected by the simple analyzer.")
        return " ".join(summary)

    def detect_simple_bugs(self, relative_path: str) -> list[CodeIssue]:
        """Detect simple, language-agnostic and Python-focused code smells."""
        content = self.read_file(relative_path)
        issues: list[CodeIssue] = []
        bracket_pairs = {"(": ")", "[": "]", "{": "}"}
        stack: list[tuple[str, int]] = []

        for line_number, line in enumerate(content.splitlines(), start=1):
            stripped = line.strip()
            if "TODO" in line or "FIXME" in line:
                issues.append(CodeIssue(line_number, "Unresolved TODO/FIXME marker."))
            if stripped.startswith("print("):
                issues.append(CodeIssue(line_number, "Debug print statement may need logging or removal."))
            starts_python_block = stripped.startswith(
                ("def ", "class ", "if ", "elif ", "else", "for ", "while ", "try", "except", "finally", "with ")
            )
            if starts_python_block and not stripped.endswith(":"):
                issues.append(CodeIssue(line_number, "Python block statement may be missing a trailing colon."))
            for char in line:
                if char in bracket_pairs:
                    stack.append((char, line_number))
                elif char in bracket_pairs.values():
                    if not stack or bracket_pairs[stack[-1][0]] != char:
                        issues.append(CodeIssue(line_number, f"Unmatched closing bracket '{char}'."))
                    else:
                        stack.pop()

        for bracket, line_number in stack:
            issues.append(CodeIssue(line_number, f"Unclosed bracket '{bracket}'."))
        return issues

    def list_project_files(self) -> list[str]:
        """List readable project files under the workspace."""
        files: list[str] = []
        for path in self.workspace.rglob("*"):
            if path.is_file() and self._is_text_project_file(path):
                files.append(path.relative_to(self.workspace).as_posix())
        return sorted(files)

    def _resolve(self, relative_path: str) -> Path:
        path = (self.workspace / relative_path).resolve()
        if path != self.workspace and self.workspace not in path.parents:
            raise ValueError(f"Path escapes workspace: {relative_path}")
        return path

    def _is_text_project_file(self, path: Path) -> bool:
        ignored_parts = {".git", "__pycache__", ".pytest_cache", ".venv"}
        return not ignored_parts.intersection(path.parts) and path.suffix in self.TEXT_EXTENSIONS

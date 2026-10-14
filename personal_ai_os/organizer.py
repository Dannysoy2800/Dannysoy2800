"""Safe, suggestion-first file organization for a single directory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


_CATEGORY_BY_SUFFIX = {
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"},
    "Archives": {".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar"},
    "Source": {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".c", ".cpp", ".h", ".css", ".html", ".json", ".yaml", ".yml"},
    "Audio": {".mp3", ".wav", ".flac", ".m4a", ".ogg"},
    "Video": {".mp4", ".mov", ".mkv", ".avi", ".webm"},
}


@dataclass(frozen=True)
class OrganizationSuggestion:
    """A proposed file move and the explanation shown to the user."""

    source: Path
    destination: Path
    category: str
    confidence: int


class FileOrganizer:
    """Create deterministic organization suggestions and apply them on request."""

    def suggest(self, directory: str | Path) -> list[OrganizationSuggestion]:
        """Suggest destinations for regular, non-hidden files directly in *directory*."""
        directory = Path(directory).expanduser().resolve()
        if not directory.is_dir():
            raise ValueError(f"Organization path is not a directory: {directory}")

        suggestions: list[OrganizationSuggestion] = []
        for source in sorted(directory.iterdir(), key=lambda item: item.name.lower()):
            if not source.is_file() or source.is_symlink() or source.name.startswith("."):
                continue
            category = self._category_for(source)
            destination = self._available_destination(directory / category / source.name)
            suggestions.append(
                OrganizationSuggestion(
                    source=source,
                    destination=destination,
                    category=category,
                    confidence=94 if category != "Other" else 62,
                )
            )
        return suggestions

    def apply(self, suggestions: list[OrganizationSuggestion]) -> list[OrganizationSuggestion]:
        """Move exactly the suggested files, creating category directories as needed."""
        for suggestion in suggestions:
            if not suggestion.source.is_file():
                raise FileNotFoundError(f"Source file no longer exists: {suggestion.source}")
            if suggestion.destination.exists():
                raise FileExistsError(f"Destination already exists: {suggestion.destination}")

        for suggestion in suggestions:
            suggestion.destination.parent.mkdir(parents=True, exist_ok=True)
            suggestion.source.rename(suggestion.destination)
        return suggestions

    @staticmethod
    def _category_for(path: Path) -> str:
        suffix = path.suffix.lower()
        for category, suffixes in _CATEGORY_BY_SUFFIX.items():
            if suffix in suffixes:
                return category
        return "Other"

    @staticmethod
    def _available_destination(destination: Path) -> Path:
        """Return a non-existing destination without overwriting any file."""
        if not destination.exists():
            return destination
        for index in range(2, 10_000):
            candidate = destination.with_name(f"{destination.stem} ({index}){destination.suffix}")
            if not candidate.exists():
                return candidate
        raise RuntimeError(f"Could not find an available filename for {destination.name}")


def render_organization_report(suggestions: list[OrganizationSuggestion], *, applied: bool) -> str:
    """Render playful but deterministic Hindi recommendations for terminal output."""
    if not suggestions:
        return "🧪 प्रयोग पूरा हुआ: व्यवस्थित करने के लिए कोई फ़ाइल नहीं मिली।"

    heading = "🧪 प्रयोग लागू किया गया:" if applied else "🧪 वैज्ञानिक अनुमान (कोई फ़ाइल नहीं बदली गई):"
    lines = [heading]
    for suggestion in suggestions:
        lines.append(
            "⚛️ "
            f"{suggestion.source.name} → {suggestion.destination.relative_to(suggestion.source.parent)} "
            f"| {suggestion.category} | विश्वास: {suggestion.confidence}%"
        )
    if not applied:
        lines.append("\nपरिकल्पना स्वीकार करने के लिए यही कमांड `--apply` के साथ चलाएँ।")
    return "\n".join(lines)

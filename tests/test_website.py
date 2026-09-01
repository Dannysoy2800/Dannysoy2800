from html.parser import HTMLParser
from pathlib import Path


class _AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stylesheets: list[str] = []
        self.scripts: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if "id" in attrs_dict:
            self.ids.add(attrs_dict["id"])
        if tag == "link" and attrs_dict.get("rel") == "stylesheet":
            href = attrs_dict.get("href")
            if href:
                self.stylesheets.append(href)
        if tag == "script":
            src = attrs_dict.get("src")
            if src:
                self.scripts.append(src)


def test_static_website_references_existing_local_assets():
    root = Path(__file__).resolve().parents[1]
    parser = _AssetParser()
    parser.feed((root / "index.html").read_text(encoding="utf-8"))

    local_assets = [*parser.stylesheets, *parser.scripts]
    assert "assets/styles.css" in local_assets
    assert "assets/site.js" in local_assets
    for asset in local_assets:
        if not asset.startswith("http"):
            assert (root / asset).is_file()


def test_static_website_contains_primary_sections():
    root = Path(__file__).resolve().parents[1]
    parser = _AssetParser()
    parser.feed((root / "index.html").read_text(encoding="utf-8"))

    assert {"home", "projects", "skills", "contact"}.issubset(parser.ids)

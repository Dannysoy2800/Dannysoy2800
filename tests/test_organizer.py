from personal_ai_os.cli import main
from personal_ai_os.organizer import FileOrganizer


def test_suggest_groups_known_types_without_changing_files(tmp_path):
    (tmp_path / "report.pdf").write_text("report", encoding="utf-8")
    (tmp_path / "photo.PNG").write_text("photo", encoding="utf-8")
    (tmp_path / "mystery.bin").write_text("data", encoding="utf-8")

    suggestions = FileOrganizer().suggest(tmp_path)

    assert [(item.source.name, item.destination.relative_to(tmp_path).as_posix(), item.confidence) for item in suggestions] == [
        ("mystery.bin", "Other/mystery.bin", 62),
        ("photo.PNG", "Images/photo.PNG", 94),
        ("report.pdf", "Documents/report.pdf", 94),
    ]
    assert (tmp_path / "report.pdf").exists()


def test_apply_uses_numbered_destination_when_category_has_same_name(tmp_path):
    (tmp_path / "report.pdf").write_text("new", encoding="utf-8")
    existing = tmp_path / "Documents" / "report.pdf"
    existing.parent.mkdir()
    existing.write_text("old", encoding="utf-8")

    organizer = FileOrganizer()
    suggestions = organizer.suggest(tmp_path)
    organizer.apply(suggestions)

    assert not (tmp_path / "report.pdf").exists()
    assert (tmp_path / "Documents" / "report (2).pdf").read_text(encoding="utf-8") == "new"
    assert existing.read_text(encoding="utf-8") == "old"


def test_cli_organize_is_a_dry_run_by_default(tmp_path, capsys):
    source = tmp_path / "notes.txt"
    source.write_text("notes", encoding="utf-8")

    exit_code = main(["organize", str(tmp_path)])

    assert exit_code == 0
    assert source.exists()
    assert "कोई फ़ाइल नहीं बदली गई" in capsys.readouterr().out


def test_cli_organize_apply_moves_files(tmp_path, capsys):
    source = tmp_path / "notes.txt"
    source.write_text("notes", encoding="utf-8")

    exit_code = main(["organize", str(tmp_path), "--apply"])

    assert exit_code == 0
    assert not source.exists()
    assert (tmp_path / "Documents" / "notes.txt").read_text(encoding="utf-8") == "notes"
    assert "प्रयोग लागू किया गया" in capsys.readouterr().out

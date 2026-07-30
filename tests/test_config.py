from personal_ai_os.config import load_settings


def test_load_settings_reads_env_file_without_overwriting_existing_env(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=from-file\nOPENAI_MODEL=test-model\n", encoding="utf-8")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_MODEL", "from-env")

    settings = load_settings(env_file)

    assert settings.openai_api_key == "from-file"
    assert settings.openai_model == "from-env"

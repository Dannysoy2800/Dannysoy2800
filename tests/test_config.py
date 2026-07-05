from personal_ai_os.config import load_settings


def test_model_writes_disabled_by_default(tmp_path, monkeypatch):
    monkeypatch.delenv("PAI_ENABLE_MODEL_WRITES", raising=False)
    settings = load_settings()

    assert settings.enable_model_writes is False


def test_model_writes_can_be_explicitly_enabled(tmp_path, monkeypatch):
    monkeypatch.setenv("PAI_ENABLE_MODEL_WRITES", "true")
    settings = load_settings()

    assert settings.enable_model_writes is True

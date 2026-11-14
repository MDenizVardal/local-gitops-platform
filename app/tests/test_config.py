import pytest

from shortener.config import load_settings

REQUIRED = {
    "REDIS_URL": "redis://localhost:6379/0",
    "BASE_URL": "http://localhost:8080/",
    "APP_VERSION": "abc123",
}


def test_load_settings_reads_all_variables(monkeypatch):
    for name, value in REQUIRED.items():
        monkeypatch.setenv(name, value)

    settings = load_settings()

    assert settings.redis_url == "redis://localhost:6379/0"
    assert settings.base_url == "http://localhost:8080"
    assert settings.app_version == "abc123"


@pytest.mark.parametrize("missing", REQUIRED)
def test_load_settings_fails_when_a_variable_is_missing(monkeypatch, missing):
    for name, value in REQUIRED.items():
        monkeypatch.setenv(name, value)
    monkeypatch.delenv(missing)

    with pytest.raises(KeyError, match=missing):
        load_settings()

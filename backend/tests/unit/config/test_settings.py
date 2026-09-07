from app.config.settings import Settings


def test_default_settings() -> None:
    settings = Settings()

    assert settings.background_max_queue_size == 1000
    assert settings.background_max_retries == 3
    assert settings.background_retry_delay == 0.1
    assert settings.background_shutdown_timeout == 30.0


def test_settings_can_be_loaded_from_environment(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "BACKGROUND_MAX_QUEUE_SIZE",
        "5000",
    )
    monkeypatch.setenv(
        "BACKGROUND_MAX_RETRIES",
        "5",
    )
    monkeypatch.setenv(
        "BACKGROUND_RETRY_DELAY",
        "0.5",
    )
    monkeypatch.setenv(
        "BACKGROUND_SHUTDOWN_TIMEOUT",
        "60",
    )

    settings = Settings.from_environment()

    assert settings.background_max_queue_size == 5000
    assert settings.background_max_retries == 5
    assert settings.background_retry_delay == 0.5
    assert settings.background_shutdown_timeout == 60.0
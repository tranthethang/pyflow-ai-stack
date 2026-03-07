from pyflow_ai_stack.core.config import Settings
from pyflow_ai_stack.services.configs import GeminiConfig, RedisConfig, S3Config


def test_settings_load_default(monkeypatch):
    """Test loading settings with defaults."""
    # Ensure environment variables do not interfere with the test
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    monkeypatch.delenv("REDIS_HOST", raising=False)

    settings = Settings.load()
    assert settings.REDIS_HOST == "localhost"
    assert settings.GEMINI_MODEL == "gemini-2.0-flash"


def test_settings_load_with_env_file(tmp_path):
    """Test loading settings from a temporary .env file."""
    env_file = tmp_path / ".env"
    env_file.write_text("REDIS_HOST=test_host\nGEMINI_API_KEY=test_key")

    settings = Settings.load(env_file=str(env_file))
    assert settings.REDIS_HOST == "test_host"
    assert settings.GEMINI_API_KEY == "test_key"


def test_settings_properties():
    """Test the configuration properties of the Settings class."""
    settings = Settings(
        GEMINI_API_KEY="test_key", REDIS_HOST="redis_host", S3_BUCKET_NAME="test_bucket"
    )

    assert isinstance(settings.gemini, GeminiConfig)
    assert settings.gemini.api_key == "test_key"

    assert isinstance(settings.redis, RedisConfig)
    assert settings.redis.host == "redis_host"

    assert isinstance(settings.s3, S3Config)
    assert settings.s3.bucket_name == "test_bucket"


def test_settings_customise_sources():
    """Test that settings_customise_sources returns the expected sources."""
    # This is more of a structural check to ensure the method exists and returns a tuple
    sources = Settings.settings_customise_sources(
        Settings,
        init_settings=lambda x: x,
        env_settings=lambda x: x,
        dotenv_settings=lambda x: x,
        file_secret_settings=lambda x: x,
    )
    assert len(sources) == 4

"""
Configuration management module for the PyFlow AI Stack library.
"""

from typing import Optional, Tuple, Type

from pydantic import AliasChoices, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from pyflow_ai_stack.services.configs import GeminiConfig, RedisConfig, S3Config


class Settings(BaseSettings):
    """
    Library settings class using Pydantic Settings.
    """

    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def load(cls, **kwargs) -> "Settings":
        """
        Factory method to load settings from environment variables and optionally a .env file.
        """
        env_file = kwargs.pop("env_file", None)
        if env_file:
            # Pass _env_file only if provided to avoid potential 'unexpected keyword argument'
            # in some environments/versions of pydantic-settings.
            return cls(_env_file=env_file, **kwargs)
        return cls(**kwargs)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, dotenv_settings, env_settings, file_secret_settings

    # Gemini API Configuration
    GEMINI_API_KEY: Optional[str] = Field(
        default=None, validation_alias=AliasChoices("GEMINI_API_KEY", "GOOGLE_API_KEY")
    )
    GEMINI_MODEL: str = "gemini-2.0-flash"
    CONCURRENCY_LIMIT: int = 5

    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "ap-southeast-1"
    S3_BUCKET_NAME: Optional[str] = None
    S3_ENDPOINT_URL: Optional[str] = None

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0

    @property
    def gemini(self) -> GeminiConfig:
        """Get Gemini service configuration."""
        return GeminiConfig(
            api_key=self.GEMINI_API_KEY,
            model_name=self.GEMINI_MODEL,
            concurrency_limit=self.CONCURRENCY_LIMIT,
        )

    @property
    def redis(self) -> RedisConfig:
        """Get Redis service configuration."""
        return RedisConfig(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            password=self.REDIS_PASSWORD,
            db=self.REDIS_DB,
        )

    @property
    def s3(self) -> S3Config:
        """Get S3 service configuration."""
        return S3Config(
            access_key_id=self.AWS_ACCESS_KEY_ID,
            secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region=self.AWS_REGION,
            bucket_name=self.S3_BUCKET_NAME,
            endpoint_url=self.S3_ENDPOINT_URL,
        )

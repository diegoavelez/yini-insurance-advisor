"""Typed application settings and startup validation for Yini."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized environment-driven application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    groq_api_key: SecretStr | None = None
    groq_model: str = "gpt-oss-120b"
    qdrant_url: str | None = None
    qdrant_api_key: SecretStr | None = None
    qdrant_collection: str = "yini-policies"
    embedding_provider: str = "sentence-transformers"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    phoenix_project_name: str = "yini-local"
    phoenix_endpoint: str | None = None
    app_env: Literal["development", "test", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    max_input_chars: int = Field(default=4000, ge=1, le=20000)
    top_k: int = Field(default=5, ge=1, le=20)

    @field_validator("app_env", "log_level", mode="before")
    @classmethod
    def strip_enum_strings(cls, value: str | None) -> str | None:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator(
        "groq_api_key",
        "qdrant_api_key",
        "qdrant_url",
        "phoenix_endpoint",
        mode="before",
    )
    @classmethod
    def normalize_blank_optional_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped_value = value.strip()
        return stripped_value or None

    @field_validator(
        "groq_model",
        "qdrant_collection",
        "embedding_provider",
        "embedding_model",
        "phoenix_project_name",
        mode="before",
    )
    @classmethod
    def validate_non_empty_strings(cls, value: str) -> str:
        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("must not be blank")
        return stripped_value

    def validate_startup(
        self,
        *,
        require_groq: bool = False,
        require_qdrant: bool = False,
        require_phoenix: bool = False,
    ) -> "Settings":
        """Validate boot-time requirements for the currently enabled features."""

        if require_groq and self.groq_api_key is None:
            raise ValueError("GROQ_API_KEY is required when Groq usage is enabled.")
        if require_qdrant:
            if self.qdrant_url is None:
                raise ValueError("QDRANT_URL is required when Qdrant usage is enabled.")
            if self.qdrant_api_key is None:
                raise ValueError("QDRANT_API_KEY is required when Qdrant usage is enabled.")
        if require_phoenix and self.phoenix_endpoint is None:
            raise ValueError("PHOENIX_ENDPOINT is required when Phoenix usage is enabled.")
        return self


def validate_startup_settings(
    settings: Settings,
    *,
    require_groq: bool = False,
    require_qdrant: bool = False,
    require_phoenix: bool = False,
) -> Settings:
    """Validate startup requirements through the centralized configuration seam."""

    return settings.validate_startup(
        require_groq=require_groq,
        require_qdrant=require_qdrant,
        require_phoenix=require_phoenix,
    )


def clear_settings_cache() -> None:
    """Clear the cached settings instance for tests and process resets."""

    get_settings.cache_clear()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()

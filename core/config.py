"""Typed application settings for the Phase 0 scaffold."""

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

    @field_validator(
        "qdrant_url",
        "phoenix_endpoint",
        "embedding_provider",
        "embedding_model",
        "qdrant_collection",
        mode="before",
    )
    @classmethod
    def normalize_blank_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped_value = value.strip()
        return stripped_value or None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()

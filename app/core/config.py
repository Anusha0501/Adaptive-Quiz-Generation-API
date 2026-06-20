from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Adaptive Quiz Generation API"
    environment: str = "local"
    database_url: str = "sqlite+aiosqlite:///./quiz.db"
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    chroma_path: str = ".chroma"
    similarity_threshold: float = Field(0.85, ge=0, le=1)
    rate_limit_per_minute: int = Field(30, ge=1)


@lru_cache
def get_settings() -> Settings:
    return Settings()

from typing import Any, Dict, Optional
from pydantic import BaseSettings, Field, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    API_KEY: str = Field(..., env="NOVA_API_KEY")

    POSTGRES_SERVER: str = Field(..., env="NOVA_POSTGRES_SERVER")
    POSTGRES_USER: str = Field(..., env="NOVA_POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="NOVA_POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="NOVA_POSTGRES_DB")
    POSTGRES_PORT: str = Field(..., env="NOVA_POSTGRES_PORT")
    DATABASE_URI: Optional[PostgresDsn] = None
    BOT_TOKEN: str = Field(..., env="NOVA_DISCORD_BOT_TOKEN")
    SERVER_ID: int = Field(..., env="NOVA_SERVER_ID")

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
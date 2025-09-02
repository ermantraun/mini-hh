from pydantic import BaseModel, Field
from functools import lru_cache
import os


class PostgresConfig(BaseModel):
    host: str = Field(default="db")
    port: int = Field(default=5432)
    user: str = Field(default="resume")
    password: str = Field(default="resume")
    database: str = Field(default="resume")

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class JWTConfig(BaseModel):
    secret_key: str = Field(default="change_me")
    algorithm: str = Field(default="HS256")
    access_minutes: int = Field(default=60 * 24)


class AppConfig(BaseModel):
    title: str = "Resume Service"
    version: str = "1.0.0"
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"


class Config(BaseModel):
    postgres: PostgresConfig
    jwt: JWTConfig
    app: AppConfig
    log_level: str = "INFO"


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


@lru_cache
def get_config() -> Config:
    return Config(
        postgres=PostgresConfig(
            host=_env("POSTGRES_HOST", "db"),
            port=int(_env("POSTGRES_PORT", "5432")),
            user=_env("POSTGRES_USER", "resume"),
            password=_env("POSTGRES_PASSWORD", "resume"),
            database=_env("POSTGRES_DB", "resume"),
        ),
        jwt=JWTConfig(
            secret_key=_env("JWT_SECRET_KEY", "change_me"),
            algorithm=_env("JWT_ALGORITHM", "HS256"),
            access_minutes=int(_env("ACCESS_TOKEN_EXPIRE_MINUTES", str(60 * 24))),
        ),
        app=AppConfig(),
        log_level=_env("LOG_LEVEL", "INFO"),
    )
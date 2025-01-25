import os
from typing import Literal

from pydantic import BaseModel


class APIConfig(BaseModel):
    PORT: int
    LOG_LEVEL: Literal["critical", "error", "warning", "info", "debug", "trace"]
    RELOAD: bool


class DataBaseConfig(BaseModel):
    USER: str
    PASSWORD: str
    HOST: str
    DATABASE: str
    PORT: int
    URL: str


class ServerConfig(BaseModel):
    api: APIConfig
    database: DataBaseConfig


def get_config() -> ServerConfig:
    return ServerConfig(
        api=APIConfig(
            PORT=int(os.environ.get("SERVICE_PORT", 8080)),
            LOG_LEVEL=os.environ.get("LOG_LEVEL", "info"),
            RELOAD=os.environ.get("RELOAD", "false").lower() == "true",
        ),
        database=DataBaseConfig(
            USER=os.environ.get("POSTGRES_USER"),
            PASSWORD=os.environ.get("POSTGRES_PASSWORD"),
            HOST=os.environ.get("POSTGRES_HOST"),
            DATABASE=os.environ.get("POSTGRES_DB"),
            PORT=int(os.environ.get("POSTGRES_PORT")),
            URL=os.environ.get("DATABASE_URL"),
        ),
    )

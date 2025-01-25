import uvicorn
from fastapi import FastAPI

from config.cfg import get_config

app = FastAPI(
    title="Meta Gameplay",
    description="Meta Gameplay Server",
)


async def main() -> None:
    app.dependency_overrides[get_config] = get_config


if __name__ == "__main__":
    config = get_config()
    uvicorn_config = uvicorn.Config(
        "main:app",
        host="0.0.0.0",
        port=config.api.PORT,
        log_level=config.api.LOG_LEVEL,
        reload=config.api.RELOAD,
    )
    server = uvicorn.Server(uvicorn_config)
    server.run()

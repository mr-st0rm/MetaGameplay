import logging

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from server.config.cfg import get_config, ServerConfig
from server.repositories import get_engine
from server.repositories.base import DBProvider, user_repo_stub, item_repo_stub
from server.repositories.item import ItemRepo
from server.services.base import (
    user_service_stub,
    get_user_service,
    item_service_stub,
    get_item_service,
)
from server.api.v1.api import router as api_v1_router
from server.services.item import ItemService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Starting server...")
    await main(get_config(), application)
    yield
    logger.info("Stopping server...")


app = FastAPI(
    title="Meta Gameplay",
    description="Meta Gameplay Server",
    version="1.0.0",
    lifespan=lifespan,
)


async def main(cfg: ServerConfig, application: FastAPI) -> None:
    db_pool = async_sessionmaker(get_engine(cfg.database), expire_on_commit=False)
    repo_provider = DBProvider(db_pool)

    application.dependency_overrides[user_repo_stub] = repo_provider.get_user_repo
    application.dependency_overrides[user_service_stub] = get_user_service

    application.dependency_overrides[item_repo_stub] = repo_provider.get_item_repo
    application.dependency_overrides[item_service_stub] = get_item_service

    application.include_router(api_v1_router, prefix="/api/v1")

    await _initial_items_migration(db_pool)


async def _initial_items_migration(db_pool: async_sessionmaker) -> None:
    """Миграцию предметов инвентаря"""
    session: AsyncSession = db_pool()
    try:
        item_service = ItemService(ItemRepo(session))
        await item_service.add_initial_items("server/initial_items.json")
    finally:
        await session.close()


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

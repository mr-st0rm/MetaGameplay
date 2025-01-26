import logging
import sqlalchemy.orm
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from server.config.cfg import DataBaseConfig

logger = logging.getLogger(__name__)


def make_connection_string(db: DataBaseConfig) -> str:
    result = f"postgresql+asyncpg://{db.USER}:{db.PASSWORD}@{db.HOST}:{db.PORT}/{db.DATABASE}"
    return result


def get_engine(db: DataBaseConfig) -> sqlalchemy.ext.asyncio.AsyncEngine:
    engine: sqlalchemy.ext.asyncio.AsyncEngine = create_async_engine(
        make_connection_string(db), echo=False
    )

    return engine


class BaseSQLAlchemyRepo:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def commit(self):
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error while commit - {e}", exc_info=e)

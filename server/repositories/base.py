import typing

from sqlalchemy.ext.asyncio import AsyncSession

from server.repositories.item import ItemRepo
from server.repositories.user import UserRepo


def user_repo_stub():
    raise NotImplementedError


def item_repo_stub():
    raise NotImplementedError


class DBProvider:
    def __init__(self, pool):
        self.pool = pool

    async def get_user_repo(self) -> typing.AsyncGenerator:
        session: AsyncSession = self.pool()

        try:
            repo = UserRepo(session)
            yield repo
        finally:
            await session.close()

    async def get_item_repo(self) -> typing.AsyncGenerator:
        session: AsyncSession = self.pool()

        try:
            repo = ItemRepo(session)
            yield repo
        finally:
            await session.close()

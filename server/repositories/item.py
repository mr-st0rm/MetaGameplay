from typing import Iterable

from sqlalchemy import select

from server.repositories import BaseSQLAlchemyRepo
from server.models import Item


class ItemRepo(BaseSQLAlchemyRepo):
    async def items(self) -> Iterable[Item]:
        statement = select(Item).order_by(Item.id)
        return (await self.session.scalars(statement)).all()

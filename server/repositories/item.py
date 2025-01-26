from typing import Iterable

from sqlalchemy import select

from server.api.schemas.item import ItemInSchema
from server.repositories import BaseSQLAlchemyRepo
from server.models import Item


class ItemRepo(BaseSQLAlchemyRepo):
    async def items(self) -> Iterable[Item]:
        statement = select(Item).order_by(Item.id)
        return (await self.session.scalars(statement)).all()

    async def add_items(self, items: list[ItemInSchema]) -> None:
        items = [Item(**item.model_dump()) for item in items]
        self.session.add_all(items)
        await self.commit()

    async def get_by_id(self, item_id: int) -> Item | None:
        statement = select(Item).where(Item.id == item_id)
        return await self.session.scalar(statement)

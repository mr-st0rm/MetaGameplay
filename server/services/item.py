import json

from server.api.schemas.item import ItemOutSchema, ItemInSchema
from server.services import BaseService


class ItemService(BaseService):
    async def items(self) -> list[ItemOutSchema]:
        # todo: cache
        items = await self.repository.items()
        return [ItemOutSchema.model_validate(item) for item in items]

    async def add_initial_items(self, path: str) -> None:
        with open(path, "r") as file:
            items = json.loads(file.read())

        items = [ItemInSchema.model_validate(item) for item in items]
        existing_items = [item.name for item in await self.repository.items()]

        need_add_items = [item for item in items if item.name not in existing_items]

        await self.repository.add_items(need_add_items)

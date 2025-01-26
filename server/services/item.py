from server.api.schemas.item import ItemOutSchema
from server.services import BaseService


class ItemService(BaseService):
    async def items(self) -> list[ItemOutSchema]:
        # todo: cache
        items = await self.repository.items()
        return [ItemOutSchema.model_validate(item) for item in items]

from typing import Annotated

from fastapi import APIRouter, Depends

from server.api.schemas.item import ItemOutSchema
from server.services.base import item_service_stub
from server.services.item import ItemService

router = APIRouter()
item_service_dependency = Annotated[ItemService, Depends(item_service_stub)]


@router.get("/", description="Список всех предметов")
async def all_items(service: item_service_dependency) -> list[ItemOutSchema]:
    return await service.items()

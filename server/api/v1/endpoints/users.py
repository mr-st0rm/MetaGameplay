from typing import Annotated

from fastapi import APIRouter, Depends

from server.api.schemas.user import (
    UserLoginInSchema,
    UserLoginOutSchema,
    UserItemOutSchema,
    UserFinanceOutSchema,
    UserOutSchema,
)
from server.services.base import user_service_stub
from server.services.user import UserService


router = APIRouter()
user_service_dependency = Annotated[UserService, Depends(user_service_stub)]


@router.post(
    "/login/",
    description="Создание нового пользователя или авторизация с существующим username",
)
async def login(
    payload: UserLoginInSchema,
    service: user_service_dependency,
) -> UserLoginOutSchema:
    return await service.login(payload)


@router.get("/{user_id}/", description="Получение пользователя по ID")
async def get_user_by_id(
    user_id: int,
    service: user_service_dependency,
) -> UserOutSchema:
    return await service.get_user_by_id(user_id)


@router.get(
    "/{user_id}/items/",
    description="Весь инвентарь пользователя",
)
async def get_user_items(
    user_id: int,
    service: user_service_dependency,
) -> list[UserItemOutSchema]:
    return await service.get_user_items(user_id)


@router.get("/{user_id}/balance/", description="Баланс пользователя")
async def get_user_balance(
    user_id: int,
    service: user_service_dependency,
) -> UserFinanceOutSchema:
    return await service.get_user_balance(user_id)


@router.post(
    "/{user_id}/buy_item/{item_id}/", description="Покупка пользователем предмета"
)
async def user_buy_item(
    user_id: int,
    item_id: int,
    service: user_service_dependency,
) -> None:
    return await service.user_buy_item(user_id, item_id)


@router.post(
    "/{user_id}/sell_item/{item_id}/",
    description="Продажа пользователем предмета из инвентаря",
)
async def user_sell_item(
    user_id: int,
    item_id: int,
    service: user_service_dependency,
) -> None:
    return await service.user_sell_item(user_id, item_id)

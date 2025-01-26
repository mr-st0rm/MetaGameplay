from typing import Annotated

from fastapi import APIRouter, Depends

from server.api.schemas.user import (
    UserLoginInSchema,
    UserLoginOutSchema,
    UserItemOutSchema,
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
) -> float:
    return await service.get_user_balance(user_id)

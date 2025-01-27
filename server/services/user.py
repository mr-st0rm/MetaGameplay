import random

from fastapi import HTTPException
from starlette import status

from server.api.exceptions import ValidationExceptionCode
from server.api.schemas.user import (
    UserLoginInSchema,
    UserLoginOutSchema,
    UserStatesEnum,
    UserOutSchema,
    UserItemOutSchema,
)
from server.config.cfg import get_config
from server.models import User, Item
from server.repositories.item import ItemRepo
from server.repositories.user import UserRepo
from server.services import BaseService


class UserService(BaseService):
    def __init__(self, repository: UserRepo, item_repo: ItemRepo):
        super().__init__(repository)
        self.item_repository = item_repo

    async def login(self, login_data: UserLoginInSchema) -> UserLoginOutSchema:
        user = await self.repository.get_by_username(login_data.username)

        if not user:
            user = await self.repository.create(login_data.username)

        await self._add_random_credits_for_login(user.id)

        return UserLoginOutSchema(
            state=UserStatesEnum.GAME_SESSION,
            user=UserOutSchema.model_validate(user),
        )

    async def get_user_items(self, user_id: int) -> list[UserItemOutSchema]:
        # todo: cache
        user = await self.repository.get_by_id(user_id)
        self._validate_user(user)

        return [UserItemOutSchema.model_validate(user_item) for user_item in user.items]

    async def get_user_balance(self, user_id: int) -> float:
        # todo: cache
        user = await self.repository.get_by_id(user_id)
        self._validate_user(user)

        return user.finance.balance

    def _validate_user(self, user: User) -> None:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ValidationExceptionCode.USER_NOT_FOUND.value,
            )

    async def _add_random_credits_for_login(self, user_id: int) -> None:
        config = get_config()

        if config.game.ALLOW_ADD_CREDITS:
            # генерация рандомного значения с плавающей точкой
            amount = round(
                random.uniform(
                    config.game.RANDOM_CREDITS_FROM_RANGE,
                    config.game.RANDOM_CREDITS_TO_RANGE,
                ),
                2,
            )
            await self.repository.add_balance(user_id, amount)

    async def user_buy_item(self, user_id: int, item_id: int) -> UserOutSchema:
        user = await self.repository.get_by_id(user_id)
        self._validate_user(user)

        item = await self.item_repository.get_by_id(item_id)
        self._validate_user_buy_item(user, item)

        await self.repository.buy_item(user.id, item.id, item.price)

        return UserOutSchema.model_validate(await self.repository.get_by_id(user_id))

    async def user_sell_item(self, user_id: int, item_id: int) -> UserOutSchema:
        user = await self.repository.get_by_id(user_id)
        item = await self.item_repository.get_by_id(item_id)

        self._validate_user_sell_item(user, item)

        await self.repository.user_sell_item(user_id, item.id, item.price)

        return UserOutSchema.model_validate(await self.repository.get_by_id(user_id))

    def _validate_user_buy_item(self, user: User, item: Item | None) -> None:
        self._validate_item_exists(item)

        if user.finance.balance < item.price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ValidationExceptionCode.NOT_ENOUGH_BALANCE.value,
            )

        if item.id in {user_item.id for user_item in user.items}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ValidationExceptionCode.ALREADY_HAVE_ITEM.value,
            )

    def _validate_item_exists(self, item: Item | None) -> None:
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ValidationExceptionCode.ITEM_NOT_FOUND.value,
            )

    def _validate_user_sell_item(self, user: User, item: Item | None) -> None:
        self._validate_user(user)
        self._validate_item_exists(item)

        if item.id not in {item.id for item in user.items}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ValidationExceptionCode.USER_ITEM_NOT_FOUND.value,
            )

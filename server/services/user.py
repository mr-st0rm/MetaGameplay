import random

from fastapi import HTTPException
from starlette import status

from server.api.schemas.user import (
    UserLoginInSchema,
    UserLoginOutSchema,
    UserStatesEnum,
    UserOutSchema,
    UserItemOutSchema,
)
from server.config.cfg import get_config
from server.models import User
from server.services import BaseService


class UserService(BaseService):
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
                detail="User not found",
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

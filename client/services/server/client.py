import logging

from client.services.api_client.base_api_client import AbstractHttpClient
from client.services.server.schemas import (
    UserLoginInSchema,
    UserFinanceInSchema,
    UserItemInSchema,
    UserInSchema,
)

server_client_logger = logging.getLogger(__name__)


class ServerService:
    def __init__(self, client: AbstractHttpClient):
        self.client = client

    async def login(
        self, username: str, api_version: str = "v1"
    ) -> UserLoginInSchema | None:
        user = await self.client.post(
            f"/api/{api_version}/users/login/",
            payload={"username": username},
        )

        if user:
            return UserLoginInSchema.model_validate(user)

        server_client_logger.error("Can't login with username: {}".format(username))

    async def get_balance(
        self, user_id: int, api_version: str = "v1"
    ) -> UserFinanceInSchema | None:
        user_finance = await self.client.get(
            f"/api/{api_version}/users/{user_id}/balance/",
        )

        if user_finance:
            return UserFinanceInSchema.model_validate(user_finance)

        server_client_logger.error("Can't get balance for user {}".format(user_id))

    async def get_all_items(
        self, api_version: str = "v1"
    ) -> list[UserItemInSchema] | None:
        items = await self.client.get(
            f"/api/{api_version}/items/",
        )

        if items:
            return [UserItemInSchema.model_validate(item) for item in items]

        server_client_logger.error("Can't get all items")

    async def buy_item(
        self, user_id: int, item_id: str, api_version: str = "v1"
    ) -> dict[str, str]:
        buy_item_result = await self.client.post(
            f"/api/{api_version}/users/{user_id}/buy_item/{item_id}/"
        )
        return buy_item_result

    async def get_user_by_id(
        self, user_id: int, api_version: str = "v1"
    ) -> UserInSchema | None:
        user = await self.client.get(
            f"/api/{api_version}/users/{user_id}/",
        )

        if user:
            return UserInSchema.model_validate(user)

        server_client_logger.error("Can't get user with id {}".format(user_id))

    async def get_user_items(
        self, user_id: int, api_version: str = "v1"
    ) -> list[UserItemInSchema] | None:
        items = await self.client.get(
            f"/api/{api_version}/users/{user_id}/items/",
        )

        if items:
            return [UserItemInSchema.model_validate(item) for item in items]

        server_client_logger.error("Can't get user items for user {}".format(user_id))

    async def sell_item(
        self, user_id: int, item_id: str, api_version: str = "v1"
    ) -> dict[str, str] | None:
        sold_response = await self.client.post(
            f"/api/{api_version}/users/{user_id}/sell_item/{item_id}/",
        )
        return sold_response

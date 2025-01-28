import logging

from client.services.api_client.base_api_client import AbstractHttpClient
from client.services.server.schemas import UserLoginInSchema


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

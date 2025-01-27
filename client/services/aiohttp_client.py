import logging
from typing import Any, Literal

from aiohttp import ClientSession, ClientResponse

from client.services.base_api_client import AbstractHttpClient


api_logger = logging.getLogger(__name__)


class AioHttpClient(AbstractHttpClient):
    client: ClientSession

    def __init__(self, base_url: str) -> None:
        super().__init__(ClientSession(base_url.rstrip("/")))

    async def get(
        self, path: str, params: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        async with self.client.get(path, params=params) as response:
            return await self._handle_response("GET", response)

    async def post(
        self, path: str, payload: dict[str, Any] | None, params: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        async with self.client.post(path, json=payload, params=params) as response:
            return await self._handle_response("POST", response)

    async def _handle_response(
        self, request_type: Literal["GET", "POST"], response: ClientResponse
    ) -> dict[str, Any] | None:
        if response.ok:
            try:
                return await response.json()
            except Exception as exc:
                await self._log_response_error(request_type, response, error=exc)
        else:
            await self._log_response_error(request_type, response)

        return None

    async def _log_response_error(
        self,
        request_type: Literal["GET", "POST"],
        response: ClientResponse,
        error: Exception | None = None,
    ) -> None:
        response_text = await response.text()
        error_message = (
            f"API {request_type} error with status code {response.status} for url {response.url} "
            f"got response: {response_text}"
        )
        api_logger.error(error_message, exc_info=error)

import abc
from typing import Any


class AbstractHttpClient(abc.ABC):
    def __init__(self, client: Any) -> None:
        self.client = client

    @abc.abstractmethod
    async def get(self, path: str, params: dict[str, Any] | None) -> dict[str, Any]: ...

    @abc.abstractmethod
    async def post(
        self, path: str, payload: dict[str, Any] | None, params: dict[str, Any] | None
    ) -> dict[str, Any]: ...

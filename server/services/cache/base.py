import abc
from typing import Any


class AbstractCache(abc.ABC):
    def __init__(self, cache: Any) -> None:
        self.cache = cache

    @abc.abstractmethod
    def generate_key(self, func_name: str, **kwargs) -> str: ...

    async def get(self, key: str) -> Any | None: ...

    async def set(self, key: str, value: Any, expire: int) -> None: ...

    async def delete(self, key: str) -> None: ...

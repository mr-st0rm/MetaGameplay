import typing

from server.repositories.user import UserRepo
from server.repositories.item import ItemRepo


class BaseService:
    def __init__(
        self,
        repository: typing.Union[UserRepo, ItemRepo],
    ):
        self.repository = repository

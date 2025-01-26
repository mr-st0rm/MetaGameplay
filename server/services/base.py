from typing import Annotated, AsyncGenerator
from fastapi import Depends

from server.repositories.base import user_repo_stub, UserRepo, item_repo_stub
from server.repositories.item import ItemRepo
from server.services.item import ItemService
from server.services.user import UserService


def user_service_stub():
    raise NotImplementedError


def get_user_service(
    user_repo: Annotated[UserRepo, Depends(user_repo_stub)],
    item_repo: Annotated[ItemRepo, Depends(item_repo_stub)],
) -> AsyncGenerator:
    service = UserService(user_repo, item_repo)
    yield service


def item_service_stub():
    raise NotImplementedError


def get_item_service(
    item_repo: Annotated[ItemRepo, Depends(item_repo_stub)],
) -> AsyncGenerator:
    service = ItemService(item_repo)
    yield service

from enum import StrEnum

from pydantic import BaseModel

from server.api.schemas import BaseOrmModel


class UserStatesEnum(StrEnum):
    LOGIN = "login"
    GAME_SESSION = "game_session"


class UserItemOutSchema(BaseOrmModel):
    id: int
    name: str
    price: float


class UserFinance(BaseOrmModel):
    balance: float


class UserOutSchema(BaseOrmModel):
    id: int
    username: str
    items: list[UserItemOutSchema]
    finance: UserFinance


class UserLoginInSchema(BaseModel):
    username: str


class UserLoginOutSchema(BaseModel):
    state: UserStatesEnum
    user: UserOutSchema

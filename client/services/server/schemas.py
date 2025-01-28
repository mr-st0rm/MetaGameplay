from enum import StrEnum

from pydantic import BaseModel


class UserStatesEnum(StrEnum):
    LOGIN = "login"
    GAME_SESSION = "game_session"


class UserItemInSchema(BaseModel):
    id: int
    name: str
    price: float


class UserFinanceInSchema(BaseModel):
    balance: float


class UserInSchema(BaseModel):
    id: int
    username: str
    items: list[UserItemInSchema]
    finance: UserFinanceInSchema


class UserLoginInSchema(BaseModel):
    state: UserStatesEnum
    user: UserInSchema

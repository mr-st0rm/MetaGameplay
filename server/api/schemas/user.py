from enum import Enum

from pydantic import BaseModel, field_validator

from server.api.schemas import BaseOrmModel


class DecimalRoundValidator:
    @field_validator("price", "balance", mode="before", check_fields=False)
    def validate_decimal(cls, value) -> float:
        return round(float(value), 2)


class UserStatesEnum(str, Enum):
    LOGIN = "login"
    GAME_SESSION = "game_session"


class UserItemOutSchema(BaseOrmModel, DecimalRoundValidator):
    id: int
    name: str
    price: float


class UserFinanceOutSchema(BaseOrmModel, DecimalRoundValidator):
    balance: float


class UserOutSchema(BaseOrmModel):
    id: int
    username: str
    items: list[UserItemOutSchema]
    finance: UserFinanceOutSchema


class UserLoginInSchema(BaseModel):
    username: str


class UserLoginOutSchema(BaseModel):
    state: UserStatesEnum
    user: UserOutSchema

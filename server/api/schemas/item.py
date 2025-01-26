from pydantic import BaseModel

from server.api.schemas import BaseOrmModel


class ItemOutSchema(BaseOrmModel):
    id: int
    name: str
    price: float


class ItemInSchema(BaseModel):
    name: str
    price: float

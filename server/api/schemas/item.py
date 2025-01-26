from server.api.schemas import BaseOrmModel


class ItemOutSchema(BaseOrmModel):
    id: int
    name: str
    price: float

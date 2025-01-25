from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import BaseModel


class Item(BaseModel):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float] = mapped_column(Numeric)

    def __str__(self) -> str:
        return f"Item {self.name} with price {self.price}"

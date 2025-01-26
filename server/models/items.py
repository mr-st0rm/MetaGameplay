from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.models.base import BaseModel


class Item(BaseModel):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float] = mapped_column(Numeric)

    users = relationship("User", secondary="user_items", back_populates="items")

    def __str__(self) -> str:
        return f"Item {self.name} with price {self.price}"

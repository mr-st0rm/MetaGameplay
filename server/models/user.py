from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)

    finance = relationship("UserFinance", uselist=False, back_populates="user")
    items = relationship("Item", secondary="user_items", back_populates="users")

    def __str__(self) -> str:
        return f"User {self.username}"


class UserFinance(BaseModel):
    __tablename__ = "user_finances"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    balance: Mapped[float] = mapped_column(Numeric)

    user = relationship("User", back_populates="finance")

    def __str__(self) -> str:
        return f"User {self.user_id} has {self.balance}"


class UserItem(BaseModel):
    __tablename__ = "user_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))

    def __str__(self) -> str:
        return f"User {self.user_id} has item {self.item_id}"

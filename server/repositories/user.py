from decimal import Decimal

from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload

from server.repositories import BaseSQLAlchemyRepo
from server.models import User, UserFinance, UserItem


class UserRepo(BaseSQLAlchemyRepo):
    async def get_by_id(self, user_id: int) -> User | None:
        statement = (
            select(User)
            .where(User.id == user_id)
            .options(joinedload(User.finance), joinedload(User.items))
        )
        return await self.session.scalar(statement)

    async def get_by_username(self, username: str) -> User | None:
        statement = (
            select(User)
            .where(User.username == username)
            .options(joinedload(User.finance), joinedload(User.items))
        )
        return await self.session.scalar(statement)

    async def create(self, username: str) -> User | None:
        user = User(username=username)
        self.session.add(user)
        await self.session.flush([user])

        finance = UserFinance(user_id=user.id, balance=0)
        self.session.add(finance)
        await self.session.flush([user, finance])

        await self.commit()

        return await self.get_by_username(username)

    async def add_balance(self, user_id: int, amount: float) -> None:
        statement = (
            update(UserFinance)
            .where(UserFinance.user_id == user_id)
            .values({UserFinance.balance: UserFinance.balance + Decimal(amount)})
        )
        await self.session.execute(statement)
        await self.commit()

    async def buy_item(self, user_id: int, item_id: int, item_price: float) -> None:
        user_item = UserItem(user_id=user_id, item_id=item_id)
        self.session.add(user_item)

        statement = (
            update(UserFinance)
            .where(UserFinance.user_id == user_id)
            .values({UserFinance.balance: UserFinance.balance - Decimal(item_price)})
        )
        await self.session.execute(statement)
        await self.commit()

    async def user_sell_item(
        self, user_id: int, item_id: int, item_price: float
    ) -> None:
        statement = delete(UserItem).where(
            UserItem.user_id == user_id, UserItem.item_id == item_id
        )
        await self.session.execute(statement)

        statement = (
            update(UserFinance)
            .where(UserFinance.user_id == user_id)
            .values({UserFinance.balance: UserFinance.balance + Decimal(item_price)})
        )
        await self.session.execute(statement)
        await self.commit()

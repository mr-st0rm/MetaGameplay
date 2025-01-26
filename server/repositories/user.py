from decimal import Decimal

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from server.repositories import BaseSQLAlchemyRepo
from server.models import User, UserFinance


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

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from src.users.user_scheme import UserCreate
from src.users.user_model import UserModel


class UserRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.telegram_id == telegram_id)
        user = await self._session.execute(stmt)
        return user.scalar_one_or_none()

    async def create_user(self, user_scheme: UserCreate) -> UserModel | None:
        user = UserModel(**user_scheme.model_dump())
        self._session.add(user)
        try:
            await self._session.commit()
            await self._session.refresh(user)
            return user
        except SQLAlchemyError as e:
            await self._session.rollback()
            print(e)
            return None

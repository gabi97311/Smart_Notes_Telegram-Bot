from src.users.user_repo import UserRepo
from src.users.user_scheme import UserCreate
from src.users.user_model import UserModel


class UserService:
    def __init__(self, user_repository: UserRepo):
        self._repo = user_repository

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        return await self._repo.get_user_by_telegram_id(telegram_id)

    async def create_user(self, user_scheme: UserCreate) -> UserModel | None:
        if await self.get_user_by_telegram_id(user_scheme.telegram_id):
            return None

        user = await self._repo.create_user(user_scheme)

        if user is not None:
            return None

        return user

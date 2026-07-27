from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Awaitable, Any, Optional

from src.raw_inputs import RawInputsRepo, RawInputsService
from src.gpt_annotations import GptAnnotataionRepo, GptAnnotataionService
from src.users import UserService, UserRepo


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker) -> None:
        self._session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        async with self._session_pool() as session:
            data["services"] = ServiceConteiner(session)
            return await handler(event, data)


class ServiceConteiner:

    def __init__(self, session: AsyncSession):
        self._session = session

        self._raw_inputs: Optional[RawInputsService] = None
        self._gpt_annotation: Optional[GptAnnotataionService] = None
        self._users: Optional[UserService] = None

    @property
    def raw_inputs(self) -> RawInputsService:
        if self._raw_inputs is None:
            repo = RawInputsRepo(self._session)
            self._raw_inputs = RawInputsService(repo)
        return self._raw_inputs

    @property
    def gpt_annotation(self) -> GptAnnotataionService:
        if self._gpt_annotation is None:
            repo = GptAnnotataionRepo(self._session)
            self._gpt_annotation = GptAnnotataionService(repo)
        return self._gpt_annotation

    @property
    def users(self) -> UserService:
        if self._users is None:
            repo = UserRepo(self._session)
            self._users = UserService(repo)
        return self._users

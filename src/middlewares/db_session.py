from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession 

from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Awaitable, Any, Optional

from src.raw_inputs import RawInputsRepo, RawInputsService


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker) -> None:
        self._session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str,Any]
    ) -> Any:
        async with self._session_pool() as session:
            data['services'] = ServiceConteiner(session)
            return await handler(event, data)


class ServiceConteiner:

    def __init__(self, session: AsyncSession):
        self.session = session
        
        self._raw_inputs: Optional[RawInputsService] = None
        
    @property
    def raw_inputs(self) -> RawInputsService:
        if self._raw_inputs is None: 
            repo = RawInputsRepo(self.session)
            self._raw_inputs = RawInputsService(repo)
        return self._raw_inputs
    
    
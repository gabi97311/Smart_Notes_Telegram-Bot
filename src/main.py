import asyncio
from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.middlewares import DBSessionMiddleware
from src.handlers import raw_input_router, start_router
from src.core import setting
from src.core.base import _AsyncSessionLocal

bot = Bot(token=setting.BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.message.middleware(DBSessionMiddleware(session_pool=_AsyncSessionLocal))
    dp.include_router(raw_input_router)
    dp.include_router(start_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from . import setting


class Base(DeclarativeBase, AsyncAttrs):
    pass


_engine = create_async_engine(setting.DATABASE_URL)

_AsyncSessionLocal = async_sessionmaker(bind=_engine, expire_on_commit=False)

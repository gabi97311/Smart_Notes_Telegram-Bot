from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger, String, DateTime,func
from datetime import datetime

from src.core import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    
    username: Mapped[str | None] = mapped_column(String(32))
    first_name: Mapped[str | None] = mapped_column(String(64))
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(default=True)
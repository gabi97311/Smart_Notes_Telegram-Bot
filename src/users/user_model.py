from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger, String, DateTime
from sqlalchemy import func
from datetime import datetime


from src.core import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    
    username: Mapped[str | None] = mapped_column()
    first_name: Mapped[str | None] = mapped_column()
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(default=True)
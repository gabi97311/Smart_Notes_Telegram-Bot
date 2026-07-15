from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.gpt_annotations import GptAnnotationsModel

from src.core import Base


class RawInputsModel(Base):
    __tablename__ = 'raw_inputs'
    
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement= True)
    telegram_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    message_id: Mapped[int]
    content_type: Mapped[str]
    raw_text: Mapped[str | None]
    voice_file_id: Mapped[str | None] 
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import RawInputs 
from src.core.base import Base


class ProcessedNotes(Base):
    __tablename__ = "processed_notes"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    gpt_annotation_id: Mapped[int] = mapped_column(ForeignKey('gpt_annotations.id'))
    
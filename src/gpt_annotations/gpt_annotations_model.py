from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import Base
from src.raw_inputs import RawInputsModel

class GptAnnotationsModel(Base):
    __tablename__ = 'gpt_annotations'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    raw_input_id: Mapped[int] = mapped_column(ForeignKey('raw_inputs.id'))
    raw_inputs: Mapped[RawInputsModel] = relationship(back_populates="gpt_annotations")
    transcribed_text: Mapped[str]
    extracted_intent: Mapped[str]
    extracted_keywords: Mapped[list[str]]
    target_date: Mapped[date]
    
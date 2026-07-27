from pydantic import BaseModel
from datetime import datetime


class GptAnnatataionScheme(BaseModel):
    raw_input_id: int
    transcribed_text: str
    extracted_intent: str
    extracted_keywords: list[str]
    target_date: datetime


class GptAnnatataionSchemeCreate(GptAnnatataionScheme): ...


class GptAnnatationSchemeResponse(GptAnnatataionScheme):
    id: int

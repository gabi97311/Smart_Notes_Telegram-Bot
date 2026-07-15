from pydantic import BaseModel
from datetime import datetime 

class RawInputsScheme(BaseModel):
    telegram_user_id: int
    message_id: int
    content_type: str
    raw_text: str | None = None
    voice_file_id: int | None = None
    create_at: datetime
    
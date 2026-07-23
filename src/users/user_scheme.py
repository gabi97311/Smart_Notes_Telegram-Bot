from pydantic import BaseModel
from datetime import datetime


class UserSheme(BaseModel):

    telegram_id: int
    username: str
    first_name: str

class UserCreate(UserSheme):
    pass

class UserResponse(UserSheme):
    id: int
    created_at: datetime
    is_active: bool


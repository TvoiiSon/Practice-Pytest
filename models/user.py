from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    photo_path: str | None = None
    created_at: datetime

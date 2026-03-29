from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserReadDto(BaseModel):
    id: int
    username: str
    email: str
    name: str
    surname: str
    role_id: int
    is_active: bool
    email_verified: bool
    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
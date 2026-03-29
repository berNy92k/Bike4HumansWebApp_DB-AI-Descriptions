from pydantic import BaseModel, Field


class UserUpdateDto(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: str = Field(..., min_length=3, max_length=30)
    name: str = Field(..., min_length=3, max_length=30)
    surname: str = Field(..., min_length=3, max_length=30)
    role_id: int = Field(...)
    is_active: bool = Field(default=True)
    email_verified: bool = Field(default=True)

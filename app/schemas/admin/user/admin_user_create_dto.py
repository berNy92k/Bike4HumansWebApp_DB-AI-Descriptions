from pydantic import BaseModel, Field


class UserCreateDto(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: str = Field(..., min_length=3, max_length=30)
    name: str = Field(..., min_length=3, max_length=30)
    surname: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=5, max_length=30)
    is_active: bool = Field(default=True)
    email_verified: bool = Field(default=True)
    role_id: int = Field(...)
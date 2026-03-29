from pydantic import BaseModel, Field


class RoleUpdateDto(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    description: str | None = Field(..., min_length=5, max_length=200)

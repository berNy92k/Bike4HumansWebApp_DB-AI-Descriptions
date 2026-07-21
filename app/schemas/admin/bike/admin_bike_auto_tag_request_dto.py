from pydantic import BaseModel, Field


class BikeAutoTagRequestDto(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=2000)

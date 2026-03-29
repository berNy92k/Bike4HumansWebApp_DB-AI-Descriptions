from pydantic import BaseModel, Field


class AddCartItemDto(BaseModel):
    bike_id: int = Field(..., gt=0)

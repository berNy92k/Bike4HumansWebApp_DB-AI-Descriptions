from decimal import Decimal

from pydantic import BaseModel, Field


class BikeListRequestDto(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=5, ge=1, le=100)
    bike_type: str | None = Field(default=None, max_length=100)
    usage: str | None = Field(default=None, max_length=100)
    target_user: str | None = Field(default=None, max_length=100)
    price_min: Decimal | None = Field(default=None, ge=0)
    price_max: Decimal | None = Field(default=None, ge=0)

from decimal import Decimal

from pydantic import Field, BaseModel


class BikeUpdateDto(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    stock_quantity: int = Field(default=0, ge=0)
    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
    brand_id: int = Field(...)

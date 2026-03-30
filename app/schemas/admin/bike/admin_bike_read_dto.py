from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BikeReadDto(BaseModel):
    id: int
    name: str
    description: str | None = None

    price: Decimal
    stock_quantity: int
    image_url: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    brand_id: int

    model_config = ConfigDict(from_attributes=True)
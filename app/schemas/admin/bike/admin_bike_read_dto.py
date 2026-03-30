from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BikeReadDto(BaseModel):
    id: int
    name: str
    description: str | None = None

    bike_type: str | None = None
    frame_material: str | None = None
    frame_size: int | None = None
    frame_size_label: str | None = None
    wheel_size: int | None = None
    tire_width: int | None = None
    gear_count: int | None = None
    brake_type: str | None = None
    suspension_type: str | None = None
    color: str | None = None
    weight_kg: Decimal | None = None
    recommended_height_min: int | None = None
    recommended_height_max: int | None = None
    usage: str | None = None
    target_user: str | None = None

    price: Decimal
    stock_quantity: int
    image_url: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    brand_id: int

    model_config = ConfigDict(from_attributes=True)
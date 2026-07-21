from decimal import Decimal

from pydantic import Field, BaseModel


class BikeCreateDto(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    is_description_ai_generated: bool = Field(default=False)

    bike_type: str | None = Field(default=None, max_length=100)
    frame_material: str | None = Field(default=None, max_length=100)
    frame_size: int | None = Field(default=None, ge=0)
    frame_size_label: str | None = Field(default=None, max_length=20)
    wheel_size: int | None = Field(default=None, ge=0)
    tire_width: Decimal | None = Field(default=None, ge=0, max_digits=5, decimal_places=2)
    gear_count: int | None = Field(default=None, ge=0)
    brake_type: str | None = Field(default=None, max_length=100)
    suspension_type: str | None = Field(default=None, max_length=100)
    color: str | None = Field(default=None, max_length=255)
    weight_kg: Decimal | None = Field(default=None, max_digits=5, decimal_places=2)
    recommended_height_min: int | None = Field(default=None, ge=0)
    recommended_height_max: int | None = Field(default=None, ge=0)
    usage: str | None = Field(default=None, max_length=100)
    target_user: str | None = Field(default=None, max_length=100)

    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    stock_quantity: int = Field(default=0, ge=0)
    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
    created_by: int = Field(default=2)
    brand_id: int = Field(...)
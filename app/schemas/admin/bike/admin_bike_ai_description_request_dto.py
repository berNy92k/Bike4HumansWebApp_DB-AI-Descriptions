from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BikeAiDescriptionRequestDto(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    bike_type: str | None = Field(default=None, max_length=100)
    frame_material: str | None = Field(default=None, max_length=100)
    frame_size: int | None = Field(default=None, ge=0)
    frame_size_label: str | None = Field(default=None, max_length=20)
    wheel_size: int | None = Field(default=None, ge=0)
    tire_width: int | None = Field(default=None, ge=0)
    gear_count: int | None = Field(default=None, ge=0)
    brake_type: str | None = Field(default=None, max_length=100)
    suspension_type: str | None = Field(default=None, max_length=100)
    color: str | None = Field(default=None, max_length=255)
    weight_kg: Decimal | None = Field(default=None, max_digits=5, decimal_places=2)
    recommended_height_min: int | None = Field(default=None, ge=0)
    recommended_height_max: int | None = Field(default=None, ge=0)
    usage: str | None = Field(default=None, max_length=100)
    target_user: str | None = Field(default=None, max_length=100)
    brand_id: int = Field(..., gt=0)

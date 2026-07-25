from pydantic import BaseModel, Field

from app.models.bike import BikeType, BikeUsage, TargetUser


class BikeSearchFiltersResponseDto(BaseModel):
    bike_type: BikeType | None = Field(default=None)
    usage: BikeUsage | None = Field(default=None)
    target_user: TargetUser | None = Field(default=None)
    price_min: float | None = Field(default=None)
    price_max: float | None = Field(default=None)

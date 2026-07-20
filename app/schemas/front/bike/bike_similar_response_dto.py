from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SimilarBikeDto(BaseModel):
    id: int
    name: str
    price: Decimal
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class BikeSimilarRecommendationResponseDto(BaseModel):
    note: str | None = Field(default=None)
    bikes: list[SimilarBikeDto]

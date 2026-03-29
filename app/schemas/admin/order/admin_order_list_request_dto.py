from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class OrderListRequestDto(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=5, ge=1, le=100)

    order_id: str | None = None
    user_id: int | None = None
    status: str | None = None

    total_price_min: float | None = Field(default=None, ge=0)
    total_price_max: float | None = Field(default=None, ge=0)

    created_at_min: datetime | None = None
    created_at_max: datetime | None = None

    sort_by: Literal["created_at", "status"] = "created_at"
    sort_direction: Literal["asc", "desc"] = "desc"

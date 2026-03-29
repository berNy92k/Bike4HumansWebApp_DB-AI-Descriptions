from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderItemReadDto(BaseModel):
    id: int
    bike_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PaymentMethodReadDto(BaseModel):
    id: int
    name: str
    price: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

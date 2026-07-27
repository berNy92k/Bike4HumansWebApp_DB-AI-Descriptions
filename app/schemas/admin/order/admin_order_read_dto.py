from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.admin.address.admin_address_read_dto import AddressReadDto
from app.schemas.admin.order.admin_order_item_read_dto import OrderItemReadDto


class OrderReadDto(BaseModel):
    id: int
    order_id: str
    user_id: int
    currency: str
    status: str
    total_price: float
    payment_method_id: int
    created_at: datetime
    updated_at: datetime
    ai_summary: str | None = None
    address: AddressReadDto | None = None
    items: list[OrderItemReadDto]

    model_config = ConfigDict(from_attributes=True)

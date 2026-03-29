from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.admin.cart.admin_cart_item_read_dto import CartItemReadDto


class CartReadDto(BaseModel):
    id: int
    user_id: int
    currency: str
    status: str
    created_at: datetime
    updated_at: datetime
    items: list[CartItemReadDto]

    model_config = ConfigDict(from_attributes=True)

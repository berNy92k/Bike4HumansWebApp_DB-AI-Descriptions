from pydantic import BaseModel

from app.schemas.admin.order.admin_order_read_dto import OrderReadDto


class OrderListResponseDto(BaseModel):
    orders: list[OrderReadDto]
    page: int
    size: int
    total: int
    pages: int

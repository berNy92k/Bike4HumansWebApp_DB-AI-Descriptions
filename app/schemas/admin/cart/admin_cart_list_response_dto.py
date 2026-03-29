from pydantic import BaseModel

from app.schemas.admin.cart.admin_cart_read_dto import CartReadDto


class CartListResponseDto(BaseModel):
    carts: list[CartReadDto]
    page: int
    size: int
    total: int
    pages: int

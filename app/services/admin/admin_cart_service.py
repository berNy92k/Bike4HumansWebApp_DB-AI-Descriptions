from sqlalchemy.orm import Session

from app.repositories.cart_repository import CartRepository
from app.schemas.admin.cart.admin_cart_list_request_dto import CartListRequestDto
from app.schemas.admin.cart.admin_cart_list_response_dto import CartListResponseDto
from app.schemas.admin.cart.admin_cart_read_dto import CartReadDto


class AdminCartService:

    def __init__(self, db: Session):
        self.cart_repository = CartRepository(db)

    def get_carts_paginated(self, request_dto: CartListRequestDto) -> CartListResponseDto:
        items, total = self.cart_repository.get_carts_paginated(
            page=request_dto.page,
            size=request_dto.size,
        )
        pages = (total + request_dto.size - 1) // request_dto.size if total > 0 else 0

        carts = [CartReadDto.model_validate(cart) for cart in items]

        return CartListResponseDto(
            carts=carts,
            page=request_dto.page,
            size=request_dto.size,
            total=total,
            pages=pages,
        )

    def delete_cart_by_id(self, cart_id):
        cart = self.cart_repository.get_cart_by_id(cart_id)

        self.cart_repository.delete(cart)

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.cart_repository import CartRepository
from app.schemas.admin.cart.admin_cart_list_request_dto import CartListRequestDto
from app.schemas.admin.cart.admin_cart_list_response_dto import CartListResponseDto
from app.schemas.admin.cart.admin_cart_read_dto import CartReadDto
from app.schemas.admin.cart.admin_cart_summary_response_dto import CartSummaryResponseDto
from app.services.ai.cart_summary_ai_service import CartSummaryAiService


class AdminCartService:

    def __init__(self, db: Session, ai_summary_service: CartSummaryAiService | None = None):
        self.cart_repository = CartRepository(db)
        self.ai_summary_service = ai_summary_service or CartSummaryAiService()

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

    def delete_cart_by_id(self, cart_id: int) -> None:
        cart = self.cart_repository.get_cart_by_id(cart_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        self.cart_repository.delete(cart)

    def generate_cart_summary(self, cart_id: int) -> CartSummaryResponseDto:
        cart = self.cart_repository.get_cart_by_id(cart_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        if cart.ai_summary is None:
            cart.ai_summary = self.ai_summary_service.generate_summary(cart)
            cart.ai_summary_generated_at = datetime.now(timezone.utc)
            self.cart_repository.create_or_update(cart)

        return CartSummaryResponseDto(summary=cart.ai_summary)

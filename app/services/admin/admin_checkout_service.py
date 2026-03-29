from sqlalchemy.orm import Session

from app.repositories.checkout_repository import CheckoutRepository
from app.schemas.admin.checkout.admin_checkout_list_request_dto import CheckoutListRequestDto
from app.schemas.admin.checkout.admin_checkout_list_response_dto import CheckoutListResponseDto
from app.schemas.admin.checkout.admin_checkout_read_dto import CheckoutReadDto


class AdminCheckoutService:

    def __init__(self, db: Session):
        self.checkout_repository = CheckoutRepository(db)

    def get_checkouts_paginated(self, request_dto: CheckoutListRequestDto) -> CheckoutListResponseDto:
        items, total = self.checkout_repository.get_checkouts_paginated(
            page=request_dto.page,
            size=request_dto.size,
        )
        pages = (total + request_dto.size - 1) // request_dto.size if total > 0 else 0

        checkouts = [CheckoutReadDto.model_validate(checkout_item) for checkout_item in items]

        return CheckoutListResponseDto(
            checkouts=checkouts,
            page=request_dto.page,
            size=request_dto.size,
            total=total,
            pages=pages,
        )

    def delete_checkout_by_id(self, checkout_id):
        checkout = self.checkout_repository.get_checkout_by_id(checkout_id)

        self.checkout_repository.delete(checkout)

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.checkout_repository import CheckoutRepository
from app.schemas.admin.checkout.admin_checkout_list_request_dto import CheckoutListRequestDto
from app.schemas.admin.checkout.admin_checkout_list_response_dto import CheckoutListResponseDto
from app.schemas.admin.checkout.admin_checkout_read_dto import CheckoutReadDto
from app.schemas.admin.checkout.admin_checkout_summary_response_dto import CheckoutSummaryResponseDto
from app.services.ai.checkout_summary_ai_service import CheckoutSummaryAiService


class AdminCheckoutService:

    def __init__(self, db: Session, ai_summary_service: CheckoutSummaryAiService | None = None):
        self.checkout_repository = CheckoutRepository(db)
        self.ai_summary_service = ai_summary_service or CheckoutSummaryAiService()

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

    def delete_checkout_by_id(self, checkout_id: int) -> None:
        checkout = self.checkout_repository.get_checkout_by_id(checkout_id)
        if not checkout:
            raise HTTPException(status_code=404, detail="Checkout not found")

        self.checkout_repository.delete(checkout)

    def generate_checkout_summary(self, checkout_id: int) -> CheckoutSummaryResponseDto:
        checkout = self.checkout_repository.get_checkout_by_id(checkout_id)
        if not checkout:
            raise HTTPException(status_code=404, detail="Checkout not found")

        if checkout.ai_summary is None:
            checkout.ai_summary = self.ai_summary_service.generate_summary(checkout)
            checkout.ai_summary_generated_at = datetime.now(timezone.utc)
            self.checkout_repository.create_or_update(checkout)

        return CheckoutSummaryResponseDto(summary=checkout.ai_summary)

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.admin.checkout.admin_checkout_list_request_dto import CheckoutListRequestDto
from app.schemas.admin.checkout.admin_checkout_list_response_dto import CheckoutListResponseDto
from app.schemas.admin.checkout.admin_checkout_summary_response_dto import CheckoutSummaryResponseDto
from app.services.admin.admin_checkout_service import AdminCheckoutService
from app.services.auth.auth_service import get_current_admin_user

current_user_dependency = Annotated[dict, Depends(get_current_admin_user)]
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/admin/checkouts",
    dependencies=[Depends(get_current_admin_user)],
    include_in_schema=False
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=CheckoutListResponseDto)
async def find_checkouts(db: db_dependency, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    service = AdminCheckoutService(db)
    return service.get_checkouts_paginated(CheckoutListRequestDto(page=page, size=size))


@router.delete("/{cart_id}", status_code=status.HTTP_200_OK)
async def delete_cart(cart_id: int, db: db_dependency):
    service = AdminCheckoutService(db)
    service.delete_checkout_by_id(cart_id)

@router.post("/{checkout_id}/ai-summary", status_code=status.HTTP_201_CREATED)
async def generate_checkout_summary(checkout_id: int, db: db_dependency) -> CheckoutSummaryResponseDto:
    service = AdminCheckoutService(db)
    return service.generate_checkout_summary(checkout_id)

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.admin.cart.admin_cart_list_request_dto import CartListRequestDto
from app.schemas.admin.cart.admin_cart_list_response_dto import CartListResponseDto
from app.schemas.admin.cart.admin_cart_summary_response_dto import CartSummaryResponseDto
from app.services.admin.admin_cart_service import AdminCartService
from app.services.auth.auth_service import get_current_admin_user

current_user_dependency = Annotated[dict, Depends(get_current_admin_user)]
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/admin/carts",
    dependencies=[Depends(get_current_admin_user)],
    include_in_schema=False
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=CartListResponseDto)
async def find_carts(db: db_dependency, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    service = AdminCartService(db)
    return service.get_carts_paginated(CartListRequestDto(page=page, size=size))


@router.delete("/{cart_id}", status_code=status.HTTP_200_OK)
async def delete_cart(cart_id: int, db: db_dependency):
    service = AdminCartService(db)
    service.delete_cart_by_id(cart_id)

@router.post("/{cart_id}/ai-summary", status_code=status.HTTP_201_CREATED)
async def generate_cart_summary(cart_id: int, db: db_dependency) -> CartSummaryResponseDto:
    service = AdminCartService(db)
    return service.generate_cart_summary(cart_id)

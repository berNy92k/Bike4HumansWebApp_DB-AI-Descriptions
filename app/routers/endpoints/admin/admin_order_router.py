from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.models.order import OrderStatus, Order
from app.schemas.admin.order.admin_order_list_request_dto import OrderListRequestDto
from app.schemas.admin.order.admin_order_list_response_dto import OrderListResponseDto
from app.schemas.admin.order.admin_order_summary_response_dto import OrderSummaryResponseDto
from app.services.admin.admin_order_service import AdminOrderService
from app.services.auth.auth_service import get_current_admin_user

current_user_dependency = Annotated[dict, Depends(get_current_admin_user)]
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/admin/orders",
    dependencies=[Depends(get_current_admin_user)],
    include_in_schema=False
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=OrderListResponseDto)
async def find_orders(
    db: db_dependency,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    order_id: str | None = Query(None),
    user_id: int | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    total_price_min: float | None = Query(None, ge=0),
    total_price_max: float | None = Query(None, ge=0),
    created_at_min: datetime | None = Query(None),
    created_at_max: datetime | None = Query(None),
    sort_by: Literal["created_at", "status"] = Query("created_at"),
    sort_direction: Literal["asc", "desc"] = Query("desc"),
):
    service = AdminOrderService(db)
    return service.get_orders_paginated(OrderListRequestDto(
        page=page,
        size=size,
        order_id=order_id,
        user_id=user_id,
        status=status_filter,
        total_price_min=total_price_min,
        total_price_max=total_price_max,
        created_at_min=created_at_min,
        created_at_max=created_at_max,
        sort_by=sort_by,
        sort_direction=sort_direction,
    ))


@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
async def delete_cart(order_id: int, db: db_dependency):
    service = AdminOrderService(db)
    service.delete_order_by_id(order_id)

@router.put("/{order_id}", status_code=status.HTTP_200_OK)
async def update_order_status(order_id: int, logged_user: current_user_dependency, db: db_dependency, status: OrderStatus):
    service = AdminOrderService(db)
    service.update_status_by_id(logged_user.get("user_id"), status.upper(), order_id)

@router.post("/{order_id}/ai-summary", status_code=status.HTTP_201_CREATED)
async def generate_order_summary(order_id: int, db: db_dependency) -> OrderSummaryResponseDto:
    service = AdminOrderService(db)
    return service.generate_order_summary(order_id)

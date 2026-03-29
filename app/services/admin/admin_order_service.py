from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus
from app.repositories.order_repository import OrderRepository
from app.schemas.admin.order.admin_order_list_request_dto import OrderListRequestDto
from app.schemas.admin.order.admin_order_list_response_dto import OrderListResponseDto
from app.schemas.admin.order.admin_order_read_dto import OrderReadDto


class AdminOrderService:

    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)

    def get_orders_paginated(self, request_dto: OrderListRequestDto) -> OrderListResponseDto:
        items, total = self.order_repository.get_orders_paginated(
            page=request_dto.page,
            size=request_dto.size,
            order_id=request_dto.order_id,
            user_id=request_dto.user_id,
            status=request_dto.status,
            total_price_min=request_dto.total_price_min,
            total_price_max=request_dto.total_price_max,
            created_at_min=request_dto.created_at_min,
            created_at_max=request_dto.created_at_max,
            sort_by=request_dto.sort_by,
            sort_direction=request_dto.sort_direction,
        )
        pages = (total + request_dto.size - 1) // request_dto.size if total > 0 else 0

        orders = [OrderReadDto.model_validate(order_item) for order_item in items]

        return OrderListResponseDto(
            orders=orders,
            page=request_dto.page,
            size=request_dto.size,
            total=total,
            pages=pages,
        )

    def update_status_by_id(self, user_id: int, status: OrderStatus, order_id: int):
        order: Order = self.order_repository.get_order_by_user_id_and_order_id(user_id, order_id)
        if not order or not order.items or len(order.items) == 0:
            raise HTTPException(status_code=404, detail="Order not found or empty")

        order.status = status
        self.order_repository.create_or_update(order)

    def delete_order_by_id(self, order_id):
        order = self.order_repository.get_order_by_id(order_id)

        self.order_repository.delete(order)

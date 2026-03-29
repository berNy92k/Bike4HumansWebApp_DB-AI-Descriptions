from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.models.order import OrderStatus, Order
from app.services.admin.admin_order_service import AdminOrderService
from app.services.auth.auth_service import get_current_user

current_user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/admin/orders",
    dependencies=[Depends(get_current_user)],
    include_in_schema=False
)


@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
async def delete_cart(order_id: int, db: db_dependency):
    service = AdminOrderService(db)
    service.delete_order_by_id(order_id)

@router.put("/{order_id}", status_code=status.HTTP_200_OK)
async def update_order_status(order_id: int, logged_user: current_user_dependency, db: db_dependency, status: OrderStatus):
    service = AdminOrderService(db)
    service.update_status_by_id(logged_user.get("user_id"), status.upper(), order_id)

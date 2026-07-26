from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.models.order import OrderStatus, Order
from app.schemas.admin.order.admin_order_read_dto import OrderReadDto
from app.services.auth.auth_service import get_current_user
from app.services.front.order_service import OrderService

current_user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/order",
    tags=["Order"],
    dependencies=[Depends(get_current_user)]
)

# Separate prefix ("/api/order" instead of "/order") for the read endpoint below: the React
# SPA's order details page lives at "/order/details" (see frontend/src/App.tsx), served by the
# catch-all in init_spa() (app/routers/init_routers.py). order_id is a free-form string (see
# OrderService._generate_order_id), so "GET /order/{order_id}" would happily match
# "/order/details" too (with order_id="details") and return a 404 JSON body instead of falling
# through to the SPA shell — unlike the admin int-id routes, there's no digits-only converter
# to lean on here, so this uses the same distinct-prefix fix as the public bike/manufacturer
# catalog reads.
public_router = APIRouter(
    prefix="/api/order",
    tags=["Order"],
    dependencies=[Depends(get_current_user)]
)


@public_router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderReadDto)
async def get_my_order(order_id: str, logged_user: current_user_dependency, db: db_dependency):
    service = OrderService(db)
    return service.get_order_by_user_id_and_order_id(logged_user.get("user_id"), order_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(logged_user: current_user_dependency, db: db_dependency):
    service = OrderService(db)
    service.create_order(logged_user.get("user_id"))


@router.put("/", status_code=status.HTTP_201_CREATED)
async def update_order_status(logged_user: current_user_dependency, db: db_dependency, status: OrderStatus,
                              previous_status: OrderStatus):
    service = OrderService(db)
    order: Order = service.update_status(logged_user.get("user_id"), status.upper(), previous_status.upper())

    return {
        "order_id": order.order_id
    }

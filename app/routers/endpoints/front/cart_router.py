from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from app.database.database import get_db
from app.schemas.admin.cart.admin_cart_read_dto import CartReadDto
from app.schemas.front.cart.add_cart_item_dto import AddCartItemDto
from app.services.auth.auth_service import get_current_user
from app.services.front.cart_service import CartService

current_user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=CartReadDto)
async def get_my_cart(logged_user: current_user_dependency, db: db_dependency):
    service = CartService(db)
    return service.get_cart_by_user_id_and_pending_status(logged_user.get("user_id"))


@router.post("/item", status_code=status.HTTP_204_NO_CONTENT)
async def add_item_to_cart(add_cart_item_dto: AddCartItemDto, logged_user: current_user_dependency, db: db_dependency):
    service = CartService(db)
    service.add_item_to_cart(logged_user.get("user_id"), add_cart_item_dto.bike_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

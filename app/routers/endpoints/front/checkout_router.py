from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.admin.checkout.admin_checkout_read_dto import CheckoutReadDto
from app.services.auth.auth_service import get_current_user
from app.services.front.checkout_service import CheckoutService

current_user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/checkout",
    tags=["Checkout"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=CheckoutReadDto)
async def get_my_pending_checkout(logged_user: current_user_dependency, db: db_dependency):
    service = CheckoutService(db)
    return service.get_cart_by_user_id_and_status_pending(logged_user.get("user_id"))


@router.get("/completed", status_code=status.HTTP_200_OK, response_model=CheckoutReadDto)
async def get_my_completed_checkout(logged_user: current_user_dependency, db: db_dependency):
    service = CheckoutService(db)
    return service.get_cart_by_user_id_and_status_completed(logged_user.get("user_id"))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_checkout(logged_user: current_user_dependency, db: db_dependency):
    service = CheckoutService(db)
    service.create_checkout(logged_user.get("user_id"))

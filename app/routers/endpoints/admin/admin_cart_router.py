from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.services.admin.admin_cart_service import AdminCartService
from app.services.auth.auth_service import get_current_user

current_user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/admin/carts",
    dependencies=[Depends(get_current_user)],
    include_in_schema=False
)


@router.delete("/{cart_id}", status_code=status.HTTP_200_OK)
async def delete_cart(cart_id: int, db: db_dependency):
    service = AdminCartService(db)
    service.delete_cart_by_id(cart_id)

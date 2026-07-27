from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.admin.address.admin_address_read_dto import AddressReadDto
from app.schemas.front.address.address_upsert_dto import AddressUpsertDto
from app.services.auth.auth_service import get_current_user
from app.services.front.address_service import AddressService

current_user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/address",
    tags=["Address"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=AddressReadDto)
async def get_my_address(logged_user: current_user_dependency, db: db_dependency):
    service = AddressService(db)
    return service.get_my_address(logged_user.get("user_id"))


@router.put("/me", status_code=status.HTTP_200_OK, response_model=AddressReadDto)
async def save_my_address(address_upsert_dto: AddressUpsertDto, logged_user: current_user_dependency, db: db_dependency):
    service = AddressService(db)
    return service.save_my_address(logged_user.get("user_id"), address_upsert_dto)

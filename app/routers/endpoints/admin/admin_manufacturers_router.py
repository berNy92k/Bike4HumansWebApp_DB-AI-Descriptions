from typing import List, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.admin.manufacturers.admin_manufacturer_create_dto import ManufacturerCreateDto
from app.schemas.admin.manufacturers.admin_manufacturer_read_dto import ManufacturerReadDto
from app.schemas.admin.manufacturers.admin_manufacturer_update_dto import ManufacturerUpdateDto
from app.services.admin.admin_manufacturer_service import AdminManufacturerService
from app.services.auth.auth_service import get_current_user

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(
    prefix="/admin/manufacturer",
    tags=["Admin - manufacturer"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ManufacturerReadDto])
async def find_all_manufacturers(db: db_dependency):
    service = AdminManufacturerService(db)
    return service.get_all_manufacturers()


@router.get("/{manufacturer_id}", status_code=status.HTTP_200_OK, response_model=ManufacturerReadDto)
async def find_manufacturer_by_id(manufacturer_id: int, db: db_dependency):
    service = AdminManufacturerService(db)
    return service.get_manufacturer_by_id(manufacturer_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_manufacturer(manufacturer_create_dto: ManufacturerCreateDto, db: db_dependency,
                              current_user: current_user_dependency):
    service = AdminManufacturerService(db)
    service.create_manufacturer(manufacturer_create_dto, current_user)


@router.put("/{manufacturer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_single_field_for_manufacturer(manufacturer_id: int, manufacturer_update_dto: ManufacturerUpdateDto,
                                               db: db_dependency):
    service = AdminManufacturerService(db)
    service.update_manufacturer_all_fields(manufacturer_id, manufacturer_update_dto)


@router.patch("/{manufacturer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_manufacturer(manufacturer_id: int, manufacturer_update_dto: ManufacturerUpdateDto,
                              db: db_dependency):
    service = AdminManufacturerService(db)
    service.update_manufacturer_separate_fields(manufacturer_id, manufacturer_update_dto)


@router.delete("/{manufacturer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_manufacturer_by_id(manufacturer_id: int, db: db_dependency):
    service = AdminManufacturerService(db)
    service.delete_manufacturer_by_id(manufacturer_id)

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.admin.manufacturers.admin_manufacturer_ai_description_request_dto import ManufacturerAiDescriptionRequestDto
from app.schemas.admin.manufacturers.admin_manufacturer_ai_description_response_dto import ManufacturerAiDescriptionResponseDto
from app.schemas.admin.manufacturers.admin_manufacturer_create_dto import ManufacturerCreateDto
from app.schemas.admin.manufacturers.admin_manufacturer_list_request_dto import ManufacturerListRequestDto
from app.schemas.admin.manufacturers.admin_manufacturer_list_response_dto import ManufacturerListResponseDto
from app.schemas.admin.manufacturers.admin_manufacturer_read_dto import ManufacturerReadDto
from app.schemas.admin.manufacturers.admin_manufacturer_update_dto import ManufacturerUpdateDto
from app.services.admin.admin_manufacturer_service import AdminManufacturerService
from app.services.auth.auth_service import get_current_admin_user

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[dict, Depends(get_current_admin_user)]

router = APIRouter(
    prefix="/admin/manufacturer",
    tags=["Admin - manufacturer"],
    dependencies=[Depends(get_current_admin_user)],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=ManufacturerListResponseDto)
async def find_all_manufacturers(db: db_dependency, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    service = AdminManufacturerService(db)
    return service.get_manufacturers_paginated(ManufacturerListRequestDto(page=page, size=size))


# ":int" constrains Starlette's path matching to digits-only, so GET /admin/manufacturer/list
# or /create fall through to the SPA client routes at those paths (frontend/src/App.tsx)
# instead of matching here with "list"/"create" as manufacturer_id and 422-ing.
@router.get("/{manufacturer_id:int}", status_code=status.HTTP_200_OK, response_model=ManufacturerReadDto)
async def find_manufacturer_by_id(manufacturer_id: int, db: db_dependency):
    service = AdminManufacturerService(db)
    return service.get_manufacturer_by_id(manufacturer_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_manufacturer(manufacturer_create_dto: ManufacturerCreateDto, db: db_dependency,
                              current_user: current_user_dependency):
    service = AdminManufacturerService(db)
    service.create_manufacturer(manufacturer_create_dto, current_user)


@router.put("/{manufacturer_id:int}", status_code=status.HTTP_204_NO_CONTENT)
async def update_single_field_for_manufacturer(manufacturer_id: int, manufacturer_update_dto: ManufacturerUpdateDto,
                                               db: db_dependency):
    service = AdminManufacturerService(db)
    service.update_manufacturer_all_fields(manufacturer_id, manufacturer_update_dto)


@router.patch("/{manufacturer_id:int}", status_code=status.HTTP_204_NO_CONTENT)
async def update_manufacturer(manufacturer_id: int, manufacturer_update_dto: ManufacturerUpdateDto,
                              db: db_dependency):
    service = AdminManufacturerService(db)
    service.update_manufacturer_separate_fields(manufacturer_id, manufacturer_update_dto)


@router.delete("/{manufacturer_id:int}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_manufacturer_by_id(manufacturer_id: int, db: db_dependency):
    service = AdminManufacturerService(db)
    service.delete_manufacturer_by_id(manufacturer_id)


@router.post("/ai-generate-description", status_code=status.HTTP_201_CREATED)
async def create_ai_description_for_manufacturer(manufacturer_ai_desc_req_dto: ManufacturerAiDescriptionRequestDto, db: db_dependency) -> ManufacturerAiDescriptionResponseDto:
    service = AdminManufacturerService(db)
    return service.create_ai_description(manufacturer_ai_desc_req_dto)

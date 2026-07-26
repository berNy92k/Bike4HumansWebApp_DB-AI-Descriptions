from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.admin.bike.admin_bike_read_dto import BikeReadDto
from app.schemas.admin.manufacturers.admin_manufacturer_list_request_dto import ManufacturerListRequestDto
from app.schemas.admin.manufacturers.admin_manufacturer_list_response_dto import ManufacturerListResponseDto
from app.schemas.admin.manufacturers.admin_manufacturer_read_dto import ManufacturerReadDto
from app.services.front.bike_service import BikeService
from app.services.front.manufacturer_service import ManufacturerService

db_dependency = Annotated[Session, Depends(get_db)]

# "/api/manufacturers" instead of "/manufacturers": the React SPA's client-side catalog pages
# live at bare "/manufacturers" and "/manufacturers/{id}" (see frontend/src/App.tsx), served by
# the catch-all in init_spa() (app/routers/init_routers.py), which is registered last. If this
# JSON API reused those same paths, it would be matched first and a browser hard-refresh would
# get JSON instead of the SPA shell.
router = APIRouter(
    prefix="/api/manufacturers",
    tags=["Manufacturers"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=ManufacturerListResponseDto)
async def find_manufacturers(db: db_dependency, page: int = Query(1, ge=1), size: int = Query(9, ge=1, le=100)):
    service = ManufacturerService(db)
    return service.get_manufacturers_paginated(ManufacturerListRequestDto(page=page, size=size))


@router.get("/{manufacturer_id}", status_code=status.HTTP_200_OK, response_model=ManufacturerReadDto)
async def find_manufacturer_by_id(manufacturer_id: int, db: db_dependency):
    service = ManufacturerService(db)
    return service.get_manufacturer_by_id(manufacturer_id)


@router.get("/{manufacturer_id}/bikes", status_code=status.HTTP_200_OK, response_model=list[BikeReadDto])
async def find_bikes_by_manufacturer(manufacturer_id: int, db: db_dependency):
    service = BikeService(db)
    return service.get_bikes_by_manufacturer_id(manufacturer_id)

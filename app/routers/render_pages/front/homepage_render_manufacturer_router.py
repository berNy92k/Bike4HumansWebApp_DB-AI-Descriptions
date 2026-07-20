from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.schemas.admin.manufacturers.admin_manufacturer_list_request_dto import ManufacturerListRequestDto
from app.services.front.bike_service import BikeService
from app.services.front.manufacturer_service import ManufacturerService

router = APIRouter(
    prefix="/manufacturers",
    include_in_schema=False
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


@router.get("/", status_code=status.HTTP_200_OK)
async def render_manufacturers(request: Request, db: db_dependency):
    page = int(request.query_params.get("page", 1))
    size = int(request.query_params.get("size", 9))

    pagination = ManufacturerService(db).get_manufacturers_paginated(
        ManufacturerListRequestDto(page=page, size=size)
    )
    bike_service = BikeService(db)
    bike_counts = {m.id: len(bike_service.get_bikes_by_manufacturer_id(m.id)) for m in pagination.items}

    return templates.TemplateResponse(
        "front/manufacturers/manufacturers.html",
        {
            "request": request,
            "manufacturers": pagination.items,
            "bike_counts": bike_counts,
            "page": pagination.page,
            "size": pagination.size,
            "total": pagination.total,
            "pages": pagination.pages,
        },
    )


@router.get("/{manufacturer_id}", status_code=status.HTTP_200_OK)
async def render_manufacturer_details(request: Request, manufacturer_id: int, db: db_dependency):
    manufacturer = ManufacturerService(db).get_manufacturer_by_id(manufacturer_id)
    bikes = BikeService(db).get_bikes_by_manufacturer_id(manufacturer_id)

    return templates.TemplateResponse(
        "front/manufacturers/manufacturer_details.html",
        {
            "request": request,
            "manufacturer": manufacturer,
            "bikes": bikes,
        },
    )

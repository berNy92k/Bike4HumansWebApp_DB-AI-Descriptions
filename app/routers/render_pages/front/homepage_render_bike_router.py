from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.services.front.bike_service import BikeService
from app.services.front.manufacturer_service import ManufacturerService

router = APIRouter(
    prefix="/bikes",
    include_in_schema=False
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")

@router.get("/", status_code=status.HTTP_200_OK)
async def render_bikes(request: Request, db: db_dependency):

    page = int(request.query_params.get("page", 1))
    size = int(request.query_params.get("size", 16))

    pagination = BikeService(db).get_bikes_paginated(BikeListRequestDto(page=page, size=size))
    return templates.TemplateResponse(
        "front/bikes/bikes.html",
        {
            "request": request,
            "bikes": pagination.items,
            "page": pagination.page,
            "size": pagination.size,
            "total": pagination.total,
            "pages": pagination.pages,
        },
    )

@router.get("/{bike_id}", status_code=status.HTTP_200_OK)
async def render_bike_details(request: Request, bike_id: int, db: db_dependency):
    bike = BikeService(db).get_bike_by_id(bike_id)
    manufacturers = ManufacturerService(db).get_all_manufacturers()

    return templates.TemplateResponse(
        "front/bikes/bike_details.html",
        {
            "request": request,
            "bike": bike,
            "manufacturers": manufacturers,
        },
    )
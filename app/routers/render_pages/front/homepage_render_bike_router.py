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
    bike_type = request.query_params.get("bike_type") or None
    usage = request.query_params.get("usage") or None
    target_user = request.query_params.get("target_user") or None
    price_min = request.query_params.get("price_min") or None
    price_max = request.query_params.get("price_max") or None

    list_request_dto = BikeListRequestDto(
        page=page,
        size=size,
        bike_type=bike_type,
        usage=usage,
        target_user=target_user,
        price_min=price_min,
        price_max=price_max,
    )
    pagination = BikeService(db).get_bikes_paginated(list_request_dto)
    manufacturers = ManufacturerService(db).get_all_manufacturers()
    manufacturer_names = {m.id: m.name for m in manufacturers}

    active_filters = {
        "bike_type": bike_type or "",
        "usage": usage or "",
        "target_user": target_user or "",
        "price_min": price_min or "",
        "price_max": price_max or "",
    }
    filter_query_string = "&".join(f"{key}={value}" for key, value in active_filters.items() if value)

    return templates.TemplateResponse(
        "front/bikes/bikes.html",
        {
            "request": request,
            "bikes": pagination.items,
            "manufacturer_names": manufacturer_names,
            "page": pagination.page,
            "size": pagination.size,
            "total": pagination.total,
            "pages": pagination.pages,
            "active_filters": active_filters,
            "filter_query_string": filter_query_string,
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
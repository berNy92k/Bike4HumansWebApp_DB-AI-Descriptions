from typing import Annotated

from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.routers.utils.admin_utils_router import redirect_to_login
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.services.admin.admin_bike_service import AdminBikeService
from app.services.admin.admin_manufacturer_service import AdminManufacturerService
from app.services.auth.auth_service import AuthService

router = APIRouter(
    prefix="/admin/bikes",
    tags=["Admin - bikes"]
)

templates = Jinja2Templates(directory="app/templates")

db_dependency = Annotated[Session, Depends(get_db)]


### Pages ###
@router.get("/list", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_bikes_page(request: Request, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        bike_service = AdminBikeService(db)
        manufacturer_service = AdminManufacturerService(db)

        page = int(request.query_params.get("page", 1))
        size = int(request.query_params.get("size", 5))

        pagination = bike_service.get_bikes_paginated(BikeListRequestDto(page=page, size=size))
        manufacturers = manufacturer_service.get_all_manufacturers()

        return templates.TemplateResponse(
            "admin/bikes/bikes.html",
            {
                "request": request,
                "bikes": pagination.items,
                "manufacturers": manufacturers,
                "page": pagination.page,
                "size": pagination.size,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/create", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_create_bike(request: Request, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        manufacturer_service = AdminManufacturerService(db)
        manufacturers = manufacturer_service.get_all_manufacturers()

        return templates.TemplateResponse(
            "admin/bikes/bike_create.html",
            {
                "request": request,
                "manufacturers": manufacturers,
            },
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/{bike_id}/details", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_bike_details(request: Request, bike_id: int, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        bike_service = AdminBikeService(db)
        manufacturer_service = AdminManufacturerService(db)

        bike = bike_service.get_bike_by_id(bike_id)
        manufacturers = manufacturer_service.get_all_manufacturers()

        return templates.TemplateResponse(
            "admin/bikes/bike_details.html",
            {
                "request": request,
                "bike": bike,
                "manufacturers": manufacturers,
            },
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/{bike_id}/edit", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_bike_edit(request: Request, bike_id: int, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        bike_service = AdminBikeService(db)
        manufacturer_service = AdminManufacturerService(db)

        bike = bike_service.get_bike_by_id(bike_id)
        manufacturers = manufacturer_service.get_all_manufacturers()

        return templates.TemplateResponse(
            "admin/bikes/bike_edit.html",
            {
                "request": request,
                "bike": bike,
                "manufacturers": manufacturers,
            },
        )
    except HTTPException:
        return redirect_to_login()

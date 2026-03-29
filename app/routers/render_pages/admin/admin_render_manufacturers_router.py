from typing import Annotated

from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.routers.utils.admin_utils_router import redirect_to_login
from app.schemas.admin.manufacturers.admin_manufacturer_list_request_dto import ManufacturerListRequestDto
from app.services.admin.admin_manufacturer_service import AdminManufacturerService
from app.services.auth.auth_service import AuthService

router = APIRouter(
    prefix="/admin/manufacturer",
    tags=["Admin - manufacturer"]
)

templates = Jinja2Templates(directory="app/templates")

db_dependency = Annotated[Session, Depends(get_db)]


### Pages ###
@router.get("/list", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_manufacturer_page(request: Request, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        page = int(request.query_params.get("page", 1))
        size = int(request.query_params.get("size", 5))
        pagination = AdminManufacturerService(db).get_manufacturers_paginated(
            ManufacturerListRequestDto(page=page, size=size)
        )

        return templates.TemplateResponse(
            "admin/manufacturers/manufacturers.html",
            {
                "request": request,
                "manufacturers": pagination.items,
                "page": pagination.page,
                "size": pagination.size,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/create", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_manufacturer_create_page(request: Request, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        return templates.TemplateResponse("admin/manufacturers/manufacturers_create.html", {"request": request})
    except HTTPException:
        return redirect_to_login()


@router.get("/{manufacturer_id}/details", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_manufacturer_create_page(request: Request, manufacturer_id: int, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        manufacturer = AdminManufacturerService(db).get_manufacturer_by_id(manufacturer_id)
        return templates.TemplateResponse("admin/manufacturers/manufacturers_details.html",
                                          {"request": request, "manufacturer": manufacturer})
    except HTTPException:
        return redirect_to_login()


@router.get("/{manufacturer_id}/edit", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_manufacturer_create_page(request: Request, manufacturer_id: int, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        manufacturer = AdminManufacturerService(db).get_manufacturer_by_id(manufacturer_id)
        return templates.TemplateResponse("admin/manufacturers/manufacturers_edit.html",
                                          {"request": request, "manufacturer": manufacturer})
    except HTTPException:
        return redirect_to_login()

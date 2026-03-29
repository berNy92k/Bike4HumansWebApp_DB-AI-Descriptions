from typing import Annotated

from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.routers.utils.admin_utils_router import redirect_to_login
from app.schemas.admin.cart.admin_cart_list_request_dto import CartListRequestDto
from app.services.admin.admin_cart_service import AdminCartService
from app.services.auth.auth_service import AuthService

router = APIRouter(
    prefix="/admin/carts",
    tags=["Admin - cart"]
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


## USERS ##
@router.get("/list", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_user_page(request: Request, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        page = int(request.query_params.get("page", 1))
        size = int(request.query_params.get("size", 5))
        pagination = AdminCartService(db).get_carts_paginated(CartListRequestDto(page=page, size=size))

        return templates.TemplateResponse(
            "admin/carts/carts.html",
            {
                "request": request,
                "carts": pagination.carts,
                "page": pagination.page,
                "size": pagination.size,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        )
    except HTTPException:
        return redirect_to_login()
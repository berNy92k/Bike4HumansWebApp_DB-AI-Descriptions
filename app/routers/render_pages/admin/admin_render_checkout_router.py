from typing import Annotated

from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.routers.utils.admin_utils_router import redirect_to_login
from app.schemas.admin.checkout.admin_checkout_list_request_dto import CheckoutListRequestDto
from app.services.admin.admin_checkout_service import AdminCheckoutService
from app.services.auth.auth_service import AuthService

router = APIRouter(
    prefix="/admin/checkouts",
    tags=["Admin - checkout"]
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


@router.get("/list", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_user_page(request: Request, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        page = int(request.query_params.get("page", 1))
        size = int(request.query_params.get("size", 5))
        pagination = AdminCheckoutService(db).get_checkouts_paginated(CheckoutListRequestDto(page=page, size=size))

        return templates.TemplateResponse(
            "admin/checkouts/checkouts.html",
            {
                "request": request,
                "checkouts": pagination.checkouts,
                "page": pagination.page,
                "size": pagination.size,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        )
    except HTTPException:
        return redirect_to_login()

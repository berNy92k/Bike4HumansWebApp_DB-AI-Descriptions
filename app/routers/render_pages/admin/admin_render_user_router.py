from typing import Annotated

from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.routers.utils.admin_utils_router import redirect_to_login
from app.schemas.admin.user.admin_user_list_request_dto import UserListRequestDto
from app.schemas.admin.user.role.admin_role_list_request_dto import RoleListRequestDto
from app.services.admin.admin_user_service import AdminUserService
from app.services.auth.auth_service import AuthService

router = APIRouter(
    prefix="/admin/user",
    tags=["Admin - user"]
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
        pagination = AdminUserService(db).get_users_paginated(UserListRequestDto(page=page, size=size))

        return templates.TemplateResponse(
            "admin/users/users.html",
            {
                "request": request,
                "users": pagination.items,
                "page": pagination.page,
                "size": pagination.size,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/create", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_user_create_page(request: Request, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        roles = AdminUserService(db).get_all_roles()
        return templates.TemplateResponse("admin/users/user_create.html", {"request": request, "roles": roles})
    except HTTPException:
        return redirect_to_login()


@router.get("/{user_id}/details", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_user_details_page(request: Request, user_id: int, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        user = AdminUserService(db).get_user_by_id(user_id)
        return templates.TemplateResponse("admin/users/user_details.html", {"request": request, "user": user})

    except HTTPException:
        return redirect_to_login()


@router.get("/{user_id}/edit", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_user_edit_page(request: Request, user_id: int, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        service = AdminUserService(db)
        user = service.get_user_by_id(user_id)
        roles = service.get_all_roles()
        return templates.TemplateResponse("admin/users/user_edit.html",
                                          {"request": request, "user": user, "roles": roles})

    except HTTPException:
        return redirect_to_login()


## ROLES ##
@router.get("/role/list", include_in_schema=False)
async def render_role_list_page(request: Request, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        page = int(request.query_params.get("page", 1))
        size = int(request.query_params.get("size", 5))
        pagination = AdminUserService(db).get_roles_paginated(RoleListRequestDto(page=page, size=size))

        return templates.TemplateResponse(
            "admin/users/roles/roles.html",
            {
                "request": request,
                "roles": pagination.items,
                "page": pagination.page,
                "size": pagination.size,
                "total": pagination.total,
                "pages": pagination.pages,
            }
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/role/create", include_in_schema=False)
async def render_user_create_page(request: Request, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        return templates.TemplateResponse("admin/users/roles/role_create.html", {"request": request})
    except HTTPException:
        return redirect_to_login()


@router.get("/role/{role_id}", include_in_schema=False)
async def render_role_details_page(request: Request, role_id: int, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        role = AdminUserService(db).get_role_by_id(role_id)
        return templates.TemplateResponse("admin/users/roles/role_details.html", {"request": request, "role": role})

    except HTTPException:
        return redirect_to_login()


@router.get("/role/{role_id}/edit", include_in_schema=False)
async def render_role_edit_page(request: Request, role_id: int, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        role = AdminUserService(db).get_role_by_id(role_id)
        return templates.TemplateResponse("admin/users/roles/role_edit.html", {"request": request, "role": role})

    except HTTPException:
        return redirect_to_login()

from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.admin.user.admin_user_create_dto import UserCreateDto
from app.schemas.admin.user.admin_user_list_request_dto import UserListRequestDto
from app.schemas.admin.user.admin_user_list_response_dto import UserListResponseDto
from app.schemas.admin.user.admin_user_read_details_dto import UserDetailsDto
from app.schemas.admin.user.admin_user_read_dto import UserReadDto
from app.schemas.admin.user.admin_user_update_dto import UserUpdateDto
from app.schemas.admin.user.role.admin_role_create_dto import RoleCreateDto
from app.schemas.admin.user.role.admin_role_list_request_dto import RoleListRequestDto
from app.schemas.admin.user.role.admin_role_list_response_dto import RoleListResponseDto
from app.schemas.admin.user.role.admin_role_read_dto import RoleReadDto
from app.schemas.admin.user.role.admin_role_update_dto import RoleUpdateDto
from app.services.admin.admin_user_service import AdminUserService
from app.services.auth.auth_service import get_current_admin_user

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[dict, Depends(get_current_admin_user)]

router = APIRouter(
    prefix="/admin/user",
    tags=["Admin - user"],
    dependencies=[Depends(get_current_admin_user)],
)


## ROLES ##
# Registered before the dynamic "/{user_id}" user routes below: "/roles" is a static
# path segment at the same depth as "/{user_id}" and Starlette matches routes in
# registration order, so it must come first or GET /admin/user/roles would be
# swallowed by GET /{user_id} (and fail int conversion on "roles").
@router.get("/roles", status_code=status.HTTP_200_OK, response_model=RoleListResponseDto)
async def get_all_roles(db: db_dependency, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    service = AdminUserService(db)
    return service.get_roles_paginated(RoleListRequestDto(page=page, size=size))


# "/roles/{role_id}" (plural) instead of "/role/{role_id}" (singular): the React SPA's role
# details page lives at singular "/admin/user/role/{id}" (see frontend/src/App.tsx), served by
# the catch-all in init_spa() (app/routers/init_routers.py). Reusing that exact path here would
# make a browser hard-refresh on that page return JSON instead of the SPA shell.
@router.get("/roles/{role_id:int}", status_code=status.HTTP_200_OK, response_model=RoleReadDto)
async def get_role_by_id(role_id: int, db: db_dependency):
    service = AdminUserService(db)
    return service.get_role_details(role_id)


@router.post("/role", status_code=status.HTTP_201_CREATED)
async def create_new_role(role: RoleCreateDto, db: db_dependency, current_user: current_user_dependency):
    service = AdminUserService(db)
    service.create_role(role, current_user)


@router.patch("/role/{role_id:int}", status_code=status.HTTP_200_OK)
async def update_role_by_id(role_id: int, role: RoleUpdateDto, db: db_dependency,
                            current_user: current_user_dependency):
    service = AdminUserService(db)
    service.update_role_by_id(role_id, role, current_user)


@router.delete("/role/{role_id:int}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_by_id(role_id: int, db: db_dependency, current_user: current_user_dependency):
    service = AdminUserService(db)
    service.delete_role_by_id(role_id, current_user)


## USERS ##
@router.get("/", status_code=status.HTTP_200_OK, response_model=UserListResponseDto)
async def get_all_users(db: db_dependency, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    service = AdminUserService(db)
    return service.get_users_paginated(UserListRequestDto(page=page, size=size))


# ":int" constrains Starlette's path matching to digits-only, so GET /admin/user/list or
# /create fall through to the SPA client routes at those paths (frontend/src/App.tsx) instead
# of matching here with "list"/"create" as user_id and 422-ing.
@router.get("/{user_id:int}", status_code=status.HTTP_200_OK, response_model=UserDetailsDto)
async def get_user_by_id(user_id: int, db: db_dependency):
    service = AdminUserService(db)
    return service.get_user_by_id(user_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreateDto, db: db_dependency, current_user: current_user_dependency):
    service = AdminUserService(db)
    service.create_user(user, current_user)


@router.put("/{user_id:int}", status_code=status.HTTP_200_OK)
async def update_new_user(user_id: int, user_update_dto: UserUpdateDto, db: db_dependency,
                          current_user: current_user_dependency):
    service = AdminUserService(db)
    service.update_user_all_fields(user_id, user_update_dto, current_user)


@router.delete("/{user_id:int}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: int, db: db_dependency):
    service = AdminUserService(db)
    service.delete_user_by_id(user_id)

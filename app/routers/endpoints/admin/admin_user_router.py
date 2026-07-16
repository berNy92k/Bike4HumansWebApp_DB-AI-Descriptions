from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.admin.user.admin_user_create_dto import UserCreateDto
from app.schemas.admin.user.admin_user_read_dto import UserReadDto
from app.schemas.admin.user.admin_user_update_dto import UserUpdateDto
from app.schemas.admin.user.role.admin_role_create_dto import RoleCreateDto
from app.schemas.admin.user.role.admin_role_list_request_dto import RoleListRequestDto
from app.schemas.admin.user.role.admin_role_list_response_dto import RoleListResponseDto
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


## USERS ##
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserReadDto])
async def get_all_users(db: db_dependency):
    service = AdminUserService(db)
    return service.get_all_users()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreateDto, db: db_dependency, current_user: current_user_dependency):
    service = AdminUserService(db)
    service.create_user(user, current_user)


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_new_user(user_id: int, user_update_dto: UserUpdateDto, db: db_dependency,
                          current_user: current_user_dependency):
    service = AdminUserService(db)
    service.update_user_all_fields(user_id, user_update_dto, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: int, db: db_dependency):
    service = AdminUserService(db)
    service.delete_user_by_id(user_id)


## ROLES ##
@router.get("/roles", status_code=status.HTTP_200_OK, response_model=RoleListResponseDto)
async def get_all_roles(db: db_dependency, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    service = AdminUserService(db)
    return service.get_roles_paginated(RoleListRequestDto(page=page, size=size))


@router.post("/role", status_code=status.HTTP_201_CREATED)
async def create_new_role(role: RoleCreateDto, db: db_dependency, current_user: current_user_dependency):
    service = AdminUserService(db)
    service.create_role(role, current_user)


@router.patch("/role/{role_id}", status_code=status.HTTP_200_OK)
async def update_role_by_id(role_id: int, role: RoleUpdateDto, db: db_dependency,
                            current_user: current_user_dependency):
    service = AdminUserService(db)
    service.update_role_by_id(role_id, role, current_user)


@router.delete("/role/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_by_id(role_id: int, db: db_dependency, current_user: current_user_dependency):
    service = AdminUserService(db)
    service.delete_role_by_id(role_id, current_user)

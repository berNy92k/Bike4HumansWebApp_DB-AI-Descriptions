from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
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

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminUserService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def get_users_paginated(self, request_dto: UserListRequestDto) -> UserListResponseDto:
        items, total = self.user_repository.get_users_paginated(
            page=request_dto.page,
            size=request_dto.size,
        )
        pages = (total + request_dto.size - 1) // request_dto.size if total > 0 else 0

        user_items = [UserReadDto.model_validate(user) for user in items]

        return UserListResponseDto(
            items=user_items,
            page=request_dto.page,
            size=request_dto.size,
            total=total,
            pages=pages,
        )

    def get_user_by_id(self, user_id: int) -> UserDetailsDto:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        role = self.role_repository.get_role_by_id(user.role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        return UserDetailsDto(
            id=user.id,
            username=user.username,
            email=user.email,
            name=user.name,
            surname=user.surname,
            role_id=user.role_id,
            role_name=role.name,
            is_active=user.is_active,
            email_verified=user.email_verified,
            last_login=user.last_login,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def create_user(self, user_dto: UserCreateDto):
        user = User(
            username=user_dto.username,
            email=user_dto.email,
            name=user_dto.name,
            surname=user_dto.surname,
            is_active=user_dto.is_active,
            email_verified=user_dto.email_verified,
            hashed_password=bcrypt_context.hash(user_dto.password),
            role_id=user_dto.role_id,
        )
        self.user_repository.create_user(user)

    def update_user_all_fields(self, user_id: int, user_update_dto: UserUpdateDto):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user_update_dto.model_dump()

        for f, v in user_data.items():
            setattr(user, f, v)

        self.user_repository.update_user(user)

    def delete_user_by_id(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        self.user_repository.delete_user(user)

    def get_all_roles(self):
        return self.role_repository.get_all_roles()

    def get_roles_paginated(self, request_dto: RoleListRequestDto) -> RoleListResponseDto:
        items, total = self.role_repository.get_roles_paginated(page=request_dto.page, size=request_dto.size)
        pages = (total + request_dto.size - 1) // request_dto.size if total > 0 else 0

        role_items = [RoleReadDto.model_validate(role) for role in items]

        return RoleListResponseDto(
            items=role_items,
            page=request_dto.page,
            size=request_dto.size,
            total=total,
            pages=pages,
        )

    def get_role_by_id(self, role_id: int):
        role = self.role_repository.get_role_by_id(role_id)

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        return role

    def create_role(self, role_dto: RoleCreateDto):
        role = Role(**role_dto.model_dump())
        self.role_repository.create_role(role)

    def update_role_by_id(self, role_id: int, role_dto: RoleUpdateDto):
        role = self.get_role_by_id(role_id)

        role.name = role_dto.name
        role.description = role_dto.description

        self.role_repository.update_role(role)

    def delete_role_by_id(self, role_id):
        role = self.get_role_by_id(role_id)
        self.role_repository.delete_role(role)

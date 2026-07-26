from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.permission import Permission, PermissionCode
from app.models.role import Role
from app.models.user import User
from app.repositories.permission_repository import PermissionRepository
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
        self.permission_repository = PermissionRepository(db)

    def _ensure_super_admin(self, current_user: dict) -> None:
        role = self.role_repository.get_role_by_id(int(current_user["role_id"]))
        if not role or not role.has_permission(PermissionCode.SUPER_ADMIN):
            raise HTTPException(status_code=403, detail="Only super admin can perform this action")

    def _resolve_permissions(self, codes: list[str]) -> list[Permission]:
        permissions = self.permission_repository.get_by_codes(codes)
        if len(permissions) != len(set(codes)):
            raise HTTPException(status_code=400, detail="Unknown permission code(s)")

        return permissions

    def _ensure_role_assignment_allowed(self, role_id: int, current_user: dict) -> Role:
        target_role = self.role_repository.get_role_by_id(role_id)
        if not target_role:
            raise HTTPException(status_code=404, detail="Role not found")

        if target_role.has_permission(PermissionCode.ADMIN_PANEL_ACCESS):
            self._ensure_super_admin(current_user)

        return target_role

    @staticmethod
    def _to_role_read_dto(role: Role) -> RoleReadDto:
        return RoleReadDto(
            id=role.id,
            name=role.name,
            description=role.description,
            permission_codes=[permission.code for permission in role.permissions],
            created_at=role.created_at,
            updated_at=role.updated_at,
        )

    def get_all_users(self) -> list[User]:
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

    def create_user(self, user_dto: UserCreateDto, current_user: dict) -> None:
        self._ensure_role_assignment_allowed(user_dto.role_id, current_user)

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

    def update_user_all_fields(self, user_id: int, user_update_dto: UserUpdateDto, current_user: dict) -> None:
        self._ensure_role_assignment_allowed(user_update_dto.role_id, current_user)

        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user_update_dto.model_dump()

        for f, v in user_data.items():
            setattr(user, f, v)

        self.user_repository.update_user(user)

    def delete_user_by_id(self, user_id: int) -> None:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        self.user_repository.delete_user(user)

    def get_all_roles(self) -> list[Role]:
        return self.role_repository.get_all_roles()

    def get_roles_paginated(self, request_dto: RoleListRequestDto) -> RoleListResponseDto:
        items, total = self.role_repository.get_roles_paginated(page=request_dto.page, size=request_dto.size)
        pages = (total + request_dto.size - 1) // request_dto.size if total > 0 else 0

        role_items = [self._to_role_read_dto(role) for role in items]

        return RoleListResponseDto(
            items=role_items,
            page=request_dto.page,
            size=request_dto.size,
            total=total,
            pages=pages,
        )

    def get_role_by_id(self, role_id: int) -> Role:
        role = self.role_repository.get_role_by_id(role_id)

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        return role

    def get_role_details(self, role_id: int) -> RoleReadDto:
        return self._to_role_read_dto(self.get_role_by_id(role_id))

    def create_role(self, role_dto: RoleCreateDto, current_user: dict) -> None:
        self._ensure_super_admin(current_user)

        role = Role(
            name=role_dto.name,
            description=role_dto.description,
            permissions=self._resolve_permissions(role_dto.permission_codes),
        )
        self.role_repository.create_role(role)

    def update_role_by_id(self, role_id: int, role_dto: RoleUpdateDto, current_user: dict) -> None:
        self._ensure_super_admin(current_user)

        role = self.get_role_by_id(role_id)

        role.name = role_dto.name
        role.description = role_dto.description
        role.permissions = self._resolve_permissions(role_dto.permission_codes)

        self.role_repository.update_role(role)

    def delete_role_by_id(self, role_id: int, current_user: dict) -> None:
        self._ensure_super_admin(current_user)

        role = self.get_role_by_id(role_id)
        self.role_repository.delete_role(role)

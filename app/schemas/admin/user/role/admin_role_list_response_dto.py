from pydantic import BaseModel

from app.schemas.admin.user.role.admin_role_read_dto import RoleReadDto


class RoleListResponseDto(BaseModel):
    items: list[RoleReadDto]
    page: int
    size: int
    total: int
    pages: int

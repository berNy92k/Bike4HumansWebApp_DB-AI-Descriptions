from pydantic import BaseModel

from app.schemas.admin.user.admin_user_read_dto import UserReadDto


class UserListResponseDto(BaseModel):
    items: list[UserReadDto]
    page: int
    size: int
    total: int
    pages: int

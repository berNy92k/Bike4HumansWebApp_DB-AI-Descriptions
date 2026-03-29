from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models import Role
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin.user.admin_user_create_dto import UserCreateDto

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)

    def create_user(self, user_dto: UserCreateDto):
        user_role: Role = self.role_repository.get_role_by_id(4)
        if not user_role:
            raise HTTPException(status_code= 404, detail="Role not found.")

        user = User(
            username=user_dto.username,
            email=user_dto.email,
            name=user_dto.name,
            surname=user_dto.surname,
            is_active=False,
            email_verified=False,
            hashed_password=bcrypt_context.hash(user_dto.password),
            role_id=user_role.id,
        )
        self.user_repository.create_user(user)

    def find_user_by_id(self, user_id: int) -> User:
        user: User = self.user_repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def find_user_by_username(self, username: str) -> User:
        user: User = self.user_repository.find_user_by_username(username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
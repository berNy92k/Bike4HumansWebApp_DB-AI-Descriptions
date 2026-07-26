import os
from datetime import datetime, timezone, timedelta
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.models import User
from app.models.permission import PermissionCode
from app.repositories.role_repository import RoleRepository
from app.services.auth.user_service import UserService

load_dotenv()

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    return _decode_jwt_token(token)


async def get_current_admin_user(current_user: Annotated[dict, Depends(get_current_user)],
                                 db: Annotated[Session, Depends(get_db)], ) -> dict:

    role = RoleRepository(db).get_role_by_id(int(current_user["role_id"]))
    if not role or not role.has_permission(PermissionCode.ADMIN_PANEL_ACCESS):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is forbidden")

    return current_user


def _decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        role_id: str = payload.get("role_id")
        exp: datetime = payload.get("exp")

        if username is None or user_id is None or role_id is None or exp is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized")

        return {"username": username, "user_id": user_id, "role_id": role_id, "exp": exp}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized")


def generate_jwt_token(username: str, user_id: int, role_id: int, expire_delta: timedelta):
    token = {"sub": username, "id": user_id, "role_id": role_id}
    expire = datetime.now(timezone.utc) + expire_delta
    token.update({"exp": expire})

    return jwt.encode(token, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))


class AuthService:

    def __init__(self, db: Session):
        self.user_service = UserService(db)

    def authenticate_user(self, username: str, password: str) -> User:
        user: User = self.user_service.find_user_by_username(username)
        if not bcrypt_context.verify(password, str(user.hashed_password)):
            raise HTTPException(status_code=401, detail="User is not authorized")

        return user

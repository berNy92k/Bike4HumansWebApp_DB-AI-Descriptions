from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.models import User
from app.schemas.auth.user_create_dto import UserCreateDto
from app.services.auth.auth_service import AuthService, generate_jwt_token
from app.services.auth.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user: UserCreateDto):
    service = UserService(db)
    service.create_user(user)


@router.post("/token", status_code=status.HTTP_201_CREATED)
async def create_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    service = AuthService(db)
    user: User = service.authenticate_user(form_data.username, form_data.password)

    minutes: int = 20
    token = generate_jwt_token(form_data.username, user.id, user.role_id, timedelta(minutes=minutes))

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=False,
        samesite="lax",
        secure=False,
        max_age=minutes * 60,
        path="/",
    )
    return response

@router.get("/logout", status_code=status.HTTP_200_OK)
async def logout():
    response = RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token", path="/")
    return response

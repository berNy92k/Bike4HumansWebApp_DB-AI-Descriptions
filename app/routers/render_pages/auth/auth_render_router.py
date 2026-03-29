from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.database.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def render_login_page(request: Request):
    return templates.TemplateResponse("authentication/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse, include_in_schema=False)
async def render_register_page(request: Request):
    return templates.TemplateResponse("authentication/register.html", {"request": request})

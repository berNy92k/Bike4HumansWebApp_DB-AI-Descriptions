from typing import Annotated

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.models import User
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.services.auth.auth_service import AuthService
from app.services.admin.admin_manufacturer_service import AdminManufacturerService
from app.services.front.bike_service import BikeService
from app.services.front.cart_service import CartService
from app.services.front.checkout_service import CheckoutService

router = APIRouter(
    include_in_schema=False
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def render_homepage(request: Request, db: db_dependency):
    logged_user = None
    has_cart = False
    has_checkout = False

    try:
        user: User = await AuthService(db).validate_access(request)
        logged_user = user

        try:
            CartService(db).get_cart_by_user_id_and_pending_status(user.id)
            has_cart = True
        except Exception:
            has_cart = False

        try:
            CheckoutService(db).get_cart_by_user_id_and_status_pending(user.id)
            has_checkout = True
        except Exception:
            has_checkout = False

    except Exception:
        pass

    return templates.TemplateResponse(
        "front/homepage/index.html",
        {
            "request": request,
            "equipmentShortList": BikeService(db).get_bikes_paginated(BikeListRequestDto(page=1, size=4)),
            "bikeSize": len(BikeService(db).get_all_bikes()),
            "manufacturerSize": len(AdminManufacturerService(db).get_all_manufacturers()),
            "logged_user": logged_user,
            "has_cart": has_cart,
            "has_checkout": has_checkout,
        }
    )

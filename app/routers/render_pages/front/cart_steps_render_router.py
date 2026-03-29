from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.models import User, Cart, Checkout, PaymentMethod
from app.routers.utils.admin_utils_router import redirect_to_login
from app.services.auth.auth_service import AuthService
from app.services.front.cart_service import CartService
from app.services.front.checkout_service import CheckoutService
from app.services.front.payment_methods_service import PaymentMethodService

router = APIRouter(
    prefix="/cart",
    include_in_schema=False
)

db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="app/templates")


@router.get("/step1", status_code=status.HTTP_200_OK)
async def render_cart_step1(request: Request, db: db_dependency):
    try:
        user: User = await AuthService(db).validate_access(request)

        cart: Cart = CartService(db).get_cart_by_user_id_and_pending_status(user.id)

        return templates.TemplateResponse(
            "front/cart/step1.html",
            {
                "request": request,
                "cart": cart,
                "logged_user": user,
                "has_cart": True,
                "has_checkout": False,
            },
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/step2", status_code=status.HTTP_200_OK)
async def render_cart_step2(request: Request, db: db_dependency):
    try:
        user: User = await AuthService(db).validate_access(request)

        checkout: Checkout = CheckoutService(db).get_cart_by_user_id_and_status_pending(user.id)
        methods: PaymentMethod = PaymentMethodService(db).get_methods()

        return templates.TemplateResponse(
            "front/cart/step2.html",
            {
                "request": request,
                "checkout": checkout,
                "payment_methods": methods,
                "logged_user": user,
                "has_cart": False,
                "has_checkout": True,
            },
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/payment-provider", status_code=status.HTTP_200_OK)
async def render_payment_provider(request: Request, db: db_dependency):
    try:
        user: User = await AuthService(db).validate_access(request)

        checkout: Checkout = CheckoutService(db).get_cart_by_user_id_and_status_completed(user.id)
        method : PaymentMethod = PaymentMethodService(db).get_method_by_id(checkout.payment_method_id)

        return templates.TemplateResponse(
            "front/cart/payment_provider.html",
            {
                "request": request,
                "user": user, # change for DTO and send only required fields
                "checkout": checkout,
                "method": method,
                "tax": 0,
            },
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/payment-result", status_code=status.HTTP_200_OK)
async def render_payment_result(db: db_dependency, request: Request, payment_status: str = Query(...)):
    try:
        user: User = await AuthService(db).validate_access(request)

        checkout: Checkout = CheckoutService(db).get_cart_by_user_id_and_status_pending(user.id)

        return templates.TemplateResponse(
            "front/cart/step3.html",
            {
                "request": request,
                "checkout": checkout,
                "checkout_id": checkout.id,
                "tax": 0,
                "payment_method_id": checkout.payment_method_id,
                "payment_status": payment_status
            },
        )
    except HTTPException:
        return redirect_to_login()

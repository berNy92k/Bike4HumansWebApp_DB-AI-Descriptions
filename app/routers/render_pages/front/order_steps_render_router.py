from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.models import User, PaymentMethod
from app.models.order import Order
from app.routers.utils.admin_utils_router import redirect_to_login
from app.services.auth.auth_service import AuthService
from app.services.front.cart_service import CartService
from app.services.front.checkout_service import CheckoutService
from app.services.front.order_service import OrderService
from app.services.front.payment_methods_service import PaymentMethodService

router = APIRouter(
    prefix="/order",
    include_in_schema=False
)

db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="app/templates")


@router.get("/details", status_code=status.HTTP_200_OK)
async def render_payment_result(db: db_dependency, request: Request, orderId: str):
    try:
        user: User = await AuthService(db).validate_access(request)

        order: Order = OrderService(db).get_order_by_user_id_and_order_id(user.id, orderId)
        method: PaymentMethod = PaymentMethodService(db).get_method_by_id(order.payment_method_id)
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
            "front/order/order.html",
            {
                "request": request,
                "order": order,
                "order_id": order.id,
                "tax": 0,
                "payment_method_name": method.name,
                "payment_status": order.status,
                "logged_user": logged_user,
                "has_cart": has_cart,
                "has_checkout": has_checkout,
            },
        )
    except HTTPException:
        return redirect_to_login()

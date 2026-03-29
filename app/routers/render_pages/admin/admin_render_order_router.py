from typing import Annotated

from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.routers.utils.admin_utils_router import redirect_to_login
from app.schemas.admin.order.admin_order_list_request_dto import OrderListRequestDto
from app.services.admin.admin_order_service import AdminOrderService
from app.services.auth.auth_service import AuthService

router = APIRouter(
    prefix="/admin/orders",
    tags=["Admin - order"]
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


@router.get("/list", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_user_page(request: Request, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)

        page = int(request.query_params.get("page", 1))
        size = int(request.query_params.get("size", 5))
        order_id = request.query_params.get("order_id") or None
        user_id_raw = request.query_params.get("user_id")
        status_raw = request.query_params.get("status") or None
        total_price_min_raw = request.query_params.get("total_price_min")
        total_price_max_raw = request.query_params.get("total_price_max")
        created_at_min_raw = request.query_params.get("created_at_min")
        created_at_max_raw = request.query_params.get("created_at_max")
        sort_by = request.query_params.get("sort_by", "created_at")
        sort_direction = request.query_params.get("sort_direction", "desc")

        user_id = int(user_id_raw) if user_id_raw else None
        total_price_min = float(total_price_min_raw) if total_price_min_raw else None
        total_price_max = float(total_price_max_raw) if total_price_max_raw else None

        created_at_min = created_at_min_raw if created_at_min_raw else None
        created_at_max = created_at_max_raw if created_at_max_raw else None

        pagination = AdminOrderService(db).get_orders_paginated(
            OrderListRequestDto(
                page=page,
                size=size,
                order_id=order_id,
                user_id=user_id,
                status=status_raw,
                total_price_min=total_price_min,
                total_price_max=total_price_max,
                created_at_min=created_at_min,
                created_at_max=created_at_max,
                sort_by=sort_by,
                sort_direction=sort_direction,
            )
        )

        return templates.TemplateResponse(
            "admin/orders/orders.html",
            {
                "request": request,
                "orders": pagination.orders,
                "page": pagination.page,
                "size": pagination.size,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        )
    except HTTPException:
        return redirect_to_login()

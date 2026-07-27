from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.admin.dashboard.admin_dashboard_stats_response_dto import DashboardStatsResponseDto
from app.services.admin.admin_dashboard_service import AdminDashboardService
from app.services.auth.auth_service import get_current_admin_user

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/admin/dashboard",
    tags=["Admin - dashboard"],
    dependencies=[Depends(get_current_admin_user)],
)


@router.get("/stats", status_code=status.HTTP_200_OK, response_model=DashboardStatsResponseDto)
async def get_dashboard_stats(db: db_dependency):
    service = AdminDashboardService(db)
    return service.get_dashboard_stats()

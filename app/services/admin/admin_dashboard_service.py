from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.admin.dashboard.admin_dashboard_stats_response_dto import (
    CatalogHealthDto,
    DashboardStatsResponseDto,
    MonthlyRevenueDto,
    StatusCountDto,
    TopBikeDto,
)


class AdminDashboardService:

    def __init__(self, db: Session):
        self.dashboard_repository = DashboardRepository(db)

    def get_dashboard_stats(self) -> DashboardStatsResponseDto:
        total_revenue, realized_orders_count = self.dashboard_repository.get_realized_revenue_stats()
        average_order_value = round(total_revenue / realized_orders_count, 2) if realized_orders_count else 0.0

        orders_by_status = [
            StatusCountDto(status=order_status, count=count)
            for order_status, count in self.dashboard_repository.get_orders_by_status()
        ]
        revenue_by_month = [
            MonthlyRevenueDto(month=month, revenue=revenue)
            for month, revenue in self.dashboard_repository.get_revenue_by_month()
        ]
        top_bikes = [
            TopBikeDto(bike_id=bike_id, name=name, quantity_sold=quantity, revenue=revenue)
            for bike_id, name, quantity, revenue in self.dashboard_repository.get_top_selling_bikes()
        ]
        catalog_health = CatalogHealthDto(**self.dashboard_repository.get_catalog_health())

        return DashboardStatsResponseDto(
            bikes_count=self.dashboard_repository.get_bikes_count(),
            manufacturers_count=self.dashboard_repository.get_manufacturers_count(),
            users_count=self.dashboard_repository.get_users_count(),
            roles_count=self.dashboard_repository.get_roles_count(),
            orders_count=self.dashboard_repository.get_orders_count(),
            orders_total_revenue=round(total_revenue, 2),
            average_order_value=average_order_value,
            orders_by_status=orders_by_status,
            revenue_by_month=revenue_by_month,
            top_bikes=top_bikes,
            catalog_health=catalog_health,
        )

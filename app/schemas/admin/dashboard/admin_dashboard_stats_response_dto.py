from pydantic import BaseModel


class StatusCountDto(BaseModel):
    status: str
    count: int


class MonthlyRevenueDto(BaseModel):
    month: str
    revenue: float


class TopBikeDto(BaseModel):
    bike_id: int
    name: str
    quantity_sold: int
    revenue: float


class CatalogHealthDto(BaseModel):
    bikes_with_image_pct: float
    bikes_with_description_pct: float
    bikes_complete_pct: float
    manufacturers_with_bikes_pct: float


class DashboardStatsResponseDto(BaseModel):
    bikes_count: int
    manufacturers_count: int
    users_count: int
    roles_count: int
    orders_count: int
    orders_total_revenue: float
    average_order_value: float
    orders_by_status: list[StatusCountDto]
    revenue_by_month: list[MonthlyRevenueDto]
    top_bikes: list[TopBikeDto]
    catalog_health: CatalogHealthDto

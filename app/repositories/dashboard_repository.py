from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.bike import Bike
from app.models.manufacturer import Manufacturer
from app.models.order import Order, OrderItem
from app.models.role import Role
from app.models.user import User

# Orders whose value counts as realized revenue - excludes PENDING (not yet paid),
# CANCELED, and FAILED.
REALIZED_ORDER_STATUSES = ("COMPLETED", "DELIVERY")


class DashboardRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_bikes_count(self) -> int:
        return self.db.query(Bike).count()

    def get_manufacturers_count(self) -> int:
        return self.db.query(Manufacturer).count()

    def get_users_count(self) -> int:
        return self.db.query(User).count()

    def get_roles_count(self) -> int:
        return self.db.query(Role).count()

    def get_orders_count(self) -> int:
        return self.db.query(Order).count()

    def get_realized_revenue_stats(self) -> tuple[float, int]:
        total_revenue, count = (
            self.db.query(func.coalesce(func.sum(Order.total_price), 0), func.count(Order.id))
            .filter(Order.status.in_(REALIZED_ORDER_STATUSES))
            .one()
        )
        return float(total_revenue), count

    def get_orders_by_status(self) -> list[tuple[str, int]]:
        return (
            self.db.query(Order.status, func.count(Order.id))
            .group_by(Order.status)
            .all()
        )

    def get_revenue_by_month(self, months: int = 6) -> list[tuple[str, float]]:
        cutoff = datetime.utcnow() - timedelta(days=30 * months)
        month_expr = func.strftime("%Y-%m", Order.created_at)

        rows = (
            self.db.query(month_expr, func.coalesce(func.sum(Order.total_price), 0))
            .filter(Order.status.in_(REALIZED_ORDER_STATUSES))
            .filter(Order.created_at >= cutoff)
            .group_by(month_expr)
            .order_by(month_expr)
            .all()
        )
        return [(month, float(revenue)) for month, revenue in rows]

    def get_top_selling_bikes(self, limit: int = 5) -> list[tuple[int, str, int, float]]:
        rows = (
            self.db.query(
                OrderItem.bike_id,
                Bike.name,
                func.sum(OrderItem.quantity),
                func.sum(OrderItem.quantity * Bike.price),
            )
            .join(Order, Order.id == OrderItem.order_id)
            .join(Bike, Bike.id == OrderItem.bike_id)
            .filter(Order.status.in_(REALIZED_ORDER_STATUSES))
            .group_by(OrderItem.bike_id, Bike.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
            .all()
        )
        return [(bike_id, name, int(qty), float(revenue)) for bike_id, name, qty, revenue in rows]

    def get_catalog_health(self) -> dict:
        bikes_total = self.db.query(Bike).count()
        bikes_with_image = self.db.query(Bike).filter(Bike.image_url.isnot(None)).count()
        bikes_with_description = (
            self.db.query(Bike)
            .filter(Bike.description.isnot(None))
            .filter(Bike.description != "")
            .count()
        )
        bikes_complete = (
            self.db.query(Bike)
            .filter(Bike.image_url.isnot(None))
            .filter(Bike.description.isnot(None))
            .filter(Bike.description != "")
            .filter(Bike.bike_type.isnot(None))
            .filter(Bike.frame_material.isnot(None))
            .count()
        )

        manufacturers_total = self.db.query(Manufacturer).count()
        manufacturers_with_bikes = (
            self.db.query(Manufacturer.id)
            .join(Bike, Bike.brand_id == Manufacturer.id)
            .distinct()
            .count()
        )

        def pct(part: int, whole: int) -> float:
            return round((part / whole) * 100, 1) if whole else 0.0

        return {
            "bikes_with_image_pct": pct(bikes_with_image, bikes_total),
            "bikes_with_description_pct": pct(bikes_with_description, bikes_total),
            "bikes_complete_pct": pct(bikes_complete, bikes_total),
            "manufacturers_with_bikes_pct": pct(manufacturers_with_bikes, manufacturers_total),
        }

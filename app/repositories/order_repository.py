from datetime import datetime

from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus


class OrderRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_order_by_id(self, order_id):
        return self.db.query(Order).where(Order.id == order_id).first()

    def get_order_by_user_id(self, user_id: int):
        return self.db.query(Order).where(Order.user_id == user_id).first()

    def get_order_by_user_id_and_status(self, user_id: int, status: OrderStatus):
        return (self.db.query(Order)
                .where(Order.user_id == user_id)
                .where(Order.status == status)
                .first())

    def get_order_by_user_id_and_order_id(self, user_id: int, order_id: int):
        return (self.db.query(Order)
                .where(Order.user_id == user_id)
                .where(Order.id == order_id)
                .first())

    def get_order_by_order_id_and_user_id(self, order_id: str, user_id: int):
        return (self.db.query(Order)
                .where(Order.user_id == user_id)
                .where(Order.order_id == order_id)
                .first())

    def get_orders_paginated( self, page: int, size: int, order_id: str | None = None, user_id: int | None = None,
                              status: str | None = None, total_price_min: float | None = None, total_price_max: float | None = None,
                              created_at_min: datetime | None = None, created_at_max: datetime | None = None,
                              sort_by: str = "created_at", sort_direction: str = "desc"):
        query = self.db.query(Order)

        if order_id is not None and order_id != "":
            query = query.where(Order.order_id == order_id)

        if user_id is not None:
            query = query.where(Order.user_id == user_id)

        if status is not None and status != "":
            query = query.where(Order.status == status)

        if total_price_min is not None:
            query = query.where(Order.total_price >= total_price_min)

        if total_price_max is not None:
            query = query.where(Order.total_price <= total_price_max)

        if created_at_min is not None:
            query = query.where(Order.created_at >= created_at_min)

        if created_at_max is not None:
            query = query.where(Order.created_at <= created_at_max)

        if sort_by is not None:
            if sort_by == "created_at":
                sort_column = Order.created_at
            elif sort_by == "status":
                sort_column = Order.status
            else:
                sort_column = Order.id

            if sort_direction.lower() == "asc":
                query = query.order_by(sort_column.asc())
            else:
                query = query.order_by(sort_column.desc())

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return items, total

    def create_or_update(self, order: Order):
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

    def update_order(self, order):
        self.db.add(order)
        self.db.commit()

    def delete(self, order: Order):
        self.db.delete(order)
        self.db.commit()
